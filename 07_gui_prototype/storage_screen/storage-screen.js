import { runtimeClient } from "../shared/runtime-client.js";

const fixtureSelect = document.querySelector("#fixture-select");
const titleEl = document.querySelector("#screen-title");
const subtitleEl = document.querySelector("#screen-subtitle");
const resourceStripEl = document.querySelector("#resource-strip");
const backpackTabsEl = document.querySelector("#backpack-tabs");

// Lists
const inventoryListEl = document.querySelector("#inventory-item-list");
const storageListEl = document.querySelector("#storage-item-list");

// Capacity
const capacityStatusEl = document.querySelector("#storage-status-badge");
const capacityBarFillEl = document.querySelector("#capacity-bar-fill");
const capacityTextEl = document.querySelector("#capacity-text");

// Center Transfer Action Panel & Inline Details
const transferActionPanelEl = document.querySelector("#transfer-action-panel");
const transferEmptyStateEl = document.querySelector("#transfer-empty-state");
const transferControlContentEl = document.querySelector("#transfer-control-content");
const transferItemNameEl = document.querySelector("#transfer-item-name");
const transferModeBadgeEl = document.querySelector("#transfer-mode-badge");
const transferItemUsageEl = document.querySelector("#transfer-item-usage");
const transferItemDescEl = document.querySelector("#transfer-item-desc");
const transferCountInfoEl = document.querySelector("#transfer-count-info");

// Stepper controls
const popoverValueEl = document.querySelector("#popover-value");
const popoverLimitLabelEl = document.querySelector("#popover-limit-label");
const popoverRequirementListEl = document.querySelector("#popover-requirement-list");
const popoverDecEl = document.querySelector("#popover-dec");
const popoverIncEl = document.querySelector("#popover-inc");
const popoverMaxEl = document.querySelector("#popover-max");
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
const warehouseCapacityLimit = 10; // Fixed storage capacity rows

// Emoji dictionary for list items
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

// Inline Stepper Listeners
popoverDecEl.addEventListener("click", () => adjustQuantity(-1));
popoverIncEl.addEventListener("click", () => adjustQuantity(1));
popoverMaxEl.addEventListener("click", () => {
  const max = getMaxAllowedQuantity();
  state.quantityValue = max;
  updateStepperDisplay();
  logQuantityChange();
});

popoverConfirmEl.addEventListener("click", () => {
  executeTransferAction();
});

