import { runtimeClient } from "../shared/runtime-client.js";

const fixtureSelect = document.querySelector("#fixture-select");
const titleEl = document.querySelector("#screen-title");
const subtitleEl = document.querySelector("#screen-subtitle");
const resourceStripEl = document.querySelector("#resource-strip");
const categoryTabsEl = document.querySelector("#category-tabs");
const recipeListEl = document.querySelector("#recipe-list");
const recipeDetailEl = document.querySelector("#recipe-detail");
const outputSummaryEl = document.querySelector("#output-summary");
const detailStatusEl = document.querySelector("#detail-status");
const requirementListEl = document.querySelector("#requirement-list");
const npcPortraitEl = document.querySelector("#npc-portrait");
const npcNameEl = document.querySelector("#npc-name");
const npcRoleEl = document.querySelector("#npc-role");
const feedbackMessageEl = document.querySelector("#feedback-message");
const primaryActionEl = document.querySelector("#primary-action");
const backActionEl = document.querySelector("#back-action");
const actionLogEl = document.querySelector("#action-log");
const clearLogEl = document.querySelector("#clear-log");
const shellEl = document.querySelector(".synthesis-shell");

const state = {
  model: null,
  selectedCategoryId: null,
  selectedRecipeId: null,
  actionLog: [],
};

const townHubRoute = "../town_hub/index.html";
const navigationDelayMs = 120;

if (runtimeClient.isLiveMode()) {
  const switcher = document.querySelector(".fixture-switcher");
  if (switcher) {
    switcher.style.display = "none";
  }
}

fixtureSelect.addEventListener("change", () => {
  loadFixture(fixtureSelect.value);
});

