import { runtimeClient } from "../shared/runtime-client.js";

const fixtureSelect = document.querySelector("#fixture-select");
const titleEl = document.querySelector("#screen-title");
const subtitleEl = document.querySelector("#screen-subtitle");
const resourceStripEl = document.querySelector("#resource-strip");
const facilityLayerEl = document.querySelector("#facility-node-layer");
const facilitySceneEl = document.querySelector("#facility-scene");
const guidanceEl = document.querySelector("#town-guidance");
const navigationActionsEl = document.querySelector("#navigation-actions");
const actionLogEl = document.querySelector("#action-log");
const clearLogEl = document.querySelector("#clear-log");
const shellEl = document.querySelector(".town-hub-shell");
const liveStatusBadgeEl = document.querySelector("#live-status-badge");

// 偵錯主控台 DOM 節點
const debugContainer = document.querySelector("#debug-container");
const debugModeBadge = document.querySelector("#debug-mode-badge");
const debugNotesEl = document.querySelector("#debug-notes");
const toggleDebugCollapseEl = document.querySelector("#toggle-debug-collapse");
const debugBodyEl = document.querySelector("#debug-body");
const toggleLogVisibleEl = document.querySelector("#toggle-log-visible");

const isDebugMode = new URLSearchParams(window.location.search).get("debug") === "1";

if (isDebugMode) {
  debugContainer.style.display = "block";
  document.body.dataset.debug = "1";
} else {
  debugContainer.style.display = "none";
}

let debugCollapsed = false;
toggleDebugCollapseEl.addEventListener("click", () => {
  debugCollapsed = !debugCollapsed;
  debugBodyEl.style.display = debugCollapsed ? "none" : "block";
  toggleDebugCollapseEl.textContent = debugCollapsed ? "展開" : "收合";
});

let logVisible = true;
toggleLogVisibleEl.addEventListener("click", () => {
  logVisible = !logVisible;
  actionLogEl.style.display = logVisible ? "block" : "none";
  toggleLogVisibleEl.textContent = logVisible ? "隱藏 Log" : "顯示 Log";
});

const state = {
  model: null,
  selectedFacilityId: null,
  actionLog: [],
};

const roleTokens = {
  guild: "GLD",
  bed: "INN",
  shop: "SHP",
  hammer: "FRG",
  alchemy: "ALC",
  magic: "ARC",
  temple: "TMP",
  relic: "RLC",
  storage: "STO",
};

const staticFacilityRoutes = {
  guild: "../guild_screen/index.html",
  synthesis: "../synthesis_screen/index.html",
  travel_shop: "../shop_screen/index.html",
  workshop: "../workshop_screen/index.html",
  storage: "../storage_screen/index.html",
  magic_shop: "../magic_shop_screen/index.html",
  inn: "../inn_screen/index.html",
  temple: "../temple_screen/index.html",
  relic_preview: "../relic_preview_screen/index.html",
};
const staticActionRoutes = {
  open_world_map: "../world_map/index.html",
};
const navigationDelayMs = 120;

fixtureSelect.addEventListener("change", () => {
  loadFixture(fixtureSelect.value);
});

