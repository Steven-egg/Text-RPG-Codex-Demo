import { applyFacilityBackground } from "../shared/facility-backgrounds.js";
import { runtimeClient } from "../shared/runtime-client.js";

const fixtureSelect = document.querySelector("#fixture-select");
const titleEl = document.querySelector("#screen-title");
const subtitleEl = document.querySelector("#screen-subtitle");
const resourceStripEl = document.querySelector("#resource-strip");
const slotsContainerEl = document.querySelector("#slots-container");
const focusTitleEl = document.querySelector("#focus-title");
const focusSubtitleEl = document.querySelector("#focus-subtitle");
const orbVisualEl = document.querySelector("#orb-visual");
const focusFeedbackEl = document.querySelector("#focus-feedback");
const attuneRelicBtnEl = document.querySelector("#attune-relic-btn");
const tabletTranslationTextEl = document.querySelector("#tablet-translation-text");
const backToTownBtnEl = document.querySelector("#back-to-town");
const actionLogEl = document.querySelector("#action-log");
const clearLogEl = document.querySelector("#clear-log");
const shellEl = document.querySelector(".relic-shell");

const state = {
  model: null,
  selectedElementId: null,
  actionLog: [],
};

const navigationDelayMs = 120;

const relicBackgroundByRegion = {
  fire: "./assets/relic-preview-background.jpg",
  ice: "./assets/ice-relic-investigation-table-no-npc-cropped-candidate-v02.png",
  earth: "./assets/earth-relic-investigation-table-no-npc-candidate-v01.png",
  thunder: "./assets/thunder-relic-investigation-table-no-npc-candidate-v01.png",
  final: "./assets/final-relic-investigation-table-no-npc-candidate-v01.png",
};

fixtureSelect.addEventListener("change", () => {
  loadFixture(fixtureSelect.value);
});

clearLogEl.addEventListener("click", () => {
  state.actionLog = [];
  renderActionLog();
});

attuneRelicBtnEl.addEventListener("click", () => {
  handleAttune();
});

backToTownBtnEl.addEventListener("click", () => {
  if (runtimeClient.isLiveMode()) {
    handleBackToTown();
    return;
  }
  window.setTimeout(() => {
    window.location.href = runtimeClient.withLiveMode("../town_hub/index.html");
  }, navigationDelayMs);
});

loadFixture(fixtureSelect.value);

async function loadFixture(path) {
  if (runtimeClient.isLiveMode()) {
    await loadLiveScreen();
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
    state.selectedElementId = model.slots?.[0]?.element_id ?? null;
    state.actionLog = [];
    render();
    logSystem(`loaded ${path}`);
    shellEl.dataset.loadState = "ready";
  } catch (error) {
    renderLoadError(error);
    shellEl.dataset.loadState = "error";
  }
}

