import { runtimeClient } from "../shared/runtime-client.js";

const fixtureSelect = document.querySelector("#fixture-select");
const titleEl = document.querySelector("#screen-title");
const subtitleEl = document.querySelector("#screen-subtitle");
const resourceStripEl = document.querySelector("#resource-strip");
const serviceNameEl = document.querySelector("#service-name");
const serviceDescriptionEl = document.querySelector("#service-description");
const serviceCostEl = document.querySelector("#service-cost");
const rumorsContainerEl = document.querySelector("#rumors-container");
const confirmRestBtnEl = document.querySelector("#confirm-rest-btn");
const npcNameEl = document.querySelector("#npc-name");
const npcDescriptionEl = document.querySelector("#npc-description");
const npcAvatarEl = document.querySelector("#npc-avatar");
const npcBubbleEl = document.querySelector("#npc-bubble");
const backToTownBtnEl = document.querySelector("#back-to-town");
const feedbackMessageEl = document.querySelector("#feedback-message");
const actionLogEl = document.querySelector("#action-log");
const clearLogEl = document.querySelector("#clear-log");
const shellEl = document.querySelector(".inn-shell");

// JRPG dialogue choices selectors
const dialogueChoicesEl = document.querySelector("#dialogue-choices");
const choiceYesEl = document.querySelector("#choice-yes");
const choiceNoEl = document.querySelector("#choice-no");

const state = {
  model: null,
  actionLog: [],
  uiState: "welcome", // welcome, confirm, rested
};

const navigationDelayMs = 120;

fixtureSelect.addEventListener("change", () => {
  loadFixture(fixtureSelect.value);
});

clearLogEl.addEventListener("click", () => {
  state.actionLog = [];
  renderActionLog();
});

// Trigger 2-step confirmation on rest click
confirmRestBtnEl.addEventListener("click", () => {
  if (state.uiState === "welcome") {
    enterConfirmState();
  }
});

// Dialogue choices event listeners
choiceYesEl.addEventListener("click", () => {
  triggerRest();
});

choiceNoEl.addEventListener("click", () => {
  cancelRest();
});

