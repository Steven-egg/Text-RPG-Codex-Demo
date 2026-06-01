import { runtimeClient } from "../shared/runtime-client.js";

const fixtureSelect = document.querySelector("#fixture-select");
const shellEl = document.querySelector(".combat-shell");
const titleEl = document.querySelector("#screen-title");
const subtitleEl = document.querySelector("#screen-subtitle");
const resourceStripEl = document.querySelector("#resource-strip");
const enemyNameEl = document.querySelector("#enemy-name");
const enemyHpFillEl = document.querySelector("#enemy-hp-fill");
const enemyHpLabelEl = document.querySelector("#enemy-hp-label");
const enemyMetaEl = document.querySelector("#enemy-meta");
const playerNameEl = document.querySelector("#player-name");
const playerFocusStatsEl = document.querySelector("#player-focus-stats");
const battleLogEl = document.querySelector("#battle-log");
const logModeLabelEl = document.querySelector("#log-mode-label");
const toggleBattleLogEl = document.querySelector("#toggle-battle-log");
const combatFooterEl = document.querySelector(".combat-footer");
const commandMessageEl = document.querySelector("#command-message");
const commandRowEl = document.querySelector("#command-row");
const submenuPanelEl = document.querySelector("#command-submenu");
const submenuLabelEl = document.querySelector("#submenu-label");
const submenuTitleEl = document.querySelector("#submenu-title");
const submenuSummaryEl = document.querySelector("#submenu-summary");
const submenuListEl = document.querySelector("#submenu-list");
const resultOverlayEl = document.querySelector("#result-overlay");
const resultLabelEl = document.querySelector("#result-label");
const resultTitleEl = document.querySelector("#result-title");
const resultStatusEl = document.querySelector("#result-status");
const resultSummaryEl = document.querySelector("#result-summary");
const resultRewardTitleEl = document.querySelector("#result-reward-title");
const resultLinesEl = document.querySelector("#result-lines");
const resultNextActionEl = document.querySelector("#result-next-action");
const actionLogEl = document.querySelector("#action-log");
const clearLogEl = document.querySelector("#clear-log");

const state = {
  model: null,
  actionLog: [],
  logExpanded: false,
  activeSubmenu: null,
  submenuAnchorActionId: null,
  resultOpen: false,
};

fixtureSelect.addEventListener("change", () => {
  loadFixture(fixtureSelect.value);
});

clearLogEl.addEventListener("click", () => {
  state.actionLog = [];
  renderActionLog();
});

toggleBattleLogEl.addEventListener("click", () => {
  state.logExpanded = !state.logExpanded;
  renderBattleLog();
});

resultNextActionEl.addEventListener("click", () => {
  activateResultNextAction();
});

window.addEventListener("resize", () => {
  if (state.activeSubmenu) {
    positionSubmenu();
  }
});

loadFixture(fixtureSelect.value);

async function loadFixture(path) {
  if (runtimeClient.isLiveMode()) {
    await loadLiveScreen(path);
    return;
  }

  shellEl.dataset.loadState = "loading";
  try {
    const response = await fetch(path, { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`Fixture request failed: ${response.status}`);
    }

    const model = await response.json();
    state.model = model;
    state.actionLog = [];
    state.logExpanded = false;
    state.activeSubmenu = null;
    state.submenuAnchorActionId = null;
    state.resultOpen = false;
    render();
    logSystem(`loaded ${path}`);
    shellEl.dataset.loadState = "ready";
  } catch (error) {
    renderLoadError(error);
    shellEl.dataset.loadState = "error";
  }
}

async function loadLiveScreen(path) {
  shellEl.dataset.loadState = "loading";
  try {
    const model = await runtimeClient.getScreen("combat_screen");
    state.model = model;
    state.actionLog = [];
    state.logExpanded = false;
    state.activeSubmenu = null;
    state.submenuAnchorActionId = null;
    state.resultOpen = Boolean(model.result_overlay);
    render();
    logSystem(`live runtime screen loaded from ${path}`);
    shellEl.dataset.loadState = "ready";
  } catch (error) {
    await loadStaticFallback(path, error);
  }
}