primaryActionEl.addEventListener("click", () => {
  activatePrimaryAction();
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

async function handleBackToTown() {
  const payload = { from: "storage_screen" };
  pushActionLog({
    action_id: "back_to_town_hub",
    payload,
    source: "secondary_action",
    dispatched: true,
  });
  try {
    const result = await runtimeClient.dispatchAction("storage_screen", "back_to_town_hub", payload);
    shellEl.dataset.runtimeStatus = result.status ?? "success";
    window.setTimeout(() => {
      window.location.href = runtimeClient.nextRoute(result, townHubRoute);
    }, navigationDelayMs);
  } catch (error) {
    const reason = runtimeClient.errorMessage(error);
    shellEl.dataset.runtimeStatus = error?.runtimeStatus ?? "error";
    renderFeedback("諾亞", reason);
    pushActionLog({
      action_id: "back_to_town_hub",
      payload,
      source: "secondary_action",
      dispatched: false,
      reason,
    });
  }
}

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

    state.selectedCategory = "all";
    state.selectedItemId = null;
    state.selectedListType = null;
    state.quantityValue = 1;
    state.actionLog = [];

    closeTransferControls();
    render();
    logSystem(`loaded ${path}`);

    // Set initial JRPG NPC welcome guidance into bottom bar
    const speaker = model.npc?.name ?? "諾亞";
    const welcome = model.npc?.avatar_text ?? "選擇左側背包物品 (存入) 或右側倉庫物品 (取出) 來進行轉移整理。";
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
    const model = await runtimeClient.getScreen("storage_screen");
    state.model = model;

    state.selectedCategory = "all";
    state.selectedItemId = null;
    state.selectedListType = null;
    state.quantityValue = 1;
    state.actionLog = [];

    closeTransferControls();
    render();
    logSystem("live runtime screen loaded");

    const speaker = model.npc?.name ?? "諾亞";
    const welcome = model.npc?.avatar_text ?? "選擇左側背包物品 (存入) 或右側倉庫物品 (取出) 來進行轉移整理。";
    renderFeedback(speaker, welcome);

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

    state.selectedCategory = "all";
    state.selectedItemId = null;
    state.selectedListType = null;
    state.quantityValue = 1;
    state.actionLog = [];

    closeTransferControls();
    render();
    logSystem(`live unavailable; loaded fixture ${path}`);
    pushActionLog({
      action_id: "live_bridge_unavailable",
      payload: { reason: liveError instanceof Error ? liveError.message : String(liveError) },
      source: "live_loader",
      dispatched: false,
      reason: "fallback_to_fixture",
    });

    const speaker = model.npc?.name ?? "諾亞";
    const welcome = model.npc?.avatar_text ?? "選擇左側背包物品 (存入) 或右側倉庫物品 (取出) 來進行轉移整理。";
    renderFeedback(speaker, welcome);

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
  renderBackpackCategoryTabs(model.category_tabs ?? []);
  renderCapacityCard();

  // Long Lists
  renderBackpackList();
  renderStorageList();

  // Details & Action panel
  updateTransferPanel();
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
  const percentage = Math.min((capacityUsed / warehouseCapacityLimit) * 100, 100);
  capacityBarFillEl.style.width = `${percentage}%`;
  capacityTextEl.textContent = `容量: ${capacityUsed} / ${warehouseCapacityLimit}`;
}

function renderBackpackList() {
  const { model, selectedCategory } = state;
  inventoryListEl.replaceChildren();

  const rows = model.inventory_rows ?? [];
  const filtered = selectedCategory === "all" ? rows : rows.filter(row => row.category === selectedCategory);

  if (filtered.length === 0) {
    inventoryListEl.appendChild(createEmptyState("背包內沒有此類物品"));
    return;
  }

  filtered.forEach((row) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "item-row";

    const isSelected = row.item_id === state.selectedItemId && state.selectedListType === "deposit";
    button.classList.toggle("is-selected", isSelected);
    button.setAttribute("aria-pressed", String(isSelected));
    button.dataset.itemId = row.item_id;

    if (!row.enabled) {
      button.classList.add("is-blocked");
    }

    // Left info
    const leftPart = document.createElement("div");
    leftPart.className = "item-row-left";

    const icon = document.createElement("span");
    icon.className = "item-row-icon";
    icon.textContent = emojiMap[row.item_id] ?? "📦";

    const textPart = document.createElement("div");
    textPart.className = "item-row-text";

    const name = document.createElement("span");
    name.className = "item-row-name";
    name.textContent = row.title ?? "";

    const summary = document.createElement("span");
    summary.className = "item-row-summary";
    summary.textContent = row.summary ?? "";

    textPart.append(name, summary);
    leftPart.append(icon, textPart);

    // Right info
    const rightPart = document.createElement("div");
    rightPart.className = "item-row-right";

    const count = document.createElement("span");
    count.className = "item-row-quantity";
    count.textContent = `x${row.owned_count ?? 0}`;

    rightPart.append(count);

    // Badge if blocked
    if (!row.enabled) {
      const badge = document.createElement("span");
      badge.className = "item-row-badge";
      badge.dataset.status = row.item_id === "key_fire_mark_shard" ? "blocked" : "full";
      badge.textContent = row.item_id === "key_fire_mark_shard" ? "貴重物" : "容量滿";
      rightPart.append(badge);
    }

    button.append(leftPart, rightPart);
    button.addEventListener("click", () => handleRowClick(row, "deposit"));

    inventoryListEl.appendChild(button);
  });
}

