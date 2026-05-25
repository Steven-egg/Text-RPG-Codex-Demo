const fixtureSelect = document.querySelector("#fixture-select");
const titleEl = document.querySelector("#screen-title");
const subtitleEl = document.querySelector("#screen-subtitle");
const resourceStripEl = document.querySelector("#resource-strip");
const backpackTabsEl = document.querySelector("#backpack-tabs");
const inventoryGridEl = document.querySelector("#inventory-item-grid");
const storageGridEl = document.querySelector("#storage-item-grid");
const capacityStatusEl = document.querySelector("#storage-status-badge");
const capacityBarFillEl = document.querySelector("#capacity-bar-fill");
const capacityTextEl = document.querySelector("#capacity-text");
const quickDetailEl = document.querySelector("#item-quick-detail");

// NPC
const npcNameEl = document.querySelector("#npc-name");
const npcRoleEl = document.querySelector("#npc-role");
const npcSpeechBubbleEl = document.querySelector("#npc-speech-bubble");
const npcPortraitEl = document.querySelector("#npc-portrait");

// Popover Modal Elements
const popoverOverlayEl = document.querySelector("#transfer-popover");
const popoverTitleEl = document.querySelector("#popover-title");
const popoverModeBadgeEl = document.querySelector("#popover-mode-badge");
const popoverItemNameEl = document.querySelector("#popover-item-name");
const popoverItemMetaEl = document.querySelector("#popover-item-meta");
const popoverValueEl = document.querySelector("#popover-value");
const popoverLimitLabelEl = document.querySelector("#popover-limit-label");
const popoverRequirementListEl = document.querySelector("#popover-requirement-list");
const popoverDecEl = document.querySelector("#popover-dec");
const popoverIncEl = document.querySelector("#popover-inc");
const popoverMaxEl = document.querySelector("#popover-max");
const popoverCancelEl = document.querySelector("#popover-cancel");
const popoverConfirmEl = document.querySelector("#popover-confirm");

// Footer
const feedbackSpeakerEl = document.querySelector("#feedback-speaker");
const feedbackMessageEl = document.querySelector("#feedback-message");
const primaryActionEl = document.querySelector("#primary-action");
const backActionEl = document.querySelector("#back-action");
const actionLogEl = document.querySelector("#action-log");
const clearLogEl = document.querySelector("#clear-log");
const shellEl = document.querySelector(".storage-shell");

const state = {
  model: null,
  selectedCategory: "all",
  selectedItemId: null,
  selectedListType: null, // "deposit" (backpack) | "withdraw" (storage)
  quantityValue: 1,
  actionLog: [],
};

const townHubRoute = "../town_hub/index.html";
const navigationDelayMs = 120;
const totalSlotCount = 12; // Grid fixed slot sizes ( JRPG standards )

// Emoji dictionary for grid items
const emojiMap = {
  mat_iron_ore: "🪨",
  item_potion_s: "🧪",
  mat_copper_powder: "✨",
  mat_cloth: "🧵",
  key_fire_mark_shard: "🔥"
};

fixtureSelect.addEventListener("change", () => {
  loadFixture(fixtureSelect.value);
});

// Stepper within Popover listeners
popoverDecEl.addEventListener("click", () => adjustQuantity(-1));
popoverIncEl.addEventListener("click", () => adjustQuantity(1));
popoverMaxEl.addEventListener("click", () => {
  const max = getMaxAllowedQuantity();
  state.quantityValue = max;
  updateStepperDisplay();
  logQuantityChange();
});

popoverCancelEl.addEventListener("click", closePopover);
popoverOverlayEl.addEventListener("click", (e) => {
  if (e.target === popoverOverlayEl) {
    closePopover();
  }
});

popoverConfirmEl.addEventListener("click", () => {
  executePopoverAction();
});

primaryActionEl.addEventListener("click", () => {
  activatePrimaryAction();
});

