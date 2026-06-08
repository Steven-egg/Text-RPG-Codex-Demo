(function () {
const fixtureSelect = document.querySelector("#fixture-select");
const titleEl = document.querySelector("#screen-title");
const subtitleEl = document.querySelector("#screen-subtitle");
const npcPortraitEl = document.querySelector("#npc-portrait");
const npcNameEl = document.querySelector("#npc-name");
const npcRoleEl = document.querySelector("#npc-role");
const filterRowEl = document.querySelector("#task-filters");
const storyHintSlotEl = document.querySelector("#story-hint-slot");
const taskListEl = document.querySelector("#task-list");
const taskDetailEl = document.querySelector("#task-detail");
const rewardSummaryEl = document.querySelector("#reward-summary");
const conditionListEl = document.querySelector("#condition-list");
const feedbackMessageEl = document.querySelector("#feedback-message");
const primaryActionEl = document.querySelector("#primary-action");
const backActionEl = document.querySelector("#back-action");
const actionLogEl = document.querySelector("#action-log");
const clearLogEl = document.querySelector("#clear-log");
const shellEl = document.querySelector(".guild-shell");

// New DOM element selections for Material Sell mode
const tasksViewContainerEl = document.querySelector("#tasks-view-container");
const sellViewContainerEl = document.querySelector("#sell-view-container");
const tasksDetailContainerEl = document.querySelector("#tasks-detail-container");
const sellDetailContainerEl = document.querySelector("#sell-detail-container");
const materialSellListEl = document.querySelector("#material-sell-list");
const sellMaterialDetailEl = document.querySelector("#sell-material-detail");
const sellRewardSummaryEl = document.querySelector("#sell-reward-summary");
const sellConfirmContainerEl = document.querySelector("#sell-confirm-container");
const modeTasksBtn = document.querySelector("#mode-tasks-btn");
const modeSellBtn = document.querySelector("#mode-sell-btn");

const state = {
  model: null,
  selectedFilterId: null,
  selectedTaskId: null,
  selectedStoryHint: false,
  actionLog: [],
  // Material Sell state tracking
  mode: "tasks",
  selectedMaterialId: null,
  sellQuantity: 1,
};

const townHubRoute = "../town_hub/index.html";
const navigationDelayMs = 120;

modeTasksBtn.addEventListener("click", () => {
  switchMode("tasks");
});

modeSellBtn.addEventListener("click", () => {
  switchMode("sell");
});

function switchMode(mode) {
  state.mode = mode;
  modeTasksBtn.classList.toggle("is-active", mode === "tasks");
  modeSellBtn.classList.toggle("is-active", mode === "sell");

  if (mode === "tasks") {
    tasksViewContainerEl.style.display = "flex";
    sellViewContainerEl.style.display = "none";
    tasksDetailContainerEl.style.display = "contents";
    sellDetailContainerEl.style.display = "none";
  } else {
    tasksViewContainerEl.style.display = "none";
    sellViewContainerEl.style.display = "flex";
    tasksDetailContainerEl.style.display = "none";
    sellDetailContainerEl.style.display = "contents";

    // Default select first material if any
    const mList = state.model?.sellable_materials ?? [];
    if (mList.length > 0 && !mList.some(m => m.item_id === state.selectedMaterialId)) {
      state.selectedMaterialId = mList[0].item_id;
      state.sellQuantity = 1;
    }
  }

  pushActionLog({
    action_id: "switch_mode",
    payload: { mode },
    source: "mode_tabs",
    dispatched: true,
  });

  render();
}

fixtureSelect.addEventListener("change", () => {
  loadFixture(fixtureSelect.value);
});

taskListEl.addEventListener("keydown", (event) => {
  if (!["ArrowUp", "ArrowDown"].includes(event.key)) {
    return;
  }

  const rowButtons = getSelectableRows();
  const currentIndex = rowButtons.indexOf(document.activeElement);
  if (currentIndex < 0) {
    return;
  }

  event.preventDefault();
  const delta = event.key === "ArrowDown" ? 1 : -1;
  rowButtons[wrapIndex(currentIndex + delta, rowButtons.length)]?.focus();
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
  renderFeedback("工會提示", "「返回城鎮已記錄（Lab 模式不執行真實導航與頁面跳轉）。」");
}););



clearLogEl.addEventListener("click", () => {
  state.actionLog = [];
  renderActionLog();
});

loadFixture(fixtureSelect.value);

function initializeSelectionDefaults(model) {
  state.selectedFilterId = model.selected_filter_id ?? model.task_filters?.[0]?.id ?? "all";
  state.selectedTaskId = model.selected_task_id ?? model.task_rows?.[0]?.task_id ?? null;
  state.selectedStoryHint = false;

  // Default to first material if none selected or if previously selected is missing
  const mList = model.sellable_materials ?? [];
  if (mList.length > 0) {
    if (!mList.some(m => m.item_id === state.selectedMaterialId)) {
      state.selectedMaterialId = mList[0].item_id;
      state.sellQuantity = 1;
    }
  } else {
    state.selectedMaterialId = null;
    state.sellQuantity = 1;
  }
}

function loadFixture(scenarioKey) {
  shellEl.dataset.loadState = "loading";
  try {
    let model = null;
    const key = scenarioKey.replace('./fixtures/', '').replace('.json', '');
    if (key === "default" || key === "guild-default") {
      model = JSON.parse(JSON.stringify(window.GUILD_DEFAULT_FIXTURE));
    } else if (key === "quest-ready" || key === "guild-quest-ready") {
      model = JSON.parse(JSON.stringify(window.GUILD_QUEST_READY_FIXTURE));
    } else {
      throw new Error("Unknown scenario key: " + scenarioKey);
    }
    state.model = model;
    initializeSelectionDefaults(model);
    state.actionLog = [];
    render();
    shellEl.dataset.loadState = "ready";
  } catch (error) {
    console.error(error);
    shellEl.dataset.loadState = "error";
  }
}





function renderResourceStrip(strip) {
  const el = document.querySelector("#resource-strip");
  if (!el) return;
  if (!strip || strip.length === 0) {
    el.style.display = "none";
    return;
  }
  el.style.display = "flex";
  el.replaceChildren(
    ...strip.map((item) => {
      const itemEl = document.createElement("div");
      itemEl.className = "resource-item";
      itemEl.dataset.tone = item.tone ?? "neutral";
      itemEl.textContent = item.label ?? "";
      return itemEl;
    })
  );
}

function render() {
  const { model } = state;
  titleEl.textContent = model.title ?? "";
  subtitleEl.textContent = model.subtitle ?? "";
  npcNameEl.textContent = model.npc?.name ?? "";
  npcRoleEl.textContent = model.npc?.role ?? "";
  npcPortraitEl.dataset.npcId = model.npc?.id ?? "";

  renderResourceStrip(model.resource_strip);

  if (state.mode === "tasks") {
    renderFilters(model.task_filters ?? []);
    renderStoryHint(model.story_hint_card);
    renderTaskList(getVisibleTaskRows());
    ensureSelectionVisible();
    renderSelectedContent();
  } else {
    renderMaterialList(model.sellable_materials ?? []);
    renderSelectedMaterialContent();
  }
  renderActionLog();
}

function renderFilters(filters) {
  filterRowEl.replaceChildren(
    ...filters.map((filter) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "filter-button";
      button.classList.toggle("is-selected", filter.id === state.selectedFilterId);
      button.setAttribute("aria-pressed", String(filter.id === state.selectedFilterId));
      button.setAttribute("aria-disabled", String(!filter.enabled));

      const label = document.createElement("strong");
      label.textContent = filter.label ?? filter.id;

      const count = document.createElement("span");
      count.textContent = `${filter.count ?? 0} 件`;

      button.append(label, count);
      button.addEventListener("click", () => {
        if (!filter.enabled) {
          pushActionLog({
            action_id: "select_filter",
            payload: { filter_id: filter.id },
            source: "task_filter",
            dispatched: false,
            reason: filter.disabled_reason ?? "disabled",
          });
          return;
        }

        state.selectedFilterId = filter.id;
        state.selectedStoryHint = false;
        state.selectedTaskId = getVisibleTaskRows()[0]?.task_id ?? null;
        pushActionLog({
          action_id: "select_filter",
          payload: { filter_id: filter.id },
          source: "task_filter",
          dispatched: true,
        });
        render();
      });
      return button;
    }),
  );
}

