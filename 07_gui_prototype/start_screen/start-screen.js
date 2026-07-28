import { runtimeClient } from "../shared/runtime-client.js";
import { createI18n } from "../shared/i18n.js";
import { presentStoryBeat } from "../shared/story-beat.js";

const fixtureSelectEl = document.querySelector("#fixture-select");
const localeSelectEl = document.querySelector("#locale-select");
const localeLabelEl = document.querySelector("#locale-label");
const localeNoticeEl = document.querySelector("#locale-notice");
const shellEl = document.querySelector(".start-screen-shell");
const startStageEl = document.querySelector(".start-stage");
const screenKickerEl = document.querySelector("#screen-kicker");
const gameTitleEl = document.querySelector("#game-title");
const heroKickerEl = document.querySelector("#hero-kicker");
const heroTitleEl = document.querySelector("#hero-title");
const heroCopyEl = document.querySelector("#hero-copy");
const entryViewEl = document.querySelector("#entry-view");
const loginPanelEl = document.querySelector(".login-panel");
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
const registrationBackTokenEl = registrationBackEl.querySelector(".action-token");
const registrationBackLabelEl = document.querySelector("#registration-back-label");
const registrationBackDescriptionEl = document.querySelector("#registration-back-description");
const registrationConfirmEl = document.querySelector("#registration-confirm");
const registrationConfirmTokenEl = registrationConfirmEl.querySelector(".action-token");
const registrationConfirmLabelEl = document.querySelector("#registration-confirm-label");
const registrationConfirmDescriptionEl = document.querySelector("#registration-confirm-description");
const actionLogEl = document.querySelector("#action-log");
const clearLogEl = document.querySelector("#clear-log");
const fixtureControlLabelEl = document.querySelector(".fixture-control span");