backActionEl.addEventListener("click", () => {
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
  shellEl.dataset.loadState = "loading";
  try {
    const response = await fetch(path, { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`Fixture request failed: ${response.status}`);
    }
    const model = await response.json();
    state.model = model;
    
    state.selectedCategory = "all";
    state.selectedItemId = null;
    state.selectedListType = null;
    state.quantityValue = 1;
    state.actionLog = [];
    
    closePopover();
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
  
  // NPC
  npcNameEl.textContent = model.npc?.name ?? "諾亞";
  npcRoleEl.textContent = model.npc?.role ?? "冒險者工會會長";
  npcSpeechBubbleEl.replaceChildren();
  const speechText = document.createElement("p");
  speechText.textContent = model.npc?.avatar_text ?? "";
  npcSpeechBubbleEl.appendChild(speechText);
  npcPortraitEl.querySelector(".avatar-silhouette").textContent = model.npc?.portrait_placeholder ?? "Noah";

  renderResources(model.resource_strip ?? []);
  renderBackpackCategoryTabs(model.category_tabs ?? []);
  renderCapacityCard();
  
  // Grids
  renderBackpackGrid();
  renderStorageGrid();
  
  // Details & log
  renderQuickDetail();
  renderFooterActions();
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

function renderBackpackCategoryTabs(categories) {
  backpackTabsEl.replaceChildren(
    ...categories.map((category) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "category-tab";
      button.classList.toggle("is-selected", category.id === state.selectedCategory);
      button.setAttribute("aria-pressed", String(category.id === state.selectedCategory));

      const label = document.createElement("strong");
      label.textContent = category.label ?? category.id;

      button.append(label);
      button.addEventListener("click", () => selectBackpackCategory(category.id));
      return button;
    }),
  );
}

function renderCapacityCard() {
  const { model } = state;
  const locked = model.storage_state && !model.storage_state.unlocked;
  
  capacityStatusEl.dataset.status = locked ? "locked" : "unlocked";
  capacityStatusEl.textContent = locked ? "保管箱未解鎖" : "保管箱正常開放";
  
  if (locked) {
    capacityBarFillEl.style.width = "0%";
    capacityTextEl.textContent = "容量: 0 / 10";
    return;
  }
  
  const capacityUsed = model.storage_rows ? model.storage_rows.length : 0;
  const percentage = Math.min((capacityUsed / 10) * 100, 100);
  capacityBarFillEl.style.width = `${percentage}%`;
  capacityTextEl.textContent = `容量: ${capacityUsed} / 10`;
}

function renderBackpackGrid() {
  const { model, selectedCategory } = state;
  inventoryGridEl.replaceChildren();

  const rows = model.inventory_rows ?? [];
  const filtered = selectedCategory === "all" ? rows : rows.filter(row => row.category === selectedCategory);
  
  // Always render fixed size of 12 slots to align JRPG interface feeling
  for (let i = 0; i < totalSlotCount; i++) {
    const row = filtered[i];
    const button = document.createElement("button");
    button.type = "button";
    
    if (!row) {
      // Empty slot card
      button.className = "slot-card is-empty";
      const emptyDash = document.createElement("span");
      emptyDash.className = "slot-empty-dash";
      emptyDash.textContent = "--";
      button.append(emptyDash);
    } else {
      // Normal item slot card
      button.className = "slot-card";
      button.classList.toggle("is-selected", row.item_id === state.selectedItemId && state.selectedListType === "deposit");
      button.setAttribute("aria-pressed", String(row.item_id === state.selectedItemId && state.selectedListType === "deposit"));
      button.dataset.itemId = row.item_id;

      if (!row.enabled) {
        button.classList.add("is-blocked");
        const badge = document.createElement("span");
        badge.className = "slot-badge";
        badge.dataset.status = row.item_id === "key_fire_mark_shard" ? "blocked" : "full";
        badge.textContent = row.item_id === "key_fire_mark_shard" ? "貴重物" : "滿";
        button.append(badge);
      }

      const icon = document.createElement("span");
      icon.className = "slot-icon-area";
      icon.textContent = emojiMap[row.item_id] ?? "📦";

      const title = document.createElement("span");
      title.className = "slot-name";
      title.textContent = row.short_title ?? row.title ?? "";

      const count = document.createElement("span");
      count.className = "slot-quantity";
      count.textContent = `x${row.owned_count ?? 0}`;

      button.append(icon, title, count);
      button.addEventListener("click", () => handleSlotClick(row, "deposit"));
    }
    
    inventoryGridEl.appendChild(button);
  }
}

function renderStorageGrid() {
  const { model } = state;
  storageGridEl.replaceChildren();

  const locked = model.storage_state && !model.storage_state.unlocked;
  const rows = locked ? [] : (model.storage_rows ?? []);
  
  // Render fixed 12 storage slots
  for (let i = 0; i < totalSlotCount; i++) {
    const row = rows[i];
    const button = document.createElement("button");
    button.type = "button";
    
    if (locked) {
      button.className = "slot-card is-empty";
      button.style.opacity = "0.3";
      const emptyDash = document.createElement("span");
      emptyDash.className = "slot-empty-dash";
      emptyDash.textContent = "🔒";
      button.append(emptyDash);
    } else if (!row) {
      button.className = "slot-card is-empty";
      const emptyDash = document.createElement("span");
      emptyDash.className = "slot-empty-dash";
      emptyDash.textContent = "--";
      button.append(emptyDash);
    } else {
      button.className = "slot-card";
      button.classList.toggle("is-selected", row.item_id === state.selectedItemId && state.selectedListType === "withdraw");
      button.setAttribute("aria-pressed", String(row.item_id === state.selectedItemId && state.selectedListType === "withdraw"));
      button.dataset.itemId = row.item_id;

      const icon = document.createElement("span");
      icon.className = "slot-icon-area";
      icon.textContent = emojiMap[row.item_id] ?? "📦";

      const title = document.createElement("span");
      title.className = "slot-name";
      title.textContent = row.short_title ?? row.title ?? "";

      const count = document.createElement("span");
      count.className = "slot-quantity";
      count.textContent = `x${row.owned_count ?? 0}`;

      button.append(icon, title, count);
      button.addEventListener("click", () => handleSlotClick(row, "withdraw"));
    }
    
    storageGridEl.appendChild(button);
  }
}

function renderQuickDetail() {
  const { model } = state;
  quickDetailEl.replaceChildren();

  // If storage is locked
  if (model.storage_state && !model.storage_state.unlocked) {
    const header = document.createElement("h3");
    header.textContent = "倉庫服務未開啟";
    const body = document.createElement("p");
    body.className = "detail-desc";
    body.textContent = "工會倉庫現處於未啟用狀態，可點選右下角「解鎖倉庫」並提供諾亞 500G 金幣開啟。";
    quickDetailEl.append(header, body);
    return;
  }

  const item = getSelectedItemRow();
  if (!item) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.textContent = "選擇左側背包格子 (存入) 或右側倉庫格子 (取出) 來快速轉移道具";
    quickDetailEl.append(empty);
    return;
  }

  const detail = model.item_details?.[item.item_id] ?? {};
  
  const header = document.createElement("h3");
  header.textContent = detail.title ?? item.title ?? "";
  
  const type = document.createElement("p");
  type.className = "detail-type";
  type.textContent = `${detail.category_label ?? ""} | 持有量：${item.owned_count ?? 0} 個`;
  
  const body = document.createElement("p");
  body.className = "detail-desc";
  body.textContent = `${detail.description ?? ""} (${detail.use_context ?? ""})`;

  quickDetailEl.append(header, type, body);

  if (!item.enabled) {
    const warn = document.createElement("p");
    warn.className = "detail-warn";
    warn.textContent = `⚠️ 限制提示: ${item.disabled_reason ?? "未滿足存取條件"}`;
    quickDetailEl.append(warn);
  }
}

function renderFooterActions() {
  const { model } = state;
  const locked = model.storage_state && !model.storage_state.unlocked;

  if (locked) {
    const action = model.primary_actions?.["unlock_storage"] ?? {};
    primaryActionEl.textContent = action.label ?? "解鎖倉庫 (500G)";
    primaryActionEl.dataset.actionId = "unlock_storage";
    primaryActionEl.dataset.disabledReason = action.disabled_reason ?? "";
    primaryActionEl.setAttribute("aria-disabled", String(!action.enabled));
    primaryActionEl.dataset.payload = JSON.stringify(action.payload ?? {});
  } else {
    // Unlocked: upgrade warehouse preview button
    const action = model.primary_actions?.["upgrade_storage"] ?? {};
    primaryActionEl.textContent = action.label ?? "升級倉庫容量 (未開放)";
    primaryActionEl.dataset.actionId = "upgrade_storage";
    primaryActionEl.dataset.disabledReason = action.disabled_reason ?? "預留功能未開放";
    primaryActionEl.setAttribute("aria-disabled", "true");
    primaryActionEl.dataset.payload = "{}";
  }
}

// User tab filter triggers
function selectBackpackCategory(categoryId) {
  state.selectedCategory = categoryId;
  pushActionLog({
    action_id: "select_category",
    payload: { category_id: categoryId },
    source: "category_tab",
    dispatched: true,
  });
  render();
}

// User click grid cell triggers
function handleSlotClick(row, listType) {
  const { model } = state;
  state.selectedItemId = row.item_id;
  state.selectedListType = listType;
  
  // 1. Log item select UIAction
  const actionId = listType === "deposit" ? "select_inventory_item" : "select_storage_item";
  pushActionLog({
    action_id: actionId,
    payload: { item_id: row.item_id },
    source: "grid_slot",
    dispatched: true,
  });

  renderQuickDetail();
  
  // 2. Adjust speech bubble context
  npcSpeechBubbleEl.replaceChildren();
  const speechText = document.createElement("p");
  if (!row.enabled) {
    speechText.textContent = model.npc?.dialog_locked ?? "「此物品無法寄放，請確認種類或倉庫容量。」";
    npcSpeechBubbleEl.appendChild(speechText);
    render();
    return;
  }
  
  const direction = listType === "deposit" ? "寄放" : "提取";
  speechText.textContent = `「好的，想把 ${row.title} ${direction} 嗎？請在面板中選擇你要轉移的數量。」`;
  npcSpeechBubbleEl.appendChild(speechText);

  // 3. Open popover controls
  state.quantityValue = 1;
  openPopover(row, listType);
  render();
}

// Steppers inside Modal logic
function openPopover(row, listType) {
  const { model } = state;
  const detail = model.item_details?.[row.item_id] ?? {};
  
  popoverItemNameEl.textContent = row.title ?? "";
  
  const isDeposit = listType === "deposit";
  popoverModeBadgeEl.textContent = isDeposit ? "存入" : "取出";
  popoverModeBadgeEl.style.borderColor = isDeposit ? "var(--accent-gold)" : "var(--accent-green)";
  popoverModeBadgeEl.style.color = isDeposit ? "var(--accent-gold)" : "var(--accent-green)";
  popoverModeBadgeEl.style.background = isDeposit ? "rgba(212, 175, 55, 0.08)" : "rgba(141, 163, 130, 0.08)";

  const backpackCount = isDeposit ? row.owned_count : (model.inventory_rows?.find(r => r.item_id === row.item_id)?.owned_count ?? 0);
  const storageCount = isDeposit ? (model.storage_rows?.find(r => r.item_id === row.item_id)?.owned_count ?? 0) : row.owned_count;
  
  popoverItemMetaEl.textContent = `我的背包：${backpackCount} 個 | 工會倉庫：${storageCount} 個`;
  
  updateStepperDisplay();

  // Render modal validations rows
  renderPopoverRequirements(model.requirement_rows?.[row.item_id] ?? []);

  // Sync confirm payload details
  const action = model.primary_actions?.[row.item_id] ?? {};
  popoverConfirmEl.textContent = isDeposit ? "確認存入" : "確認取出";
  popoverConfirmEl.dataset.actionId = action.action_id ?? "blocked_action";
  
  popoverOverlayEl.style.display = "flex";
  popoverOverlayEl.setAttribute("aria-hidden", "false");
}

function closePopover() {
  popoverOverlayEl.style.display = "none";
  popoverOverlayEl.setAttribute("aria-hidden", "true");
}

function adjustQuantity(delta) {
  const max = getMaxAllowedQuantity();
  let next = state.quantityValue + delta;
  next = Math.max(next, 1);
  next = Math.min(next, max);

  if (state.quantityValue !== next) {
    state.quantityValue = next;
    updateStepperDisplay();
    logQuantityChange();
  }
}

function updateStepperDisplay() {
  const max = getMaxAllowedQuantity();
  popoverValueEl.textContent = state.quantityValue;
  popoverLimitLabelEl.textContent = `轉移數量範圍：1 ~ ${max}`;

  popoverDecEl.disabled = state.quantityValue <= 1;
  popoverIncEl.disabled = state.quantityValue >= max;
  popoverMaxEl.disabled = state.quantityValue === max;
}

function logQuantityChange() {
  pushActionLog({
    action_id: "set_transfer_quantity",
    payload: { item_id: state.selectedItemId, quantity: state.quantityValue },
    source: "stepper_popover",
    dispatched: true,
  });
}

function renderPopoverRequirements(rows) {
  popoverRequirementListEl.replaceChildren();
  if (rows.length === 0) {
    return;
  }

  popoverRequirementListEl.replaceChildren(
    ...rows.map((row) => {
      const el = document.createElement("div");
      el.className = "requirement-row";

      const marker = document.createElement("span");
      marker.className = "requirement-marker";
      marker.dataset.status = row.status ?? "";
      marker.textContent = row.status === "met" ? "✔" : "✘";

      const copy = document.createElement("span");
      copy.className = "requirement-copy";

      const label = document.createElement("strong");
      label.textContent = row.label ?? "";

      const values = document.createElement("span");
      values.textContent = `需求: ${row.required_value ?? ""} / 目前: ${row.current_value ?? ""}`;

      copy.append(label, values);

      const status = document.createElement("span");
      status.className = "requirement-status";
      status.dataset.status = row.status ?? "";
      status.textContent = row.status === "met" ? "滿足" : (row.disabled_reason ?? "未滿足");

      el.append(marker, copy, status);
      return el;
    }),
  );
}

function executePopoverAction() {
  const actionId = popoverConfirmEl.dataset.actionId ?? "blocked_action";
  const direction = state.selectedListType === "deposit" ? "deposit_item" : "withdraw_item";
  
  pushActionLog({
    action_id: direction,
    payload: { item_id: state.selectedItemId, quantity: state.quantityValue },
    source: "popover_confirm",
    dispatched: true,
  });

  const transferName = getSelectedItemRow()?.title ?? "物品";
  const feedbackWord = state.selectedListType === "deposit" ? "存入" : "取出";
  
  npcSpeechBubbleEl.replaceChildren();
  const speechText = document.createElement("p");
  speechText.textContent = `「妥當了！${state.quantityValue} 個 ${transferName} 已順利${feedbackWord}完畢。」`;
  npcSpeechBubbleEl.appendChild(speechText);
  
  renderFeedback("諾亞", `「${transferName} 存取轉移操作成功！（已寫入 UIAction日誌）」`);
  closePopover();
  render();
}

// Rightmost bottom unlock button trigger
function activatePrimaryAction() {
  const actionId = primaryActionEl.dataset.actionId ?? "blocked_action";
  const payload = safeJson(primaryActionEl.dataset.payload, {});
  const disabledReason = primaryActionEl.dataset.disabledReason;
  const enabled = primaryActionEl.getAttribute("aria-disabled") !== "true";

  if (!enabled) {
    pushActionLog({
      action_id: actionId,
      payload,
      source: "primary_action",
      dispatched: false,
      reason: disabledReason || "disabled",
    });
    
    let warning = "「此功能目前無法使用。」";
    if (actionId === "unlock_storage") {
      warning = "「抱歉，米菈小隊攜帶的金幣不夠支付 500G 保管保管金喔。」";
    } else {
      warning = "「升級保管箱需要更高等級的工會許可證，目前第二幕 demo 暫未開放。」";
    }
    
    renderFeedback("諾亞", warning);
    return;
  }

  pushActionLog({
    action_id: actionId,
    payload,
    source: "primary_action",
    dispatched: true,
  });

  if (actionId === "unlock_storage") {
    renderFeedback("諾亞", "「解鎖倉庫成功！倉庫空間現已為米菈的小隊啟用。（本模擬不寫入存檔，請切換測試狀態觀看其它畫面。）」");
    npcSpeechBubbleEl.replaceChildren();
    const speechText = document.createElement("p");
    speechText.textContent = "「太好了，會費已經收訖。這就幫米菈小隊辦理開啟手續！」";
    npcSpeechBubbleEl.appendChild(speechText);
  }
}

// Helpers
function getSelectedItemRow() {
  if (!state.model) return null;
  const list = state.selectedListType === "deposit" ? (state.model.inventory_rows ?? []) : (state.model.storage_rows ?? []);
  return list.find((row) => row.item_id === state.selectedItemId) ?? null;
}

function getMaxAllowedQuantity() {
  const item = getSelectedItemRow();
  if (!item || !item.enabled) return 0;
  return item.owned_count ?? 1;
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

function createEmptyState(message) {
  const empty = document.createElement("div");
  empty.className = "empty-state";
  empty.textContent = message;
  return empty;
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
  subtitleEl.textContent = "無法讀取 Storage static fixture。";
  resourceStripEl.replaceChildren();
  inventoryGridEl.replaceChildren();
  storageGridEl.replaceChildren();
  backpackTabsEl.replaceChildren();
  quickDetailEl.replaceChildren();
  disableStepperControls();
  renderFeedback("系統", "請確認 fixtures 路徑與 JSON 格式。");

  const errorEl = document.createElement("div");
  errorEl.className = "load-error";
  errorEl.textContent = error instanceof Error ? error.message : String(error);
  inventoryGridEl.append(errorEl);
}
