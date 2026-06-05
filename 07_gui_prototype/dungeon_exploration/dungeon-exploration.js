import { runtimeClient } from "../shared/runtime-client.js";

const fixtureSelect = document.querySelector("#fixture-select");
const shellEl = document.querySelector(".exploration-shell");
const titleEl = document.querySelector("#screen-title");
const subtitleEl = document.querySelector("#screen-subtitle");
const resourceStripEl = document.querySelector("#resource-strip");
const locationNameEl = document.querySelector("#location-name");
const locationSummaryEl = document.querySelector("#location-summary");
const locationMetaEl = document.querySelector("#location-meta");
const stepLabelEl = document.querySelector("#step-label");
const stepDetailEl = document.querySelector("#step-detail");
const stepFillEl = document.querySelector("#step-fill");
const runStatsEl = document.querySelector("#run-stats");
const rewardSummaryEl = document.querySelector("#reward-summary");
const eventPreviewEl = document.querySelector("#event-preview");
const narrativeMessageEl = document.querySelector("#narrative-message");
const actionRowEl = document.querySelector("#action-row");
const actionLogEl = document.querySelector("#action-log");
const clearLogEl = document.querySelector("#clear-log");

const state = {
  model: null,
  actionLog: [],
};

const staticActionRoutes = {
  enter_combat_preview: "../combat_screen/index.html",
  retreat: "../world_map/index.html",
  challenge_boss: "../combat_screen/index.html",
};
const navigationDelayMs = 120;

fixtureSelect.addEventListener("change", () => {
  loadFixture(fixtureSelect.value);
});