async function loadStaticFallback(path, liveError) {
  try {
    const response = await fetch(path, { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`Fixture request failed: ${response.status}`);
    }
    const model = await response.json();
    state.model = model;
    state.actionLog = [];
    state.logExpanded = false;
    state.activeSubmenu = null;
    state.submenuAnchorActionId = null;
    state.resultOpen = false;
    render();
    logSystem(`live unavailable; loaded fixture ${path}`);
    pushActionLog({
      action_id: "live_bridge_unavailable",
      payload: { reason: liveError instanceof Error ? liveError.message : String(liveError) },
      source: "live_loader",
      dispatched: false,
      reason: "fallback_to_fixture",
    });
    shellEl.dataset.loadState = "ready";
  } catch (error) {
    renderLoadError(error);
    shellEl.dataset.loadState = "error";
  }
}

function render() {
  const { model } = state;
  titleEl.textContent = model.title ?? "";
  subtitleEl.textContent = model.subtitle ?? "";
  renderResources(model.resource_strip ?? []);
  renderBattlefield(model);
  renderBattleLog();
  commandMessageEl.textContent = model.command_message ?? "";
  renderCommands(model.actions ?? []);
  renderSubmenu();
  renderResultOverlay();
  renderActionLog();
}

function renderResources(items) {
  const roundItem = items.find((item) => (item.label ?? "").includes("回合"));
  if (!roundItem) {
    resourceStripEl.hidden = true;
    resourceStripEl.replaceChildren();
    return;
  }

  resourceStripEl.hidden = false;
  resourceStripEl.replaceChildren(
    (() => {
      const el = document.createElement("div");
      el.className = "resource-item";
      el.dataset.tone = roundItem.tone ?? "neutral";
      el.textContent = roundItem.label ?? "";
      return el;
    })(),
  );
}

function renderBattlefield(model) {
  const player = model.player ?? {};
  const enemy = model.enemy ?? {};
  enemyNameEl.textContent = enemy.name ?? "";
  enemyHpFillEl.style.setProperty("--meter-value", `${Math.max(0, Math.min(100, enemy.hp_percent ?? 0))}%`);
  enemyHpLabelEl.textContent = enemy.hp_label ?? "";
  renderEnemyMeta(enemy);
  playerNameEl.textContent = player.name ?? "";

  const focusRows = [
    ["HP", player.hp_label ?? ""],
    ["MP", player.mp_label ?? ""],
    ["狀態", player.status_label ?? ""],
    ["姿態", player.stance_label ?? ""],
  ];
  playerFocusStatsEl.replaceChildren(
    ...focusRows.map(([label, value]) => {
      const row = document.createElement("div");
      row.className = "focus-stat";

      const strong = document.createElement("strong");
      strong.textContent = label;

      const span = document.createElement("span");
      span.textContent = value;

      row.append(strong, span);
      return row;
    }),
  );
}

function renderEnemyMeta(enemy) {
  const rows = [
    ["屬性", enemy.attribute],
    ["狀態", enemy.status_label],
  ].filter(([, value]) => Boolean(value));

  enemyMetaEl.replaceChildren(
    ...rows.map(([label, value]) => {
      const item = document.createElement("span");
      item.textContent = `${label} ${value}`;
      return item;
    }),
  );
}

function renderBattleLog() {
  const lines = state.model?.battle_log ?? [];
  const visibleLines = state.logExpanded ? lines : lines.slice(-5);
  shellEl.dataset.logExpanded = String(state.logExpanded);
  logModeLabelEl.textContent = state.logExpanded ? "完整" : "最近 5 條";
  toggleBattleLogEl.textContent = state.logExpanded ? "收合" : "展開";

  if (visibleLines.length === 0) {
    battleLogEl.replaceChildren(createEmptyState("尚無 Battle Log。"));
    return;
  }

  battleLogEl.replaceChildren(
    ...visibleLines.map((line) => {
      const item = document.createElement("li");
      item.textContent = line;
      return item;
    }),
  );
}

