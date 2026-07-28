export const SFX_STORAGE_KEY = "element_maze.sfx_muted";
export const SFX_MAX_VOLUME = 0.22;
export const SFX_CUE_NAMES = Object.freeze([
  "ui_click",
  "confirm",
  "back",
  "warning",
  "victory",
]);

export const SFX_CUE_DEFINITIONS = Object.freeze({
  ui_click: Object.freeze([
    Object.freeze({ wave: "triangle", from: 680, to: 560, start: 0, duration: 0.055, gain: 0.055 }),
  ]),
  confirm: Object.freeze([
    Object.freeze({ wave: "sine", from: 520, to: 620, start: 0, duration: 0.09, gain: 0.075 }),
    Object.freeze({ wave: "sine", from: 780, to: 880, start: 0.055, duration: 0.1, gain: 0.065 }),
  ]),
  back: Object.freeze([
    Object.freeze({ wave: "triangle", from: 440, to: 260, start: 0, duration: 0.11, gain: 0.065 }),
  ]),
  warning: Object.freeze([
    Object.freeze({ wave: "square", from: 190, to: 160, start: 0, duration: 0.1, gain: 0.038 }),
    Object.freeze({ wave: "square", from: 170, to: 140, start: 0.09, duration: 0.12, gain: 0.034 }),
  ]),
  victory: Object.freeze([
    Object.freeze({ wave: "sine", from: 523, to: 659, start: 0, duration: 0.11, gain: 0.065 }),
    Object.freeze({ wave: "sine", from: 659, to: 784, start: 0.07, duration: 0.13, gain: 0.075 }),
    Object.freeze({ wave: "sine", from: 784, to: 1047, start: 0.15, duration: 0.18, gain: 0.085 }),
  ]),
});

const TOGGLE_ID = "element-maze-sfx-toggle";
const INTERACTIVE_SELECTOR = [
  "button",
  "a[href]",
  "select",
  "summary",
  'input[type="checkbox"]',
  '[role="button"]',
  "[data-sfx]",
  ".modal-scrim",
  ".drawer-backdrop",
  ".travel-prep-overlay",
].join(", ");

let audioContext = null;
let audioUnavailable = false;
let muted = false;
let toggleEl = null;
let playCount = 0;

export function inferSfxCue(target) {
  if (!target) {
    return null;
  }

  const explicit = target.closest?.("[data-sfx]")?.dataset?.sfx;
  if (explicit === "none") {
    return null;
  }
  if (SFX_CUE_NAMES.includes(explicit)) {
    return explicit;
  }

  if (target.closest?.('[data-outcome="victory"]')) {
    return "victory";
  }

  const victoryJustOpened =
    target.matches?.(".command-button, .submenu-option") &&
    typeof document !== "undefined" &&
    document.querySelector('[data-outcome="victory"]:not([hidden])');
  if (victoryJustOpened) {
    return "victory";
  }

  if (isDisabledTarget(target)) {
    return "warning";
  }

  const descriptor = [
    target.id,
    typeof target.className === "string" ? target.className : "",
    target.dataset?.actionId,
    target.dataset?.kind,
  ]
    .filter(Boolean)
    .join(" ")
    .toLowerCase();

  if (/(?:^|[-_\s])(back|close|cancel|retreat|return)(?:$|[-_\s])/.test(descriptor)) {
    return "back";
  }

  if (
    target.getAttribute?.("type") === "submit" ||
    target.dataset?.primary === "true" ||
    /(?:^|[-_\s])(confirm|submit|purchase|buy|craft|learn|rest|attune|execute|challenge|advance|primary)(?:$|[-_\s])/.test(
      descriptor,
    )
  ) {
    return "confirm";
  }

  return "ui_click";
}

export function playSfx(cueName, { allowContextCreation = false } = {}) {
  if (muted || !SFX_CUE_DEFINITIONS[cueName]) {
    return false;
  }

  const context = getAudioContext(allowContextCreation);
  if (!context) {
    return false;
  }

  const playWhenRunning = () => {
    if (context.state === "running") {
      setAudioState("running");
      if (playDefinition(context, SFX_CUE_DEFINITIONS[cueName])) {
        recordCue(cueName);
      }
    }
  };

  try {
    if (context.state === "running") {
      playWhenRunning();
    } else if (allowContextCreation && context.state !== "closed" && typeof context.resume === "function") {
      Promise.resolve(context.resume())
        .then(playWhenRunning)
        .catch(() => setAudioState("blocked"));
    }
    return true;
  } catch {
    return false;
  }
}

