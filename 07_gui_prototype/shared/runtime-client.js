const LIVE_MODE_VALUE = "live";

function params() {
  return new URLSearchParams(window.location.search);
}

function withLiveMode(route) {
  if (!route || !isLiveMode()) {
    return route;
  }
  const url = new URL(route, window.location.href);
  url.searchParams.set("mode", LIVE_MODE_VALUE);
  return url.href;
}

async function requestJson(path, options = {}) {
  const response = await fetch(path, {
    cache: "no-store",
    headers: {
      "Content-Type": "application/json",
      ...(options.headers ?? {}),
    },
    ...options,
  });
  const body = await response.json().catch(() => ({}));
  if (!response.ok || body.ok === false) {
    const error = new Error(body.blocked_reason || body.error || `Runtime request failed: ${response.status}`);
    error.runtimeStatus = body.status || (response.status === 403 || response.status === 409 ? "blocked" : "error");
    error.blockedReason = body.blocked_reason || "";
    error.responseBody = body;
    error.httpStatus = response.status;
    throw error;
  }
  return body;
}

function isLiveMode() {
  return params().get("mode") === LIVE_MODE_VALUE || sessionStorage.getItem("elementMazeMode") === LIVE_MODE_VALUE;
}

function persistLiveMode() {
  if (params().get("mode") === LIVE_MODE_VALUE) {
    sessionStorage.setItem("elementMazeMode", LIVE_MODE_VALUE);
  }
}

async function getSession() {
  return requestJson("/api/session");
}

async function getScreen(screenId) {
  const result = await requestJson(`/api/screen/${encodeURIComponent(screenId)}`);
  return result.screen_model;
}

async function startNewGame(payload) {
  return requestJson("/api/session/new", {
    method: "POST",
    body: JSON.stringify(payload ?? {}),
  });
}

async function loadGame() {
  return requestJson("/api/session/load", {
    method: "POST",
    body: JSON.stringify({}),
  });
}

async function loadDemoSeed() {
  return requestJson("/api/session/demo-seed", {
    method: "POST",
    body: JSON.stringify({}),
  });
}

async function saveGame() {
  return requestJson("/api/save", {
    method: "POST",
    body: JSON.stringify({}),
  });
}

async function dispatchAction(screenId, actionId, payload = {}) {
  return requestJson("/api/action", {
    method: "POST",
    body: JSON.stringify({ screen_id: screenId, action_id: actionId, payload }),
  });
}

function nextRoute(result, fallbackRoute) {
  return withLiveMode(result?.next_route || fallbackRoute);
}

function errorMessage(error) {
  return error?.blockedReason || error?.message || String(error);
}

persistLiveMode();

export const runtimeClient = {
  isLiveMode,
  getSession,
  getScreen,
  startNewGame,
  loadGame,
  loadDemoSeed,
  saveGame,
  dispatchAction,
  nextRoute,
  errorMessage,
  withLiveMode,
};