clearLogEl.addEventListener("click", () => {
  state.actionLog = [];
  renderActionLog();
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
    const model = await runtimeClient.getScreen("dungeon_exploration");
    state.model = model;
    state.actionLog = [];
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
  renderDungeon(model.dungeon ?? {});
  renderRun(model.run_status ?? {});
  renderRewards(model.run_rewards ?? []);
  renderEvents(model.event_preview ?? []);
  narrativeMessageEl.textContent = model.narrative_message ?? "";
  renderActions(model.actions ?? []);
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

function renderDungeon(dungeon) {
  locationNameEl.textContent = dungeon.name ?? "";
  locationSummaryEl.textContent = dungeon.summary ?? "";

  const rows = [
    ["屬性", dungeon.attribute ?? ""],
    ["路線", dungeon.route_length ?? ""],
    ["通關狀態", dungeon.clear_state ?? ""],
    ["守護者", dungeon.boss_state ?? ""],
  ].filter(([, value]) => Boolean(value));
  locationMetaEl.replaceChildren(...rows.map(([label, value]) => createInfoRow("meta-row", label, value)));
}

function renderRun(runStatus) {
  const currentStep = Number(runStatus.current_step ?? 0);
  const totalSteps = Number(runStatus.total_steps ?? 0);
  const percent = totalSteps > 0 ? Math.round((currentStep / totalSteps) * 100) : 0;

  stepLabelEl.textContent = `${currentStep} / ${totalSteps} 步`;
  stepDetailEl.textContent = runStatus.step_note ?? "";
  stepFillEl.style.setProperty("--meter-value", `${Math.max(0, Math.min(100, percent))}%`);

  const rows = [
    ["狀態", runStatus.status_label ?? ""],
    ["危險度", runStatus.risk_label ?? ""],
    ["小隊狀態", runStatus.supply_label ?? ""],
  ];
  runStatsEl.replaceChildren(...rows.map(([label, value]) => createInfoRow("run-stat", label, value)));
}

function renderRewards(items) {
  if (items.length === 0) {
    rewardSummaryEl.replaceChildren(createEmptyState("尚未取得本趟收益。"));
    return;
  }

  const summary = items
    .slice(0, 2)
    .map((item) => `${item.label ?? ""} ${item.value ?? ""}`.trim())
    .join(" / ");
  rewardSummaryEl.replaceChildren(createSummaryLine(summary));
}

function renderEvents(lines) {
  if (lines.length === 0) {
    eventPreviewEl.replaceChildren(createEmptyState("尚無事件紀錄。"));
    return;
  }

  eventPreviewEl.replaceChildren(
    ...lines.map((line) => {
      const p = document.createElement("p");
      p.textContent = line ?? "";
      return p;
    }),
  );

  eventPreviewEl.scrollTop = eventPreviewEl.scrollHeight;
}

function renderActions(actions) {
  const visibleActionIds = new Set(["advance_step", "retreat", "challenge_boss"]);
  const visibleActions = actions.filter((action) => visibleActionIds.has(action.action_id));

  const hasBoss = visibleActions.some((a) => a.action_id === "challenge_boss");
  if (hasBoss) {
    actionRowEl.classList.add("has-three-cols");
  } else {
    actionRowEl.classList.remove("has-three-cols");
  }

  actionRowEl.replaceChildren(
    ...visibleActions.map((action) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "action-button";
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
      button.addEventListener("click", () => activateAction(action, "action_bar"));
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

async function activateAction(action, source) {
  if (!action.enabled) {
    pushActionLog({
      action_id: action.action_id,
      payload: action.payload ?? {},
      source,
      dispatched: false,
      reason: action.disabled_reason ?? "disabled",
    });
    narrativeMessageEl.textContent = action.disabled_reason || "目前無法執行這個動作。";
    return;
  }

  pushActionLog({
    action_id: action.action_id,
    payload: action.payload ?? {},
    source,
    dispatched: true,
  });

  if (runtimeClient.isLiveMode()) {
    await dispatchRuntimeAction(action, source);
    return;
  }

  if (action.feedback_message) {
    narrativeMessageEl.textContent = action.feedback_message;
  } else {
    narrativeMessageEl.textContent = `已送出 ${action.action_id}。static prototype 不會推進探索狀態。`;
  }

  navigateAfterAction(action);
}

async function dispatchRuntimeAction(action, source) {
  try {
    const result = await runtimeClient.dispatchAction("dungeon_exploration", action.action_id, action.payload ?? {});
    if (result.screen_model) {
      state.model = result.screen_model;
      render();
    }
    narrativeMessageEl.textContent = result.message ?? `Dispatched ${action.action_id}`;
    if (result.next_route) {
      window.setTimeout(() => {
        window.location.href = runtimeClient.nextRoute(result, staticActionRoutes[action.action_id]);
      }, navigationDelayMs);
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
    narrativeMessageEl.textContent = reason;
  }
}

function navigateAfterAction(action) {
  if (action.action_id === "advance_step" && action.payload?.encounter_hint) {
    window.setTimeout(() => {
      window.location.href = runtimeClient.withLiveMode(staticActionRoutes.enter_combat_preview);
    }, navigationDelayMs);
    return;
  }

  const route = staticActionRoutes[action.action_id];
  if (!route) {
    return;
  }

  window.setTimeout(() => {
    window.location.href = runtimeClient.withLiveMode(route);
  }, navigationDelayMs);
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

function createInfoRow(className, labelText, valueText) {
  const row = document.createElement("div");
  row.className = className;

  const label = document.createElement("span");
  label.textContent = labelText;

  const value = document.createElement("span");
  value.textContent = valueText;

  row.append(label, value);
  return row;
}

function createSummaryLine(text) {
  const summary = document.createElement("p");
  summary.className = "summary-line";
  summary.textContent = text;
  return summary;
}

function createEmptyState(message) {
  const empty = document.createElement("div");
  empty.className = "empty-state";
  empty.textContent = message;
  return empty;
}

function renderLoadError(error) {
  titleEl.textContent = "Fixture 載入失敗";
  subtitleEl.textContent = "無法讀取 Dungeon Exploration static fixture。";
  resourceStripEl.replaceChildren();
  locationNameEl.textContent = "無法載入探索畫面";
  locationSummaryEl.textContent = error instanceof Error ? error.message : String(error);
  locationMetaEl.replaceChildren();
  runStatsEl.replaceChildren();
  rewardSummaryEl.replaceChildren();
  eventPreviewEl.replaceChildren();
  narrativeMessageEl.textContent = "";
  actionRowEl.replaceChildren(createEmptyState("沒有可用 action。"));
}