facilitySceneEl.addEventListener("keydown", (event) => {
  const arrowKeys = ["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown"];
  if (!arrowKeys.includes(event.key)) {
    return;
  }

  const nodeButtons = getFacilityButtons();
  const currentIndex = nodeButtons.indexOf(document.activeElement);
  if (currentIndex < 0) {
    return;
  }

  event.preventDefault();
  const columnCount = getComputedStyle(facilityLayerEl).gridTemplateColumns.split(" ").length;
  const mobileGrid = Number.isFinite(columnCount) && columnCount > 1;
  const rowJump = mobileGrid ? columnCount : 3;
  const deltaByKey = {
    ArrowLeft: -1,
    ArrowRight: 1,
    ArrowUp: -rowJump,
    ArrowDown: rowJump,
  };

  const nextIndex = wrapIndex(currentIndex + deltaByKey[event.key], nodeButtons.length);
  nodeButtons[nextIndex]?.focus();
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
    state.selectedFacilityId = model.selected_facility_id ?? model.facility_nodes?.[0]?.facility_id ?? null;
    state.actionLog = [];
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
    const model = await runtimeClient.getScreen("town_hub");
    state.model = model;
    state.selectedFacilityId = model.selected_facility_id ?? model.facility_nodes?.[0]?.facility_id ?? null;
    state.actionLog = [];
    render();
    logSystem("live runtime screen loaded", {
      actionId: "live_screen_loaded",
      source: "live_loader",
      payload: { mode: "live", screen_id: "town_hub" },
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
    state.selectedFacilityId = model.selected_facility_id ?? model.facility_nodes?.[0]?.facility_id ?? null;
    state.actionLog = [];
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
  shellEl.dataset.currentRegionId = model.current_region_id ?? "border_fire";
  if (model.town_asset) {
    facilitySceneEl.style.backgroundImage = `url("${model.town_asset}")`;
  }

  // 動態處理並剝離 (Live) 大字標題，改成精緻的小徽章
  let displayTitle = model.title ?? "";
  let isLive = false;
  if (displayTitle.includes("(Live)")) {
    displayTitle = displayTitle.replace("(Live)", "").trim();
    isLive = true;
  }
  titleEl.textContent = displayTitle;

  if (liveStatusBadgeEl) {
    liveStatusBadgeEl.style.display = isLive ? "inline-block" : "none";
  }

  // 動態過濾並替換工程用語
  let displaySubtitle = model.subtitle ?? "";
  if (
    displaySubtitle.includes("Python") ||
    displaySubtitle.includes("遊戲引擎") ||
    displaySubtitle.includes("同步") ||
    displaySubtitle.includes("engine")
  ) {
    displaySubtitle = "薄霧散去，街道重新亮起微光。旅人們在廣場邊低聲交談。";
  }
  subtitleEl.textContent = displaySubtitle;

  renderResources(model.resource_strip ?? []);
  renderFacilities(model.facility_nodes ?? []);
  renderGuidance(model.town_guidance ?? []);
  renderActionButtons(navigationActionsEl, model.navigation_actions ?? [], "navigation");
  renderActionLog();

  if (isDebugMode) {
    debugModeBadge.textContent = runtimeClient.isLiveMode() ? "Live Mode" : "Fixture Mode";
    renderDebugNotes(model.debug_notes ?? []);
  }
}

function renderDebugNotes(notes) {
  if (notes.length === 0) {
    const empty = document.createElement("li");
    empty.textContent = "無備忘筆記。";
    debugNotesEl.replaceChildren(empty);
    return;
  }
  debugNotesEl.replaceChildren(
    ...notes.map((note) => {
      const li = document.createElement("li");
      li.textContent = note;
      return li;
    }),
  );
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

function renderFacilities(nodes) {
  facilityLayerEl.replaceChildren(
    ...nodes.map((node) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "facility-node";
      button.dataset.facilityId = node.facility_id;
      button.dataset.anchor = node.visual_anchor ?? "";
      button.dataset.group = node.visual_group ?? "";
      button.setAttribute("aria-disabled", String(!node.enabled));
      button.setAttribute("aria-pressed", String(node.facility_id === state.selectedFacilityId));
      button.title = node.enabled ? node.description ?? "" : node.disabled_reason ?? "";

      if (node.facility_id === state.selectedFacilityId) {
        button.classList.add("is-selected");
      }

      const icon = document.createElement("span");
      icon.className = "node-icon";
      icon.setAttribute("aria-hidden", "true");

      const iconInner = document.createElement("span");
      iconInner.className = "node-icon-inner";
      iconInner.textContent = roleTokens[node.icon_role] ?? makeRoleToken(node.icon_role);
      icon.appendChild(iconInner);

      const copy = document.createElement("span");
      copy.className = "node-copy";

      const title = document.createElement("span");
      title.className = "node-title";
      title.textContent = node.label ?? "";

      const description = document.createElement("span");
      description.className = "node-description";
      description.textContent = node.description ?? "";

      copy.append(title, description);
      button.append(icon, copy);

      const badge = getPrimaryBadge(node.badges ?? []);
      if (badge) {
        const badgeEl = document.createElement("span");
        badgeEl.className = "node-badge";
        badgeEl.dataset.kind = badge.kind ?? "notification";
        badgeEl.textContent = badge.label ?? "";
        button.append(badgeEl);
      }

      button.addEventListener("focus", () => selectFacility(node.facility_id));
      button.addEventListener("mouseenter", () => {
        button.dataset.hover = "true";
      });
      button.addEventListener("mouseleave", () => {
        delete button.dataset.hover;
      });
      button.addEventListener("click", () => activateFacility(node, "facility_node"));

      return button;
    }),
  );
}

function renderGuidance(lines) {
  const cleanedLines = lines.map((line) => {
    if (
      line.includes("Live 模式") ||
      line.includes("Python") ||
      line.includes("核心驗證") ||
      line.includes("引擎同步") ||
      line.includes("動態更新")
    ) {
      return "選擇設施進行整備，或前往世界地圖繼續冒險。";
    }
    return line;
  });

  guidanceEl.replaceChildren(
    ...cleanedLines.map((line) => {
      const p = document.createElement("p");
      p.className = "guidance-line";
      p.textContent = line;
      return p;
    }),
  );
}

function renderActionButtons(container, actions, source) {
  container.replaceChildren(
    ...actions.map((action) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "action-button";
      button.setAttribute("aria-disabled", String(!action.enabled));

      const desc = action.description ?? "";
      button.title = action.enabled ? desc : (action.disabled_reason ?? "未開啟");

      const label = document.createElement("span");
      label.className = "action-button-label";

      let text = action.label ?? action.action_id;
      if (action.action_id === "open_world_map") {
        text = "前往世界地圖 →";
      }
      label.textContent = text;

      button.append(label);
      button.addEventListener("click", () => activateAction(action, source));
      return button;
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

function selectFacility(facilityId) {
  if (state.selectedFacilityId === facilityId) {
    return;
  }
  state.selectedFacilityId = facilityId;
  for (const button of getFacilityButtons()) {
    const selected = button.dataset.facilityId === facilityId;
    button.classList.toggle("is-selected", selected);
    button.setAttribute("aria-pressed", String(selected));
  }
}

function activateFacility(node, source) {
  selectFacility(node.facility_id);
  const action = {
    action_id: node.primary_action,
    label: node.label,
    enabled: node.enabled,
    disabled_reason: node.disabled_reason,
    payload: node.payload ?? {},
    navigation_route: node.navigation_route,
    target_screen_id: node.target_screen_id,
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
    return;
  }

  pushActionLog({
    action_id: action.action_id,
    payload: action.payload ?? {},
    source,
    dispatched: true,
  });

  if (runtimeClient.isLiveMode()) {
    if (action.action_id === "open_facility") {
      navigateAfterAction(action);
      return;
    }
    await dispatchRuntimeAction(action, source);
    return;
  }
  navigateAfterAction(action);
}

function navigateAfterAction(action) {
  if (action.action_id === "open_facility") {
    const facilityId = action.payload?.facility_id;
    const route = action.navigation_route ?? staticFacilityRoutes[facilityId];
    if (!route) {
      return;
    }

    window.setTimeout(() => {
      window.location.href = runtimeClient.withLiveMode(route);
    }, navigationDelayMs);
    return;
  }

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
    const result = await runtimeClient.dispatchAction("town_hub", action.action_id, action.payload ?? {});
    shellEl.dataset.runtimeStatus = result.status ?? "success";
    if (result.screen_model) {
      state.model = result.screen_model;
      state.selectedFacilityId = result.screen_model.selected_facility_id ?? state.selectedFacilityId;
      render();
    }
    if (result.message) {
      pushActionLog({
        action_id: "runtime_feedback",
        payload: { message: result.message },
        source,
        dispatched: true,
      });
    }
    if (result.next_route) {
      window.setTimeout(() => {
        window.location.href = runtimeClient.nextRoute(result, staticActionRoutes[action.action_id]);
      }, navigationDelayMs);
    }
  } catch (error) {
    shellEl.dataset.runtimeStatus = error?.runtimeStatus ?? "error";
    pushActionLog({
      action_id: action.action_id,
      payload: action.payload ?? {},
      source,
      dispatched: false,
      reason: runtimeClient.errorMessage(error),
    });
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

function getFacilityButtons() {
  return [...facilityLayerEl.querySelectorAll(".facility-node")];
}

function getPrimaryBadge(badges) {
  return [...badges].sort((a, b) => (b.priority ?? 0) - (a.priority ?? 0))[0] ?? null;
}

function makeRoleToken(role) {
  if (!role) {
    return "NOD";
  }
  return role
    .split(/[_\s-]+/)
    .map((part) => part[0] ?? "")
    .join("")
    .slice(0, 3)
    .toUpperCase();
}

function wrapIndex(index, length) {
  return ((index % length) + length) % length;
}

function renderLoadError(error) {
  titleEl.textContent = "Fixture 載入失敗";
  subtitleEl.textContent = "無法讀取靜態 fixture。";
  facilityLayerEl.replaceChildren();
  resourceStripEl.replaceChildren();
  guidanceEl.replaceChildren();
  navigationActionsEl.replaceChildren();

  const errorEl = document.createElement("div");
  errorEl.className = "load-error";
  errorEl.textContent = error instanceof Error ? error.message : String(error);
  facilityLayerEl.append(errorEl);
}