const state = {
  i18n: null,
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

localeSelectEl.addEventListener("change", () => {
  state.i18n.setLocale(localeSelectEl.value);
  render();
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

bootstrap();

async function bootstrap() {
  try {
    state.i18n = await createI18n("../shared/start-screen-locales.json");
    localeSelectEl.value = state.i18n.locale;
    await loadFixture(fixtureSelectEl.value);
  } catch (error) {
    renderLoadError(error);
    shellEl.dataset.loadState = "error";
  }
}

function t(key, values) {
  return state.i18n?.t(key, values) ?? `[missing: ${key}]`;
}

function hasSave(model = state.model) {
  return model?.presentation?.has_save ?? (model?.actions ?? []).some((action) => action.action_id === "load_game");
}

function setFixtureControlMode(mode, model = null) {
  const isLive = mode === "live";
  fixtureSelectEl.disabled = isLive;
  fixtureControlLabelEl.textContent = t(isLive ? "control.runtime" : "control.fixture");
  fixtureSelectEl.title = "";
  if (!isLive || !model) {
    return;
  }

  const hasSaveAction = (model.actions ?? []).some((action) => action.action_id === "load_game");
  fixtureSelectEl.value = hasSaveAction ? "./fixtures/start-has-save.json" : "./fixtures/start-empty.json";
  fixtureSelectEl.title = t(hasSaveAction ? "control.has_save" : "control.empty");
}

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
    setFixtureControlMode("static");
    state.actionLog = [];
    state.modalOpen = false;
    state.registrationAction = null;
    state.selectedJobId = getDefaultJobId(model);
    render();
    logSystem(t("log.loaded", { path }));
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
    setFixtureControlMode("live", model);
    state.actionLog = [];
    state.modalOpen = false;
    state.registrationAction = null;
    state.selectedJobId = getDefaultJobId(model);
    render();
    logSystem(t("log.live_loaded"), {
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
    setFixtureControlMode("static");
    state.actionLog = [];
    state.modalOpen = false;
    state.registrationAction = null;
    state.selectedJobId = getDefaultJobId(model);
    render();
    logSystem(t("log.live_fallback", { path }));
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
  document.documentElement.lang = state.i18n.locale;
  document.title = `${t("screen.title")} — ${t("screen.label")}`;
  startStageEl.setAttribute("aria-label", t("screen.label"));
  loginPanelEl.setAttribute("aria-label", t("screen.actions_label"));
  localeLabelEl.textContent = t("control.language");
  screenKickerEl.textContent = t("screen.label");
  gameTitleEl.textContent = t("screen.title");
  heroKickerEl.textContent = t("hero.kicker");
  heroTitleEl.textContent = t("hero.title");
  heroCopyEl.textContent = t(hasSave(model) ? "hero.has_save" : "hero.empty");
  localeNoticeEl.hidden = state.i18n.locale !== "en";
  localeNoticeEl.textContent = t("notice.english_content");
  fixtureSelectEl.options[0].textContent = t("control.empty");
  fixtureSelectEl.options[1].textContent = t("control.has_save");
  fixtureControlLabelEl.textContent = t(fixtureSelectEl.disabled ? "control.runtime" : "control.fixture");
  fixtureSelectEl.title = fixtureSelectEl.disabled
    ? t(hasSave(model) ? "control.has_save" : "control.empty")
    : "";
  clearLogEl.textContent = t("control.clear_log");

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
      button.title = action.enabled ? "" : action.disabled_reason ?? "";

      const token = document.createElement("span");
      token.className = "action-token";
      token.setAttribute("aria-hidden", "true");
      token.textContent = makeActionToken(t(`action.${action.action_id}`));

      const copy = document.createElement("span");
      copy.className = "action-copy";

      const label = document.createElement("strong");
      label.textContent = t(`action.${action.action_id}`);

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
  registrationSubtitleEl.textContent = t("registration.panel_label");
  registrationTitleEl.textContent = getRegistrationTitle();
  registrationChipEl.textContent = registration.chip ?? "REG";
  nameLabelEl.textContent = t("registration.name_label");
  adventurerNameEl.placeholder = t("registration.name_placeholder");
  jobLabelEl.textContent = t("registration.job_label");
  jobHintEl.textContent = t(`registration.job_hint.${runtimeClient.isLiveMode() ? "live" : "static"}`);
  registrationFeedbackEl.textContent = getRegistrationFeedback();
  const backLabel = t("registration.back_label");
  const confirmLabel = getConfirmLabel();
  registrationBackTokenEl.textContent = makeActionToken(backLabel);
  registrationBackLabelEl.textContent = backLabel;
  registrationBackDescriptionEl.textContent = t("registration.back_description");
  registrationConfirmTokenEl.textContent = makeActionToken(confirmLabel);
  registrationConfirmLabelEl.textContent = confirmLabel;
  registrationConfirmDescriptionEl.textContent =
    t(`registration.confirm_description.${runtimeClient.isLiveMode() ? "live" : "static"}`);

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
      label.textContent = t(`job.${job.id}.label`);

      const summary = document.createElement("span");
      summary.textContent = t(`job.${job.id}.summary`);

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
    registrationFeedbackEl.textContent = t("feedback.missing_job");
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
  registrationFeedbackEl.textContent = getStaticDispatchFeedback(finalActionId);

  if (state.registrationAction?.story_beat) {
    await presentStoryBeat(state.registrationAction.story_beat);
  }

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
    registrationFeedbackEl.textContent = t("feedback.runtime_success");

    if (result.story_beat) {
      await presentStoryBeat(result.story_beat);
    }

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
    registrationFeedbackEl.textContent = t("feedback.runtime_error");
  }
}

function getDefaultJobId(model) {
  const registration = model?.registration ?? {};
  const jobs = registration.jobs ?? [];
  return registration.default_job_id ?? jobs[0]?.id ?? null;
}

function getRegistrationTitle() {
  return t(state.registrationAction?.final_action_id === "restart_game" ? "registration.restart_title" : "registration.new_title");
}

function getRegistrationFeedback() {
  if (state.registrationAction?.final_action_id === "restart_game") {
    return t(`registration.restart_feedback.${runtimeClient.isLiveMode() ? "live" : "static"}`);
  }
  return t("registration.new_feedback");
}

function getConfirmLabel() {
  return t(state.registrationAction?.final_action_id === "restart_game" ? "registration.confirm_restart" : "registration.confirm_new");
}

function getStaticDispatchFeedback(actionId) {
  if (actionId === "start_new_game") return t("feedback.static_start");
  if (actionId === "restart_game") return t("feedback.static_restart");
  return t("feedback.static_dispatched", { action_id: actionId });
}

function renderActionLog() {
  if (state.actionLog.length === 0) {
    const empty = document.createElement("li");
    empty.textContent = t("log.empty");
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
  gameTitleEl.textContent = t("screen.label");
  heroKickerEl.textContent = t("load_error.kicker");
  heroTitleEl.textContent = t("feedback.load_error");
  heroCopyEl.textContent = t("feedback.runtime_error");
  actionListEl.replaceChildren();
  jobListEl.replaceChildren();
  renderModalState();
  renderActionLog();
}

function makeActionToken(value) {
  const trimmed = String(value ?? "").trim();
  return trimmed ? trimmed.slice(0, 1) : "?";
}

// Initialize debug mode from URL query params
(() => {
  const urlParams = new URLSearchParams(window.location.search);
  const isDebug = urlParams.get("debug") === "1";

  const shell = document.querySelector(".start-screen-shell");
  if (shell) {
    shell.dataset.debug = String(isDebug);
  }
})();