function getAudioContext(allowContextCreation) {
  if (audioContext || !allowContextCreation || audioUnavailable || typeof window === "undefined") {
    return audioContext;
  }

  const AudioContextConstructor = window.AudioContext ?? window.webkitAudioContext;
  if (typeof AudioContextConstructor !== "function") {
    audioUnavailable = true;
    setAudioState("unavailable");
    return null;
  }

  try {
    audioContext = new AudioContextConstructor();
    setAudioState(audioContext.state ?? "created");
  } catch {
    audioUnavailable = true;
    audioContext = null;
    setAudioState("blocked");
  }
  return audioContext;
}

function playDefinition(context, notes) {
  try {
    const baseTime = context.currentTime + 0.004;
    for (const note of notes) {
      const oscillator = context.createOscillator();
      const envelope = context.createGain();
      const startTime = baseTime + note.start;
      const endTime = startTime + note.duration;
      const peak = Math.min(SFX_MAX_VOLUME, Math.max(0, note.gain));

      oscillator.type = note.wave;
      oscillator.frequency.setValueAtTime(note.from, startTime);
      oscillator.frequency.exponentialRampToValueAtTime(Math.max(1, note.to), endTime);
      envelope.gain.setValueAtTime(0.0001, startTime);
      envelope.gain.linearRampToValueAtTime(peak, startTime + Math.min(0.008, note.duration / 3));
      envelope.gain.exponentialRampToValueAtTime(0.0001, endTime);

      oscillator.connect(envelope);
      envelope.connect(context.destination);
      oscillator.start(startTime);
      oscillator.stop(endTime + 0.01);
    }
    return true;
  } catch {
    // Sound must never interfere with the underlying UI action.
    return false;
  }
}

function setAudioState(value) {
  if (typeof document !== "undefined") {
    document.documentElement.dataset.sfxAudioState = value;
  }
}

function recordCue(cueName) {
  if (typeof document === "undefined") {
    return;
  }
  playCount += 1;
  document.documentElement.dataset.sfxLastCue = cueName;
  document.documentElement.dataset.sfxPlayCount = String(playCount);
}

function isDisabledTarget(target) {
  try {
    return (
      target.matches?.(":disabled") ||
      target.getAttribute?.("aria-disabled") === "true" ||
      target.dataset?.disabled === "true" ||
      target.dataset?.enabled === "false"
    );
  } catch {
    return false;
  }
}

function handleDelegatedClick(event) {
  // Keyboard activation is trusted with detail=0; pointer activation has
  // detail>0. Programmatic element.click() is untrusted with detail=0.
  if (!event.isTrusted && event.detail === 0) {
    return;
  }

  const target = event.target?.closest?.(INTERACTIVE_SELECTOR);
  if (!target) {
    return;
  }

  if (target.id === TOGGLE_ID) {
    setMuted(!muted);
    if (!muted) {
      playSfx("confirm", { allowContextCreation: true });
    }
    return;
  }

  if (muted) {
    return;
  }

  const cueName = inferSfxCue(target);
  if (cueName) {
    playSfx(cueName, { allowContextCreation: true });
  }
}

function readMutedPreference() {
  try {
    return window.localStorage.getItem(SFX_STORAGE_KEY) === "true";
  } catch {
    return false;
  }
}

function storeMutedPreference() {
  try {
    window.localStorage.setItem(SFX_STORAGE_KEY, String(muted));
  } catch {
    // Storage denial is a silent, non-blocking fallback.
  }
}

function setMuted(nextMuted) {
  muted = Boolean(nextMuted);
  document.documentElement.dataset.sfxMuted = String(muted);
  storeMutedPreference();
  renderToggle();
}

function renderToggle() {
  if (!toggleEl) {
    return;
  }

  toggleEl.dataset.muted = String(muted);
  toggleEl.setAttribute("aria-pressed", String(muted));
  toggleEl.setAttribute("aria-label", muted ? "音效已靜音；按下可開啟音效" : "音效已開啟；按下可靜音");
  toggleEl.title = muted ? "開啟音效" : "靜音";
  toggleEl.querySelector(".sfx-toggle-icon").textContent = muted ? "🔇" : "🔊";
  toggleEl.querySelector(".sfx-toggle-label").textContent = muted ? "靜音" : "音效";
}

function createToggle() {
  toggleEl = document.createElement("button");
  toggleEl.id = TOGGLE_ID;
  toggleEl.className = "sfx-toggle";
  toggleEl.type = "button";
  toggleEl.innerHTML =
    '<span class="sfx-toggle-icon" aria-hidden="true"></span><span class="sfx-toggle-label"></span>';
  document.body.append(toggleEl);
  renderToggle();
}

function initializeSfx() {
  muted = readMutedPreference();
  document.documentElement.dataset.sfxMuted = String(muted);
  setAudioState("idle");
  createToggle();
  document.addEventListener("click", handleDelegatedClick);
}

if (typeof window !== "undefined" && typeof document !== "undefined") {
  initializeSfx();
}