recipeListEl.addEventListener("keydown", (event) => {
  if (!["ArrowUp", "ArrowDown"].includes(event.key)) {
    return;
  }

  const rows = getRecipeButtons();
  const currentIndex = rows.indexOf(document.activeElement);
  if (currentIndex < 0) {
    return;
  }

  event.preventDefault();
  const delta = event.key === "ArrowDown" ? 1 : -1;
  rows[wrapIndex(currentIndex + delta, rows.length)]?.focus();
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
  if (runtimeClient.isLiveMode()) {
    runtimeClient.dispatchAction("synthesis_screen", "back_to_town_hub", {})
      .then((result) => {
        window.setTimeout(() => {
          window.location.href = runtimeClient.nextRoute(result, '../town_hub/index.html');
        }, navigationDelayMs);
      })
      .catch((err) => {
        console.error(err);
        window.location.href = '../town_hub/index.html?mode=live';
      });
  } else {
    navigateToPrototype(townHubRoute);
  }
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
  await loadStaticFallback(path);
}

async function loadLiveScreen() {
  shellEl.dataset.loadState = "loading";
  try {
    const model = await runtimeClient.getScreen("synthesis_screen");
    state.model = model;
    state.selectedCategoryId = model.selected_category_id ?? model.category_tabs?.[0]?.id ?? "all";
    state.selectedRecipeId = model.selected_recipe_id ?? getVisibleRecipeRows()[0]?.recipe_id ?? null;
    state.actionLog = [];
    ensureSelectionVisible();
    render();
    pushActionLog({
      action_id: "live_screen_loaded",
      payload: { mode: "live", screen_id: "synthesis_screen" },
      source: "live_loader",
      dispatched: true,
    });
    shellEl.dataset.loadState = "ready";
  } catch (error) {
    console.error(error);
    const reason = runtimeClient.errorMessage(error);
    pushActionLog({
      action_id: "live_bridge_unavailable",
      payload: { reason },
      source: "live_loader",
      dispatched: false,
      reason: "fallback_to_fixture",
    });
    await loadStaticFallback(fixtureSelect.value);
  }
}

async function loadStaticFallback(path) {
  shellEl.dataset.loadState = "loading";
  try {
    const response = await fetch(path, { cache: "no-store" });
    if (!response.ok) {
      throw new Error(`Fixture request failed: ${response.status}`);
    }
    const model = await response.json();
    state.model = model;
    state.selectedCategoryId = model.selected_category_id ?? model.category_tabs?.[0]?.id ?? "all";
    state.selectedRecipeId = model.selected_recipe_id ?? getVisibleRecipeRows()[0]?.recipe_id ?? null;
    state.actionLog = [];
    ensureSelectionVisible();
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
  npcNameEl.textContent = model.npc?.name ?? "";
  npcRoleEl.textContent = model.npc?.role ?? "";
  npcPortraitEl.dataset.npcId = model.npc?.id ?? "";
  renderResources(model.resource_strip ?? []);
  renderCategories(model.category_tabs ?? []);
  renderRecipeList(getVisibleRecipeRows());
  ensureSelectionVisible();
  renderSelectedRecipe();
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

function renderCategories(categories) {
  categoryTabsEl.replaceChildren(
    ...categories.map((category) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "category-tab";
      button.classList.toggle("is-selected", category.id === state.selectedCategoryId);
      button.setAttribute("aria-pressed", String(category.id === state.selectedCategoryId));
      button.setAttribute("aria-disabled", String(!category.enabled));

      const label = document.createElement("strong");
      label.textContent = category.label ?? category.id;

      const count = document.createElement("span");
      count.textContent = `${category.count ?? 0} 張`;

      button.append(label, count);
      button.addEventListener("click", () => selectCategory(category));
      return button;
    }),
  );
}

function renderRecipeList(rows) {
  if (rows.length === 0) {
    recipeListEl.replaceChildren(createEmptyState("此分類目前沒有可用配方。"));
    return;
  }

  recipeListEl.replaceChildren(
    ...rows.map((row) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "recipe-row";
      button.dataset.recipeId = row.recipe_id;
      button.classList.toggle("is-selected", row.recipe_id === state.selectedRecipeId);
      button.setAttribute("aria-pressed", String(row.recipe_id === state.selectedRecipeId));

      const copy = document.createElement("span");
      copy.className = "recipe-row-copy";

      const title = document.createElement("span");
      title.className = "recipe-title";
      title.textContent = row.title ?? "";

      const summary = document.createElement("span");
      summary.className = "recipe-summary";
      summary.textContent = `${row.output_summary ?? ""} / ${row.gold ?? 0}G`;

      const meta = document.createElement("span");
      meta.className = "recipe-meta";
      meta.textContent = `持有：${row.owned_summary ?? "無"} / 最多 ${row.max_count ?? 0} 次`;

      copy.append(title, summary, meta);

      const status = document.createElement("span");
      status.className = "status-badge";
      status.dataset.status = row.status ?? "";
      status.textContent = row.status_label ?? row.status ?? "";

      button.append(copy, status);
      button.addEventListener("focus", () => selectRecipe(row.recipe_id, false));
      button.addEventListener("click", () => selectRecipe(row.recipe_id, true));
      return button;
    }),
  );
}

function renderSelectedRecipe() {
  const row = getSelectedRecipe();
  if (!row) {
    recipeDetailEl.replaceChildren(createEmptyState("請先選擇配方。"));
    outputSummaryEl.replaceChildren();
    requirementListEl.replaceChildren();
    renderPrimaryAction({
      action_id: "craft_recipe",
      label: "不可用",
      enabled: false,
      disabled_reason: "請先選擇配方",
      payload: {},
    });
    renderFeedback(state.model.empty_state?.message ?? "目前沒有可顯示的配方。");
    return;
  }

  const detail = state.model.recipe_details?.[row.recipe_id] ?? {};
  detailStatusEl.dataset.status = row.status ?? "";
  detailStatusEl.textContent = row.status_label ?? "";

  const title = document.createElement("h2");
  title.textContent = detail.title ?? row.title ?? "";

  const subtitle = document.createElement("p");
  subtitle.className = "detail-subtitle";
  subtitle.textContent = `${row.category_label ?? row.category ?? ""} / ${row.status_label ?? ""}`;

  const description = document.createElement("p");
  description.className = "detail-description";
  description.textContent = detail.description ?? "";

  const effect = document.createElement("p");
  effect.className = "detail-effect";
  effect.textContent = `效果：${detail.effect ?? "無"}`;

  const primaryAction = detail.primary_action ?? row.primary_action;
  const disabledReason = primaryAction?.enabled === false ? primaryAction.disabled_reason : "";
  const reason = document.createElement("p");
  reason.className = "detail-disabled-reason";
  reason.textContent = disabledReason ? `目前不可合成：${disabledReason}` : "";

  recipeDetailEl.replaceChildren(title, subtitle, description, effect);
  if (disabledReason) {
    recipeDetailEl.append(reason);
  }
  renderOutputSummary(detail.outputs ?? []);
  renderRequirements(state.model.requirement_rows?.[row.recipe_id] ?? []);
  renderPrimaryAction(primaryAction);
  renderFeedback(getFeedbackForRecipe(row));
}

function renderOutputSummary(outputs) {
  if (outputs.length === 0) {
    outputSummaryEl.replaceChildren(createEmptyState("沒有產出資料。"));
    return;
  }

  outputSummaryEl.replaceChildren(
    ...outputs.map((output) => {
      const el = document.createElement("div");
      el.className = "output-pill";
      const label = document.createElement("strong");
      label.textContent = output.label ?? output.item_id ?? "";
      const value = document.createElement("span");
      value.textContent = `x${output.quantity ?? 1}`;
      el.append(label, value);
      return el;
    }),
  );
}

function renderRequirements(rows) {
  if (rows.length === 0) {
    requirementListEl.replaceChildren(createEmptyState("沒有需求資料。"));
    return;
  }

  requirementListEl.replaceChildren(
    ...rows.map((row) => {
      const el = document.createElement("div");
      el.className = "requirement-row";

      const marker = document.createElement("span");
      marker.className = "requirement-marker";
      marker.dataset.status = row.status ?? "";
      marker.textContent = row.icon_label ?? "REQ";

      const copy = document.createElement("span");
      copy.className = "requirement-copy";

      const label = document.createElement("strong");
      label.textContent = row.label ?? "";

      const values = document.createElement("span");
      values.textContent = `${row.required_value ?? ""} / 目前：${row.current_value ?? ""}`;

      copy.append(label, values);

      const status = document.createElement("span");
      status.className = "requirement-status";
      status.dataset.status = row.status ?? "";
      status.textContent = row.status_label ?? row.status ?? "";
      status.title = row.disabled_reason ?? "";

      el.append(marker, copy, status);
      return el;
    }),
  );
}

function renderPrimaryAction(action) {
  const normalized = action ?? {
    action_id: "craft_recipe",
    label: "不可用",
    enabled: false,
    disabled_reason: "沒有可執行的合成操作",
    payload: {},
  };
  primaryActionEl.textContent = normalized.label ?? normalized.action_id ?? "合成";
  primaryActionEl.dataset.actionId = normalized.action_id ?? "craft_recipe";
  primaryActionEl.dataset.payload = JSON.stringify(normalized.payload ?? {});
  primaryActionEl.dataset.disabledReason = normalized.disabled_reason ?? "";
  primaryActionEl.dataset.resultMessage = normalized.result_message ?? "";
  primaryActionEl.setAttribute("aria-disabled", String(!normalized.enabled));
}

function renderFeedback(message) {
  const feedback = typeof message === "string" ? { text: message } : message;
  feedbackMessageEl.textContent = feedback?.speaker ? `${feedback.speaker}：${feedback.text}` : (feedback?.text ?? "");
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

function selectCategory(category) {
  if (!category.enabled) {
    pushActionLog({
      action_id: "select_category",
      payload: { category_id: category.id },
      source: "category_tab",
      dispatched: false,
      reason: category.disabled_reason ?? "disabled",
    });
    return;
  }

  state.selectedCategoryId = category.id;
  state.selectedRecipeId = getVisibleRecipeRows()[0]?.recipe_id ?? null;
  pushActionLog({
    action_id: "select_category",
    payload: { category_id: category.id },
    source: "category_tab",
    dispatched: true,
  });
  render();
}

function selectRecipe(recipeId, shouldLog) {
  state.selectedRecipeId = recipeId;
  if (shouldLog) {
    pushActionLog({
      action_id: "select_recipe",
      payload: { recipe_id: recipeId },
      source: "recipe_row",
      dispatched: true,
    });
  }
  render();
}

function activatePrimaryAction() {
  const actionId = primaryActionEl.dataset.actionId ?? "craft_recipe";
  const payload = safeJson(primaryActionEl.dataset.payload, {});
  const disabledReason = primaryActionEl.dataset.disabledReason;
  const resultMessage = primaryActionEl.dataset.resultMessage;
  const enabled = primaryActionEl.getAttribute("aria-disabled") !== "true";

  if (!enabled) {
    pushActionLog({
      action_id: actionId,
      payload,
      source: "primary_action",
      dispatched: false,
      reason: disabledReason || "disabled",
    });
    renderFeedback({ speaker: state.model.npc?.name, text: disabledReason || "目前無法合成。" });
    return;
  }

  pushActionLog({
    action_id: actionId,
    payload,
    source: "primary_action",
    dispatched: true,
  });

  if (runtimeClient.isLiveMode()) {
    dispatchRuntimeAction(actionId, payload);
    return;
  }

  renderFeedback({
    speaker: state.model.npc?.name,
    text: resultMessage || "已送出 UIAction；static prototype 不會扣除素材或產出物品。",
  });
}

async function dispatchRuntimeAction(actionId, payload) {
  try {
    const result = await runtimeClient.dispatchAction("synthesis_screen", actionId, payload);
    if (result.screen_model) {
      state.model = result.screen_model;
      state.selectedRecipeId = result.screen_model.selected_recipe_id ?? state.selectedRecipeId;
      render();
    }
    if (result.message) {
      renderFeedback({
        speaker: state.model.npc?.name,
        text: result.message,
      });
      pushActionLog({
        action_id: "runtime_feedback",
        payload: { message: result.message },
        source: "primary_action",
        dispatched: true,
      });
    }
  } catch (error) {
    const reason = runtimeClient.errorMessage(error);
    pushActionLog({
      action_id: actionId,
      payload,
      source: "primary_action",
      dispatched: false,
      reason: reason,
    });
    renderFeedback({
      speaker: state.model.npc?.name,
      text: reason || "合成失敗。",
    });
  }
}

function getVisibleRecipeRows() {
  const rows = state.model?.recipe_rows ?? [];
  if (state.selectedCategoryId === "all") {
    return rows;
  }
  return rows.filter((row) => row.category === state.selectedCategoryId);
}

function ensureSelectionVisible() {
  const rows = getVisibleRecipeRows();
  if (!rows.some((row) => row.recipe_id === state.selectedRecipeId)) {
    state.selectedRecipeId = rows[0]?.recipe_id ?? null;
  }
}

function getSelectedRecipe() {
  return state.model?.recipe_rows?.find((row) => row.recipe_id === state.selectedRecipeId) ?? null;
}

function getFeedbackForRecipe(row) {
  const detail = state.model.recipe_details?.[row.recipe_id] ?? {};
  if (row.status === "craftable") {
    return detail.ready_feedback ?? state.model.feedback_message;
  }
  return detail.blocked_feedback ?? state.model.feedback_message;
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

function navigateToPrototype(route) {
  window.setTimeout(() => {
    window.location.href = route;
  }, navigationDelayMs);
}

function getRecipeButtons() {
  return [...recipeListEl.querySelectorAll(".recipe-row")];
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

function wrapIndex(index, length) {
  return ((index % length) + length) % length;
}

function renderLoadError(error) {
  titleEl.textContent = "Fixture 載入失敗";
  subtitleEl.textContent = "無法讀取 Synthesis static fixture。";
  resourceStripEl.replaceChildren();
  categoryTabsEl.replaceChildren();
  recipeListEl.replaceChildren();
  recipeDetailEl.replaceChildren();
  outputSummaryEl.replaceChildren();
  requirementListEl.replaceChildren();
  detailStatusEl.textContent = "";
  renderFeedback("請確認 fixtures 路徑與 JSON 格式。");

  const errorEl = document.createElement("div");
  errorEl.className = "load-error";
  errorEl.textContent = error instanceof Error ? error.message : String(error);
  recipeListEl.append(errorEl);
}
