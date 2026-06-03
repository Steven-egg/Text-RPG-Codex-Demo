import { runtimeClient } from "../shared/runtime-client.js";

const fixtureSelect = document.querySelector("#fixture-select");
const shellEl = document.querySelector(".world-map-shell");
const menuToggleEl = document.querySelector("#menu-toggle");
const closeMenuEl = document.querySelector("#close-menu");
const closeDetailEl = document.querySelector("#close-detail");
const drawerBackdropEl = document.querySelector("#drawer-backdrop");
const menuDrawerEl = document.querySelector("#menu-drawer");
const detailPanelEl = document.querySelector(".location-detail-panel");
const menuActionsEl = document.querySelector("#menu-actions");
const drawerPlayerSummaryEl = document.querySelector("#drawer-player-summary");
const heroTitleEl = document.querySelector("#hero-title");
const heroMetaEl = document.querySelector("#hero-meta");
const resourceStripEl = document.querySelector("#resource-strip");
const routeLayerEl = document.querySelector("#route-layer");
const locationLayerEl = document.querySelector("#location-layer");
const locationTitleEl = document.querySelector("#location-title");
const locationFavoriteEl = document.querySelector("#location-favorite");
const locationPreviewEl = document.querySelector("#location-preview");
const locationDescriptionEl = document.querySelector("#location-description");
const locationStatsEl = document.querySelector("#location-stats");
const feedbackMessageEl = document.querySelector("#feedback-message");
const confirmActionEl = document.querySelector("#confirm-action");
const actionLogEl = document.querySelector("#action-log");
const clearLogEl = document.querySelector("#clear-log");

const state = {
  model: null,
  selectedLocationId: null,
  actionLog: [],
};

const staticActionRoutes = {
  back_to_town_hub: "../town_hub/index.html",
  back_to_start_screen: "../start_screen/index.html",
  confirm_travel: "../dungeon_exploration/index.html",
};
const liveShellOnlyActions = new Set(["open_settings"]);
const navigationDelayMs = 120;

let utilityPanelEl = null;
let utilityTitleEl = null;
let utilityPanelLabelEl = null;
let utilityContentEl = null;
let closeUtilityEl = null;
let utilityBackActionEl = null;

fixtureSelect.addEventListener("change", () => {
  loadFixture(fixtureSelect.value);
});

menuToggleEl.addEventListener("click", () => {
  setMenuOpen(shellEl.dataset.menuOpen !== "true", true);
});

closeMenuEl.addEventListener("click", () => {
  setMenuOpen(false, true);
});

closeDetailEl.addEventListener("click", () => {
  setDetailOpen(false);
});

document.addEventListener("keydown", (event) => {
  if (event.key !== "Escape") {
    return;
  }

  if (shellEl.dataset.menuOpen === "true") {
    setMenuOpen(false, true);
    return;
  }

  if (shellEl.dataset.detailOpen === "true") {
    setDetailOpen(false);
    return;
  }

  if (shellEl.dataset.utilityOpen === "true") {
    setUtilityOpen(false);
  }
});

drawerBackdropEl.addEventListener("click", () => {
  setMenuOpen(false, true);
});

confirmActionEl.addEventListener("click", () => {
  activateStoredAction(confirmActionEl, "primary_action");
});

clearLogEl.addEventListener("click", () => {
  state.actionLog = [];
  renderActionLog();
});

initUtilityPanel();
loadFixture(fixtureSelect.value);

async function loadFixture(path) {
  if (runtimeClient.isLiveMode()) {
    await loadLiveScreen(path);
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
    state.selectedLocationId = null;
    state.actionLog = [];
    setMenuOpen(false, false);
    setDetailOpen(false);
    render();
    logSystem(`loaded ${path}`);
    shellEl.dataset.loadState = "ready";
  } catch (error) {
    renderLoadError(error);
    shellEl.dataset.loadState = "error";
  }
}

