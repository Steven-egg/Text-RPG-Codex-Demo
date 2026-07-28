export async function presentStoryBeat(storyBeat) {
  if (!storyBeat || typeof storyBeat !== "object") return Promise.resolve();

  // Exactly 6 fields
  const STORY_BEAT_KEYS = ["id", "kind", "title", "lines", "dismiss_label", "tone"];
  const keys = Object.keys(storyBeat);
  if (keys.length !== 6 || !STORY_BEAT_KEYS.every(k => keys.includes(k))) {
    return Promise.resolve();
  }

  const { id, kind, title, lines, dismiss_label, tone } = storyBeat;

  if (typeof id !== "string" || id.trim() === "") return Promise.resolve();
  if (typeof title !== "string" || title.trim() === "") return Promise.resolve();
  if (typeof dismiss_label !== "string" || dismiss_label.trim() === "") return Promise.resolve();

  if (!Array.isArray(lines) || lines.length === 0) return Promise.resolve();
  for (const line of lines) {
    if (typeof line !== "string" || line.trim() === "") return Promise.resolve();
  }

  const validKinds = ["prologue", "region_transition", "boss_before", "boss_after", "ending"];
  const validTones = ["neutral", "warning", "victory", "ending"];

  if (!validKinds.includes(kind)) return Promise.resolve();
  if (!validTones.includes(tone)) return Promise.resolve();

  return new Promise((resolve) => {
    const overlay = document.createElement("div");
    overlay.className = "story-beat-overlay";
    overlay.dataset.tone = storyBeat.tone || "neutral";
    overlay.dataset.kind = storyBeat.kind || "region_transition";

    const dialog = document.createElement("section");
    dialog.className = "story-beat-dialog";
    dialog.setAttribute("role", "dialog");
    dialog.setAttribute("aria-modal", "true");
    dialog.setAttribute("aria-label", storyBeat.title || "Story Beat");

    const header = document.createElement("header");
    header.className = "story-beat-header";
    const titleEl = document.createElement("h2");
    titleEl.textContent = storyBeat.title || "";
    header.appendChild(titleEl);
    dialog.appendChild(header);

    const body = document.createElement("div");
    body.className = "story-beat-body";
    (storyBeat.lines || []).forEach(line => {
      const p = document.createElement("p");
      p.className = "story-beat-line";
      p.textContent = line;
      body.appendChild(p);
    });
    dialog.appendChild(body);

    const footer = document.createElement("footer");
    footer.className = "story-beat-footer";
    const dismissBtn = document.createElement("button");
    dismissBtn.type = "button";
    dismissBtn.className = "story-beat-dismiss";
    dismissBtn.textContent = storyBeat.dismiss_label || "繼續";
    footer.appendChild(dismissBtn);
    dialog.appendChild(footer);

    overlay.appendChild(dialog);
    document.body.appendChild(overlay);

    const previousFocus = document.activeElement;

    // Simple focus trap
    const focusableEls = dialog.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])');
    const firstFocusableEl = focusableEls[0];
    const lastFocusableEl = focusableEls[focusableEls.length - 1];

    function handleKeyDown(e) {
      if (e.key === "Tab") {
        if (e.shiftKey && document.activeElement === firstFocusableEl) {
          e.preventDefault();
          lastFocusableEl?.focus();
        } else if (!e.shiftKey && document.activeElement === lastFocusableEl) {
          e.preventDefault();
          firstFocusableEl?.focus();
        }
      } else if (e.key === "Escape") {
        if (storyBeat.kind !== "ending") {
          e.preventDefault();
          closeBeat();
        }
      }
    }

    function closeBeat() {
      dismissBtn.removeEventListener("click", closeBeat);
      document.removeEventListener("keydown", handleKeyDown);
      overlay.remove();
      if (previousFocus) {
        previousFocus.focus();
      }
      resolve();
    }

    dismissBtn.addEventListener("click", closeBeat);
    document.addEventListener("keydown", handleKeyDown);

    // Initial focus
    dismissBtn.focus();
  });
}

// Inject default styles for the story beat overlay to be self-contained,
// though specific screens can override in their styles.css.
const style = document.createElement("style");
style.textContent = `
.story-beat-overlay {
  position: fixed;
  inset: 0;
  z-index: 9999;
  background-color: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  backdrop-filter: blur(4px);
  animation: story-beat-fade-in 0.2s ease-out;
}
.story-beat-dialog {
  background-color: #1a1a1a;
  color: #f0f0f0;
  border: 1px solid #444;
  border-radius: 8px;
  max-width: 600px;
  width: 100%;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.6);
  display: flex;
  flex-direction: column;
}
.story-beat-overlay[data-tone="warning"] .story-beat-dialog { border-color: #c0392b; }
.story-beat-overlay[data-tone="victory"] .story-beat-dialog { border-color: #27ae60; }
.story-beat-overlay[data-tone="ending"] .story-beat-dialog { border-color: #f39c12; }

.story-beat-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid #333;
}
.story-beat-header h2 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: #fff;
  letter-spacing: 0.05em;
}
.story-beat-body {
  padding: 1.5rem;
  max-height: 60vh;
  overflow-y: auto;
  font-size: 1.05rem;
  line-height: 1.6;
}
.story-beat-line {
  margin: 0 0 1rem 0;
}
.story-beat-line:last-child {
  margin-bottom: 0;
}
.story-beat-footer {
  padding: 1.25rem 1.5rem;
  border-top: 1px solid #333;
  display: flex;
  justify-content: flex-end;
}
.story-beat-dismiss {
  background-color: #333;
  color: #fff;
  border: 1px solid #555;
  padding: 0.5rem 1.25rem;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.15s, border-color 0.15s;
}
.story-beat-dismiss:hover, .story-beat-dismiss:focus {
  background-color: #444;
  border-color: #888;
  outline: none;
}
.story-beat-overlay[data-tone="warning"] .story-beat-dismiss { background-color: #5a1a14; border-color: #c0392b; }
.story-beat-overlay[data-tone="victory"] .story-beat-dismiss { background-color: #114022; border-color: #27ae60; }
.story-beat-overlay[data-tone="ending"] .story-beat-dismiss { background-color: #634007; border-color: #f39c12; }
.story-beat-overlay[data-tone="warning"] .story-beat-dismiss:hover, .story-beat-overlay[data-tone="warning"] .story-beat-dismiss:focus { background-color: #c0392b; }
.story-beat-overlay[data-tone="victory"] .story-beat-dismiss:hover, .story-beat-overlay[data-tone="victory"] .story-beat-dismiss:focus { background-color: #27ae60; }
.story-beat-overlay[data-tone="ending"] .story-beat-dismiss:hover, .story-beat-overlay[data-tone="ending"] .story-beat-dismiss:focus { background-color: #f39c12; }

@keyframes story-beat-fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
`;
document.head.appendChild(style);
