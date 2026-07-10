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

function cleanTitle(title) {
  if (!title) return "";
  let cleaned = title;
  const replacements = [
    [" / CLI 任務骨架", ""],
    [" / 委託板 (Live)", ""],
    [" (Relic Altar)", ""],
    [" (Temple & Church)", ""],
    [" (Ember Inn)", ""],
    [" (Live)", ""],
    [" (Shop)", ""],
    [" (Guild)", ""],
    [" (Magic Shop)", ""],
    [" (Synthesis)", ""],
    [" (Inn)", ""],
    [" (Storage)", ""],
    [" (Temple)", ""],
    [" (Workshop)", ""],
    [" (Relic Preview)", ""]
  ];
  for (const [target, replacement] of replacements) {
    cleaned = cleaned.replace(target, replacement);
  }
  return cleaned.trim();
}

function getElementIcon(elementId) {
  switch (elementId) {
    case "fire":
      return `<svg class="element-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M13.2 2.2c.5 3-1.5 4.5-3 6.2-1.5 1.7-2.7 3.3-2.7 5.8A4.6 4.6 0 0 0 12.1 19c2.7 0 4.9-2.1 4.9-4.9 0-2.6-1.5-5.1-3.8-7.2.2 2-1 3.1-2 4.1.3-3.4 2.8-5 2-8.8Z"/></svg>`;
    case "ice":
      return `<svg class="element-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M12 3v18M4.2 7.5l15.6 9M4.2 16.5l15.6-9M12 3l-2 2M12 3l2 2M12 21l-2-2M12 21l2-2"/></svg>`;
    case "water":
      return `<svg class="element-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2.7 6.3 8.4a8 8 0 1 0 11.4 0L12 2.7Zm0 15.8a4.5 4.5 0 0 1-4.5-4.5c0-1.5.8-2.8 1.7-4l1.1-1.3c-.3 2.9 1.5 5.7 4.4 6.3-.5 2-1.4 3.5-2.7 3.5Z"/></svg>`;
    case "wind":
      return `<svg class="element-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M4 8h10a2.5 2.5 0 1 0-2.5-2.5M3 12h15a2 2 0 1 1-2 2M5 16h8"/></svg>`;
    case "earth":
      return `<svg class="element-icon" viewBox="0 0 24 24" fill="currentColor" fill-rule="evenodd"><path d="M12 3 2.5 20h19L12 3Zm0 6 4.2 7.5H7.8L12 9Z"/></svg>`;
    case "thunder":
      return `<svg class="element-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M13.5 2 5 13h6l-1 9 9-13h-6l.5-7Z"/></svg>`;
    case "light":
      return `<svg class="element-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M5 12H2M22 12h-3M4.9 4.9 7 7M17 17l2.1 2.1M19.1 4.9 17 7M7 17l-2.1 2.1"/></svg>`;
    case "dark":
      return `<svg class="element-icon" viewBox="0 0 24 24" fill="currentColor"><path d="M12.3 2A10 10 0 0 0 2 12.3a1 1 0 0 0 1.2 1.2A8 8 0 1 1 13.5 3.3a1 1 0 0 0-1.2-1.3Z"/></svg>`;
    default:
      return `<svg class="element-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="8"/></svg>`;
  }
}

function render() {
  const { model } = state;
  applyFacilityBackground({ model, shell: shellEl, backgrounds: relicBackgroundByRegion });
  titleEl.textContent = cleanTitle(model.title);
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
      const cleanLabel = (slot.label ?? "")
        .replace(/[\uE000-\uF8FF]/g, "")
        .replace(/[\p{Extended_Pictographic}\p{Emoji_Presentation}\p{Symbol}]/gu, "")
        .trim();
      label.innerHTML = `
        ${getElementIcon(slot.element_id)}
        <span class="label-text">${cleanLabel}</span>
      `;

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