async function loadLiveScreen(path) {
  shellEl.dataset.loadState = "loading";
  try {
    const model = await runtimeClient.getScreen("world_map");
    state.model = model;
    state.selectedLocationId = model.selected_location_id ?? model.locations?.[0]?.location_id ?? null;
    state.actionLog = [];
    setMenuOpen(false, false);
    setDetailOpen(false);
    render();
    logSystem("live runtime screen loaded", {
      actionId: "live_screen_loaded",
      source: "live_loader",
      payload: { mode: "live", screen_id: "world_map" },
    });
    shellEl.dataset.loadState = "ready";
  } catch (error) {
    await loadStaticFallback(path, error);
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
    state.selectedLocationId = model.selected_location_id ?? model.locations?.[0]?.location_id ?? null;
    state.actionLog = [];
    setMenuOpen(false, false);
    setDetailOpen(false);
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
  renderPlayer(model.player);
  renderMenu(model.menu_actions ?? []);
  renderRoutes(model.route_segments ?? []);
  renderLocations(model.locations ?? []);
  renderSelectedLocation();
  renderActionLog();
}

function renderPlayer(player = {}) {
  heroTitleEl.textContent = player.name ?? "";
  heroMetaEl.textContent = `${player.class_label ?? ""} ${player.level_label ?? ""}`.trim();

  const resources = [
    { id: "hp", label: player.hp?.label ?? "HP", percent: player.hp?.percent ?? 0, tone: "hp" },
    { id: "mp", label: player.mp?.label ?? "MP", percent: player.mp?.percent ?? 0, tone: "mp" },
    { id: "gold", label: player.gold_label ?? "0G", percent: null, tone: "gold" },
  ];

  resourceStripEl.replaceChildren(
    ...resources.map((resource) => {
      const item = document.createElement("div");
      item.className = "resource-item";
      item.dataset.tone = resource.tone;

      const label = document.createElement("span");
      label.className = "resource-label";
      label.textContent = resource.label;
      item.append(label);

      if (resource.percent != null) {
        const meter = document.createElement("span");
        meter.className = "resource-meter";
        meter.setAttribute("aria-hidden", "true");
        meter.style.setProperty("--meter-value", `${Math.max(0, Math.min(100, resource.percent))}%`);

        const fill = document.createElement("span");
        meter.append(fill);
        item.append(meter);
      }

      return item;
    }),
  );

  drawerPlayerSummaryEl.replaceChildren(
    createDrawerPlayerRow("角色", `${player.name ?? ""} / ${player.class_label ?? ""} ${player.level_label ?? ""}`.trim()),
    createDrawerPlayerRow("生命", player.hp?.label ?? ""),
    createDrawerPlayerRow("魔力", player.mp?.label ?? ""),
    createDrawerPlayerRow("金幣", player.gold_label ?? ""),
  );
}

function renderMenu(actions) {
  menuActionsEl.replaceChildren(
    ...actions.map((action) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "menu-action";
      button.dataset.actionId = action.action_id;
      button.dataset.disabled = String(!action.enabled);
      button.title = action.enabled ? action.description ?? "" : action.disabled_reason ?? "";

      const token = document.createElement("span");
      token.className = "menu-action-token";
      token.setAttribute("aria-hidden", "true");
      token.textContent = makeActionToken(action.label ?? action.action_id);

      const copy = document.createElement("span");
      copy.className = "menu-action-copy";

      const label = document.createElement("strong");
      label.textContent = action.label ?? action.action_id;

      const description = document.createElement("span");
      description.textContent = action.description ?? "";

      const chevron = document.createElement("span");
      chevron.className = "menu-action-chevron";
      chevron.setAttribute("aria-hidden", "true");
      chevron.textContent = ">";

      copy.append(label, description);
      button.append(token, copy, chevron);
      button.addEventListener("click", () => {
        if (action.enabled) {
          setMenuOpen(false, false);
        }
        activateAction(action, "main_menu");
      });

      return button;
    }),
  );
}

function renderRoutes(routeSegments) {
  routeLayerEl.replaceChildren(
    ...routeSegments.map((segment) => {
      const line = document.createElementNS("http://www.w3.org/2000/svg", "polyline");
      line.classList.add("route-line");
      line.dataset.status = segment.status ?? "open";
      line.setAttribute("points", (segment.points ?? []).map(([x, y]) => `${x * 10},${y * 10}`).join(" "));
      return line;
    }),
  );
}

