(function () {
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
const npcBubbleEl = document.querySelector("#npc-bubble");

// Modal Selectors
const openInquiriesBtnEl = document.querySelector("#open-inquiries-btn");
const openPromotionsBtnEl = document.querySelector("#open-promotions-btn");
const closePromotionsBtnEl = document.querySelector("#close-promotions-btn");
const promotionsModalEl = document.querySelector("#promotions-modal");

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

// Hidden Moon Well listener for compatibility
if (drawWellwaterBtnEl) {
  drawWellwaterBtnEl.addEventListener("click", () => {
    handlePray();
  });
}

// Directly trigger inquiry dialog in the main dialogue box
openInquiriesBtnEl.addEventListener("click", () => {
  const inq = state.model?.inquiries?.[0];
  if (inq) {
    handleInquiry(inq);
  } else {
    npcBubbleEl.textContent = "大祭司賽恩：「願聖光指引你，旅人。目前沒有新的線索。」";
  }
});

openPromotionsBtnEl.addEventListener("click", () => {
  promotionsModalEl.style.display = "flex";
  pushActionLog({
    action_id: "open_promotions_modal",
    payload: {},
    source: "open_promotions_btn",
    dispatched: true,
  });
});

closePromotionsBtnEl.addEventListener("click", () => {
  promotionsModalEl.style.display = "none";
});

// Close promotions modal when clicking backdrop
promotionsModalEl.addEventListener("click", (e) => {
  if (e.target === promotionsModalEl) {
    promotionsModalEl.style.display = "none";
  }
});

backToTownBtnEl.addEventListener("click", () => {
  pushActionLog({
    action_id: "back_to_town_hub",
    payload: {},
    source: "back_to_town",
    dispatched: true,
  });
  npcBubbleEl.textContent = "大祭司賽恩：「返回城鎮已記錄（Lab 模式不執行真實導航與頁面跳轉）。」";
});

loadFixture(fixtureSelect.value);

function loadFixture(scenarioKey) {
  shellEl.dataset.loadState = "loading";
  try {
    let model = null;
    const key = scenarioKey.replace('temple-', '').replace('.json', '');
    if (key === "default") {
      model = JSON.parse(JSON.stringify(window.TEMPLE_DEFAULT_FIXTURE));
    } else {
      throw new Error("Unknown scenario key: " + scenarioKey);
    }
    state.model = model;
    state.actionLog = [];
    render();
    logSystem(`loaded in-memory scenario: ${scenarioKey}`);
    shellEl.dataset.loadState = "ready";
  } catch (error) {
    console.error(error);
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
  if (wellNameEl) wellNameEl.textContent = well.label ?? "月神之井";
  if (wellDescriptionEl) wellDescriptionEl.textContent = well.description ?? "";
  if (drawWellwaterBtnEl) drawWellwaterBtnEl.disabled = !well.enabled;
  if (wellFeedbackEl) wellFeedbackEl.textContent = "";
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

async function handlePray() {
  const well = state.model?.moon_well ?? { cost: 30, payload: {} };
  
  

  pushActionLog({
    action_id: "temple_pray",
    payload: well.payload ?? {},
    source: "draw_wellwater_btn",
    dispatched: true,
  });

  if (wellFeedbackEl) {
    wellFeedbackEl.textContent = "汲取了微光閃爍的泉水... 您獲得了 [月華庇護] (冰/火抗性 +10%，持續下一次探索)！(靜態模擬)";
  }
}

function handlePromotion(promo) {
  pushActionLog({
    action_id: "claim_promotion",
    payload: { class_id: promo.class_id },
    source: "promotion_altar",
    dispatched: false,
    reason: promo.disabled_reason ?? "requirements_not_met",
  });
}

async function handleInquiry(inq) {
  const actionId = inq.action_id || "fire_mark_inquiry";
  
  

  pushActionLog({
    action_id: actionId,
    payload: inq.payload ?? {},
    source: "inquiry_panel",
    dispatched: true,
  });

  // Direct JRPG dialog bubble integration
  npcBubbleEl.textContent = `大祭司賽恩：「${inq.response_text ?? "該線索十分深奧..."}」`;
  if (inquiryFeedbackEl) {
    inquiryFeedbackEl.textContent = inq.response_text ?? "大祭司表示該線索十分深奧...";
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
  promotionsContainerEl.replaceChildren();
  inquiriesContainerEl.replaceChildren();
  if (drawWellwaterBtnEl) drawWellwaterBtnEl.disabled = true;

  const errorEl = document.createElement("div");
  errorEl.className = "load-error";
  errorEl.textContent = error instanceof Error ? error.message : String(error);
  promotionsContainerEl.append(errorEl);
}

})();