function renderStoryHint(card) {
  if (!card?.visible) {
    storyHintSlotEl.replaceChildren();
    return;
  }

  const button = document.createElement("button");
  button.type = "button";
  button.className = "story-hint-card";
  button.classList.toggle("is-selected", state.selectedStoryHint);
  button.setAttribute("aria-pressed", String(state.selectedStoryHint));
  button.setAttribute("aria-disabled", String(!card.enabled));
  button.title = card.enabled ? card.description ?? "" : card.disabled_reason ?? "";

  const title = document.createElement("strong");
  title.textContent = card.title ?? "";

  const description = document.createElement("span");
  description.textContent = card.description ?? "";

  button.append(title, description);
  button.addEventListener("focus", () => {
    selectStoryHint(false);
  });
  button.addEventListener("click", () => {
    selectStoryHint(true);
  });

  storyHintSlotEl.replaceChildren(button);
}

function renderTaskList(rows) {
  if (rows.length === 0) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.textContent = state.model?.empty_state?.message ?? "目前沒有可顯示的委託。";
    taskListEl.replaceChildren(empty);
    return;
  }

  taskListEl.replaceChildren(
    ...rows.map((row) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "task-row";
      button.dataset.taskId = row.task_id;
      button.classList.toggle("is-selected", row.task_id === state.selectedTaskId && !state.selectedStoryHint);
      button.setAttribute("aria-pressed", String(row.task_id === state.selectedTaskId && !state.selectedStoryHint));
      button.setAttribute("aria-disabled", String(!row.enabled));
      button.title = row.enabled ? row.title ?? "" : row.disabled_reason ?? "";

      const copy = document.createElement("span");
      const title = document.createElement("span");
      title.className = "task-title";
      title.textContent = row.title ?? "";

      const giver = document.createElement("span");
      giver.className = "task-giver";
      giver.textContent = `委託人：${row.giver ?? "未知"}`;

      copy.append(title, giver);

      const status = document.createElement("span");
      status.className = "status-badge";
      status.dataset.status = row.status ?? "";
      status.textContent = row.status_label ?? "";

      button.append(copy, status);
      button.addEventListener("focus", () => {
        selectTask(row.task_id, false);
      });
      button.addEventListener("click", () => {
        selectTask(row.task_id, true);
      });
      return button;
    }),
  );
}

