(function () {
const fixtureSelect = document.querySelector("#fixture-select");
const titleEl = document.querySelector("#screen-title");
const subtitleEl = document.querySelector("#screen-subtitle");
const resourceStripEl = document.querySelector("#resource-strip");
const categoryTabsEl = document.querySelector("#category-tabs");
const spellbookListEl = document.querySelector("#spellbook-list");

// Detail Column
const detailStatusBadgeEl = document.querySelector("#detail-status-badge");
const itemDetailContentEl = document.querySelector("#item-detail-content");
const detailPriceTextEl = document.querySelector("#detail-price-text");
const requirementListEl = document.querySelector("#requirement-list");

// NPC Column
const npcPortraitEl = document.querySelector("#npc-portrait");
const npcNameEl = document.querySelector("#npc-name");
const npcRoleEl = document.querySelector("#npc-role");

// Footer Controls
const feedbackSpeakerEl = document.querySelector("#feedback-speaker");
const feedbackMessageEl = document.querySelector("#feedback-message");
const primaryActionEl = document.querySelector("#primary-action");
const backActionEl = document.querySelector("#back-action");
const actionLogEl = document.querySelector("#action-log");
const clearLogEl = document.querySelector("#clear-log");
const shellEl = document.querySelector(".magic-shop-shell");

const state = {
  model: null,
  selectedCategory: "all",
  selectedBookId: null,
  actionLog: [],
};

const townHubRoute = "../town_hub/index.html";
const navigationDelayMs = 120;

// Emoji dictionary for spellbooks
const emojiMap = {
  book_spark: "🔥",
  book_ice_needle: "❄",
  book_minor_heal: "✨",
  book_guardian_rune: "🛡",
  book_quickstep: "💨",
  book_cinder_mark: "🌟",
};

fixtureSelect.addEventListener("change", () => {
  loadFixture(fixtureSelect.value);
});

primaryActionEl.addEventListener("click", () => {
  executeLearnAction();
});

backActionEl.addEventListener("click", () => {
  pushActionLog({
    action_id: "back_to_town_hub",
    payload: {},
    source: "secondary_action",
    dispatched: true,
  });
  renderFeedback(state.model.npc?.name ?? "伊芙", "「返回城鎮已記錄（Lab 模式不執行真實導航與頁面跳轉）。」");
}););

clearLogEl.addEventListener("click", () => {
  state.actionLog = [];
  renderActionLog();
});

loadFixture(fixtureSelect.value);

function loadFixture(scenarioKey) {
  shellEl.dataset.loadState = "loading";
  try {
    let model = null;
    const key = scenarioKey.replace('magic-shop-', '').replace('.json', '');
    if (key === "default") {
      model = JSON.parse(JSON.stringify(window.MAGIC_SHOP_DEFAULT_FIXTURE));
    } else if (key === "constrained") {
      model = JSON.parse(JSON.stringify(window.MAGIC_SHOP_CONSTRAINED_FIXTURE));
    } else if (key === "discount") {
      model = JSON.parse(JSON.stringify(window.MAGIC_SHOP_DISCOUNT_FIXTURE));
    } else if (key === "learned") {
      model = JSON.parse(JSON.stringify(window.MAGIC_SHOP_LEARNED_FIXTURE));
    } else {
      throw new Error("Unknown scenario key: " + scenarioKey);
    }
    state.model = model;
    state.selectedCategory = model.selected_category_id ?? "all";
    state.selectedBookId = model.selected_book_id ?? null;
    state.actionLog = [];
    render();
    logSystem(`loaded in-memory scenario: ${scenarioKey}`);
    const speaker = model.npc?.name ?? "伊芙";
    const welcome = model.npc?.guidance ?? "選擇一本魔法書來開始研讀。";
    renderFeedback(speaker, welcome);
    shellEl.dataset.loadState = "ready";
  } catch (error) {
    console.error(error);
    shellEl.dataset.loadState = "error";
  }
}







function getVisibleBookRows() {
  const rows = state.model?.list_rows ?? [];
  if (state.selectedCategory === "all") {
    return rows;
  }
  return rows.filter((row) => row.category === state.selectedCategory);
}

function getFirstVisibleBookId() {
  return getVisibleBookRows()[0]?.book_id ?? null;
}

function ensureSelectionVisible() {
  const rows = getVisibleBookRows();
  if (!rows.some((row) => row.book_id === state.selectedBookId)) {
    state.selectedBookId = rows[0]?.book_id ?? null;
  }
}

function render() {
  const { model } = state;
  titleEl.textContent = model.title ?? "";
  subtitleEl.textContent = model.subtitle ?? "";

  renderResources();
  renderCategoryTabs();
  renderSpellbookList();
  renderDetailsPanel();
  renderNpcRegion();
}

function renderResources() {
  const { model } = state;
  const items = [];
  
  if (model.player_summary) {
    const p = model.player_summary;
    items.push({ label: `冒險者: ${p.name} (${p.job})`, tone: "primary" });
    items.push({ label: `等級: Lv ${p.level}`, tone: "primary" });
    items.push({ label: `持有金幣: ${p.gold} G`, tone: "gold" });
  }

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

function renderCategoryTabs() {
  const { model } = state;
  const categories = model.category_tabs ?? [];

  categoryTabsEl.replaceChildren(
    ...categories.map((category) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "category-tab";
      button.classList.toggle("is-selected", category.id === state.selectedCategory);
      button.setAttribute("aria-pressed", String(category.id === state.selectedCategory));

      const label = document.createElement("strong");
      label.textContent = category.label ?? category.id;
      button.append(label);

      button.addEventListener("click", () => selectCategory(category.id));
      return button;
    }),
  );
}

function renderSpellbookList() {
  const { model, selectedCategory } = state;
  spellbookListEl.replaceChildren();

  const rows = model.list_rows ?? [];
  const filtered = selectedCategory === "all" ? rows : rows.filter(row => row.category === selectedCategory);
  
  if (filtered.length === 0) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.textContent = "沒有此分類的魔法書";
    spellbookListEl.appendChild(empty);
    return;
  }

  filtered.forEach((row) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "item-row";
    
    const isSelected = row.book_id === state.selectedBookId;
    button.classList.toggle("is-selected", isSelected);
    button.setAttribute("aria-pressed", String(isSelected));
    button.dataset.bookId = row.book_id;

    if (!row.enabled && row.status !== "learned") {
      button.classList.add("is-blocked");
    }

    // Left info
    const leftPart = document.createElement("div");
    leftPart.className = "item-row-left";

    const textPart = document.createElement("div");
    textPart.className = "item-row-copy";

    const name = document.createElement("span");
    name.className = "item-title";
    name.textContent = `${emojiMap[row.book_id] ?? "📖"} ${row.title ?? ""}`;

    const summary = document.createElement("span");
    summary.className = "item-summary";
    summary.textContent = row.summary ?? "";

    const meta = document.createElement("span");
    meta.className = "item-meta";
    meta.textContent = `可用職業: ${row.jobs?.join(", ") ?? ""} | 需求等級: Lv ${row.req_level} | MP 消耗: ${row.mp}`;

    textPart.append(name, summary, meta);
    leftPart.append(textPart);

    // Right info
    const rightPart = document.createElement("div");
    rightPart.className = "item-row-right";

    const badge = document.createElement("span");
    badge.className = "status-badge";
    badge.dataset.status = row.status ?? "learnable";
    
    let statusText = "可研讀";
    if (row.status === "learned") statusText = "已學會";
    else if (row.status === "job_restricted") statusText = "職業不符";
    else if (row.status === "level_restricted") statusText = "等級不足";
    badge.textContent = statusText;

    rightPart.append(badge);

    button.append(leftPart, rightPart);
    button.addEventListener("click", () => handleSpellbookSelect(row.book_id));
    
    spellbookListEl.appendChild(button);
  });
}