function renderCommands(actions) {
  commandRowEl.replaceChildren(
    ...actions.map((action) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "command-button";
      button.dataset.actionId = action.action_id ?? "unavailable";
      button.dataset.payload = JSON.stringify(action.payload ?? {});
      button.dataset.disabledReason = action.disabled_reason ?? "";
      button.dataset.primary = String(Boolean(action.primary));
      button.dataset.active = "false";
      button.dataset.enabled = String(Boolean(action.enabled));
      button.setAttribute("aria-disabled", String(!action.enabled));
      button.disabled = state.resultOpen;
      button.title = action.enabled ? action.description ?? "" : action.disabled_reason ?? "";

      const label = document.createElement("strong");
      label.textContent = action.label ?? action.action_id;

      const description = document.createElement("span");
      description.textContent = action.description ?? "";

      button.append(label, description);
      button.addEventListener("click", () => activateAction(action, "command_bar", button));
      return button;
    }),
  );
  updateCommandActiveState();
}

function renderActionLog() {
  if (state.actionLog.length === 0) {
    const empty = document.createElement("li");
    empty.textContent = "尚無 UIAction event。";
    actionLogEl.replaceChildren(empty);
    return;
  }

  actionLogEl.replaceChildren(
    ...state.actionLog.map((entry) => {
      const li = document.createElement("li");
      li.className = entry.dispatched ? "log-dispatched" : "log-blocked";
      li.textContent = `[${entry.time}] ${entry.dispatched ? "dispatch" : "blocked"} ${entry.action_id} ${JSON.stringify(
        entry.payload ?? {},
      )}${entry.reason ? ` reason=${entry.reason}` : ""}`;
      return li;
    }),
  );
}

async function activateAction(action, source, triggerEl = null) {
  if (state.resultOpen) {
    pushActionLog({
      action_id: action.action_id,
      payload: action.payload ?? {},
      source,
      dispatched: false,
      reason: "combat already resolved",
    });
    commandMessageEl.textContent = "戰鬥已結束，請確認結算。";
    return;
  }

  if (!action.enabled) {
    pushActionLog({
      action_id: action.action_id,
      payload: action.payload ?? {},
      source,
      dispatched: false,
      reason: action.disabled_reason ?? "disabled",
    });
    commandMessageEl.textContent = action.disabled_reason || "目前無法執行這個指令。";
    return;
  }

  if (action.action_id === "open_skill_menu" && state.activeSubmenu === "skill") {
    closeSubmenu("已收回技能選單。");
    return;
  }

  if (action.action_id === "open_item_menu" && state.activeSubmenu === "item") {
    closeSubmenu("已收回道具選單。");
    return;
  }

  pushActionLog({
    action_id: action.action_id,
    payload: action.payload ?? {},
    source,
    dispatched: true,
  });

  if (action.action_id === "open_skill_menu") {
    commandMessageEl.textContent = action.feedback_message ?? "已開啟技能選單。再次按技能可收回。";
    openSubmenu("skill", triggerEl);
    return;
  }

  if (action.action_id === "open_item_menu") {
    commandMessageEl.textContent = action.feedback_message ?? "已開啟道具選單。再次按道具可收回。";
    openSubmenu("item", triggerEl);
    return;
  }

  if (runtimeClient.isLiveMode()) {
    await dispatchRuntimeAction(action, source);
    return;
  }

  state.activeSubmenu = null;
  state.submenuAnchorActionId = null;
  renderSubmenu();
  commandMessageEl.textContent =
    action.feedback_message ?? `已送出 ${action.action_id}。static prototype 不會計算戰鬥結果。`;

  if (action.opens_result) {
    openResultOverlay(action);
  }
}

