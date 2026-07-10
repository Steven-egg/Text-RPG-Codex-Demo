import { applyFacilityBackground } from "../shared/facility-backgrounds.js";
import { runtimeClient } from "../shared/runtime-client.js";

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

const magicShopBackgroundByRegion = {
  fire: "./assets/magic-shop-background.jpg",
  ice: "./assets/ice-magic-shop-background-with-eve-overscan-master-v01.png",
  earth: "./assets/earth-magic-shop-background-with-eve-cropped-candidate-v01.png",
  thunder: "./assets/thunder-magic-shop-background-with-eve-candidate-v01.png",
  final: "./assets/final-magic-shop-with-eve-candidate-v01.png",
};

const defaultSpellbookIcon = `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H11v16H6.5A2.5 2.5 0 0 0 4 21.5v-16ZM20 5.5A2.5 2.5 0 0 0 17.5 3H13v16h4.5a2.5 2.5 0 0 1 2.5 2.5v-16Z"/></svg>`;

const spellbookIconMap = {
  book_spark: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="M13.2 2.2c.5 3-1.5 4.5-3 6.2-1.5 1.7-2.7 3.3-2.7 5.8A4.6 4.6 0 0 0 12.1 19c2.7 0 4.9-2.1 4.9-4.9 0-2.6-1.5-5.1-3.8-7.2.2 2-1 3.1-2 4.1.3-3.4 2.8-5 2-8.8Z"/></svg>`,
  book_ice_needle: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><path d="M12 3v18M4.2 7.5l15.6 9M4.2 16.5l15.6-9M12 3l-2 2M12 3l2 2M12 21l-2-2M12 21l2-2"/></svg>`,
  book_minor_heal: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="8"/><path d="M12 8v8M8 12h8"/></svg>`,
  book_guardian_rune: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"><path d="M12 3 5 6v5c0 4.8 2.9 8.1 7 10 4.1-1.9 7-5.2 7-10V6l-7-3Z"/><path d="m9 12 2 2 4-5"/></svg>`,
  book_quickstep: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7h8M2 12h10M5 17h7M13 6l5 6-5 6"/></svg>`,
  book_cinder_mark: `<svg viewBox="0 0 24 24" fill="currentColor"><path d="m12 2 1.8 6.2L20 10l-6.2 1.8L12 18l-1.8-6.2L4 10l6.2-1.8L12 2Zm6 14 .8 2.2L21 19l-2.2.8L18 22l-.8-2.2L15 19l2.2-.8L18 16Z"/></svg>`,
};

fixtureSelect.addEventListener("change", () => {
  loadFixture(fixtureSelect.value);
});

primaryActionEl.addEventListener("click", () => {
  executeLearnAction();
});

backActionEl.addEventListener("click", () => {
  if (runtimeClient.isLiveMode()) {
    handleBackToTown();
    return;
  }
  pushActionLog({
    action_id: "back_to_town_hub",
    payload: {},
    source: "secondary_action",
    dispatched: true,
  });
  navigateToPrototype(townHubRoute);
});

clearLogEl.addEventListener("click", () => {
  state.actionLog = [];
  renderActionLog();
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
    
    state.selectedCategory = model.selected_category_id ?? "all";
    state.selectedBookId = model.selected_book_id ?? null;
    state.actionLog = [];
    
    render();
    logSystem(`loaded ${path}`);
    
    // Initial welcome guidance
    const speaker = model.npc?.name ?? "伊芙";
    const welcome = model.npc?.guidance ?? "選擇一本魔法書來開始研讀。";
    renderFeedback(speaker, welcome);
    
    shellEl.dataset.loadState = "ready";
  } catch (error) {
    renderLoadError(error);
    shellEl.dataset.loadState = "error";
  }
}