// Keyboard listener for JRPG-CLI alignment (Y/N/Enter)
document.addEventListener("keydown", (e) => {
  if (state.uiState === "confirm") {
    if (e.key === "y" || e.key === "Y") {
      triggerRest();
    } else if (e.key === "n" || e.key === "N") {
      cancelRest();
    }
  } else if (state.uiState === "rested") {
    if (e.key === "Enter" || e.key === " ") {
      resetToWelcome();
    }
  }
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
    const model = await runtimeClient.getScreen("inn_screen");
    state.model = model;
    state.actionLog = [];
    render();
    logSystem(`live runtime screen model loaded`);
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
  renderService(model.service ?? {});
  renderRumors(model.rumors ?? []);
  renderNPC(model.npc ?? {});
  renderActionLog();
  if (state.uiState === "welcome" && model.feedback_message) {
    feedbackMessageEl.textContent = model.feedback_message;
  }
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

function renderService(service) {
  serviceNameEl.textContent = service.label ?? "過夜休息";
  serviceDescriptionEl.textContent = service.description ?? "";
  serviceCostEl.textContent = `${service.cost ?? 30} G`;
  
  if (state.uiState === "welcome") {
    confirmRestBtnEl.disabled = !service.enabled;
    if (!service.enabled) {
      confirmRestBtnEl.title = service.disabled_reason ?? "";
      feedbackMessageEl.textContent = service.disabled_reason ?? "";
    } else {
      confirmRestBtnEl.removeAttribute("title");
      feedbackMessageEl.textContent = "";
    }
  }
}

function renderRumors(rumors) {
  rumorsContainerEl.replaceChildren(
    ...rumors.map((rumor) => {
      const el = document.createElement("div");
      el.className = "rumor-item";

      const title = document.createElement("p");
      title.className = "rumor-title";
      title.textContent = rumor.title ?? "";

      const content = document.createElement("p");
      content.className = "rumor-content";
      content.textContent = rumor.content ?? "";

      el.append(title, content);
      return el;
    }),
  );
}

function renderNPC(npc) {
  npcNameEl.textContent = npc.name ?? "莉莉 (Lily)";
  npcDescriptionEl.textContent = npc.description ?? "";
  npcAvatarEl.textContent = npc.avatar_token ?? "LY";
  if (state.uiState === "welcome") {
    npcBubbleEl.textContent = npc.prompt ?? "歡迎來到旅店！";
  }
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

// 2-Step Confirmation States
function enterConfirmState() {
  state.uiState = "confirm";
  dialogueChoicesEl.style.display = "flex";
  confirmRestBtnEl.disabled = true;
  backToTownBtnEl.disabled = true;

  const cost = state.model?.service?.cost ?? 30;
  const goldResource = state.model?.resource_strip?.find((r) => r.id === "gold");
  const goldText = goldResource ? goldResource.label : "1957G";

  npcBubbleEl.textContent = `莉莉 (Lily)：「要休息一晚嗎？費用：${cost}G / 目前金幣：${goldText}」`;

  pushActionLog({
    action_id: "inn_rest_prompt",
    payload: { cost },
    source: "confirm_rest_btn",
    dispatched: true,
  });
}

function cancelRest() {
  state.uiState = "welcome";
  dialogueChoicesEl.style.display = "none";
  confirmRestBtnEl.disabled = false;
  backToTownBtnEl.disabled = false;

  npcBubbleEl.textContent = state.model?.npc?.prompt ?? "歡迎來到旅店！";
  feedbackMessageEl.textContent = "";

  pushActionLog({
    action_id: "inn_rest_cancel",
    payload: {},
    source: "choice_no_btn",
    dispatched: true,
  });
}

function triggerRest() {
  dialogueChoicesEl.style.display = "none";
  handleRest();
}

async function handleRest() {
  const service = state.model?.service ?? { service_id: "overnight_rest", cost: 30 };
  
  if (runtimeClient.isLiveMode()) {
    pushActionLog({
      action_id: "rest_at_inn",
      payload: service.payload ?? {},
      source: "confirm_rest_btn",
      dispatched: true,
    });
    
    try {
      const result = await runtimeClient.dispatchAction("inn_screen", "rest_at_inn", service.payload ?? {});
      shellEl.dataset.runtimeStatus = result.status ?? "success";
      if (result.screen_model) {
        state.model = result.screen_model;
        render();
      }
      if (result.message) {
        feedbackMessageEl.textContent = result.message;
        npcBubbleEl.textContent = "莉莉 (Lily)：「休息好了嗎？祝你今天冒險順利！」";
      }
      enterRestedState();
    } catch (error) {
      const reason = runtimeClient.errorMessage(error);
      shellEl.dataset.runtimeStatus = error?.runtimeStatus ?? "error";
      pushActionLog({
        action_id: "rest_at_inn",
        payload: service.payload ?? {},
        source: "confirm_rest_btn",
        dispatched: false,
        reason,
      });
      resetToWelcome();
      feedbackMessageEl.textContent = reason;
    }
    return;
  }

  // 靜態模式：純前端模擬
  pushActionLog({
    action_id: "rest_at_inn",
    payload: service.payload ?? {},
    source: "confirm_rest_btn",
    dispatched: true,
  });

  feedbackMessageEl.textContent = "在旅館休息了一晚，HP/MP 已完全回滿。";
  npcBubbleEl.textContent = "莉莉 (Lily)：「看起來精神飽滿呢！今天也是充滿活力的一天！」";
  
  // 更新前端資源條模擬回滿
  const updatedStrip = [
    { id: "hp", label: "HP 192/192", tone: "hp" },
    { id: "mp", label: "MP 38/38", tone: "mp" },
    { id: "gold", label: "1927G", tone: "gold" } // 扣除 30G
  ];
  renderResources(updatedStrip);

  enterRestedState();
}

function enterRestedState() {
  state.uiState = "rested";
  confirmRestBtnEl.disabled = true;
  backToTownBtnEl.disabled = true;

  const hint = document.createElement("div");
  hint.className = "continue-hint";
  hint.style.fontSize = "11px";
  hint.style.color = "var(--gold-color)";
  hint.style.marginTop = "8px";
  hint.style.cursor = "pointer";
  hint.textContent = "按 Enter 鍵或點選此處繼續...";
  feedbackMessageEl.appendChild(hint);

  hint.addEventListener("click", () => {
    resetToWelcome();
  });
}

function resetToWelcome() {
  state.uiState = "welcome";
  confirmRestBtnEl.disabled = false;
  backToTownBtnEl.disabled = false;
  feedbackMessageEl.textContent = "";

  npcBubbleEl.textContent = state.model?.npc?.prompt ?? "歡迎來到旅店！";

  if (state.model) {
    render();
  }
}

async function handleBackToTown() {
  const payload = { from: "inn_screen" };
  pushActionLog({
    action_id: "back_to_town_hub",
    payload,
    source: "back_to_town",
    dispatched: true,
  });
  try {
    const result = await runtimeClient.dispatchAction("inn_screen", "back_to_town_hub", payload);
    shellEl.dataset.runtimeStatus = result.status ?? "success";
    window.setTimeout(() => {
      window.location.href = runtimeClient.nextRoute(result, "../town_hub/index.html");
    }, navigationDelayMs);
  } catch (error) {
    const reason = runtimeClient.errorMessage(error);
    shellEl.dataset.runtimeStatus = error?.runtimeStatus ?? "error";
    feedbackMessageEl.textContent = reason;
    pushActionLog({
      action_id: "back_to_town_hub",
      payload,
      source: "back_to_town",
      dispatched: false,
      reason,
    });
  }
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
  rumorsContainerEl.replaceChildren();
  confirmRestBtnEl.disabled = true;

  const errorEl = document.createElement("div");
  errorEl.className = "load-error";
  errorEl.textContent = error instanceof Error ? error.message : String(error);
  rumorsContainerEl.append(errorEl);
}