function renderDetailsPanel() {
  const { model, selectedBookId } = state;
  itemDetailContentEl.replaceChildren();
  requirementListEl.replaceChildren();
  
  const book = model.list_rows?.find(r => r.book_id === selectedBookId);
  const detail = model.book_details?.[selectedBookId];

  if (!book || !detail) {
    detailStatusBadgeEl.style.display = "none";
    detailPriceTextEl.textContent = "--";
    primaryActionEl.setAttribute("aria-disabled", "true");
    primaryActionEl.textContent = "解讀術式中";
    
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.textContent = "選擇左側魔法書查看術式詳情";
    itemDetailContentEl.appendChild(empty);
    return;
  }

  // Render detail contents
  detailStatusBadgeEl.style.display = "inline-block";
  detailStatusBadgeEl.dataset.status = detail.status ?? "learnable";
  
  let statusText = "可學習";
  if (detail.status === "learned") statusText = "已學會";
  else if (detail.status === "job_restricted") statusText = "職業不符";
  else if (detail.status === "level_restricted") statusText = "等級不足";
  detailStatusBadgeEl.textContent = statusText;

  const h2 = document.createElement("h2");
  h2.textContent = detail.title ?? "";

  const subtitle = document.createElement("p");
  subtitle.className = "detail-subtitle";
  subtitle.textContent = `學會技能: ${detail.skill_name} / 基礎消耗 MP: ${detail.mp_cost}`;

  const desc = document.createElement("p");
  desc.className = "detail-description";
  desc.textContent = detail.description ?? "";

  const effect = document.createElement("div");
  effect.className = "detail-effect";
  effect.textContent = `技能效果預覽：${detail.effect_summary ?? ""}`;

  const context = document.createElement("p");
  context.className = "detail-context";
  context.textContent = `傳承限制：需要等級 Lv ${detail.req_level} 及符合學識職業 (${detail.jobs?.join(", ")})。學會後永久生效。`;

  itemDetailContentEl.append(h2, subtitle, desc, effect, context);

  // Price
  detailPriceTextEl.textContent = `${detail.price} G`;

  // Render requirements list
  const reqs = model.requirement_rows?.[selectedBookId] ?? [];
  if (reqs.length === 0) {
    const row = document.createElement("div");
    row.className = "requirement-row";
    row.textContent = "此項沒有額外要求";
    requirementListEl.appendChild(row);
  } else {
    reqs.forEach((row) => {
      const el = document.createElement("div");
      el.className = "requirement-row";

      const marker = document.createElement("span");
      marker.className = "requirement-marker";
      marker.dataset.status = row.status ?? "met";
      marker.textContent = row.status === "met" ? "✔" : "✘";

      const copy = document.createElement("div");
      copy.className = "requirement-copy";

      const label = document.createElement("strong");
      label.textContent = row.label ?? "";

      const values = document.createElement("span");
      values.textContent = `要求: ${row.required_value ?? ""} | 目前: ${row.current_value ?? ""}`;

      copy.append(label, values);

      const status = document.createElement("span");
      status.className = "requirement-status";
      status.dataset.status = row.status ?? "met";
      status.textContent = row.status === "met" ? "滿足" : (row.disabled_reason ?? "未滿足");

      el.append(marker, copy, status);
      requirementListEl.appendChild(el);
    });
  }

  // Footer learn spell button state
  const action = model.primary_actions?.[selectedBookId] ?? {};
  primaryActionEl.textContent = action.label ?? "學習魔法";
  
  const canLearn = action.enabled && book.enabled;
  primaryActionEl.setAttribute("aria-disabled", String(!canLearn));
}