function renderSelectedContent() {
  if (state.selectedStoryHint) {
    renderStoryDetail();
    return;
  }

  const task = getSelectedTask();
  if (!task) {
    renderEmptyDetail();
    return;
  }

  const detail = state.model.task_details?.[task.task_id] ?? {};
  const titleRow = document.createElement("div");
  titleRow.className = "detail-title-row";

  const titleCopy = document.createElement("div");
  const title = document.createElement("h2");
  title.textContent = detail.title ?? task.title ?? "";

  const giver = document.createElement("p");
  giver.className = "detail-subtitle";
  giver.textContent = `委託人：${detail.giver ?? task.giver ?? "未知"} / ${detail.status_label ?? task.status_label ?? ""}`;

  titleCopy.append(title, giver);

  const status = document.createElement("span");
  status.className = "status-badge";
  status.dataset.status = task.status ?? "";
  status.textContent = task.status_label ?? "";

  titleRow.append(titleCopy, status);

  const description = document.createElement("p");
  description.className = "detail-description";
  description.textContent = detail.description ?? "";

  const note = document.createElement("p");
  note.className = "detail-note";
  note.textContent = detail.notes ?? "這份資料只來自 static fixture，用於驗證 Guild Screen GUI。";

  taskDetailEl.replaceChildren(titleRow, description, note);
  renderRewards(state.model.reward_summaries?.[task.task_id]);
  renderConditions(state.model.condition_rows?.[task.task_id] ?? []);
  renderFeedback(getFeedbackForTask(task));
  renderPrimaryAction(getPrimaryActionForTask(task));
}

