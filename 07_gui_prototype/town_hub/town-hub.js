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

function render() {
  const { model } = state;
  titleEl.textContent = model.title ?? "";
  subtitleEl.textContent = model.subtitle ?? "";
  renderResources(model.resource_strip ?? []);
  renderFacilities(model.facility_nodes ?? []);
  renderGuidance(model.town_guidance ?? []);
  renderActionButtons(navigationActionsEl, model.navigation_actions ?? [], "navigation");
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
      icon.textContent = roleTokens[node.icon_role] ?? makeRoleToken(node.icon_role);

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
  guidanceEl.replaceChildren(
    ...lines.map((line) => {
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
      button.title = action.enabled ? action.description ?? "" : action.disabled_reason ?? "";

      const label = document.createElement("strong");
      label.textContent = action.label ?? action.action_id;

      const description = document.createElement("span");
      description.textContent = action.description ?? "";

      button.append(label, description);
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
  };
  activateAction(action, source);
}

function activateAction(action, source) {
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
  navigateAfterAction(action);
}

function navigateAfterAction(action) {
  if (action.action_id === "open_facility") {
    const facilityId = action.payload?.facility_id;
    const route = staticFacilityRoutes[facilityId];
    if (!route) {
      return;
    }

    window.setTimeout(() => {
      window.location.href = route;
    }, navigationDelayMs);
    return;
  }

  const route = staticActionRoutes[action.action_id];
  if (!route) {
    return;
  }

  window.setTimeout(() => {
    window.location.href = route;
  }, navigationDelayMs);
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