function renderNpcRegion() {
  const { model } = state;
  if (!model.npc) return;

  npcPortraitEl.dataset.npcPlaceholder = model.npc.portrait_placeholder ?? "EV";
  npcNameEl.textContent = model.npc.name ?? "伊芙";
  npcRoleEl.textContent = model.npc.role ?? "魔法商店館長";
}

function selectCategory(categoryId) {
  state.selectedCategory = categoryId;
  pushActionLog({
    action_id: "select_category",
    payload: { category_id: categoryId },
    source: "category_tab",
    dispatched: true,
  });

  // Auto select first spellbook in the selected category
  const { model } = state;
  const rows = model.list_rows ?? [];
  const filtered = categoryId === "all" ? rows : rows.filter(r => r.category === categoryId);
  if (filtered.length > 0) {
    state.selectedBookId = filtered[0].book_id;
  } else {
    state.selectedBookId = null;
  }

  render();
}

function handleSpellbookSelect(bookId) {
  state.selectedBookId = bookId;
  pushActionLog({
    action_id: "select_book",
    payload: { book_id: bookId },
    source: "list_row",
    dispatched: true,
  });

  const { model } = state;
  const book = model.list_rows?.find(r => r.book_id === bookId);
  const detail = model.book_details?.[bookId];
  const speaker = model.npc?.name ?? "伊芙";

  if (book && detail) {
    if (detail.status === "learned") {
      renderFeedback(speaker, `「這本《${detail.title}》中刻印的術式你已經完全熟捻在心，不需要再重複研讀了。」`);
    } else if (detail.status === "job_restricted") {
      renderFeedback(speaker, `「很遺憾，《${detail.title}》需要具備特定的智慧與魔網親和力。以你的職業很難理解其奧秘。」`);
    } else if (detail.status === "level_restricted") {
      renderFeedback(speaker, `「魔力積累是循序漸進的。以你目前的等階，強行解讀此術式會使靈魂受損，提升到 Lv ${detail.req_level} 再來吧。」`);
    } else {
      const matText = detail.price ? `研讀需要消耗 ${detail.price} G 術式材料費。` : "";
      renderFeedback(speaker, `「好的，這本《${detail.title}》記載著高深的『${detail.skill_name}』。${matText}準備好進行傳承了嗎？」`);
    }
  }

  render();
}