function renderStoryDetail() {
  const card = state.model.story_hint_card;
  const title = document.createElement("h2");
  title.textContent = card.title ?? "";

  const subtitle = document.createElement("p");
  subtitle.className = "detail-subtitle";
  subtitle.textContent = card.status_label ?? "主線線索";

  const description = document.createElement("p");
  description.className = "detail-description";
  description.textContent = card.detail_description ?? card.description ?? "";

  const note = document.createElement("p");
  note.className = "detail-note";
  note.textContent = card.notes ?? "這是特殊互動入口，不計入 task filter。";

  taskDetailEl.replaceChildren(title, subtitle, description, note);
  renderRewards(card.reward_summary);
  renderConditions(card.condition_rows ?? []);
  renderFeedback(card.feedback_message ?? state.model.feedback_message);
  renderPrimaryAction({
    action_id: card.primary_action ?? "open_story_hint",
    label: card.action_label ?? "詢問線索",
    enabled: card.enabled,
    disabled_reason: card.disabled_reason,
    payload: { story_hint_id: card.id },
  });
}

function renderEmptyDetail() {
  taskDetailEl.replaceChildren(createEmptyState("請先選擇委託。"));
  renderRewards(null);
  renderConditions([]);
  renderFeedback(state.model.empty_state?.message ?? "目前沒有可顯示的委託。");
  renderPrimaryAction({
    action_id: "unavailable",
    label: "不可用",
    enabled: false,
    disabled_reason: "請先選擇委託",
    payload: {},
  });
}

function renderRewards(summary) {
  if (!summary) {
    rewardSummaryEl.replaceChildren(createEmptyState("沒有報酬資料。"));
    return;
  }

  const items = [];
  if (summary.gold != null) {
    items.push({ label: "金幣", value: `${summary.gold}G` });
  }
  if (summary.guild_points != null) {
    items.push({ label: "工會積分", value: `${summary.guild_points}` });
  }
  for (const item of summary.items ?? []) {
    items.push({ label: item.label, value: `x${item.quantity}` });
  }
  for (const unlock of summary.unlocks ?? []) {
    items.push({ label: "解鎖", value: unlock });
  }

  if (summary.notes) {
    items.push({ label: "備註", value: summary.notes });
  }

  rewardSummaryEl.replaceChildren(
    createList("reward-list", items, (item) => {
      const row = document.createElement("div");
      row.className = "reward-item";
      const label = document.createElement("strong");
      label.textContent = item.label;
      const value = document.createElement("span");
      value.textContent = item.value;
      row.append(label, value);
      return row;
    }),
  );
}

function renderConditions(rows) {
  if (rows.length === 0) {
    conditionListEl.replaceChildren(createEmptyState("沒有回報條件。"));
    return;
  }

  conditionListEl.replaceChildren(
    createList("condition-list", rows, (row) => {
      const el = document.createElement("div");
      el.className = "condition-row";

      const copy = document.createElement("div");
      const label = document.createElement("span");
      label.className = "condition-label";
      label.textContent = row.label ?? "";

      const values = document.createElement("span");
      values.className = "condition-values";
      values.textContent = `${row.required_value ?? ""} / 目前：${row.current_value ?? ""}`;

      copy.append(label, values);

      const status = document.createElement("span");
      status.className = "condition-status";
      status.dataset.status = row.status ?? "";
      status.textContent = row.status_label ?? row.status ?? "";

      el.append(copy, status);
      return el;
    }),
  );
}

function renderFeedback(message) {
  const feedback = typeof message === "string" ? { text: message } : message;
  feedbackMessageEl.textContent = feedback?.speaker ? `${feedback.speaker}：${feedback.text}` : (feedback?.text ?? "");
}

