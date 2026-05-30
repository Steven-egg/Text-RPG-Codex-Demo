import { runtimeClient } from "../shared/runtime-client.js";

const fixtureSelectEl = document.querySelector("#fixture-select");
const shellEl = document.querySelector(".start-screen-shell");
const screenKickerEl = document.querySelector("#screen-kicker");
const gameTitleEl = document.querySelector("#game-title");
const heroKickerEl = document.querySelector("#hero-kicker");
const heroTitleEl = document.querySelector("#hero-title");
const heroCopyEl = document.querySelector("#hero-copy");
const entryViewEl = document.querySelector("#entry-view");
const actionListEl = document.querySelector("#action-list");
const registrationModalEl = document.querySelector("#registration-modal");
const modalScrimEl = document.querySelector(".modal-scrim");
const registrationViewEl = document.querySelector("#registration-view");
const registrationSubtitleEl = document.querySelector("#registration-subtitle");
const registrationTitleEl = document.querySelector("#registration-title");
const registrationChipEl = document.querySelector("#registration-chip");
const adventurerNameEl = document.querySelector("#adventurer-name");
const nameLabelEl = document.querySelector("#name-label");
const jobLabelEl = document.querySelector("#job-label");
const jobHintEl = document.querySelector("#job-hint");
const jobListEl = document.querySelector("#job-list");
const registrationFeedbackEl = document.querySelector("#registration-feedback");
const registrationBackEl = document.querySelector("#registration-back");
const registrationBackLabelEl = document.querySelector("#registration-back-label");
const registrationBackDescriptionEl = document.querySelector("#registration-back-description");
const registrationConfirmEl = document.querySelector("#registration-confirm");
const registrationConfirmLabelEl = document.querySelector("#registration-confirm-label");
const registrationConfirmDescriptionEl = document.querySelector("#registration-confirm-description");
const actionLogEl = document.querySelector("#action-log");
const clearLogEl = document.querySelector("#clear-log");

const state = {
  model: null,
  actionLog: [],
  modalOpen: false,
  selectedJobId: null,
  registrationAction: null,
};

const staticActionRoutes = {
  load_game: "../world_map/index.html",
  restart_game: "../world_map/index.html",
  start_new_game: "../world_map/index.html",
};
const navigationDelayMs = 120;

fixtureSelectEl.addEventListener("change", () => {
  loadFixture(fixtureSelectEl.value);
});

clearLogEl.addEventListener("click", () => {
  state.actionLog = [];
  renderActionLog();
});

registrationViewEl.addEventListener("submit", (event) => {
  event.preventDefault();
  confirmRegistration();
});

registrationBackEl.addEventListener("click", () => {
  cancelRegistration();
});

modalScrimEl.addEventListener("click", () => {
  cancelRegistration();
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && state.modalOpen) {
    cancelRegistration();
  }
});

