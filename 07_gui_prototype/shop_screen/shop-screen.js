import { applyFacilityBackground } from "../shared/facility-backgrounds.js";
import { runtimeClient } from "../shared/runtime-client.js";

const fixtureSelect = document.querySelector("#fixture-select");
const titleEl = document.querySelector("#screen-title");
const subtitleEl = document.querySelector("#screen-subtitle");
const resourceStripEl = document.querySelector("#resource-strip");
const categoryTabsEl = document.querySelector("#category-tabs");
const itemListEl = document.querySelector("#item-list");
const itemDetailEl = document.querySelector("#item-detail");
const detailStatusEl = document.querySelector("#detail-status");
const requirementListEl = document.querySelector("#requirement-list");
const npcPortraitEl = document.querySelector("#npc-portrait");
const npcNameEl = document.querySelector("#npc-name");
const npcRoleEl = document.querySelector("#npc-role");
const feedbackSpeakerEl = document.querySelector("#feedback-speaker");
const feedbackMessageEl = document.querySelector("#feedback-message");
const primaryActionEl = document.querySelector("#primary-action");
const backActionEl = document.querySelector("#back-action");
const actionLogEl = document.querySelector("#action-log");
const clearLogEl = document.querySelector("#clear-log");
const shellEl = document.querySelector(".shop-shell");

const state = {
  model: null,
  selectedCategoryId: null,
  selectedItemId: null,
  actionLog: [],
};

const townHubRoute = "../town_hub/index.html";
const navigationDelayMs = 120;

const shopBackgroundByRegion = {
  fire: "./bg-npc.jpg",
  ice: "./assets/ice-travel-shop-background-with-terry-overscan-master-v03.png",
  earth: "./assets/earth-travel-shop-background-with-rabi-cropped-candidate-v01.png",
  thunder: "./assets/thunder-travel-shop-background-with-rabi-candidate-v01.png",
  final: "./assets/final-travel-shop-with-rabi-candidate-v01.png",
};

fixtureSelect.addEventListener("change", () => {
  loadFixture(fixtureSelect.value);
});

itemListEl.addEventListener("keydown", (event) => {
  if (!["ArrowUp", "ArrowDown"].includes(event.key)) {
    return;
  }

  const rows = getItemButtons();
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
    state.selectedCategoryId = model.selected_category_id ?? model.category_tabs?.[0]?.id ?? "all";
    state.selectedItemId = model.selected_item_id ?? getVisibleItemRows()[0]?.item_id ?? null;
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

function render() {
  const { model } = state;
  applyFacilityBackground({ model, shell: shellEl, backgrounds: shopBackgroundByRegion });
  titleEl.textContent = cleanTitle(model.title);
  subtitleEl.textContent = model.subtitle ?? "";
  npcNameEl.textContent = model.npc?.name ?? "";
  npcRoleEl.textContent = model.npc?.role ?? "";
  npcPortraitEl.dataset.npcPlaceholder = model.npc?.portrait_placeholder ?? "NPC";
  
  if (model.resource_strip && resourceStripEl) {
    resourceStripEl.hidden = false;
    renderResources(model.resource_strip);
  } else if (resourceStripEl) {
    resourceStripEl.hidden = true;
  }

  renderCategories(model.category_tabs ?? []);
  renderItemList(getVisibleItemRows());
  ensureSelectionVisible();
  renderSelectedItem();
  renderActionLog();
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

      const icon = document.createElement("span");
      icon.className = "category-tab-icon";
      icon.setAttribute("aria-hidden", "true");
      const iconMap = {
        all: "❖",
        consumables: "🧪",
        tactical: "⚔",
        accessories: "💍"
      };
      icon.textContent = iconMap[category.id] ?? "📦";

      const label = document.createElement("strong");
      label.textContent = category.label ?? category.id;

      const count = document.createElement("span");
      count.className = "category-tab-count";
      count.textContent = `(${category.count ?? 0})`;

      button.append(icon, label, count);
      button.addEventListener("click", () => selectCategory(category));
      return button;
    }),
  );
}