function renderStorageList() {
  const { model } = state;
  storageListEl.replaceChildren();

  const locked = model.storage_state && !model.storage_state.unlocked;
  const rows = locked ? [] : (model.storage_rows ?? []);

  // JRPG standard visual limit: Always render exactly 10 rows
  for (let i = 0; i < warehouseCapacityLimit; i++) {
    const row = rows[i];

    if (locked) {
      // Locked warehouse slot placeholder row
      const el = document.createElement("div");
      el.className = "item-row is-locked";

      const leftPart = document.createElement("div");
      leftPart.className = "item-row-left";

      const icon = document.createElement("span");
      icon.className = "item-row-icon";
      icon.textContent = "🔒";

      const textPart = document.createElement("div");
      textPart.className = "item-row-text";

      const name = document.createElement("span");
      name.className = "item-row-name";
      name.textContent = "保管欄位鎖定";

      const summary = document.createElement("span");
      summary.className = "item-row-summary";
      summary.textContent = "尚未支付工會解鎖會費";

      textPart.append(name, summary);
      leftPart.append(icon, textPart);
      el.append(leftPart);
      storageListEl.appendChild(el);

    } else if (!row) {
      // Empty placeholder row
      const el = document.createElement("div");
      el.className = "item-row is-empty";

      const leftPart = document.createElement("div");
      leftPart.className = "item-row-left";

      const icon = document.createElement("span");
      icon.className = "item-row-icon";
      icon.textContent = "➖";

      const emptyText = document.createElement("span");
      emptyText.className = "item-row-empty-text";
      emptyText.textContent = "[ 空置保管欄位 ]";

      leftPart.append(icon, emptyText);
      el.append(leftPart);
      storageListEl.appendChild(el);

    } else {
      // Occupied storage row
      const button = document.createElement("button");
      button.type = "button";
      button.className = "item-row";

      const isSelected = row.item_id === state.selectedItemId && state.selectedListType === "withdraw";
      button.classList.toggle("is-selected", isSelected);
      button.setAttribute("aria-pressed", String(isSelected));
      button.dataset.itemId = row.item_id;

      // Left info
      const leftPart = document.createElement("div");
      leftPart.className = "item-row-left";

      const icon = document.createElement("span");
      icon.className = "item-row-icon";
      icon.textContent = emojiMap[row.item_id] ?? "📦";

      const textPart = document.createElement("div");
      textPart.className = "item-row-text";

      const name = document.createElement("span");
      name.className = "item-row-name";
      name.textContent = row.title ?? "";

      const summary = document.createElement("span");
      summary.className = "item-row-summary";
      summary.textContent = row.summary ?? "";

      textPart.append(name, summary);
      leftPart.append(icon, textPart);

      // Right info
      const rightPart = document.createElement("div");
      rightPart.className = "item-row-right";

      const count = document.createElement("span");
      count.className = "item-row-quantity";
      count.textContent = `x${row.owned_count ?? 0}`;

      rightPart.append(count);

      button.append(leftPart, rightPart);
      button.addEventListener("click", () => handleRowClick(row, "withdraw"));

      storageListEl.appendChild(button);
    }
  }
}

