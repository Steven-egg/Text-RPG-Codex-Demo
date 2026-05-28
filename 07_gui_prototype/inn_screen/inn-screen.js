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

const state = {
  model: null,
  actionLog: [],
};

const navigationDelayMs = 120;

fixtureSelect.addEventListener("change", () => {
  loadFixture(fixtureSelect.value);
});

clearLogEl.addEventListener("click", () => {
  state.actionLog = [];
  renderActionLog();
});

confirmRestBtnEl.addEventListener("click", () => {
  handleRest();
});

backToTownBtnEl.addEventListener("click", () => {
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
  
  confirmRestBtnEl.disabled = !service.enabled;
  if (!service.enabled) {
    confirmRestBtnEl.title = service.disabled_reason ?? "";
    feedbackMessageEl.textContent = service.disabled_reason ?? "";
  } else {
    confirmRestBtnEl.removeAttribute("title");
    feedbackMessageEl.textContent = "";
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
  npcBubbleEl.textContent = npc.prompt ?? "歡迎來到旅店！";
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
      if (result.screen_model) {
        state.model = result.screen_model;
        render();
      }
      if (result.message) {
        feedbackMessageEl.textContent = result.message;
        npcBubbleEl.textContent = "休息好了嗎？祝你今天冒險順利！";
      }
    } catch (error) {
      feedbackMessageEl.textContent = error instanceof Error ? error.message : String(error);
      pushActionLog({
        action_id: "rest_at_inn",
        payload: service.payload ?? {},
        source: "confirm_rest_btn",
        dispatched: false,
        reason: error instanceof Error ? error.message : String(error),
      });
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

  feedbackMessageEl.textContent = "一夜好眠。您的體力與魔力已完全恢復！(靜態模擬)";
  npcBubbleEl.textContent = "看起來精神飽滿呢！今天也是充滿活力的一天！";
  
  // 更新前端資源條模擬回滿
  const updatedStrip = [
    { id: "hp", label: "HP 192/192", tone: "hp" },
    { id: "mp", label: "MP 38/38", tone: "mp" },
    { id: "gold", label: "1927G", tone: "gold" } // 扣除 30G
  ];
  renderResources(updatedStrip);
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