function renderItemList(rows) {
  if (rows.length === 0) {
    itemListEl.replaceChildren(createEmptyState("此分類目前沒有販售商品。"));
    return;
  }

  itemListEl.replaceChildren(
    ...rows.map((row) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "item-row";
      button.dataset.itemId = row.item_id;
      button.classList.toggle("is-selected", row.item_id === state.selectedItemId);
      button.setAttribute("aria-pressed", String(row.item_id === state.selectedItemId));
      
      if (!row.enabled) {
        button.setAttribute("aria-disabled", "true");
      }

      const copy = document.createElement("span");
      copy.className = "item-row-copy";

      const title = document.createElement("span");
      title.className = "item-title";
      title.textContent = row.title ?? "";

      const summary = document.createElement("span");
      summary.className = "item-summary";
      summary.textContent = `${row.summary ?? ""} / ${row.price ?? 0}G`;

      const meta = document.createElement("span");
      meta.className = "item-meta";
      meta.textContent = `持有：${row.owned_count ?? 0} | ${row.stock_label ?? ""}`;

      copy.append(title, summary, meta);

      const status = document.createElement("span");
      status.className = "status-badge";
      status.dataset.status = row.status ?? "";
      status.textContent = row.enabled ? "可購買" : (row.disabled_reason ?? "不可購買");

      button.append(copy, status);
      button.addEventListener("focus", () => selectItem(row.item_id, false));
      button.addEventListener("click", () => selectItem(row.item_id, true));
      return button;
    }),
  );
}

function renderSelectedItem() {
  const row = getSelectedItem();
  if (!row) {
    itemDetailEl.replaceChildren(createEmptyState("請先選擇商品。"));
    requirementListEl.replaceChildren();
    renderPrimaryAction({
      action_id: "buy_item",
      label: "不可用",
      enabled: false,
      disabled_reason: "請先選擇商品",
      payload: {},
    });
    renderFeedback(state.model.npc?.name ?? "特里", "目前沒有選中的商品。");
    return;
  }

  const detail = state.model.item_details?.[row.item_id] ?? {};
  detailStatusEl.dataset.status = row.status ?? "";
  detailStatusEl.textContent = row.enabled ? "可購買" : (row.disabled_reason ?? "受限");

  const title = document.createElement("h2");
  title.textContent = detail.title ?? row.title ?? "";

  const subtitle = document.createElement("p");
  subtitle.className = "detail-subtitle";
  subtitle.textContent = `${detail.category_label ?? ""} / 持有：${detail.owned_count ?? 0}`;

  const description = document.createElement("p");
  description.className = "detail-description";
  description.textContent = detail.description ?? "";

  const effect = document.createElement("p");
  effect.className = "detail-effect";
  effect.textContent = `效果：${detail.effect_summary ?? "無"}`;

  const context = document.createElement("p");
  context.className = "detail-context";
  context.textContent = `用途：${detail.use_context ?? "無"}`;

  const primaryAction = state.model.primary_actions?.[row.item_id] ?? {};
  const disabledReason = row.enabled === false ? row.disabled_reason : "";
  const reason = document.createElement("p");
  reason.className = "detail-disabled-reason";
  reason.textContent = disabledReason ? `無法購買理由：${disabledReason}` : "";

  itemDetailEl.replaceChildren(title, subtitle, description, effect, context);
  if (disabledReason) {
    itemDetailEl.append(reason);
  }
  
  renderRequirements(state.model.requirement_rows?.[row.item_id] ?? []);
  renderPrimaryAction(primaryAction);
  renderFeedback(state.model.npc?.name ?? "特里", getFeedbackForItem(row));
}