function updateTransferPanel() {
  const { model } = state;

  // If warehouse is locked, keep inline panel showing the guide
  if (model.storage_state && !model.storage_state.unlocked) {
    transferEmptyStateEl.style.display = "flex";
    transferControlContentEl.style.display = "none";

    transferEmptyStateEl.replaceChildren();
    const h3 = document.createElement("h3");
    h3.textContent = "倉庫保管服務未啟用";
    h3.style.color = "var(--accent-gold)";
    h3.style.fontSize = "0.95rem";

    const p1 = document.createElement("p");
    p1.textContent = "請點選右下角「解鎖倉庫」";
    p1.style.fontSize = "0.82rem";
    p1.style.marginTop = "0.5rem";

    const p2 = document.createElement("p");
    p2.textContent = "支付諾亞 500G 保管金開啟服務。";
    p2.style.fontSize = "0.75rem";
    p2.className = "empty-sub";

    transferEmptyStateEl.append(h3, p1, p2);
    return;
  }

  const item = getSelectedItemRow();
  if (!item) {
    // Show default instruction empty state
    transferEmptyStateEl.style.display = "flex";
    transferControlContentEl.style.display = "none";

    transferEmptyStateEl.replaceChildren();
    const p1 = document.createElement("p");
    p1.textContent = "選擇左側背包物品 (存入)";
    const p2 = document.createElement("p");
    p2.textContent = "或右側倉庫物品 (取出)";
    const p3 = document.createElement("p");
    p3.className = "empty-sub";
    p3.textContent = "即可進行物品整理";

    transferEmptyStateEl.append(p1, p2, p3);
    return;
  }

  // Show active controls
  transferEmptyStateEl.style.display = "none";
  transferControlContentEl.style.display = "block";

  const detail = model.item_details?.[item.item_id] ?? {};

  transferItemNameEl.textContent = item.title ?? "";

  const isDeposit = state.selectedListType === "deposit";
  transferModeBadgeEl.textContent = isDeposit ? "存入倉庫 ➔" : "🠔 取出背包";

  // Badge styling
  transferModeBadgeEl.style.borderColor = isDeposit ? "var(--accent-gold)" : "var(--accent-green)";
  transferModeBadgeEl.style.color = isDeposit ? "var(--accent-gold)" : "var(--accent-green)";
  transferModeBadgeEl.style.background = isDeposit ? "rgba(212, 175, 55, 0.05)" : "rgba(141, 163, 130, 0.05)";

  transferItemUsageEl.textContent = detail.category_label ?? "物品";
  transferItemDescEl.textContent = `${detail.description ?? ""} (${detail.use_context ?? ""})`;

  // Meta count preview
  const backpackCount = isDeposit ? item.owned_count : (model.inventory_rows?.find(r => r.item_id === item.item_id)?.owned_count ?? 0);
  const storageCount = isDeposit ? (model.storage_rows?.find(r => r.item_id === item.item_id)?.owned_count ?? 0) : item.owned_count;
  transferCountInfoEl.textContent = `我的背包：${backpackCount} 個 | 工會倉庫：${storageCount} 個`;

  updateStepperDisplay();

  // Render inline requirements
  renderPopoverRequirements(model.requirement_rows?.[item.item_id] ?? []);

  // Confirm button settings
  const action = model.primary_actions?.[item.item_id] ?? {};
  popoverConfirmEl.textContent = isDeposit ? "確認存入" : "確認取出";
  popoverConfirmEl.dataset.actionId = action.action_id ?? "blocked_action";
  popoverConfirmEl.dataset.disabledReason = action.disabled_reason ?? "";

  const canConfirm = action.enabled && item.enabled;
  popoverConfirmEl.setAttribute("aria-disabled", String(!canConfirm));
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
    const action = model.primary_actions?.["upgrade_storage"] ?? {};
    primaryActionEl.textContent = action.label ?? "升級倉庫容量 (未開放)";
    primaryActionEl.dataset.actionId = "upgrade_storage";
    primaryActionEl.dataset.disabledReason = action.disabled_reason ?? "預留功能未開放";
    primaryActionEl.setAttribute("aria-disabled", "true");
    primaryActionEl.dataset.payload = "{}";
  }
}

// Category tabs triggers
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

// Click long list item triggers
function handleRowClick(row, listType) {
  const { model } = state;
  state.selectedItemId = row.item_id;
  state.selectedListType = listType;

  // 1. Log select action
  const actionId = listType === "deposit" ? "select_inventory_item" : "select_storage_item";
  pushActionLog({
    action_id: actionId,
    payload: { item_id: row.item_id },
    source: "list_row",
    dispatched: true,
  });

  // 2. NPC response dialog printed to the bottom JRPG guidance bar
  const speaker = model.npc?.name ?? "諾亞";
  if (!row.enabled) {
    const reason = row.disabled_reason ? `（原因：${row.disabled_reason}）` : "";
    renderFeedback(speaker, `「此物品無法寄放 ${reason}。普通素材可以存，貴重物請隨身保管。」`);
    state.quantityValue = 0;
    render();
    return;
  }

  const directionText = listType === "deposit" ? "存入" : "取出";
  renderFeedback(speaker, `「好的，想把 ${row.title} ${directionText} 嗎？請在面板中選擇你要轉移的數量。」`);

  // 3. Reset stepper
  state.quantityValue = 1;
  render();
}

function closeTransferControls() {
  state.selectedItemId = null;
  state.selectedListType = null;
  state.quantityValue = 1;
}

function adjustQuantity(delta) {
  const max = getMaxAllowedQuantity();
  if (max === 0) return;

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
  popoverIncEl.disabled = state.quantityValue >= max || max === 0;
  popoverMaxEl.disabled = state.quantityValue === max || max === 0;
}