async function dispatchRuntimeAction(action, source) {
  try {
    const result = await runtimeClient.dispatchAction("combat_screen", action.action_id, action.payload ?? {});
    if (result.screen_model) {
      state.model = result.screen_model;
      state.activeSubmenu = null;
      state.submenuAnchorActionId = null;
      state.resultOpen = Boolean(result.screen_model.result_overlay);
      render();
    }
    if (result.message && !state.resultOpen) {
      commandMessageEl.textContent = result.message;
    }
    if (result.next_route) {
      window.setTimeout(() => {
        window.location.href = runtimeClient.nextRoute(result, "../town_hub/index.html");
      }, 140);
    }
  } catch (error) {
    const reason = error instanceof Error ? error.message : String(error);
    pushActionLog({
      action_id: action.action_id,
      payload: action.payload ?? {},
      source,
      dispatched: false,
      reason,
    });
    commandMessageEl.textContent = reason;
  }
}

function openSubmenu(type, triggerEl = null) {
  state.activeSubmenu = type;
  state.submenuAnchorActionId =
    triggerEl?.dataset.actionId ?? (type === "skill" ? "open_skill_menu" : "open_item_menu");
  renderSubmenu();
}

function closeSubmenu(message) {
  state.activeSubmenu = null;
  state.submenuAnchorActionId = null;
  renderSubmenu();
  if (message) {
    commandMessageEl.textContent = message;
  }
}

function renderSubmenu() {
  const menu = getActiveMenu();
  if (!menu) {
    submenuPanelEl.hidden = true;
    submenuPanelEl.dataset.menuType = "none";
    submenuLabelEl.textContent = "";
    submenuTitleEl.textContent = "";
    submenuSummaryEl.textContent = "";
    submenuListEl.replaceChildren();
    submenuPanelEl.dataset.placement = "none";
    submenuPanelEl.style.removeProperty("--submenu-left");
    submenuPanelEl.style.removeProperty("--submenu-width");
    submenuPanelEl.style.removeProperty("--submenu-anchor-x");
    submenuPanelEl.style.removeProperty("--submenu-under-top");
    submenuPanelEl.style.removeProperty("--submenu-under-max-height");
    updateCommandActiveState();
    return;
  }

  submenuPanelEl.hidden = false;
  submenuPanelEl.dataset.menuType = state.activeSubmenu;
  submenuLabelEl.textContent = menu.label ?? "";
  submenuTitleEl.textContent = menu.title ?? "";
  submenuSummaryEl.textContent = menu.summary ?? "";

  const items = menu.items ?? [];
  if (items.length === 0) {
    submenuListEl.replaceChildren(createEmptyState(menu.empty_message ?? "沒有可用項目。"));
    positionSubmenu();
    updateCommandActiveState();
    return;
  }

  submenuListEl.replaceChildren(
    ...items.map((item) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "submenu-option";
      button.dataset.actionId = item.action_id ?? "unavailable";
      button.dataset.payload = JSON.stringify(item.payload ?? {});
      button.dataset.disabledReason = item.disabled_reason ?? "";
      button.setAttribute("aria-disabled", String(!item.enabled));
      button.title = item.enabled ? item.description ?? "" : item.disabled_reason ?? "";

      const title = document.createElement("strong");
      title.textContent = item.label ?? item.action_id;

      const meta = document.createElement("span");
      meta.textContent = item.meta ?? "";

      const description = document.createElement("small");
      description.textContent = item.enabled ? item.description ?? "" : item.disabled_reason ?? item.description ?? "";

      button.append(title, meta, description);
      button.addEventListener("click", () => activateSubmenuItem(item));
      return button;
    }),
  );
  positionSubmenu();
  updateCommandActiveState();
}