function renderPrimaryAction(action) {
  primaryActionEl.textContent = action.label ?? action.action_id ?? "不可用";
  primaryActionEl.dataset.actionId = action.action_id ?? "unavailable";
  primaryActionEl.dataset.payload = JSON.stringify(action.payload ?? {});
  primaryActionEl.dataset.disabledReason = action.disabled_reason ?? "";
  primaryActionEl.setAttribute("aria-disabled", String(!action.enabled));
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

function selectTask(taskId, shouldLog) {
  state.selectedTaskId = taskId;
  state.selectedStoryHint = false;
  if (shouldLog) {
    pushActionLog({
      action_id: "view_quest_detail",
      payload: { task_id: taskId },
      source: "task_row",
      dispatched: true,
    });
  }
  render();
}

function selectStoryHint(shouldLog) {
  state.selectedStoryHint = true;
  state.selectedTaskId = null;
  if (shouldLog) {
    pushActionLog({
      action_id: "view_story_hint",
      payload: { story_hint_id: state.model.story_hint_card?.id },
      source: "story_hint_card",
      dispatched: true,
    });
  }
  render();
}

function activatePrimaryAction() {
  const actionId = primaryActionEl.dataset.actionId ?? "unavailable";
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
    renderFeedback({ speaker: state.model.npc?.name, text: disabledReason || "目前無法執行這個動作。" });
    return;
  }

  pushActionLog({
    action_id: actionId,
    payload,
    source: "primary_action",
    dispatched: true,
  });

  

  renderFeedback({ speaker: state.model.npc?.name, text: "已送出 UIAction；static prototype 不會修改任務狀態。" });
}



function getVisibleTaskRows() {
  const rows = state.model?.task_rows ?? [];
  if (state.selectedFilterId === "all") {
    return rows;
  }
  return rows.filter((row) => row.status === state.selectedFilterId);
}

function ensureSelectionVisible() {
  if (state.selectedStoryHint) {
    return;
  }

  const rows = getVisibleTaskRows();
  if (!rows.some((row) => row.task_id === state.selectedTaskId)) {
    state.selectedTaskId = rows[0]?.task_id ?? null;
  }
}

function getSelectedTask() {
  return state.model?.task_rows?.find((row) => row.task_id === state.selectedTaskId) ?? null;
}

function getPrimaryActionForTask(task) {
  const detail = state.model.task_details?.[task.task_id] ?? {};
  const payload = { task_id: task.task_id };

  if (task.status === "ready_to_submit") {
    return {
      action_id: "submit_quest",
      label: "回報委託",
      enabled: true,
      payload,
    };
  }

  if (task.status === "completed") {
    return {
      action_id: "unavailable",
      label: "已完成",
      enabled: false,
      disabled_reason: "這個委託已完成",
      payload,
    };
  }

  return {
    action_id: "unavailable",
    label: "條件不足",
    enabled: false,
    disabled_reason: detail.disabled_reason ?? "尚未滿足回報條件",
    payload,
  };
}