loadFixture(fixtureSelectEl.value);

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
    state.actionLog = [];
    state.modalOpen = false;
    state.registrationAction = null;
    state.selectedJobId = getDefaultJobId(model);
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
    const model = await runtimeClient.getScreen("start_screen");
    state.model = model;
    state.actionLog = [];
    state.modalOpen = false;
    state.registrationAction = null;
    state.selectedJobId = getDefaultJobId(model);
    render();
    logSystem("live runtime screen loaded", {
      actionId: "live_screen_loaded",
      source: "live_loader",
      payload: { mode: "live", screen_id: "start_screen" },
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
    state.actionLog = [];
    state.modalOpen = false;
    state.registrationAction = null;
    state.selectedJobId = getDefaultJobId(model);
    render();
    logSystem(`live unavailable; loaded fixture ${path}`);
    pushActionLog({
      action_id: "live_bridge_unavailable",
      payload: { reason: liveError instanceof Error ? liveError.message : String(liveError) },
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
  screenKickerEl.textContent = model.screen_label ?? "登入畫面";
  gameTitleEl.textContent = model.title ?? "";
  heroKickerEl.textContent = model.hero_kicker ?? "";
  heroTitleEl.textContent = model.hero_title ?? "";
  heroCopyEl.textContent = model.hero_copy ?? "";

  renderActions(model.actions ?? []);
  renderRegistration();
  renderModalState();
  renderActionLog();
}

function renderActions(actions) {
  actionListEl.replaceChildren(
    ...actions.map((action) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "start-action";
      button.dataset.actionId = action.action_id;
      button.dataset.kind = action.kind ?? "secondary";
      button.dataset.disabled = String(!action.enabled);
      button.title = action.enabled ? action.description ?? "" : action.disabled_reason ?? "";

      const token = document.createElement("span");
      token.className = "action-token";
      token.setAttribute("aria-hidden", "true");
      token.textContent = action.token ?? makeActionToken(action.label ?? action.action_id);

      const copy = document.createElement("span");
      copy.className = "action-copy";

      const label = document.createElement("strong");
      label.textContent = action.label ?? action.action_id;

      copy.append(label);
      if (action.description) {
        const description = document.createElement("span");
        description.textContent = action.description;
        copy.append(description);
      }
      button.append(token, copy);
      button.addEventListener("click", () => {
        activateAction(action);
      });

      return button;
    }),
  );
}

function renderRegistration() {
  const registration = state.model?.registration ?? {};
  registrationSubtitleEl.textContent = registration.panel_label ?? "冒險者登錄";
  registrationTitleEl.textContent = getRegistrationTitle();
  registrationChipEl.textContent = registration.chip ?? "REG";
  nameLabelEl.textContent = registration.name_label ?? "冒險者名字";
  adventurerNameEl.placeholder = registration.name_placeholder ?? registration.fallback_name ?? "見習冒險者";
  jobLabelEl.textContent = registration.job_label ?? "初始職業";
  jobHintEl.textContent = registration.job_hint ?? "選擇一個初始職業。";
  registrationFeedbackEl.textContent = getRegistrationFeedback();
  registrationBackLabelEl.textContent = registration.back_label ?? "返回";
  registrationBackDescriptionEl.textContent = registration.back_description ?? "回到開始畫面";
  registrationConfirmLabelEl.textContent = getConfirmLabel();
  registrationConfirmDescriptionEl.textContent =
    registration.confirm_description ?? "只記錄 static UIAction，前往 World Map prototype。";

  const jobs = registration.jobs ?? [];
  jobListEl.replaceChildren(
    ...jobs.map((job) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "job-card";
      button.dataset.jobId = job.id;
      button.dataset.selected = String(job.id === state.selectedJobId);
      button.setAttribute("aria-pressed", String(job.id === state.selectedJobId));

      const index = document.createElement("span");
      index.className = "job-index";
      index.textContent = job.index ?? "";

      const copy = document.createElement("span");
      copy.className = "job-copy";

      const label = document.createElement("strong");
      label.textContent = job.label ?? job.id;

      const summary = document.createElement("span");
      summary.textContent = job.summary ?? "";

      copy.append(label, summary);
      button.append(index, copy);
      button.addEventListener("click", () => {
        state.selectedJobId = job.id;
        renderRegistration();
      });

      return button;
    }),
  );
}

function renderModalState() {
  registrationModalEl.hidden = !state.modalOpen;
  registrationModalEl.dataset.state = state.modalOpen ? "open" : "closed";
  entryViewEl.inert = state.modalOpen;
}

async function activateAction(action) {
  if (!action.enabled) {
    pushActionLog({
      action_id: action.action_id,
      payload: action.payload ?? {},
      dispatched: false,
      reason: action.disabled_reason ?? "disabled",
    });
    return;
  }

  if (action.opens_registration) {
    openRegistration(action);
    return;
  }

  if (runtimeClient.isLiveMode()) {
    await dispatchRuntimeAction(action, action.payload ?? {});
    return;
  }

  pushActionLog({
    action_id: action.action_id,
    payload: action.payload ?? {},
    dispatched: true,
  });
  navigateAfterAction(action.action_id);
}

function openRegistration(action) {
  state.modalOpen = true;
  state.registrationAction = action;
  state.selectedJobId = getDefaultJobId(state.model);
  adventurerNameEl.value = "";
  renderRegistration();
  renderModalState();
  pushActionLog({
    action_id: "open_adventurer_registration",
    payload: {
      entry: action.registration_entry ?? action.payload?.entry ?? "new_game",
      final_action_id: action.final_action_id ?? action.action_id,
    },
    dispatched: true,
  });
  window.setTimeout(() => adventurerNameEl.focus(), 0);
}

function cancelRegistration() {
  const entry = state.registrationAction?.registration_entry ?? state.registrationAction?.payload?.entry ?? "new_game";
  state.modalOpen = false;
  pushActionLog({
    action_id: "cancel_adventurer_registration",
    payload: { entry },
    dispatched: true,
  });
  renderModalState();
}

async function confirmRegistration() {
  const registration = state.model?.registration ?? {};
  const jobs = registration.jobs ?? [];
  const selectedJob = jobs.find((job) => job.id === state.selectedJobId) ?? jobs[0];
  const fallbackName = registration.fallback_name ?? "見習冒險者";
  const name = adventurerNameEl.value.trim() || fallbackName;

  if (!selectedJob) {
    registrationFeedbackEl.textContent = "請先選擇初始職業。";
    pushActionLog({
      action_id: "confirm_adventurer_registration",
      payload: { name },
      dispatched: false,
      reason: "missing_job",
    });
    return;
  }

  const finalActionId = state.registrationAction?.final_action_id ?? state.registrationAction?.action_id ?? "start_new_game";
  const entry = state.registrationAction?.registration_entry ?? state.registrationAction?.payload?.entry ?? "new_game";

  if (runtimeClient.isLiveMode()) {
    await dispatchRuntimeAction(
      { action_id: finalActionId, payload: { entry } },
      {
        entry,
        name,
        job_id: selectedJob.id,
        job_label: selectedJob.label,
      },
    );
    return;
  }

  pushActionLog({
    action_id: finalActionId,
    payload: {
      entry,
      name,
      job_id: selectedJob.id,
      job_label: selectedJob.label,
    },
    dispatched: true,
  });
  registrationFeedbackEl.textContent =
    state.registrationAction?.dispatch_message ?? `已送出 ${finalActionId}。`;
  navigateAfterAction(finalActionId);
}

function navigateAfterAction(actionId) {
  const route = staticActionRoutes[actionId];
  if (!route) {
    return;
  }

  window.setTimeout(() => {
    window.location.href = runtimeClient.withLiveMode(route);
  }, navigationDelayMs);
}

async function dispatchRuntimeAction(action, payload) {
  try {
    let result;
    if (action.action_id === "load_game") {
      result = await runtimeClient.loadGame();
    } else if (action.action_id === "load_demo_seed") {
      result = await runtimeClient.loadDemoSeed();
    } else if (action.action_id === "start_new_game") {
      result = await runtimeClient.startNewGame(payload);
    } else if (action.action_id === "restart_game") {
      result = await runtimeClient.dispatchAction("start_screen", "restart_game", payload);
    } else {
      result = await runtimeClient.dispatchAction("start_screen", action.action_id, payload);
    }

    shellEl.dataset.runtimeStatus = result.status ?? "success";
    pushActionLog({
      action_id: action.action_id,
      payload,
      dispatched: true,
    });
    registrationFeedbackEl.textContent = result.message ?? `Dispatched ${action.action_id}`;
    const route = runtimeClient.nextRoute(result, staticActionRoutes[action.action_id] ?? "../town_hub/index.html");
    if (route) {
      window.setTimeout(() => {
        window.location.href = route;
      }, navigationDelayMs);
    }
  } catch (error) {
    const reason = runtimeClient.errorMessage(error);
    shellEl.dataset.runtimeStatus = error?.runtimeStatus ?? "error";
    pushActionLog({
      action_id: action.action_id,
      payload,
      dispatched: false,
      reason,
    });
    registrationFeedbackEl.textContent = reason;
  }
}

function getDefaultJobId(model) {
  const registration = model?.registration ?? {};
  const jobs = registration.jobs ?? [];
  return registration.default_job_id ?? jobs[0]?.id ?? null;
}

function getRegistrationTitle() {
  return state.registrationAction?.registration_title ?? state.model?.registration?.title ?? "建立冒險者名冊";
}

function getRegistrationFeedback() {
  return state.registrationAction?.registration_feedback ?? state.model?.registration?.feedback ?? "";
}

function getConfirmLabel() {
  return state.registrationAction?.confirm_label ?? state.model?.registration?.confirm_label ?? "確認開始";
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

function pushActionLog(entry) {
  state.actionLog.push({
    ...entry,
    time: new Date().toLocaleTimeString("zh-TW", { hour12: false }),
  });
  renderActionLog();
}

function logSystem(message, options = {}) {
  pushActionLog({
    action_id: options.actionId ?? "fixture_loaded",
    payload: { message, ...(options.payload ?? {}) },
    source: options.source ?? "fixture_loader",
    dispatched: true,
  });
}

function renderLoadError(error) {
  state.modalOpen = false;
  gameTitleEl.textContent = "Start Screen";
  heroKickerEl.textContent = "Fixture Error";
  heroTitleEl.textContent = "讀取失敗";
  heroCopyEl.textContent = error instanceof Error ? error.message : String(error);
  actionListEl.replaceChildren();
  jobListEl.replaceChildren();
  renderModalState();
  renderActionLog();
}

function makeActionToken(value) {
  const trimmed = String(value ?? "").trim();
  return trimmed ? trimmed.slice(0, 1) : "?";
}
