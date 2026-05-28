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
const navigationDelayMs = 120;

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
    logSystem(`live runtime screen loaded from ${path}`);
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

  if (runtimeClient.isLiveMode() && action.action_id !== "back_to_start_screen") {
    await dispatchRuntimeAction(action, source);
    return;
  }

  if (action.action_id === "confirm_travel") {
    const location = getSelectedLocation();
    feedbackMessageEl.textContent = `已送出 confirm_travel：${location?.label ?? action.payload?.location_id ?? ""}。即將進入 Dungeon Exploration static prototype。`;
  } else {
    feedbackMessageEl.textContent = `已送出 ${action.action_id}。static prototype 不執行正式流程。`;
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
    if (result.screen_model) {
      state.model = result.screen_model;
      state.selectedLocationId = result.screen_model.selected_location_id ?? state.selectedLocationId;
      render();
    }
    feedbackMessageEl.textContent = result.message ?? `Dispatched ${action.action_id}`;
    if (result.next_route) {
      window.setTimeout(() => {
        window.location.href = runtimeClient.nextRoute(result, staticActionRoutes[action.action_id]);
      }, navigationDelayMs);
    }
  } catch (error) {
    const reason = error instanceof Error ? error.message : String(error);
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