function logQuantityChange() {
  pushActionLog({
    action_id: "set_transfer_quantity",
    payload: { item_id: state.selectedItemId, quantity: state.quantityValue },
    source: "inline_stepper",
    dispatched: true,
  });
}

function renderPopoverRequirements(rows) {
  popoverRequirementListEl.replaceChildren();
  if (rows.length === 0) return;

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

// Inline confirm button execute
function executeTransferAction() {
  const isEnabled = popoverConfirmEl.getAttribute("aria-disabled") !== "true";
  if (!isEnabled) {
    const disabledReason = popoverConfirmEl.dataset.disabledReason || "未滿足存取條件";
    pushActionLog({
      action_id: "blocked_action",
      payload: { item_id: state.selectedItemId, quantity: state.quantityValue },
      source: "inline_confirm",
      dispatched: false,
      reason: disabledReason,
    });

    renderFeedback("諾亞", `「無法存取：${disabledReason}，請重新選取。」`);
    return;
  }

  const direction = state.selectedListType === "deposit" ? "deposit_item" : "withdraw_item";
  const payload = { item_id: state.selectedItemId, quantity: state.quantityValue };

  pushActionLog({
    action_id: direction,
    payload,
    source: "inline_confirm",
    dispatched: true,
  });

  if (runtimeClient.isLiveMode()) {
    handleLiveTransferAction(direction, payload);
    return;
  }

  const transferName = getSelectedItemRow()?.title ?? "物品";
  const feedbackWord = state.selectedListType === "deposit" ? "存入" : "取出";

  renderFeedback("諾亞", `「妥當了！${state.quantityValue} 個 ${transferName} 已順利${feedbackWord}完畢，保管箱容量已即時更新。」`);

  closeTransferControls();
  render();
}

async function handleLiveTransferAction(actionId, payload) {
  try {
    const result = await runtimeClient.dispatchAction("storage_screen", actionId, payload);
    shellEl.dataset.runtimeStatus = result.status ?? "success";
    if (result.screen_model) {
      state.model = result.screen_model;
      closeTransferControls();
      render();
    }
    if (result.message) {
      renderFeedback("諾亞", result.message);
    }
  } catch (error) {
    const reason = runtimeClient.errorMessage(error);
    shellEl.dataset.runtimeStatus = error?.runtimeStatus ?? "error";
    renderFeedback("諾亞", reason);
    pushActionLog({
      action_id: actionId,
      payload,
      source: "inline_confirm",
      dispatched: false,
      reason,
    });
  }
}

// Unlock storage bottom button trigger
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
      warning = "「抱歉，米菈小隊攜帶的金幣不夠支付 500G 保管金喔。」";
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

  if (runtimeClient.isLiveMode()) {
    handleLivePrimaryAction(actionId, payload);
    return;
  }

  if (actionId === "unlock_storage") {
    renderFeedback("諾亞", "「解鎖成功！這就幫米菈小隊開啟專屬的保管箱空間！（請切換上方測試狀態以觀看開啟後畫面）」");
  }
}

async function handleLivePrimaryAction(actionId, payload) {
  try {
    const result = await runtimeClient.dispatchAction("storage_screen", actionId, payload);
    shellEl.dataset.runtimeStatus = result.status ?? "success";
    if (result.screen_model) {
      state.model = result.screen_model;
      render();
    }
    if (result.message) {
      renderFeedback("諾亞", result.message);
    }
  } catch (error) {
    const reason = runtimeClient.errorMessage(error);
    shellEl.dataset.runtimeStatus = error?.runtimeStatus ?? "error";
    renderFeedback("諾亞", reason);
    pushActionLog({
      action_id: actionId,
      payload,
      source: "primary_action",
      dispatched: false,
      reason,
    });
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
  inventoryListEl.replaceChildren();
  storageListEl.replaceChildren();
  backpackTabsEl.replaceChildren();
  closeTransferControls();
  updateTransferPanel();
  renderFeedback("系統", "請確認 fixtures 路徑與 JSON 格式。");

  const errorEl = document.createElement("div");
  errorEl.className = "load-error";
  errorEl.textContent = error instanceof Error ? error.message : String(error);
  inventoryListEl.append(errorEl);
}