function getFeedbackForTask(task) {
  const detail = state.model.task_details?.[task.task_id] ?? {};
  if (task.status === "ready_to_submit") {
    return detail.ready_feedback ?? state.model.feedback_message;
  }
  if (task.status === "completed") {
    return detail.completed_feedback ?? { speaker: state.model.npc?.name, text: "這份委託已完成，仍可查看記錄。" };
  }
  return detail.missing_feedback ?? state.model.feedback_message;
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

function navigateToPrototype(path) {
  window.setTimeout(() => {
    window.location.href = path;
  }, navigationDelayMs);
}

function logSystem(message, options = {}) {
  state.actionLog = [
    {
      time: new Date().toLocaleTimeString("zh-TW", { hour12: false }),
      action_id: options.actionId ?? "fixture_loaded",
      payload: { message, ...(options.payload ?? {}) },
      source: options.source ?? "fixture_loader",
      dispatched: true,
    },
  ];
  renderActionLog();
}

function getSelectableRows() {
  return [...taskListEl.querySelectorAll(".task-row")];
}

function createEmptyState(message) {
  const empty = document.createElement("div");
  empty.className = "empty-state";
  empty.textContent = message;
  return empty;
}

function createList(className, items, renderItem) {
  const list = document.createElement("div");
  list.className = className;
  list.append(...items.map(renderItem));
  return list;
}

function safeJson(value, fallback) {
  try {
    return JSON.parse(value);
  } catch {
    return fallback;
  }
}

function wrapIndex(index, length) {
  return ((index % length) + length) % length;
}

function renderLoadError(error) {
  titleEl.textContent = "Fixture 載入失敗";
  subtitleEl.textContent = "無法讀取 Guild static fixture。";
  taskListEl.replaceChildren();
  storyHintSlotEl.replaceChildren();
  filterRowEl.replaceChildren();
  taskDetailEl.replaceChildren(createEmptyState(error instanceof Error ? error.message : String(error)));
  rewardSummaryEl.replaceChildren();
  conditionListEl.replaceChildren();
  feedbackMessageEl.textContent = "";
  primaryActionEl.textContent = "不可用";
  primaryActionEl.setAttribute("aria-disabled", "true");
}

function renderMaterialList(materials) {
  if (materials.length === 0) {
    const empty = document.createElement("div");
    empty.className = "empty-state";
    empty.textContent = "目前沒有符合工會收購登記的素材。";
    materialSellListEl.replaceChildren(empty);
    return;
  }

  materialSellListEl.replaceChildren(
    ...materials.map((m) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "task-row material-row";
      button.dataset.itemId = m.item_id;
      button.classList.toggle("is-selected", m.item_id === state.selectedMaterialId);
      button.setAttribute("aria-pressed", String(m.item_id === state.selectedMaterialId));

      const copy = document.createElement("span");
      const title = document.createElement("span");
      title.className = "task-title";
      title.textContent = m.title ?? m.item_id;

      const giver = document.createElement("span");
      giver.className = "task-giver";
      giver.textContent = `單價：${m.unit_price}G`;

      copy.append(title, giver);

      const status = document.createElement("span");
      status.className = "status-badge";
      status.dataset.status = "ready_to_submit";
      status.textContent = `x${m.owned_count}`;

      button.append(copy, status);
      button.addEventListener("click", () => {
        state.selectedMaterialId = m.item_id;
        state.sellQuantity = 1;
        pushActionLog({
          action_id: "select_material",
          payload: { item_id: m.item_id },
          source: "material_row",
          dispatched: true,
        });
        render();
      });
      return button;
    })
  );
}