function renderLocations(locations) {
  locationLayerEl.replaceChildren(
    ...locations.map((location) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "location-node";
      button.dataset.locationId = location.location_id;
      button.dataset.tone = location.tone ?? "neutral";
      button.dataset.unlocked = String(Boolean(location.unlocked));
      button.style.setProperty("--x", `${location.position?.x ?? 50}%`);
      button.style.setProperty("--y", `${location.position?.y ?? 50}%`);
      button.setAttribute("aria-pressed", String(location.location_id === state.selectedLocationId));
      button.title = location.unlocked ? location.description ?? "" : location.locked_reason ?? "";

      if (location.location_id === state.selectedLocationId) {
        button.classList.add("is-selected");
      }

      const emblem = document.createElement("span");
      emblem.className = "marker-emblem";
      emblem.setAttribute("aria-hidden", "true");
      const token = document.createElement("span");
      token.textContent = location.icon_token ?? "地";
      emblem.append(token);

      const title = document.createElement("span");
      title.className = "node-title";
      title.textContent = location.label ?? "";

      const meta = document.createElement("span");
      meta.className = "node-meta";
      meta.textContent = location.unlocked ? location.recommended_level ?? "" : location.status_label ?? "尚未解鎖";

      button.append(emblem, title, meta);

      if (!location.unlocked) {
        const lock = document.createElement("span");
        lock.className = "node-lock";
        lock.textContent = "LOCK";
        button.append(lock);
      }

      button.addEventListener("focus", () => {
        selectLocation(location.location_id, false);
      });
      button.addEventListener("click", () => {
        selectLocation(location.location_id, true);
        setDetailOpen(true);
      });
      return button;
    }),
  );
}

function renderSelectedLocation() {
  const location = getSelectedLocation();
  if (!location) {
    locationTitleEl.textContent = "未選擇地點";
    locationDescriptionEl.textContent = "請先選擇地圖上的點位。";
    locationFavoriteEl.textContent = "";
    locationPreviewEl.dataset.previewRole = "";
    locationStatsEl.replaceChildren();
    feedbackMessageEl.textContent = "";
    renderPrimaryAction({
      action_id: "unavailable",
      label: "無法前往",
      enabled: false,
      disabled_reason: "尚未選擇地點",
      payload: {},
    });
    return;
  }

  locationTitleEl.textContent = location.label ?? "";
  locationFavoriteEl.textContent = location.favorite ? "★" : "";
  locationPreviewEl.dataset.previewRole = location.preview_role ?? "";
  locationDescriptionEl.textContent = location.description ?? "";
  feedbackMessageEl.textContent = location.detail_note ?? "";

  const stats = [
    ["推薦等級", location.recommended_level ?? ""],
    ["步數", location.steps ?? ""],
    ["屬性", location.attribute ?? ""],
    ["通關狀態", location.clear_state ?? location.status_label ?? ""],
    ["探索評價", location.exploration_rating ?? ""],
    ["Boss", location.boss ?? ""],
  ];
  locationStatsEl.replaceChildren(...stats.map(([label, value]) => createStatRow(label, value)));
  renderPrimaryAction(location.primary_action);

  for (const button of getLocationButtons()) {
    const selected = button.dataset.locationId === location.location_id;
    button.classList.toggle("is-selected", selected);
    button.setAttribute("aria-pressed", String(selected));
  }
}

function renderPrimaryAction(action = {}) {
  confirmActionEl.textContent = action.label ?? action.action_id ?? "無法前往";
  confirmActionEl.dataset.actionId = action.action_id ?? "unavailable";
  confirmActionEl.dataset.payload = JSON.stringify(action.payload ?? {});
  confirmActionEl.dataset.disabledReason = action.disabled_reason ?? "";
  confirmActionEl.dataset.disabled = String(!action.enabled);
}