function renderResultOverlay() {
  const result = state.model?.result_overlay ?? null;
  shellEl.dataset.resultOpen = String(state.resultOpen && Boolean(result));

  if (!state.resultOpen || !result) {
    resultOverlayEl.hidden = true;
    resultOverlayEl.dataset.outcome = "none";
    resultLabelEl.textContent = "";
    resultTitleEl.textContent = "";
    resultStatusEl.textContent = "";
    resultSummaryEl.textContent = "";
    resultRewardTitleEl.textContent = "";
    resultLinesEl.replaceChildren();
    resultNextActionEl.textContent = "";
    resultNextActionEl.disabled = true;
    updateCommandActiveState();
    return;
  }

  resultOverlayEl.hidden = false;
  resultOverlayEl.dataset.outcome = result.outcome ?? "neutral";
  resultLabelEl.textContent = result.label ?? "戰鬥結算";
  resultTitleEl.textContent = result.title ?? "";
  resultStatusEl.textContent = result.status_summary ?? "";
  resultSummaryEl.textContent = result.battle_summary ?? "";
  resultRewardTitleEl.textContent = result.reward_title ?? "結果";
  resultLinesEl.replaceChildren(...(result.rows ?? []).map(createResultLine));

  const nextAction = result.next_action ?? {};
  resultNextActionEl.textContent = nextAction.label ?? "下一步";
  resultNextActionEl.title = nextAction.description ?? "";
  resultNextActionEl.disabled = !nextAction.action_id;
  updateCommandActiveState();
}

function openResultOverlay(action) {
  if (!state.model?.result_overlay) {
    commandMessageEl.textContent = "這個 static fixture 尚未提供 result_overlay。";
    return;
  }

  state.resultOpen = true;
  state.activeSubmenu = null;
  state.submenuAnchorActionId = null;
  renderSubmenu();
  renderResultOverlay();
  commandMessageEl.textContent =
    action.result_message ?? action.feedback_message ?? "戰鬥已結束，請確認結算。";
}

async function activateResultNextAction() {
  const nextAction = state.model?.result_overlay?.next_action ?? null;
  if (!state.resultOpen || !nextAction?.action_id) {
    return;
  }

  pushActionLog({
    action_id: nextAction.action_id,
    payload: nextAction.payload ?? {},
    source: "result_overlay",
    dispatched: true,
  });
  commandMessageEl.textContent = nextAction.feedback_message ?? `已送出 ${nextAction.action_id}。`;

  if (runtimeClient.isLiveMode()) {
    try {
      const result = await runtimeClient.dispatchAction("combat_screen", nextAction.action_id, nextAction.payload ?? {});
      window.setTimeout(() => {
        window.location.href = runtimeClient.nextRoute(result, nextAction.navigate_to ?? "../town_hub/index.html");
      }, 140);
    } catch (error) {
      pushActionLog({
        action_id: nextAction.action_id,
        payload: nextAction.payload ?? {},
        source: "result_overlay",
        dispatched: false,
        reason: error instanceof Error ? error.message : String(error),
      });
    }
    return;
  }

  if (nextAction.navigate_to) {
    window.setTimeout(() => {
      window.location.href = nextAction.navigate_to;
    }, 140);
  }
}

function createResultLine(row) {
  const item = document.createElement("div");
  item.className = "result-line";
  item.dataset.tone = row.tone ?? "neutral";

  const labelText = row.label ?? "";
  const isNumericLabel = /^\d+\.?$/.test(labelText.trim());
  if (isNumericLabel) {
    item.classList.add("result-line-list");
  } else {
    item.classList.add("result-line-kv");
  }

  const label = document.createElement("strong");
  label.textContent = labelText;

  const value = document.createElement("span");
  value.textContent = row.value ?? "";

  item.append(label, value);
  if (row.detail) {
    const detail = document.createElement("small");
    detail.textContent = row.detail;
    item.append(detail);
  }
  return item;
}