async function loadLiveScreen() {
  shellEl.dataset.loadState = "loading";
  try {
    const model = await runtimeClient.getScreen("magic_shop_screen");
    state.model = model;
    state.selectedCategory = model.selected_category_id ?? "all";
    state.selectedBookId = model.selected_book_id ?? getFirstVisibleBookId() ?? null;
    state.actionLog = [];
    ensureSelectionVisible();
    render();
    logSystem("live runtime screen loaded", {
      actionId: "live_screen_loaded",
      source: "live_loader",
      payload: { mode: "live", screen_id: "magic_shop_screen" },
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
    state.selectedCategory = model.selected_category_id ?? "all";
    state.selectedBookId = model.selected_book_id ?? getFirstVisibleBookId() ?? null;
    state.actionLog = [];
    ensureSelectionVisible();
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
  const payload = { from: "magic_shop_screen" };
  pushActionLog({
    action_id: "back_to_town_hub",
    payload,
    source: "secondary_action",
    dispatched: true,
  });
  try {
    const result = await runtimeClient.dispatchAction("magic_shop_screen", "back_to_town_hub", payload);
    shellEl.dataset.runtimeStatus = result.status ?? "success";
    window.setTimeout(() => {
      window.location.href = runtimeClient.nextRoute(result, townHubRoute);
    }, navigationDelayMs);
  } catch (error) {
    const reason = runtimeClient.errorMessage(error);
    shellEl.dataset.runtimeStatus = error?.runtimeStatus ?? "error";
    renderFeedback(state.model.npc?.name ?? "伊芙", reason);
    pushActionLog({
      action_id: "back_to_town_hub",
      payload,
      source: "secondary_action",
      dispatched: false,
      reason,
    });
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

function setPrimaryAction(label, enabled) {
  primaryActionEl.innerHTML = `
    <svg class="btn-icon-svg" viewBox="0 0 24 24"><path d="M12 11.55C9.64 9.35 6.48 8 3 8v11c3.48 0 6.64 1.35 9 3.55 2.36-2.2 5.52-3.55 9-3.55V8c-3.48 0-6.64 1.35-9 3.55zM12 8c1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3 1.34 3 3 3z" fill="currentColor"/></svg>
    <span class="btn-text">${label}</span>
  `;
  primaryActionEl.setAttribute("aria-disabled", String(!enabled));
}

function render() {
  const { model } = state;
  applyFacilityBackground({ model, shell: shellEl, backgrounds: magicShopBackgroundByRegion });
  titleEl.textContent = cleanTitle(model.title);
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

    const icon = document.createElement("span");
    icon.className = "spellbook-icon";
    icon.setAttribute("aria-hidden", "true");
    icon.innerHTML = spellbookIconMap[row.book_id] ?? defaultSpellbookIcon;

    const nameText = document.createElement("span");
    nameText.className = "item-title-text";
    nameText.textContent = row.title ?? "";
    name.append(icon, nameText);

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
    setPrimaryAction("解讀術式中", false);
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
  const canLearn = action.enabled && book.enabled;
  setPrimaryAction(action.label ?? "學習魔法", canLearn);
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

  if (runtimeClient.isLiveMode()) {
    pushActionLog({
      action_id: "learn_magic_book",
      payload: { book_id: selectedBookId },
      source: "primary_action",
      dispatched: true,
    });
    runtimeClient.dispatchAction("magic_shop_screen", "learn_magic_book", { book_id: selectedBookId })
      .then((result) => {
        shellEl.dataset.runtimeStatus = result.status ?? "success";
        if (result.screen_model) {
          state.model = result.screen_model;
          ensureSelectionVisible();
          render();
        }
        if (result.message) {
          const npcMsg = result.screen_model?.feedback_message?.text || result.message;
          renderFeedback(state.model.npc?.name ?? "伊芙", npcMsg);
        }
      })
      .catch((error) => {
        const reason = runtimeClient.errorMessage(error);
        shellEl.dataset.runtimeStatus = error?.runtimeStatus ?? "error";
        pushActionLog({
          action_id: "learn_magic_book",
          payload: { book_id: selectedBookId },
          source: "primary_action",
          dispatched: false,
          reason,
        });
        renderFeedback(state.model.npc?.name ?? "伊芙", `「研讀受阻：${reason}。」`);
      });
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
  feedbackSpeakerEl.textContent = speaker;
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
  setPrimaryAction("解讀術式中", false);
  
  const errorEl = document.createElement("div");
  errorEl.className = "load-error";
  errorEl.textContent = error instanceof Error ? error.message : String(error);
  itemDetailContentEl.replaceChildren(errorEl);
  requirementListEl.replaceChildren();

  renderFeedback("系統", "請確認 fixtures 路徑與 JSON 格式。");
}