function renderActionLog() {
  if (state.actionLog.length === 0) {
    const empty = document.createElement("li");
    empty.textContent = "尚無 UIAction event";
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

function selectLocation(locationId, shouldLog) {
  const alreadySelected = state.selectedLocationId === locationId;

  if (!alreadySelected) {
    state.selectedLocationId = locationId;
  }
  if (shouldLog) {
    pushActionLog({
      action_id: "select_world_location",
      payload: { location_id: locationId },
      source: "map_node",
      dispatched: true,
    });
  }
  if (!alreadySelected) {
    renderSelectedLocation();
  }
}

function activateStoredAction(button, source) {
  const action = {
    action_id: button.dataset.actionId ?? "unavailable",
    payload: safeJson(button.dataset.payload, {}),
    enabled: button.dataset.disabled !== "true",
    disabled_reason: button.dataset.disabledReason,
  };
  activateAction(action, source);
}

async function activateAction(action, source) {
  if (!action.enabled) {
    pushActionLog({
      action_id: action.action_id,
      payload: action.payload ?? {},
      source,
      dispatched: false,
      reason: action.disabled_reason ?? "disabled",
    });
    feedbackMessageEl.textContent = action.disabled_reason || "此動作目前不可用。";
    return;
  }

  pushActionLog({
    action_id: action.action_id,
    payload: action.payload ?? {},
    source,
    dispatched: true,
  });

  if (runtimeClient.isLiveMode() && liveShellOnlyActions.has(action.action_id)) {
    feedbackMessageEl.textContent = "設定功能尚未開放。";
    return;
  }

  // Handle Offline Static Fallback for utilities
  if (!runtimeClient.isLiveMode() && ["view_status", "open_inventory", "open_bestiary"].includes(action.action_id)) {
    let mockPreview = null;
    if (action.action_id === "view_status") {
      mockPreview = {
        type: "status",
        title: "角色狀態摘要",
        data: {
          name: state.model?.player?.name ?? "見習冒險者",
          job_label: state.model?.player?.class_label ?? "劍士",
          level: 7,
          exp: 280,
          exp_next: 490,
          gold: 1957,
          guild_points: 120,
          hp_current: 183,
          hp_max: 192,
          mp_current: 38,
          mp_max: 38,
          attack: 24,
          magic_attack: 4,
          defense: 18,
          agility: 12,
          crit: 5,
          fire_resist: 15,
          equipment: [
            { slot_label: "武器", item_name: "微光鐵劍" },
            { slot_label: "頭部", item_name: "皮帽" },
            { slot_label: "身體", item_name: "硬皮甲" },
            { slot_label: "飾品", item_name: "溫暖護身符" },
            { slot_label: "特殊", item_name: "見習徽章" }
          ],
          skills: [
            { name: "斬擊", mp: 3, desc: "凝聚鬥氣的快速揮砍，造成 1.35x 物理傷害。" },
            { name: "重擊", mp: 5, desc: "蓄力猛擊，造成 1.7x 物理傷害並有機會擊暈敵人。" }
          ]
        }
      };
    } else if (action.action_id === "open_inventory") {
      mockPreview = {
        type: "inventory",
        title: "背包 / 裝備",
        data: [
          { name: "小回復藥水", quantity: 3, category: "補給品", desc: "微風平原產的草藥製成。戰鬥中可用，回復 35 HP。" },
          { name: "集中滴露", quantity: 1, category: "補給品", desc: "晶瑩的露珠。戰鬥中可用，回復 12 MP。" },
          { name: "微光鐵劍（已裝備）", quantity: 2, category: "裝備", desc: "鐵刃工坊精製的輕型鐵劍。可用職業：劍士、盜賊。" },
          { name: "皮帽（已裝備）", quantity: 1, category: "裝備", desc: "初級防具，提供微量防禦。" },
          { name: "硬皮甲（已裝備）", quantity: 1, category: "裝備", desc: "初級防具，提供基礎防禦。" },
          { name: "溫暖護身符（已裝備）", quantity: 1, category: "裝備", desc: "帶有溫暖氣息的護身符。提供火抗性。" },
          { name: "見習徽章（已裝備）", quantity: 1, category: "裝備", desc: "見習冒險者的證明。" },
          { name: "青苔纖維", quantity: 5, category: "素材", desc: "青苔洞窟黏附的韌性纖維。可用於合成配方。" },
          { name: "裂石碎片", quantity: 3, category: "素材", desc: "小魔像崩落的岩石碎片。可用於合成強化。" }
        ]
      };
    } else if (action.action_id === "open_bestiary") {
      mockPreview = {
        type: "bestiary",
        title: "魔物圖鑑摘要",
        data: [
          { name: "青苔鼠", level: 1, hp: 28, element: "自然", exp: 12, gold_range: "8 - 14G", drops: "青苔纖維 (45%機率)、小回復藥水 (8%機率)" },
          { name: "洞窟黏蟲", level: 2, hp: 42, element: "自然", exp: 18, gold_range: "10 - 18G", drops: "青苔纖維 (55%機率)、微光水晶 (18%機率)" }
        ]
      };
    }

    renderUtilityPreview(mockPreview);
    feedbackMessageEl.textContent = `已載入${action.label}預覽。`;
    return;
  }

  if (runtimeClient.isLiveMode() && action.action_id !== "back_to_start_screen") {
    await dispatchRuntimeAction(action, source);
    return;
  }

  if (action.action_id === "confirm_travel") {
    const location = getSelectedLocation();
    feedbackMessageEl.textContent = `已送出 confirm_travel：${location?.label ?? action.payload?.location_id ?? ""}。即將進入迷宮探索靜態原型。`;
  } else {
    feedbackMessageEl.textContent = `已送出 ${action.action_id}。靜態原型不執行正式流程。`;
  }

  navigateAfterAction(action);
}

function navigateAfterAction(action) {
  const route = staticActionRoutes[action.action_id];
  if (!route) {
    return;
  }

  window.setTimeout(() => {
    window.location.href = runtimeClient.withLiveMode(route);
  }, navigationDelayMs);
}

async function dispatchRuntimeAction(action, source) {
  try {
    const result = await runtimeClient.dispatchAction("world_map", action.action_id, action.payload ?? {});
    shellEl.dataset.runtimeStatus = result.status ?? "success";
    if (result.screen_model) {
      state.model = result.screen_model;
      state.selectedLocationId = result.screen_model.selected_location_id ?? state.selectedLocationId;
      render();
      if (result.screen_model.utility_preview) {
        renderUtilityPreview(result.screen_model.utility_preview);
      }
    }
    feedbackMessageEl.textContent = result.message ?? `Dispatched ${action.action_id}`;
    if (result.next_route) {
      window.setTimeout(() => {
        window.location.href = runtimeClient.nextRoute(result, staticActionRoutes[action.action_id]);
      }, navigationDelayMs);
    }
  } catch (error) {
    const reason = runtimeClient.errorMessage(error);
    shellEl.dataset.runtimeStatus = error?.runtimeStatus ?? "error";
    pushActionLog({
      action_id: action.action_id,
      payload: action.payload ?? {},
      source,
      dispatched: false,
      reason,
    });
    feedbackMessageEl.textContent = reason;
  }
}

function setMenuOpen(open, shouldLog) {
  shellEl.dataset.menuOpen = String(open);
  menuToggleEl.setAttribute("aria-expanded", String(open));
  menuDrawerEl.setAttribute("aria-hidden", String(!open));
  drawerBackdropEl.hidden = !open;

  if (shouldLog) {
    pushActionLog({
      action_id: open ? "open_main_menu" : "close_main_menu",
      payload: {},
      source: "menu_toggle",
      dispatched: true,
    });
  }
}

function setDetailOpen(open) {
  shellEl.dataset.detailOpen = String(open);
  detailPanelEl.setAttribute("aria-hidden", String(!open));
  if (open) {
    setUtilityOpen(false);
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

function getSelectedLocation() {
  return state.model?.locations?.find((location) => location.location_id === state.selectedLocationId) ?? null;
}

function getLocationButtons() {
  return [...locationLayerEl.querySelectorAll(".location-node")];
}

function createStatRow(labelText, valueText) {
  const row = document.createElement("div");
  row.className = "stat-row";

  const label = document.createElement("span");
  label.className = "stat-label";
  label.textContent = labelText;

  const value = document.createElement("span");
  value.className = "stat-value";
  value.textContent = valueText;

  row.append(label, value);
  return row;
}

function createDrawerPlayerRow(labelText, valueText) {
  const row = document.createElement("div");
  row.className = "drawer-player-row";

  const label = document.createElement("span");
  label.textContent = labelText;

  const value = document.createElement("strong");
  value.textContent = valueText;

  row.append(label, value);
  return row;
}

function makeActionToken(label) {
  return [...String(label).trim()][0] ?? ">";
}

function safeJson(value, fallback) {
  try {
    return JSON.parse(value);
  } catch {
    return fallback;
  }
}

function renderLoadError(error) {
  heroTitleEl.textContent = "Fixture 載入失敗";
  heroMetaEl.textContent = "World Map";
  resourceStripEl.replaceChildren();
  routeLayerEl.replaceChildren();
  locationLayerEl.replaceChildren();
  locationTitleEl.textContent = "無法載入地圖";
  locationDescriptionEl.textContent = error instanceof Error ? error.message : String(error);
  locationStatsEl.replaceChildren();
  feedbackMessageEl.textContent = "";
  confirmActionEl.textContent = "無法前往";
  confirmActionEl.dataset.disabled = "true";
}

/* --- World Map Utility Read-Only Preview Dynamic Controllers --- */
function escapeHtml(str) {
  if (str === null || str === undefined) {
    return "";
  }
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function initUtilityPanel() {
  utilityPanelEl = document.createElement("aside");
  utilityPanelEl.className = "utility-preview-panel";
  utilityPanelEl.setAttribute("aria-live", "polite");
  utilityPanelEl.setAttribute("aria-hidden", "true");
  utilityPanelEl.innerHTML = `
    <div class="detail-heading">
      <div>
        <p id="utility-panel-label" class="panel-label">工具預覽</p>
        <h1 id="utility-title">預覽摘要</h1>
      </div>
      <div class="detail-heading-actions">
        <button id="close-utility" class="close-detail" type="button" aria-label="關閉預覽">×</button>
      </div>
    </div>
    <div id="utility-content" class="utility-content"></div>
    <div class="detail-actions">
      <button id="utility-back-action" class="secondary-action" type="button" style="width: 100%;">返回地圖</button>
    </div>
  `;
  document.querySelector(".world-layout").appendChild(utilityPanelEl);

  utilityTitleEl = utilityPanelEl.querySelector("#utility-title");
  utilityPanelLabelEl = utilityPanelEl.querySelector("#utility-panel-label");
  utilityContentEl = utilityPanelEl.querySelector("#utility-content");
  closeUtilityEl = utilityPanelEl.querySelector("#close-utility");
  utilityBackActionEl = utilityPanelEl.querySelector("#utility-back-action");

  closeUtilityEl.addEventListener("click", () => {
    setUtilityOpen(false);
  });
  utilityBackActionEl.addEventListener("click", () => {
    setUtilityOpen(false);
  });
}

function setUtilityOpen(open) {
  shellEl.dataset.utilityOpen = String(open);
  utilityPanelEl.setAttribute("aria-hidden", String(!open));
  if (open) {
    setDetailOpen(false);
  }
}

function renderUtilityPreview(preview) {
  if (!preview) {
    return;
  }

  utilityPanelLabelEl.textContent = preview.type === "status" ? "角色狀態" :
                                    preview.type === "inventory" ? "背包 / 裝備" :
                                    preview.type === "bestiary" ? "怪物圖鑑" : "工具預覽";
  utilityTitleEl.textContent = preview.title ?? "預覽摘要";

  let html = "";
  if (preview.type === "status") {
    html = `
      <div class="utility-section">
        <p class="utility-section-title">基礎屬性</p>
        <div class="utility-grid">
          <div class="utility-grid-item"><span class="label">名字</span><span class="value">${escapeHtml(preview.data.name)}</span></div>
          <div class="utility-grid-item"><span class="label">職業</span><span class="value">${escapeHtml(preview.data.job_label)}</span></div>
          <div class="utility-grid-item"><span class="label">等級</span><span class="value">Lv${escapeHtml(preview.data.level)}</span></div>
          <div class="utility-grid-item"><span class="label">經驗值</span><span class="value">${escapeHtml(preview.data.exp)}/${escapeHtml(preview.data.exp_next)}</span></div>
          <div class="utility-grid-item"><span class="label">金幣</span><span class="value">${escapeHtml(preview.data.gold)}G</span></div>
          <div class="utility-grid-item"><span class="label">工會積分</span><span class="value">${escapeHtml(preview.data.guild_points)}</span></div>
          <div class="utility-grid-item"><span class="label">生命值</span><span class="value">${escapeHtml(preview.data.hp_current)}/${escapeHtml(preview.data.hp_max)}</span></div>
          <div class="utility-grid-item"><span class="label">魔力值</span><span class="value">${escapeHtml(preview.data.mp_current)}/${escapeHtml(preview.data.mp_max)}</span></div>
        </div>
      </div>
      <div class="utility-section">
        <p class="utility-section-title">戰鬥能力</p>
        <div class="utility-grid">
          <div class="utility-grid-item"><span class="label">攻擊力</span><span class="value">${escapeHtml(preview.data.attack)}</span></div>
          <div class="utility-grid-item"><span class="label">魔法攻擊</span><span class="value">${escapeHtml(preview.data.magic_attack)}</span></div>
          <div class="utility-grid-item"><span class="label">防禦力</span><span class="value">${escapeHtml(preview.data.defense)}</span></div>
          <div class="utility-grid-item"><span class="label">敏捷度</span><span class="value">${escapeHtml(preview.data.agility)}</span></div>
          <div class="utility-grid-item"><span class="label">暴擊率</span><span class="value">${escapeHtml(preview.data.crit)}%</span></div>
          <div class="utility-grid-item"><span class="label">火抗性</span><span class="value">${escapeHtml(preview.data.fire_resist)}%</span></div>
        </div>
      </div>
      <div class="utility-section">
        <p class="utility-section-title">目前裝備</p>
        <div style="display: grid; gap: 6px;">
          ${preview.data.equipment.map(eq => `
            <div class="utility-grid-item">
              <span class="label">${escapeHtml(eq.slot_label)}</span>
              <span class="value" style="color: var(--gold);">${escapeHtml(eq.item_name)}</span>
            </div>
          `).join("")}
        </div>
      </div>
      <div class="utility-section">
        <p class="utility-section-title">已學技能</p>
        <div style="display: grid; gap: 8px;">
          ${preview.data.skills.length === 0 ? `<p class="utility-empty-msg">尚未學習任何特殊技能。</p>` : preview.data.skills.map(skill => `
            <div class="utility-list-item">
              <div class="utility-list-item-header">
                <span class="name">${escapeHtml(skill.name)}</span>
                <span class="meta">MP ${escapeHtml(skill.mp)}</span>
              </div>
              <div class="utility-list-item-desc">${escapeHtml(skill.desc)}</div>
            </div>
          `).join("")}
        </div>
      </div>
    `;
  } else if (preview.type === "inventory") {
    const categories = ["補給品", "戰術道具", "裝備", "素材", "關鍵道具", "其他"];
    if (preview.data.length === 0) {
      html = `<p class="utility-empty-msg">背包目前沒有任何物品。</p>`;
    } else {
      categories.forEach(cat => {
        const items = preview.data.filter(item => item.category === cat);
        if (items.length > 0) {
          html += `
            <div class="utility-section">
              <p class="utility-section-title">${escapeHtml(cat)} (${items.length})</p>
              <div style="display: grid; gap: 8px;">
                ${items.map(item => `
                  <div class="utility-list-item">
                    <div class="utility-list-item-header">
                      <span class="name">${escapeHtml(item.name)}</span>
                      <span class="meta">x${escapeHtml(item.quantity)}</span>
                    </div>
                    <div class="utility-list-item-desc">${escapeHtml(item.desc)}</div>
                  </div>
                `).join("")}
              </div>
            </div>
          `;
        }
      });
    }
  } else if (preview.type === "bestiary") {
    if (preview.data.length === 0) {
      html = `
        <p class="utility-empty-msg">
          目前尚未登錄任何魔物資訊。<br>
          前往迷宮探索並戰勝魔物來登錄圖鑑。
        </p>
      `;
    } else {
      html = `
        <div style="display: grid; gap: 10px;">
          ${preview.data.map(monster => `
            <div class="utility-list-item" style="padding: 10px; gap: 6px;">
              <div class="utility-list-item-header" style="border-bottom: 1px solid rgba(239, 231, 211, 0.08); padding-bottom: 4px;">
                <span class="name" style="font-size: 0.96rem; color: var(--gold);">${escapeHtml(monster.name)}</span>
                <span class="meta">Lv${escapeHtml(monster.level)}</span>
              </div>
              <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 4px; font-size: 0.76rem; color: var(--paper-muted);">
                <div>生命值: <strong style="color: var(--paper);">${escapeHtml(monster.hp)}</strong></div>
                <div>屬性: <strong style="color: var(--paper);">${escapeHtml(monster.element)}</strong></div>
                <div>經驗值: <strong style="color: var(--paper);">${escapeHtml(monster.exp)}</strong></div>
                <div>金幣: <strong style="color: var(--paper);">${escapeHtml(monster.gold_range)}</strong></div>
              </div>
              <div class="utility-list-item-desc" style="border-top: 1px solid rgba(239, 231, 211, 0.05); padding-top: 4px; margin-top: 2px;">
                <strong>掉落：</strong>${escapeHtml(monster.drops)}
              </div>
            </div>
          `).join("")}
        </div>
      `;
    }
  }

  utilityContentEl.innerHTML = html;
  setUtilityOpen(true);

  // 隱藏背包/裝備預覽時底部的「返回地圖」按鈕容器，其餘預覽顯示
  const detailActionsEl = utilityPanelEl.querySelector(".detail-actions");
  if (detailActionsEl) {
    if (preview.type === "inventory") {
      detailActionsEl.style.display = "none";
    } else {
      detailActionsEl.style.display = "block";
    }
  }
}