function renderRequirements(rows) {
  if (rows.length === 0) {
    requirementListEl.replaceChildren(createEmptyState("沒有購買限制資料。"));
    return;
  }

  requirementListEl.replaceChildren(
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
      values.textContent = `要求：${row.required_value ?? ""} / 目前：${row.current_value ?? ""}`;

      copy.append(label, values);

      const status = document.createElement("span");
      status.className = "requirement-status";
      status.dataset.status = row.status ?? "";
      status.textContent = row.status === "met" ? "已滿足" : (row.disabled_reason ?? "未滿足");
      status.title = row.disabled_reason ?? "";

      el.append(marker, copy, status);
      return el;
    }),
  );
}
function renderPrimaryAction(action) {
  const normalized = action ?? {
    action_id: "buy_item",
    label: "不可用",
    enabled: false,
    disabled_reason: "沒有可執行的操作",
    payload: {},
  };
  const label = normalized.label ?? "購買商品";
  primaryActionEl.innerHTML = `
    <svg class="btn-icon-svg" viewBox="0 0 24 24"><path d="M7 18c-1.1 0-1.99.9-1.99 2S5.9 22 7 22s2-.9 2-2-.9-2-2-2zM1 2v2h2l3.6 7.59-1.35 2.45c-.16.28-.25.61-.25.96 0 1.1.9 2 2 2h12v-2H7.42c-.14 0-.25-.11-.25-.25l.03-.12.9-1.63h7.45c.75 0 1.41-.41 1.75-1.03l3.58-6.49c.08-.14.12-.31.12-.48 0-.55-.45-1-1-1H5.21l-.94-2H1zm16 16c-1.1 0-1.99.9-1.99 2s.89 2 1.99 2 2-.9 2-2-.9-2-2-2z" fill="currentColor"/></svg>
    <span class="btn-text">${label}</span>
  `;
  primaryActionEl.dataset.actionId = normalized.action_id ?? "buy_item";
  primaryActionEl.dataset.payload = JSON.stringify(normalized.payload ?? {});
  primaryActionEl.dataset.disabledReason = normalized.disabled_reason ?? "";
  primaryActionEl.dataset.resultMessage = normalized.result_message ?? "";
  primaryActionEl.setAttribute("aria-disabled", String(!normalized.enabled));
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
  state.selectedItemId = getVisibleItemRows()[0]?.item_id ?? null;
  pushActionLog({
    action_id: "select_category",
    payload: { category_id: category.id },
    source: "category_tab",
    dispatched: true,
  });
  render();
}

function selectItem(itemId, shouldLog) {
  state.selectedItemId = itemId;
  if (shouldLog) {
    pushActionLog({
      action_id: "select_item",
      payload: { item_id: itemId },
      source: "item_row",
      dispatched: true,
    });
  }
  render();
}

function activatePrimaryAction() {
  const actionId = primaryActionEl.dataset.actionId ?? "buy_item";
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
    renderFeedback(state.model.npc?.name ?? "特里", disabledReason ? `「抱歉，目前不能購買：${disabledReason}。」` : "「抱歉，這個商品現在無法售賣。」");
    return;
  }

  if (runtimeClient.isLiveMode()) {
    pushActionLog({
      action_id: actionId,
      payload,
      source: "primary_action",
      dispatched: true,
    });
    runtimeClient.dispatchAction("shop_screen", actionId, payload)
      .then((result) => {
        shellEl.dataset.runtimeStatus = result.status ?? "success";
        if (result.screen_model) {
          state.model = result.screen_model;
          ensureSelectionVisible();
          render();
        }
        if (result.message) {
          const npcMsg = result.screen_model?.feedback_message?.text || result.message;
          renderFeedback(state.model.npc?.name ?? "特里", npcMsg);
        }
      })
      .catch((error) => {
        const reason = runtimeClient.errorMessage(error);
        shellEl.dataset.runtimeStatus = error?.runtimeStatus ?? "error";
        pushActionLog({
          action_id: actionId,
          payload,
          source: "primary_action",
          dispatched: false,
          reason,
        });
        renderFeedback(state.model.npc?.name ?? "特里", `「抱歉，購買失敗：${reason}。」`);
      });
    return;
  }

  pushActionLog({
    action_id: actionId,
    payload,
    source: "primary_action",
    dispatched: true,
  });
  renderFeedback(state.model.npc?.name ?? "特里", resultMessage || "「非常感謝您的惠顧！Static Prototype 不會實際扣減金幣與增加物品。」");
}