function positionSubmenu() {
  const anchorId =
    state.submenuAnchorActionId ?? (state.activeSubmenu === "skill" ? "open_skill_menu" : "open_item_menu");
  const anchorEl = commandRowEl.querySelector(`[data-action-id="${anchorId}"]`);
  if (!anchorEl || !combatFooterEl) {
    return;
  }

  const footerRect = combatFooterEl.getBoundingClientRect();
  const anchorRect = anchorEl.getBoundingClientRect();
  const commandRowRect = commandRowEl.getBoundingClientRect();
  const inset = 10;
  const preferredWidth = 560;
  const minWidth = 300;
  const availableWidth = Math.max(minWidth, footerRect.width - inset * 2);
  const width = Math.min(preferredWidth, availableWidth);
  const anchorCenter = anchorRect.left - footerRect.left + anchorRect.width / 2;
  const left = Math.max(inset, Math.min(anchorCenter - width / 2, footerRect.width - width - inset));
  const anchorX = Math.max(18, Math.min(anchorCenter - left, width - 18));

  const useStackedPlacement = window.innerWidth <= 1180;
  submenuPanelEl.dataset.placement = useStackedPlacement ? "under-command" : "above-command";
  submenuPanelEl.style.setProperty("--submenu-left", `${left}px`);
  submenuPanelEl.style.setProperty("--submenu-width", `${width}px`);
  submenuPanelEl.style.setProperty("--submenu-anchor-x", `${anchorX}px`);
  submenuPanelEl.style.setProperty("--submenu-under-top", `${commandRowRect.bottom - footerRect.top + 10}px`);
  submenuPanelEl.style.setProperty(
    "--submenu-under-max-height",
    `${Math.max(140, Math.min(220, window.innerHeight - commandRowRect.bottom - 22))}px`,
  );
}

function updateCommandActiveState() {
  commandRowEl.querySelectorAll(".command-button").forEach((button) => {
    const actionId = button.dataset.actionId;
    const isBaseDisabled = button.dataset.enabled !== "true";
    const isActive =
      (state.activeSubmenu === "skill" && actionId === "open_skill_menu") ||
      (state.activeSubmenu === "item" && actionId === "open_item_menu");
    button.dataset.active = String(isActive);
    button.disabled = state.resultOpen;
    button.setAttribute("aria-disabled", String(state.resultOpen || isBaseDisabled));
  });
}

function getActiveMenu() {
  if (state.activeSubmenu === "skill") {
    return state.model?.skill_menu ?? null;
  }

  if (state.activeSubmenu === "item") {
    return state.model?.item_menu ?? null;
  }

  return null;
}

async function activateSubmenuItem(item) {
  if (!item.enabled) {
    pushActionLog({
      action_id: item.action_id,
      payload: item.payload ?? {},
      source: `${state.activeSubmenu}_submenu`,
      dispatched: false,
      reason: item.disabled_reason ?? "disabled",
    });
    commandMessageEl.textContent = item.disabled_reason || "目前無法使用這個項目。";
    return;
  }

  pushActionLog({
    action_id: item.action_id,
    payload: item.payload ?? {},
    source: `${state.activeSubmenu}_submenu`,
    dispatched: true,
  });
  if (runtimeClient.isLiveMode()) {
    await dispatchRuntimeAction(item, `${state.activeSubmenu}_submenu`);
    return;
  }
  commandMessageEl.textContent =
    item.feedback_message ?? `已送出 ${item.action_id}。static prototype 不會計算戰鬥結果。`;
}

function pushActionLog(entry) {
  state.actionLog = [
    {
      time: new Date().toLocaleTimeString("zh-TW", { hour12: false }),
      ...entry,
    },
    ...state.actionLog,
  ].slice(0, 20);
  renderActionLog();
}

function logSystem(message) {
  state.actionLog = [
    {
      time: new Date().toLocaleTimeString("zh-TW", { hour12: false }),
      action_id: "fixture_loaded",
      payload: { message },
      source: "fixture_loader",
      dispatched: true,
    },
  ];
  renderActionLog();
}

function createEmptyState(message) {
  const empty = document.createElement("div");
  empty.className = "empty-state";
  empty.textContent = message;
  return empty;
}

function renderLoadError(error) {
  state.resultOpen = false;
  titleEl.textContent = "Fixture 載入失敗";
  subtitleEl.textContent = "無法讀取 Combat Screen static fixture。";
  resourceStripEl.replaceChildren();
  enemyNameEl.textContent = "無法載入戰鬥畫面";
  enemyHpLabelEl.textContent = error instanceof Error ? error.message : String(error);
  enemyMetaEl.replaceChildren();
  playerNameEl.textContent = "";
  playerFocusStatsEl.replaceChildren();
  battleLogEl.replaceChildren();
  commandMessageEl.textContent = "";
  commandRowEl.replaceChildren(createEmptyState("沒有可用指令。"));
  closeSubmenu();
  renderResultOverlay();
}
