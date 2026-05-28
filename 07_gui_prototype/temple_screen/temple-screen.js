import { runtimeClient } from "../shared/runtime-client.js";

const fixtureSelect = document.querySelector("#fixture-select");
const titleEl = document.querySelector("#screen-title");
const subtitleEl = document.querySelector("#screen-subtitle");
const resourceStripEl = document.querySelector("#resource-strip");
const wellNameEl = document.querySelector("#well-name");
const wellDescriptionEl = document.querySelector("#well-description");
const wellFeedbackEl = document.querySelector("#well-feedback");
const drawWellwaterBtnEl = document.querySelector("#draw-wellwater-btn");
const promotionsContainerEl = document.querySelector("#promotions-container");
const inquiriesContainerEl = document.querySelector("#inquiries-container");
const inquiryFeedbackEl = document.querySelector("#inquiry-feedback");
const backToTownBtnEl = document.querySelector("#back-to-town");
const actionLogEl = document.querySelector("#action-log");
const clearLogEl = document.querySelector("#clear-log");
const shellEl = document.querySelector(".temple-shell");

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

drawWellwaterBtnEl.addEventListener("click", () => {
  handlePray();
});

backToTownBtnEl.addEventListener("click", () => {
  window.setTimeout(() => {
    window.location.href = runtimeClient.withLiveMode("../town_hub/index.html");
  }, navigationDelayMs);
});

loadFixture(fixtureSelect.value);

async function loadFixture(path) {
  // 教堂/神殿畫面目前在 bridge 端尚未正式實作 Live endpoint，採 Static 優先 fallback 模式
  if (runtimeClient.isLiveMode()) {
    logSystem("live 模式已啟用，本畫面目前僅做為 static preview/display 展示。");
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

function render() {
  const { model } = state;
  titleEl.textContent = model.title ?? "";
  subtitleEl.textContent = model.subtitle ?? "";
  
  renderResources(model.resource_strip ?? []);
  renderMoonWell(model.moon_well ?? {});
  renderPromotions(model.promotions ?? []);
  renderInquiries(model.inquiries ?? []);
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

function renderMoonWell(well) {
  wellNameEl.textContent = well.label ?? "月神之井";
  wellDescriptionEl.textContent = well.description ?? "";
  drawWellwaterBtnEl.disabled = !well.enabled;
  wellFeedbackEl.textContent = "";
}

function renderPromotions(promotions) {
  promotionsContainerEl.replaceChildren(
    ...promotions.map((promo) => {
      const el = document.createElement("div");
      el.className = "promo-item";

      const header = document.createElement("div");
      header.className = "promo-header";

      const title = document.createElement("h3");
      title.className = "promo-title";
      title.textContent = promo.label ?? "";

      header.append(title);

      const description = document.createElement("p");
      description.className = "promo-description";
      description.textContent = promo.description ?? "";

      const reqLabel = document.createElement("p");
      reqLabel.className = "promo-reqs-label";
      reqLabel.textContent = "晉升要求：";

      const reqsList = document.createElement("ul");
      reqsList.className = "promo-reqs";
      
      (promo.requirements ?? []).forEach((req) => {
        const li = document.createElement("li");
        li.className = req.satisfied ? "req-satisfied" : "req-unsatisfied";
        li.textContent = `${req.name} (${req.current}) ${req.satisfied ? "✓" : "✗"}`;
        reqsList.append(li);
      });

      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "promo-action-btn";
      btn.disabled = !promo.enabled;
      btn.textContent = promo.enabled ? "宣誓晉升" : "條件不足";
      btn.title = promo.enabled ? "" : promo.disabled_reason ?? "";
      
      btn.addEventListener("click", () => handlePromotion(promo));

      el.append(header, description, reqLabel, reqsList, btn);
      return el;
    }),
  );
}

function renderInquiries(inquiries) {
  inquiriesContainerEl.replaceChildren(
    ...inquiries.map((inq) => {
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "inquiry-btn";
      btn.textContent = inq.label ?? "";
      btn.title = inq.description ?? "";
      
      btn.addEventListener("click", () => handleInquiry(inq));
      
      return btn;
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

function handlePray() {
  const well = state.model?.moon_well ?? { cost: 30, payload: {} };
  
  pushActionLog({
    action_id: "temple_pray",
    payload: well.payload ?? {},
    source: "draw_wellwater_btn",
    dispatched: true,
  });

  wellFeedbackEl.textContent = "汲取了微光閃爍的泉水... 您獲得了 [月華庇護] (冰/火抗性 +10%，持續下一次探索)！(靜態模擬)";
}

function handlePromotion(promo) {
  // 這是一個 blocked 動作示範，因為等級不夠
  pushActionLog({
    action_id: "claim_promotion",
    payload: { class_id: promo.class_id },
    source: "promotion_altar",
    dispatched: false,
    reason: promo.disabled_reason ?? "requirements_not_met",
  });
}

function handleInquiry(inq) {
  pushActionLog({
    action_id: "fire_mark_inquiry",
    payload: inq.payload ?? {},
    source: "inquiry_panel",
    dispatched: true,
  });

  inquiryFeedbackEl.textContent = inq.response_text ?? "大祭司表示該線索十分深奧...";
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
  promotionsContainerEl.replaceChildren();
  inquiriesContainerEl.replaceChildren();
  drawWellwaterBtnEl.disabled = true;

  const errorEl = document.createElement("div");
  errorEl.className = "load-error";
  errorEl.textContent = error instanceof Error ? error.message : String(error);
  promotionsContainerEl.append(errorEl);
}