async function loadLiveScreen() {
  shellEl.dataset.loadState = "loading";
  try {
    const model = await runtimeClient.getScreen("relic_preview_screen");
    state.model = model;
    state.selectedElementId = model.slots?.[0]?.element_id ?? null;
    state.actionLog = [];
    render();
    logSystem("live runtime screen loaded", {
      actionId: "live_screen_loaded",
      source: "live_loader",
      payload: { mode: "live", screen_id: "relic_preview_screen" },
    });
    shellEl.dataset.loadState = "ready";
  } catch (error) {
    await loadStaticFallback(fixtureSelect.value, error);
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
    state.selectedElementId = model.slots?.[0]?.element_id ?? null;
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

async function handleBackToTown() {
  const payload = { from: "relic_preview_screen" };
  pushActionLog({
    action_id: "back_to_town_hub",
    payload,
    source: "back_to_town",
    dispatched: true,
  });
  try {
    const result = await runtimeClient.dispatchAction("relic_preview_screen", "back_to_town_hub", payload);
    shellEl.dataset.runtimeStatus = result.status ?? "success";
    window.setTimeout(() => {
      window.location.href = runtimeClient.nextRoute(result, "../town_hub/index.html");
    }, navigationDelayMs);
  } catch (error) {
    const reason = runtimeClient.errorMessage(error);
    shellEl.dataset.runtimeStatus = error?.runtimeStatus ?? "error";
    pushActionLog({
      action_id: "back_to_town_hub",
      payload,
      source: "back_to_town",
      dispatched: false,
      reason,
    });
  }
}

function render() {
  const { model } = state;
  applyFacilityBackground({ model, shell: shellEl, backgrounds: relicBackgroundByRegion });
  titleEl.textContent = model.title ?? "";
  subtitleEl.textContent = model.subtitle ?? "";
  
  renderResources(model.resource_strip ?? []);
  renderSlots(model.slots ?? []);
  renderSelectedRelic();
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

function renderSlots(slots) {
  slotsContainerEl.replaceChildren(
    ...slots.map((slot) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "slot-btn";
      btn.dataset.elementId = slot.element_id;
      btn.dataset.unlocked = String(slot.unlocked);
      
      if (slot.element_id === state.selectedElementId) {
        btn.classList.add("is-selected");
      }

      const label = document.createElement("span");
      label.className = "slot-label";
      label.textContent = slot.label ?? "";

      const meta = document.createElement("span");
      meta.className = "slot-meta";
      meta.textContent = slot.unlocked ? `已收集 (${slot.collected}/${slot.required})` : "LOCK / 未解鎖";

      btn.append(label, meta);
      btn.addEventListener("click", () => selectSlot(slot.element_id));
      
      return btn;
    }),
  );
}

function renderSelectedRelic() {
  const slot = getSelectedSlot();
  
  if (!slot) {
    focusTitleEl.textContent = "請選擇遺物";
    focusSubtitleEl.textContent = "";
    orbVisualEl.dataset.element = "none";
    tabletTranslationTextEl.textContent = "無可顯示之古代碑文譯本。";
    attuneRelicBtnEl.disabled = true;
    focusFeedbackEl.textContent = "";
    return;
  }

  focusTitleEl.textContent = slot.relic_name ?? "";
  focusSubtitleEl.textContent = slot.unlocked ? "【已解碼遺物核心】" : "【未知遺跡聖物】";
  orbVisualEl.dataset.element = slot.unlocked ? slot.element_id : "none";
  tabletTranslationTextEl.textContent = slot.ancient_text ?? "";
  
  // 只有已解鎖/已收集的聖物才可以 attune 共鳴
  attuneRelicBtnEl.disabled = !slot.unlocked;
  focusFeedbackEl.textContent = "";

  // 更新左側 button 狀態高亮
  [...slotsContainerEl.querySelectorAll(".slot-btn")].forEach((btn) => {
    const selected = btn.dataset.elementId === slot.element_id;
    btn.classList.toggle("is-selected", selected);
  });
}

function selectSlot(elementId) {
  if (state.selectedElementId === elementId) {
    return;
  }
  state.selectedElementId = elementId;
  pushActionLog({
    action_id: "select_relic_slot",
    payload: { element: elementId },
    source: "relic_altar_grid",
    dispatched: true,
  });
  renderSelectedRelic();
}

async function handleAttune() {
  const slot = getSelectedSlot();
  if (!slot) return;

  if (runtimeClient.isLiveMode()) {
    pushActionLog({
      action_id: "attune_relic",
      payload: { relic_id: slot.relic_name },
      source: "attune_button",
      dispatched: true,
    });
    
    try {
      const result = await runtimeClient.dispatchAction("relic_preview_screen", "attune_relic", { relic_id: slot.relic_name });
      shellEl.dataset.runtimeStatus = result.status ?? "success";
      if (result.screen_model) {
        state.model = result.screen_model;
        render();
      }
      if (result.message) {
        focusFeedbackEl.textContent = result.message;
      }
    } catch (error) {
      const reason = runtimeClient.errorMessage(error);
      shellEl.dataset.runtimeStatus = error?.runtimeStatus ?? "error";
      pushActionLog({
        action_id: "attune_relic",
        payload: { relic_id: slot.relic_name },
        source: "attune_button",
        dispatched: false,
        reason,
      });
      focusFeedbackEl.textContent = reason;
    }
    return;
  }

  pushActionLog({
    action_id: "attune_relic",
    payload: { relic_id: slot.relic_name },
    source: "attune_button",
    dispatched: true,
  });

  focusFeedbackEl.textContent = `共鳴度提升！核心發出微弱的脈衝反應！(靜態模擬已記錄 UIAction)`;
}

function getSelectedSlot() {
  return state.model?.slots?.find((s) => s.element_id === state.selectedElementId) ?? null;
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

function renderLoadError(error) {
  titleEl.textContent = "Fixture 載入失敗";
  subtitleEl.textContent = "無法讀取靜態 fixture。";
  resourceStripEl.replaceChildren();
  slotsContainerEl.replaceChildren();
  attuneRelicBtnEl.disabled = true;

  const errorEl = document.createElement("div");
  errorEl.className = "load-error";
  errorEl.textContent = error instanceof Error ? error.message : String(error);
  slotsContainerEl.append(errorEl);
}