function renderSelectedMaterialContent() {
  const materials = state.model?.sellable_materials ?? [];
  const m = materials.find(x => x.item_id === state.selectedMaterialId);

  if (!m) {
    sellMaterialDetailEl.replaceChildren(createEmptyState("請選擇要出售的素材。"));
    sellRewardSummaryEl.replaceChildren(createEmptyState("沒有金額資料。"));
    sellConfirmContainerEl.replaceChildren(createEmptyState("沒有確認條件。"));
    renderPrimaryAction({
      action_id: "unavailable",
      label: "條件不足",
      enabled: false,
      disabled_reason: "請選擇要出售的素材",
      payload: {},
    });
    return;
  }

  // Ensure quantity is bounded
  if (state.sellQuantity > m.owned_count) {
    state.sellQuantity = m.owned_count;
  }
  if (state.sellQuantity < 1) {
    state.sellQuantity = 1;
  }

  // 1. Material Info & Quantity Selector
  const titleRow = document.createElement("div");
  titleRow.className = "detail-title-row";
  const titleCopy = document.createElement("div");
  const title = document.createElement("h2");
  title.textContent = m.title ?? m.item_id;
  const subtitle = document.createElement("p");
  subtitle.className = "detail-subtitle";
  subtitle.textContent = `單價：${m.unit_price}G / 背包持有：${m.owned_count} 個`;
  titleCopy.append(title, subtitle);

  const status = document.createElement("span");
  status.className = "status-badge";
  status.dataset.status = "ready_to_submit";
  status.textContent = "收購中";
  titleRow.append(titleCopy, status);

  const desc = document.createElement("p");
  desc.className = "detail-description";
  desc.textContent = "由艾爾姆冒險者工會登記收購的探險素材。可用於兌換金幣。";

  const selector = document.createElement("div");
  selector.className = "quantity-selector-container";
  const qLabel = document.createElement("label");
  qLabel.textContent = "出售數量：";

  const controls = document.createElement("div");
  controls.className = "qty-controls";

  const decBtn = document.createElement("button");
  decBtn.type = "button";
  decBtn.className = "qty-btn";
  decBtn.textContent = "-";
  decBtn.addEventListener("click", () => {
    if (state.sellQuantity > 1) {
      state.sellQuantity--;
      render();
    }
  });

  const qtyInput = document.createElement("input");
  qtyInput.type = "number";
  qtyInput.value = state.sellQuantity;
  qtyInput.readOnly = true;

  const incBtn = document.createElement("button");
  incBtn.type = "button";
  incBtn.className = "qty-btn";
  incBtn.textContent = "+";
  incBtn.addEventListener("click", () => {
    if (state.sellQuantity < m.owned_count) {
      state.sellQuantity++;
      render();
    }
  });

  const maxBtn = document.createElement("button");
  maxBtn.type = "button";
  maxBtn.className = "qty-btn max-btn";
  maxBtn.textContent = "MAX";
  maxBtn.addEventListener("click", () => {
    if (state.sellQuantity < m.owned_count) {
      state.sellQuantity = m.owned_count;
      render();
    }
  });

  controls.append(decBtn, qtyInput, incBtn, maxBtn);
  selector.append(qLabel, controls);

  sellMaterialDetailEl.replaceChildren(titleRow, desc, selector);

  // 2. Rewards (Total Gold)
  const totalGold = state.sellQuantity * m.unit_price;
  const rewardList = document.createElement("div");
  rewardList.className = "reward-list";
  const rewardItem = document.createElement("div");
  rewardItem.className = "reward-item";
  const rLabel = document.createElement("strong");
  rLabel.textContent = "預計獲得金幣";
  const rValue = document.createElement("span");
  rValue.style.fontSize = "1.25rem";
  rValue.style.color = "var(--gold)";
  rValue.style.fontWeight = "bold";
  rValue.textContent = `${totalGold}G`;
  rewardItem.append(rLabel, rValue);
  rewardList.append(rewardItem);
  sellRewardSummaryEl.replaceChildren(rewardList);

  // 3. Confirmation Checkbox
  const condList = document.createElement("div");
  condList.className = "condition-list";
  const condRow = document.createElement("div");
  condRow.className = "condition-row";
  condRow.style.gridTemplateColumns = "1fr";

  const cMsg = document.createElement("p");
  cMsg.style.margin = "0 0 8px 0";
  cMsg.style.color = "var(--paper-muted)";
  cMsg.style.fontSize = "0.9rem";
  cMsg.style.lineHeight = "1.45";
  cMsg.textContent = "請確認出售數量與總金額。出售後物資將被工會收購，且該操作無法復原。";

  const cLabel = document.createElement("label");
  cLabel.style.display = "flex";
  cLabel.style.alignItems = "center";
  cLabel.style.gap = "8px";
  cLabel.style.cursor = "pointer";
  cLabel.style.color = "var(--paper)";
  cLabel.style.fontWeight = "bold";

  const cCheckbox = document.createElement("input");
  cCheckbox.type = "checkbox";
  cCheckbox.id = "sell-confirm-checkbox";
  cCheckbox.style.width = "18px";
  cCheckbox.style.height = "18px";
  cCheckbox.style.cursor = "pointer";

  cLabel.append(cCheckbox, document.createTextNode("我已確認出售數量與金額"));
  condRow.append(cMsg, cLabel);
  condList.append(condRow);
  sellConfirmContainerEl.replaceChildren(condList);

  // Checkbox listener to toggle primary button state without a full redraw
  cCheckbox.addEventListener("change", () => {
    updateSellPrimaryButtonState(cCheckbox.checked, m.item_id, state.sellQuantity);
  });

  // Initialize button state
  updateSellPrimaryButtonState(false, m.item_id, state.sellQuantity);
}

function updateSellPrimaryButtonState(confirmed, itemId, qty) {
  if (confirmed) {
    renderPrimaryAction({
      action_id: "sell_guild_material",
      label: "確認出售",
      enabled: true,
      payload: { item_id: itemId, quantity: qty, confirm: true },
    });
  } else {
    renderPrimaryAction({
      action_id: "sell_guild_material",
      label: "確認出售",
      enabled: false,
      disabled_reason: "請勾選確認框以出售素材",
      payload: { item_id: itemId, quantity: qty, confirm: false },
    });
  }
}

})();