function getVisibleItemRows() {
  const rows = state.model?.list_rows ?? [];
  if (state.selectedCategoryId === "all") {
    return rows;
  }
  return rows.filter((row) => row.category === state.selectedCategoryId);
}

function ensureSelectionVisible() {
  const rows = getVisibleItemRows();
  if (!rows.some((row) => row.item_id === state.selectedItemId)) {
    state.selectedItemId = rows[0]?.item_id ?? null;
  }
}

function getSelectedItem() {
  return state.model?.list_rows?.find((row) => row.item_id === state.selectedItemId) ?? null;
}

function getFeedbackForItem(row) {
  if (row.enabled) {
    return `「這件 ${row.title} 的成色非常好，售價 ${row.price}G，決定好就點擊右下角購買吧！」`;
  }
  return `「這件商品現在無法提供喔。原因：${row.disabled_reason ?? "未滿足限制"}。」`;
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

function getItemButtons() {
  return [...itemListEl.querySelectorAll(".item-row")];
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
  subtitleEl.textContent = "無法讀取 Shop static fixture。";
  categoryTabsEl.replaceChildren();
  itemListEl.replaceChildren();
  itemDetailEl.replaceChildren();
  requirementListEl.replaceChildren();
  detailStatusEl.textContent = "";
  renderFeedback("系統", "請確認 fixtures 路徑與 JSON 格式。");

  const errorEl = document.createElement("div");
  errorEl.className = "load-error";
  errorEl.textContent = error instanceof Error ? error.message : String(error);
  itemListEl.append(errorEl);
}

async function loadLiveScreen() {
  shellEl.dataset.loadState = "loading";
  try {
    const model = await runtimeClient.getScreen("shop_screen");
    state.model = model;
    state.selectedCategoryId = model.selected_category_id ?? model.category_tabs?.[0]?.id ?? "all";
    state.selectedItemId = model.selected_item_id ?? getVisibleItemRows()[0]?.item_id ?? null;
    state.actionLog = [];
    ensureSelectionVisible();
    render();
    logSystem("live runtime screen loaded", {
      actionId: "live_screen_loaded",
      source: "live_loader",
      payload: { mode: "live", screen_id: "shop_screen" },
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
    state.selectedCategoryId = model.selected_category_id ?? model.category_tabs?.[0]?.id ?? "all";
    state.selectedItemId = model.selected_item_id ?? getVisibleItemRows()[0]?.item_id ?? null;
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
  const payload = { from: "shop_screen" };
  pushActionLog({
    action_id: "back_to_town_hub",
    payload,
    source: "secondary_action",
    dispatched: true,
  });
  try {
    const result = await runtimeClient.dispatchAction("shop_screen", "back_to_town_hub", payload);
    shellEl.dataset.runtimeStatus = result.status ?? "success";
    window.setTimeout(() => {
      window.location.href = runtimeClient.nextRoute(result, townHubRoute);
    }, navigationDelayMs);
  } catch (error) {
    const reason = runtimeClient.errorMessage(error);
    shellEl.dataset.runtimeStatus = error?.runtimeStatus ?? "error";
    renderFeedback(state.model.npc?.name ?? "特里", reason);
    pushActionLog({
      action_id: "back_to_town_hub",
      payload,
      source: "secondary_action",
      dispatched: false,
      reason,
    });
  }
}

function renderResources(items) {
  if (!resourceStripEl) return;
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
