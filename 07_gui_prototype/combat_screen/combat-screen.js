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
const commandMessageEl = document.querySelector("#command-message");
const commandRowEl = document.querySelector("#command-row");
const actionLogEl = document.querySelector("#action-log");
const clearLogEl = document.querySelector("#clear-log");

const state = {
  model: null,
  actionLog: [],
  logExpanded: false,
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

loadFixture(fixtureSelect.value);

async function loadFixture(path) {
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
    render();
    logSystem(`loaded ${path}`);
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
  renderActionLog();
}

function renderResources(items) {
  resourceStripEl.replaceChildren(
    ...items.map((item) => {
      const el = document.createElement("div");
      el.className = "resource-item";
      el.dataset.tone = item.tone ?? "neutral";
      el.textContent = item.label ?? "";
      return el;
    }),
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
    ["弱點", enemy.weakness],
    ["威脅", enemy.threat_label],
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
      button.setAttribute("aria-disabled", String(!action.enabled));
      button.title = action.enabled ? action.description ?? "" : action.disabled_reason ?? "";

      const label = document.createElement("strong");
      label.textContent = action.label ?? action.action_id;

      const description = document.createElement("span");
      description.textContent = action.description ?? "";

      button.append(label, description);
      button.addEventListener("click", () => activateAction(action, "command_bar"));
      return button;
    }),
  );
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

function activateAction(action, source) {
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

  pushActionLog({
    action_id: action.action_id,
    payload: action.payload ?? {},
    source,
    dispatched: true,
  });

  commandMessageEl.textContent =
    action.feedback_message ?? `已送出 ${action.action_id}。static prototype 不會計算戰鬥結果。`;
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
}
