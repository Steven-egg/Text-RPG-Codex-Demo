import assert from "node:assert/strict";
import { readFile, readdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const toolsDir = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(toolsDir, "..");
const guiRoot = path.join(repoRoot, "07_gui_prototype");
const sfxModulePath = path.join(guiRoot, "shared", "sfx.js");
const sfxCssPath = path.join(guiRoot, "shared", "sfx.css");
const worldMapModulePath = path.join(guiRoot, "world_map", "world-map.js");
const expectedCues = ["ui_click", "confirm", "back", "warning", "victory"];
const expectedScreens = [
  "combat_screen",
  "dungeon_exploration",
  "guild_screen",
  "inn_screen",
  "magic_shop_screen",
  "relic_preview_screen",
  "shop_screen",
  "start_screen",
  "storage_screen",
  "synthesis_screen",
  "temple_screen",
  "town_hub",
  "workshop_screen",
  "world_map",
];

const moduleSource = await readFile(sfxModulePath, "utf8");
const cssSource = await readFile(sfxCssPath, "utf8");
const worldMapSource = await readFile(worldMapModulePath, "utf8");
const moduleUrl = `${pathToFileURL(sfxModulePath).href}?focused-test=${Date.now()}`;
const sfx = await import(moduleUrl);

assert.equal(sfx.SFX_STORAGE_KEY, "element_maze.sfx_enabled");
assert.equal(sfx.LEGACY_SFX_MUTED_STORAGE_KEY, "element_maze.sfx_muted");
assert.equal(sfx.isSfxEnabled(), true, "SFX must default to enabled");
assert.deepEqual([...sfx.SFX_CUE_NAMES], expectedCues);
assert.deepEqual(Object.keys(sfx.SFX_CUE_DEFINITIONS), expectedCues);
assert.ok(sfx.SFX_MAX_VOLUME <= 0.22, "SFX volume cap must not exceed 0.22");

for (const [cueName, notes] of Object.entries(sfx.SFX_CUE_DEFINITIONS)) {
  assert.ok(notes.length > 0, `${cueName} must contain at least one generated note`);
  for (const note of notes) {
    assert.ok(note.gain <= sfx.SFX_MAX_VOLUME, `${cueName} note exceeds the volume cap`);
    assert.ok(note.duration > 0 && note.start + note.duration <= 0.4, `${cueName} must remain a short cue`);
  }
}

function fakeTarget({ id = "", className = "", dataset = {}, attributes = {}, disabled = false, victory = false }) {
  return {
    id,
    className,
    dataset,
    closest(selector) {
      if (selector === '[data-outcome="victory"]' && victory) return this;
      return null;
    },
    getAttribute(name) {
      return attributes[name] ?? null;
    },
    matches(selector) {
      return selector === ":disabled" ? disabled : false;
    },
  };
}

assert.equal(sfx.inferSfxCue(fakeTarget({ className: "quiet-button" })), "ui_click");
assert.equal(sfx.inferSfxCue(fakeTarget({ className: "primary-action" })), "confirm");
assert.equal(sfx.inferSfxCue(fakeTarget({ id: "registration-back" })), "back");
assert.equal(sfx.inferSfxCue(fakeTarget({ attributes: { "aria-disabled": "true" } })), "warning");
assert.equal(sfx.inferSfxCue(fakeTarget({ disabled: true, victory: true })), "victory");

const gestureStats = { created: 0, resumed: 0, started: 0 };
const fakeAudioParam = {
  setValueAtTime() {},
  exponentialRampToValueAtTime() {},
  linearRampToValueAtTime() {},
};
class GestureAudioContext {
  constructor() {
    gestureStats.created += 1;
    this.state = "suspended";
    this.currentTime = 0;
    this.destination = {};
  }

  resume() {
    gestureStats.resumed += 1;
    this.state = "running";
    return Promise.resolve();
  }

  createOscillator() {
    return {
      frequency: fakeAudioParam,
      connect() {},
      start() {
        gestureStats.started += 1;
      },
      stop() {},
    };
  }

  createGain() {
    return { gain: fakeAudioParam, connect() {} };
  }
}

const windowBeforeGestureTest = globalThis.window;
globalThis.window = { AudioContext: GestureAudioContext };
const gestureSfx = await import(`${pathToFileURL(sfxModulePath).href}?gesture-test=${Date.now()}`);
const gestureTarget = fakeTarget({ className: "quiet-button" });
const closestForCueInference = gestureTarget.closest;
gestureTarget.closest = function closest(selector) {
  if (selector.startsWith("button,")) return this;
  return closestForCueInference.call(this, selector);
};

gestureSfx.handleDelegatedClick({ isTrusted: false, detail: 2, target: gestureTarget });
await Promise.resolve();
assert.deepEqual(gestureStats, { created: 0, resumed: 0, started: 0 }, "Untrusted pointer click must no-op");

gestureSfx.handleDelegatedClick({ isTrusted: true, detail: 1, target: gestureTarget });
await Promise.resolve();
await Promise.resolve();
assert.equal(gestureStats.created, 1, "Trusted pointer click must create AudioContext once");
assert.equal(gestureStats.resumed, 1, "Trusted pointer click must resume suspended AudioContext");
assert.equal(gestureStats.started, 1, "Trusted pointer click must schedule one ui_click note");

gestureSfx.handleDelegatedClick({ isTrusted: false, detail: 9, target: gestureTarget });
await Promise.resolve();
assert.equal(gestureStats.started, 1, "Untrusted detail>0 click must not record another cue");

gestureSfx.handleDelegatedClick({ isTrusted: true, detail: 0, target: gestureTarget });
await Promise.resolve();
assert.equal(gestureStats.started, 2, "Trusted keyboard click must schedule its cue");

if (windowBeforeGestureTest === undefined) {
  delete globalThis.window;
} else {
  globalThis.window = windowBeforeGestureTest;
}

assert.equal(
  (moduleSource.match(/document\.addEventListener\(\s*["']click["']/g) ?? []).length,
  1,
  "SFX must use one delegated document click listener",
);
assert.match(moduleSource, /event\.isTrusted/, "Audio initialization must be gated by a trusted user gesture");
assert.match(moduleSource, /if \(!event\.isTrusted\)\s*\{\s*return;/, "Every untrusted click must no-op");
assert.match(moduleSource, /window\.AudioContext\s*\?\?\s*window\.webkitAudioContext/);
assert.match(moduleSource, /dataset\.sfxPlayCount/, "Browser checks need a non-gameplay cue counter");
assert.match(moduleSource, /aria-label/);
assert.match(moduleSource, /aria-pressed/);
assert.match(moduleSource, /window\.localStorage\.getItem\(SFX_STORAGE_KEY\)/);
assert.match(moduleSource, /window\.localStorage\.setItem\(SFX_STORAGE_KEY, String\(enabled\)\)/);
assert.match(moduleSource, /window\.localStorage\.removeItem\(LEGACY_SFX_MUTED_STORAGE_KEY\)/);
assert.doesNotMatch(worldMapSource, /sfx_muted|settings-sfx-muted|isSfxMuted|setSfxMuted/);
assert.match(worldMapSource, /sfx_enabled:\s*isSfxEnabled\(\)/);
assert.match(worldMapSource, /preview\.data\.sfx_enabled\s*\?\s*"checked"/);
assert.match(worldMapSource, /setSfxEnabled\(sfxEnabledEl\.checked\)/);
assert.doesNotMatch(moduleSource, /save\.json|sessionStorage|indexedDB/i);
assert.match(cssSource, /\.sfx-toggle:focus-visible/);
assert.match(cssSource, /position:\s*fixed/);
assert.match(cssSource, /\.sfx-toggle\[data-enabled="false"\]/);
assert.doesNotMatch(cssSource, /data-muted/);
const toggleRule = cssSource.match(/\.sfx-toggle\s*\{([\s\S]*?)\}/)?.[1] ?? "";
const toggleZIndex = Number(toggleRule.match(/z-index:\s*(\d+)/)?.[1]);
assert.ok(Number.isFinite(toggleZIndex) && toggleZIndex < 9999, "SFX toggle must remain below story overlay z-index 9999");

const actualScreens = [];
for (const entry of await readdir(guiRoot, { withFileTypes: true })) {
  if (!entry.isDirectory() || entry.name === "shared") {
    continue;
  }
  try {
    const htmlPath = path.join(guiRoot, entry.name, "index.html");
    const html = await readFile(htmlPath, "utf8");
    actualScreens.push(entry.name);
    assert.equal((html.match(/\.\.\/shared\/sfx\.css/g) ?? []).length, 1, `${entry.name} must load sfx.css once`);
    assert.equal((html.match(/\.\.\/shared\/sfx\.js/g) ?? []).length, 1, `${entry.name} must load sfx.js once`);
    assert.doesNotMatch(html, /<(audio|source)\b/i, `${entry.name} must not add binary audio markup`);
  } catch (error) {
    if (error?.code !== "ENOENT") {
      throw error;
    }
  }
}

assert.deepEqual(actualScreens.sort(), expectedScreens);

const previousMigrationWindow = globalThis.window;
const previousMigrationDocument = globalThis.document;
const preferenceStore = new Map([["element_maze.sfx_muted", "true"]]);
globalThis.window = {
  localStorage: {
    getItem(key) { return preferenceStore.has(key) ? preferenceStore.get(key) : null; },
    setItem(key, value) { preferenceStore.set(key, value); },
    removeItem(key) { preferenceStore.delete(key); },
  },
};
globalThis.document = {
  documentElement: { dataset: {} },
  addEventListener() {},
};
const migratedSfx = await import(`${pathToFileURL(sfxModulePath).href}?migration-test=${Date.now()}`);
assert.equal(migratedSfx.isSfxEnabled(), false, "legacy muted=true must migrate to enabled=false");
assert.equal(preferenceStore.get("element_maze.sfx_enabled"), "false");
assert.equal(preferenceStore.has("element_maze.sfx_muted"), false);
migratedSfx.setSfxEnabled(true);
assert.equal(migratedSfx.isSfxEnabled(), true);
assert.equal(preferenceStore.get("element_maze.sfx_enabled"), "true");
if (previousMigrationWindow === undefined) delete globalThis.window;
else globalThis.window = previousMigrationWindow;
if (previousMigrationDocument === undefined) delete globalThis.document;
else globalThis.document = previousMigrationDocument;

const previousWindow = globalThis.window;
globalThis.window = {
  AudioContext: class RejectedAudioContext {
    constructor() {
      throw new Error("AudioContext denied for focused fallback test");
    }
  },
};
let fallbackActionRan = false;
assert.doesNotThrow(() => {
  sfx.playSfx("ui_click", { allowContextCreation: true });
  fallbackActionRan = true;
});
assert.equal(fallbackActionRan, true, "AudioContext rejection must not block the underlying action");
if (previousWindow === undefined) {
  delete globalThis.window;
} else {
  globalThis.window = previousWindow;
}

console.log(`GUI SFX focused test passed: ${expectedCues.length} cues, ${actualScreens.length} screens.`);