function executeLearnAction() {
  const { model, selectedBookId } = state;
  const book = model?.list_rows?.find(r => r.book_id === selectedBookId);
  const action = model?.primary_actions?.[selectedBookId];

  if (!book || !action) return;

  const canLearn = action.enabled && book.enabled;
  if (!canLearn) {
    const disabledReason = action.disabled_reason || "未滿足學習條件";
    pushActionLog({
      action_id: "blocked_action",
      payload: { book_id: selectedBookId },
      source: "primary_action",
      dispatched: false,
      reason: disabledReason,
    });
    
    renderFeedback("伊芙", `「研讀受阻：${disabledReason}。請提升等階或備齊魔石素材後，再嘗試解讀此術式。」`);
    return;
  }

  

  // Simulated success
  pushActionLog({
    action_id: "learn_magic_book",
    payload: { book_id: selectedBookId, price: action.payload?.price ?? 180 },
    source: "primary_action",
    dispatched: true,
  });

  const skillName = model.book_details?.[selectedBookId]?.skill_name ?? "新法術";
  renderFeedback("伊芙", `「術式編織成功！星辰奧秘已永久融入你的靈魂，你學會了高深的傳承技能【${skillName}】！」`);

  // Simulate updating UI status locally
  book.status = "learned";
  book.enabled = false;
  book.disabled_reason = "已學會";
  if (book.badges) {
    book.badges = [{ badge_id: "learned", label: "已學會", kind: "success" }];
  }

  const detail = model.book_details?.[selectedBookId];
  if (detail) {
    detail.status = "learned";
    detail.disabled_reason = "已學會";
  }

  const reqs = model.requirement_rows?.[selectedBookId];
  if (reqs) {
    model.requirement_rows[selectedBookId] = [
      {
        id: "gold",
        label: "金幣需求",
        required_value: `${action.payload?.price ?? 180}G`,
        current_value: `${model.player_summary?.gold ?? 500}G`,
        status: "met",
        disabled_reason: null
      },
      {
        id: "learned",
        label: "學習狀態",
        required_value: "未學習",
        current_value: "已學習",
        status: "unmet",
        disabled_reason: "已學會"
      }
    ];
  }

  if (action) {
    action.enabled = false;
    action.label = "已學會此法術";
  }

  render();
}

// Helpers
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

function renderFeedback(speaker, message) {
  feedbackSpeakerEl.textContent = `${speaker} 提示`;
  feedbackMessageEl.textContent = message;
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

function navigateToPrototype(route) {
  window.setTimeout(() => {
    window.location.href = route;
  }, navigationDelayMs);
}

function safeJson(value, fallback) {
  try {
    return JSON.parse(value);
  } catch {
    return fallback;
  }
}

function renderLoadError(error) {
  titleEl.textContent = "Fixture 載入失敗";
  subtitleEl.textContent = "無法讀取 Magic Shop static fixture。";
  resourceStripEl.replaceChildren();
  spellbookListEl.replaceChildren();
  categoryTabsEl.replaceChildren();
  
  detailStatusBadgeEl.style.display = "none";
  detailPriceTextEl.textContent = "--";
  primaryActionEl.setAttribute("aria-disabled", "true");
  primaryActionEl.textContent = "解讀術式中";
  
  const errorEl = document.createElement("div");
  errorEl.className = "load-error";
  errorEl.textContent = error instanceof Error ? error.message : String(error);
  itemDetailContentEl.replaceChildren(errorEl);
  requirementListEl.replaceChildren();

  renderFeedback("系統", "請確認 fixtures 路徑與 JSON 格式。");
}

})();