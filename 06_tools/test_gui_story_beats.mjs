import { test, describe } from "node:test";
import assert from "node:assert";

// Basic DOM Mock for testing presentStoryBeat
class MockElement {
  constructor(tag) {
    this.tag = tag;
    this.className = "";
    this.dataset = {};
    this.children = [];
    this.attributes = {};
    this.textContent = "";
    this.style = {};
    this.eventListeners = {};
  }
  appendChild(child) {
    this.children.push(child);
  }
  setAttribute(name, value) {
    this.attributes[name] = value;
  }
  addEventListener(type, listener) {
    this.eventListeners[type] = listener;
  }
  removeEventListener(type, listener) {
    if (this.eventListeners[type] === listener) {
      delete this.eventListeners[type];
    }
  }
  remove() {
    this.isRemoved = true;
  }
  focus() {
    this.isFocused = true;
  }
  querySelectorAll() {
    return [new MockElement("button")]; // minimal mock for focus trap
  }
}

global.document = {
  createElement: (tag) => new MockElement(tag),
  body: new MockElement("body"),
  head: new MockElement("head"),
  activeElement: new MockElement("button"),
  addEventListener: () => {},
  removeEventListener: () => {},
};

global.window = {
  setTimeout: (fn) => fn(),
};

describe("GUI Story Beats Logic", () => {
  test("strict contract - requires 6 fields to render", async () => {
    const { presentStoryBeat } = await import("../07_gui_prototype/shared/story-beat.js");
    let beatPromise = presentStoryBeat({
      id: "beat_01",
      kind: "region_transition",
      title: "Valid Title",
      lines: ["Line 1", "Line 2"],
      dismiss_label: "Continue",
      tone: "neutral"
    });

    let overlay = document.body.children.find(c => c.className === "story-beat-overlay" && !c.isRemoved);
    assert.ok(overlay, "Overlay should be added to DOM when payload is completely valid");

    const dismissBtn = overlay.children[0].children[2].children[0];
    dismissBtn.eventListeners["click"]();
    await beatPromise;
  });

  test("null or invalid payload safe no-op", async () => {
    const { presentStoryBeat } = await import("../07_gui_prototype/shared/story-beat.js");

    await presentStoryBeat(null);
    await presentStoryBeat(undefined);
    await presentStoryBeat({});
    await presentStoryBeat({ title: "Only Title" }); // missing others
    await presentStoryBeat({ lines: ["Only Lines"] });
    await presentStoryBeat({ id: "id", kind: "k", title: "t", lines: [], dismiss_label: "d", tone: "t" }); // empty lines
    await presentStoryBeat("invalid");

    // Invalid enums
    await presentStoryBeat({ id: "id", kind: "invalid_kind", title: "t", lines: ["line"], dismiss_label: "d", tone: "neutral" });
    await presentStoryBeat({ id: "id", kind: "boss_after", title: "t", lines: ["line"], dismiss_label: "d", tone: "invalid_tone" });

    // Invalid types (e.g. non-string fields)
    await presentStoryBeat({ id: 123, kind: "boss_after", title: "t", lines: ["line"], dismiss_label: "d", tone: "neutral" });
    await presentStoryBeat({ id: "id", kind: "boss_after", title: "t", lines: [123], dismiss_label: "d", tone: "neutral" });
    await presentStoryBeat({ id: "id", kind: "boss_after", title: "t", lines: ["line"], dismiss_label: "d", tone: "neutral", extra_field: true });

    const overlays = document.body.children.filter(c => c.className === "story-beat-overlay" && !c.isRemoved);
    assert.strictEqual(overlays.length, 0, "No overlay should be created for invalid payloads");
  });

  test("pure text processing (no innerHTML)", async () => {
    const { presentStoryBeat } = await import("../07_gui_prototype/shared/story-beat.js");
    let beatPromise = presentStoryBeat({
      id: "beat_02",
      kind: "boss_after",
      title: "<h1>Danger!</h1>",
      lines: ["<script>alert(1)</script>", "<b>Bold</b> text"],
      dismiss_label: "OK",
      tone: "warning"
    });

    const overlay = document.body.children.find(c => c.className === "story-beat-overlay" && !c.isRemoved);
    const dialog = overlay.children[0];
    const header = dialog.children[0];
    const body = dialog.children[1];

    // Verify textContent is used (HTML tags are escaped as text)
    assert.strictEqual(header.children[0].textContent, "<h1>Danger!</h1>");
    assert.strictEqual(body.children[0].textContent, "<script>alert(1)</script>");
    assert.strictEqual(body.children[1].textContent, "<b>Bold</b> text");

    const dismissBtn = dialog.children[2].children[0];
    dismissBtn.eventListeners["click"]();
    await beatPromise;
  });

  test("regression: queueing, result overlay closing, boss-after -> ending -> navigation", async () => {
    const { presentStoryBeat } = await import("../07_gui_prototype/shared/story-beat.js");
    let navigated = false;
    let resultOverlayOpen = true; // start with result overlay open

    const state = {
      resultOpen: true,
      pendingStoryBeat: null
    };

    const bossAfterBeat = { id: "b1", kind: "boss_after", title: "Boss After", lines: ["text"], dismiss_label: "ok", tone: "neutral" };
    const endingBeat = { id: "b2", kind: "ending", title: "Ending", lines: ["text"], dismiss_label: "ok", tone: "ending" };

    // Simulating dispatchRuntimeAction when boss is defeated
    function simulateCombatResponse(resultBeat) {
      if (state.resultOpen) {
        state.pendingStoryBeat = resultBeat; // result overlay 開啟時只保存 pending beat
      } else {
        return presentStoryBeat(resultBeat);
      }
    }

    // Step 1: Server returns result_overlay and boss-after
    simulateCombatResponse(bossAfterBeat);

    // Assert result overlay is still open and beat is pending
    assert.strictEqual(state.resultOpen, true);
    assert.deepStrictEqual(state.pendingStoryBeat, bossAfterBeat);
    let overlays = document.body.children.filter(c => c.className === "story-beat-overlay" && !c.isRemoved);
    assert.strictEqual(overlays.length, 0, "Story beat should not render while result overlay is open");

    // Step 2: User clicks "Next" on result overlay
    // Simulate activateResultNextAction()
    async function activateResultNextAction() {
      // 點下一步後先關閉 result overlay
      state.resultOpen = false;

      if (state.pendingStoryBeat) {
        const beat = state.pendingStoryBeat;
        state.pendingStoryBeat = null;
        await presentStoryBeat(beat); // waits for user to dismiss
      }

      // Simulate backend call that returns ending beat
      await presentStoryBeat(endingBeat); // wait for user to dismiss

      // Finally navigate
      navigated = true;
    }

    const actionPromise = activateResultNextAction();

    // Wait a tick to let the first beat (boss-after) render
    await new Promise(r => setTimeout(r, 10));

    assert.strictEqual(state.resultOpen, false, "Result overlay must be closed before showing boss-after");

    let activeBeat = document.body.children.find(c => c.className === "story-beat-overlay" && !c.isRemoved);
    assert.ok(activeBeat);
    assert.strictEqual(activeBeat.dataset.kind, "boss_after", "Should show boss-after beat first");
    assert.strictEqual(navigated, false, "Must not navigate while boss-after is open");

    // Step 3: Dismiss boss-after
    let dismissBtn = activeBeat.children[0].children[2].children[0];
    dismissBtn.eventListeners["click"]();

    // Wait a tick for the ending beat to render
    await new Promise(r => setTimeout(r, 10));

    activeBeat = document.body.children.find(c => c.className === "story-beat-overlay" && !c.isRemoved);
    assert.ok(activeBeat);
    assert.strictEqual(activeBeat.dataset.kind, "ending", "Should show ending beat next");
    assert.strictEqual(navigated, false, "Must not navigate while ending is open");

    // Step 4: Dismiss ending
    dismissBtn = activeBeat.children[0].children[2].children[0];
    dismissBtn.eventListeners["click"]();

    await actionPromise;
    assert.strictEqual(navigated, true, "Should navigate only after all beats are dismissed");
  });
});
