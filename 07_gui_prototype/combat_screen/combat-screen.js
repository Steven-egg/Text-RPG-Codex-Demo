import { runtimeClient } from "../shared/runtime-client.js";

const fixtureSelect = document.querySelector("#fixture-select");
const shellEl = document.querySelector(".combat-shell");
const titleEl = document.querySelector("#screen-title");
const subtitleEl = document.querySelector("#screen-subtitle");
const resourceStripEl = document.querySelector("#resource-strip");
const enemyNameEl = document.querySelector("#enemy-name");
const enemyHpFillEl = document.querySelector("#enemy-hp-fill");
const enemyHpLabelEl = document.querySelector("#enemy-hp-label");
const enemyMetaEl = document.querySelector("#enemy-meta");
const playerNameEl = document.querySelector("#player-name");
const playerFocusStatsEl = document.querySelector("#player-focus-stats");
const battleLogEl = document.querySelector("#battle-log");
const logModeLabelEl = document.querySelector("#log-mode-label");
const toggleBattleLogEl = document.querySelector("#toggle-battle-log");
const combatFooterEl = document.querySelector(".combat-footer");
const commandMessageEl = document.querySelector("#command-message");
const commandRowEl = document.querySelector("#command-row");
const submenuPanelEl = document.querySelector("#command-submenu");
const submenuLabelEl = document.querySelector("#submenu-label");
const submenuTitleEl = document.querySelector("#submenu-title");
const submenuSummaryEl = document.querySelector("#submenu-summary");
const submenuListEl = document.querySelector("#submenu-list");
const resultOverlayEl = document.querySelector("#result-overlay");
const resultLabelEl = document.querySelector("#result-label");
const resultTitleEl = document.querySelector("#result-title");
const resultStatusEl = document.querySelector("#result-status");
const resultSummaryEl = document.querySelector("#result-summary");
const resultRewardTitleEl = document.querySelector("#result-reward-title");
const resultLinesEl = document.querySelector("#result-lines");
const resultNextActionEl = document.querySelector("#result-next-action");
const actionLogEl = document.querySelector("#action-log");
const clearLogEl = document.querySelector("#clear-log");
const enemyImageEl = document.querySelector("#enemy-image");

const COMBAT_ENEMY_VISUALS = Object.freeze({
  mon_cinder_bat: {
    imageSrc: "./assets/monsters/transparent/mon-cinder-bat-v01.png",
    environment: "ember-quarry",
    role: "flying",
  },
  mon_lava_imp: {
    imageSrc: "./assets/monsters/transparent/mon-lava-imp-v01.png",
    environment: "ember-quarry",
    role: "small-ground",
  },
  mon_scorched_guard: {
    imageSrc: "./assets/monsters/transparent/mon-scorched-guard-v01.png",
    environment: "ember-quarry",
    role: "ground",
  },
  boss_glen: {
    imageSrc: "./assets/monsters/transparent/boss-glen-v01.png",
    environment: "ember-quarry",
    role: "boss",
  },
  mon_moss_rat: {
    imageSrc: "./assets/monsters/transparent/mon-moss-rat-v01.png",
    environment: "moss-cave",
    role: "small-ground",
  },
  mon_cave_slug: {
    imageSrc: "./assets/monsters/transparent/mon-cave-slug-v01.png",
    environment: "moss-cave",
    role: "low-wide",
  },
  mon_cracked_golem: {
    imageSrc: "./assets/monsters/transparent/mon-cracked-golem-v01.png",
    environment: "moss-cave",
    role: "ground",
  },
  mon_ash_imp: {
    imageSrc: "./assets/monsters/transparent/mon-ash-imp-v01.png",
    environment: "ash-ravine",
    role: "small-ground",
  },
  mon_lava_bat: {
    imageSrc: "./assets/monsters/transparent/mon-lava-bat-v01.png",
    environment: "ash-ravine",
    role: "flying",
  },
  mon_cinder_soldier: {
    imageSrc: "./assets/monsters/transparent/mon-cinder-soldier-v01.png",
    environment: "ash-ravine",
    role: "ground",
  },
  boss_ash_guardian: {
    imageSrc: "./assets/monsters/transparent/boss-ash-guardian-v01.png",
    environment: "ash-ravine",
    role: "boss-heavy",
  },
  mon_ember_stalker: {
    imageSrc: "./assets/monsters/transparent/mon-ember-stalker-v01.png",
    environment: "cinder-seal-depths",
    role: "low-wide",
  },
  mon_molten_shell: {
    imageSrc: "./assets/monsters/transparent/mon-molten-shell-v01.png",
    environment: "cinder-seal-depths",
    role: "low-wide",
  },
  mon_cinder_brand_wisp: {
    imageSrc: "./assets/monsters/transparent/mon-cinder-brand-wisp-v01.png",
    environment: "cinder-seal-depths",
    role: "floating",
  },
  boss_cinder_seal_sentinel: {
    imageSrc: "./assets/monsters/transparent/boss-cinder-seal-sentinel-v01.png",
    environment: "cinder-seal-depths",
    role: "boss-tall",
  },
  mon_ice_drowned_deckhand: {
    imageSrc: "./assets/monsters/transparent/mon-ice-drowned-deckhand-v01.png",
    environment: "ice-minor-a",
    role: "ground",
  },
  mon_ice_bilge_crab: {
    imageSrc: "./assets/monsters/transparent/mon-ice-bilge-crab-v01.png",
    environment: "ice-minor-a",
    role: "ground",
  },
  mon_ice_salt_wisp: {
    imageSrc: "./assets/monsters/transparent/mon-ice-salt-wisp-v01.png",
    environment: "ice-minor-a",
    role: "floating",
  },
  mon_ice_ghost_sail: {
    imageSrc: "./assets/monsters/transparent/mon-ice-ghost-sail-v01.png",
    environment: "ice-minor-a",
    role: "floating",
  },
  boss_ice_wreck_captain: {
    imageSrc: "./assets/monsters/transparent/boss-ice-wreck-captain-v01.png",
    environment: "ice-minor-a",
    role: "boss",
  },
  mon_ice_frostroot_lurker: {
    imageSrc: "./assets/monsters/transparent/mon-ice-frostroot-lurker-v01.png",
    environment: "ice-minor-b",
    role: "low-wide",
  },
  mon_ice_cave_mite: {
    imageSrc: "./assets/monsters/transparent/mon-ice-cave-mite-v01.png",
    environment: "ice-minor-b",
    role: "ground",
  },
  mon_ice_rime_bloom: {
    imageSrc: "./assets/monsters/transparent/mon-ice-rime-bloom-v01.png",
    environment: "ice-minor-b",
    role: "low-wide",
  },
  mon_ice_stone_shell: {
    imageSrc: "./assets/monsters/transparent/mon-ice-stone-shell-v01.png",
    environment: "ice-minor-b",
    role: "low-wide",
  },
  boss_ice_frostroot_keeper: {
    imageSrc: "./assets/monsters/transparent/boss-ice-frostroot-keeper-v01.png",
    environment: "ice-minor-b",
    role: "boss-heavy",
  },
  mon_ice_outer_guard: {
    imageSrc: "./assets/monsters/transparent/mon-ice-outer-guard-v01.png",
    environment: "ice-main-phase-1",
    role: "ground",
  },
  mon_ice_rime_hound: {
    imageSrc: "./assets/monsters/transparent/mon-ice-rime-hound-v01.png",
    environment: "ice-main-phase-1",
    role: "ground",
  },
  mon_ice_frost_armor: {
    imageSrc: "./assets/monsters/transparent/mon-ice-frost-armor-v01.png",
    environment: "ice-main-phase-1",
    role: "ground",
  },
  mon_ice_seal_spark: {
    imageSrc: "./assets/monsters/transparent/mon-ice-seal-spark-v02.png",
    environment: "ice-main-phase-1",
    role: "floating",
  },
  boss_ice_outer_gatewarden: {
    imageSrc: "./assets/monsters/transparent/boss-ice-outer-gatewarden-v01.png",
    environment: "ice-main-phase-1",
    role: "boss-heavy",
  },
  mon_ice_palace_wisp: {
    imageSrc: "./assets/monsters/transparent/mon-ice-palace-wisp-v01.png",
    environment: "ice-main-phase-2",
    role: "ground",
  },
  mon_ice_throne_shade: {
    imageSrc: "./assets/monsters/transparent/mon-ice-throne-shade-v01.png",
    environment: "ice-main-phase-2",
    role: "floating",
  },
  mon_ice_seal_knight: {
    imageSrc: "./assets/monsters/transparent/mon-ice-seal-knight-v01.png",
    environment: "ice-main-phase-2",
    role: "boss-heavy",
  },
  mon_ice_core_sentry: {
    imageSrc: "./assets/monsters/transparent/mon-ice-core-sentry-v02.png",
    environment: "ice-main-phase-2",
    role: "ground",
  },
  boss_ice_final_seal_lord: {
    imageSrc: "./assets/monsters/transparent/boss-ice-final-seal-lord-v01.png",
    environment: "ice-main-phase-2",
    role: "boss-tall",
  },
  mon_earth_rootling_scavenger: {
    imageSrc: "./assets/monsters/transparent/mon-earth-rootling-scavenger-v01.png",
    environment: "earth-minor-a",
    role: "small-ground",
  },
  mon_earth_moss_hound: {
    imageSrc: "./assets/monsters/transparent/mon-earth-moss-hound-v01.png",
    environment: "earth-minor-a",
    role: "low-wide",
  },
  mon_earth_spore_moth: {
    imageSrc: "./assets/monsters/transparent/mon-earth-spore-moth-v01.png",
    environment: "earth-minor-a",
    role: "flying",
  },
  boss_earth_rootwarden: {
    imageSrc: "./assets/monsters/transparent/boss-earth-rootwarden-v01.png",
    environment: "earth-minor-a",
    role: "boss-heavy",
  },
  mon_earth_quarry_mite: {
    imageSrc: "./assets/monsters/transparent/mon-earth-quarry-mite-v01.png",
    environment: "earth-minor-b",
    role: "small-ground",
  },
  mon_earth_stoneback_boar: {
    imageSrc: "./assets/monsters/transparent/mon-earth-stoneback-boar-v01.png",
    environment: "earth-minor-b",
    role: "low-wide",
  },
  mon_earth_fungal_sapper: {
    imageSrc: "./assets/monsters/transparent/mon-earth-fungal-sapper-v01.png",
    environment: "earth-minor-b",
    role: "ground",
  },
  mon_earth_ore_wisp: {
    imageSrc: "./assets/monsters/transparent/mon-earth-ore-wisp-v01.png",
    environment: "earth-minor-b",
    role: "floating",
  },
  boss_earth_quarry_colossus: {
    imageSrc: "./assets/monsters/transparent/boss-earth-quarry-colossus-v01.png",
    environment: "earth-minor-b",
    role: "boss-heavy",
  },
  mon_earth_leyline_guard: {
    imageSrc: "./assets/monsters/transparent/mon-earth-leyline-guard-v01.png",
    environment: "earth-main-phase-1",
    role: "ground",
  },
  mon_earth_root_bound_knight: {
    imageSrc: "./assets/monsters/transparent/mon-earth-root-bound-knight-v01.png",
    environment: "earth-main-phase-1",
    role: "ground",
  },
  mon_earth_seal_spore: {
    imageSrc: "./assets/monsters/transparent/mon-earth-seal-spore-v01.png",
    environment: "earth-main-phase-1",
    role: "floating",
  },
  boss_earth_outer_grovekeeper: {
    imageSrc: "./assets/monsters/transparent/boss-earth-outer-grovekeeper-v01.png",
    environment: "earth-main-phase-1",
    role: "boss-tall",
  },
  mon_earth_heartwood_shade: {
    imageSrc: "./assets/monsters/transparent/mon-earth-heartwood-shade-v01.png",
    environment: "earth-main-phase-2",
    role: "floating",
  },
  mon_earth_deep_core_sentry: {
    imageSrc: "./assets/monsters/transparent/mon-earth-deep-core-sentry-v01.png",
    environment: "earth-main-phase-2",
    role: "ground",
  },
  mon_earth_petrified_lasher: {
    imageSrc: "./assets/monsters/transparent/mon-earth-petrified-lasher-v01.png",
    environment: "earth-main-phase-2",
    role: "low-wide",
  },
  boss_earth_deep_leyline_lord: {
    imageSrc: "./assets/monsters/transparent/boss-earth-deep-leyline-lord-v01.png",
    environment: "earth-main-phase-2",
    role: "boss-tall",
  },
  mon_thunder_static_lizard: {
    imageSrc: "./assets/monsters/transparent/mon-thunder-static-lizard-v03.png",
    environment: "thunder-minor-a",
    role: "low-wide",
  },
  mon_thunder_plateau_runner: {
    imageSrc: "./assets/monsters/transparent/mon-thunder-plateau-runner-v03.png",
    environment: "thunder-minor-a",
    role: "low-wide",
  },
  mon_thunder_spark_wisp: {
    imageSrc: "./assets/monsters/transparent/mon-thunder-spark-wisp-v03.png",
    environment: "thunder-minor-a",
    role: "floating",
  },
  mon_thunder_glasswing: {
    imageSrc: "./assets/monsters/transparent/mon-thunder-glasswing-v03.png",
    environment: "thunder-minor-a",
    role: "flying",
  },
  boss_thunder_plateau_beacon: {
    imageSrc: "./assets/monsters/transparent/boss-thunder-plateau-beacon-v03.png",
    environment: "thunder-minor-a",
    role: "boss-tall",
  },
  mon_thunder_channel_eel: {
    imageSrc: "./assets/monsters/transparent/mon-thunder-channel-eel-v03.png",
    environment: "thunder-minor-b",
    role: "low-wide",
  },
  mon_thunder_copper_hound: {
    imageSrc: "./assets/monsters/transparent/mon-thunder-copper-hound-v03.png",
    environment: "thunder-minor-b",
    role: "low-wide",
  },
  mon_thunder_rail_sentry: {
    imageSrc: "./assets/monsters/transparent/mon-thunder-rail-sentry-v03.png",
    environment: "thunder-minor-b",
    role: "ground",
  },
  mon_thunder_cloud_mite: {
    imageSrc: "./assets/monsters/transparent/mon-thunder-cloud-mite-v03.png",
    environment: "thunder-minor-b",
    role: "small-ground",
  },
  boss_thunder_channel_keeper: {
    imageSrc: "./assets/monsters/transparent/boss-thunder-channel-keeper-v03.png",
    environment: "thunder-minor-b",
    role: "boss",
  },
  mon_thunder_array_guard: {
    imageSrc: "./assets/monsters/transparent/mon-thunder-array-guard-v03.png",
    environment: "thunder-main-phase-1",
    role: "ground",
  },
  mon_thunder_tower_lancer: {
    imageSrc: "./assets/monsters/transparent/mon-thunder-tower-lancer-v03.png",
    environment: "thunder-main-phase-1",
    role: "ground",
  },
  mon_thunder_seal_orb: {
    imageSrc: "./assets/monsters/transparent/mon-thunder-seal-orb-v03.png",
    environment: "thunder-main-phase-1",
    role: "floating",
  },
  boss_thunder_lower_array_warden: {
    imageSrc: "./assets/monsters/transparent/boss-thunder-lower-array-warden-v03.png",
    environment: "thunder-main-phase-1",
    role: "boss-heavy",
  },
  mon_thunder_crown_wisp: {
    imageSrc: "./assets/monsters/transparent/mon-thunder-crown-wisp-v03.png",
    environment: "thunder-main-phase-2",
    role: "floating",
  },
  mon_thunder_deep_core_sentry: {
    imageSrc: "./assets/monsters/transparent/mon-thunder-deep-core-sentry-v03.png",
    environment: "thunder-main-phase-2",
    role: "ground",
  },
  mon_thunder_stormbound_knight: {
    imageSrc: "./assets/monsters/transparent/mon-thunder-stormbound-knight-v03.png",
    environment: "thunder-main-phase-2",
    role: "ground",
  },
  boss_thunder_crown_storm_lord: {
    imageSrc: "./assets/monsters/transparent/boss-thunder-crown-storm-lord-v03.png",
    environment: "thunder-main-phase-2",
    role: "boss-tall",
  },
  mon_final_ash_echo: {
    imageSrc: "./assets/monsters/transparent/mon-final-ash-echo-regenerated-v02.png",
    environment: "final-minor-a",
    role: "ground",
  },
  mon_final_frost_echo: {
    imageSrc: "./assets/monsters/transparent/mon-final-frost-echo-regenerated-v01.png",
    environment: "final-minor-a",
    role: "ground",
  },
  mon_final_root_echo: {
    imageSrc: "./assets/monsters/transparent/mon-final-root-echo-regenerated-v01.png",
    environment: "final-minor-a",
    role: "ground",
  },
  mon_final_storm_echo: {
    imageSrc: "./assets/monsters/transparent/mon-final-storm-echo-regenerated-v01.png",
    environment: "final-minor-a",
    role: "flying",
  },
  boss_final_echo_vanguard: {
    imageSrc: "./assets/monsters/transparent/boss-final-echo-vanguard-regenerated-v02.png",
    environment: "final-minor-a",
    role: "boss",
  },
  mon_final_seal_larva: {
    imageSrc: "./assets/monsters/transparent/mon-final-seal-larva-regenerated-v01.png",
    environment: "final-minor-b",
    role: "low-wide",
  },
  mon_final_ruin_hound: {
    imageSrc: "./assets/monsters/transparent/mon-final-ruin-hound-regenerated-v01.png",
    environment: "final-minor-b",
    role: "low-wide",
  },
  mon_final_void_mite: {
    imageSrc: "./assets/monsters/transparent/mon-final-void-mite-regenerated-v01.png",
    environment: "final-minor-b",
    role: "small-ground",
  },
  mon_final_memory_sentry: {
    imageSrc: "./assets/monsters/transparent/mon-final-memory-sentry-regenerated-v02.png",
    environment: "final-minor-b",
    role: "ground",
  },
  boss_final_ruin_jailer: {
    imageSrc: "./assets/monsters/transparent/boss-final-ruin-jailer-regenerated-v02.png",
    environment: "final-minor-b",
    role: "boss",
  },
  mon_final_echo_knight: {
    imageSrc: "./assets/monsters/transparent/mon-final-echo-knight-regenerated-v01.png",
    environment: "final-main-phase-1",
    role: "ground",
  },
  mon_final_mirror_wisp: {
    imageSrc: "./assets/monsters/transparent/mon-final-mirror-wisp-regenerated-v01.png",
    environment: "final-main-phase-1",
    role: "floating",
  },
  mon_final_gate_sentinel: {
    imageSrc: "./assets/monsters/transparent/mon-final-gate-sentinel-regenerated-v01.png",
    environment: "final-main-phase-1",
    role: "ground",
  },
  boss_final_echo_warden: {
    imageSrc: "./assets/monsters/transparent/boss-final-echo-warden-regenerated-v01.png",
    environment: "final-main-phase-1",
    role: "boss-tall",
  },
  mon_final_core_guard: {
    imageSrc: "./assets/monsters/transparent/mon-final-core-guard-regenerated-v01.png",
    environment: "final-main-phase-2",
    role: "ground",
  },
  mon_final_void_lancer: {
    imageSrc: "./assets/monsters/transparent/mon-final-void-lancer-regenerated-v01.png",
    environment: "final-main-phase-2",
    role: "ground",
  },
  mon_final_demon_shade: {
    imageSrc: "./assets/monsters/transparent/mon-final-demon-shade-regenerated-v01.png",
    environment: "final-main-phase-2",
    role: "ground",
  },
  boss_final_seal_core: {
    imageSrc: "./assets/monsters/transparent/boss-final-seal-core-regenerated-v01.png",
    environment: "final-main-phase-2",
    role: "boss-tall",
  },
  mon_final_throne_wraith: {
    imageSrc: "./assets/monsters/transparent/mon-final-throne-wraith-regenerated-v01.png",
    environment: "final-main-phase-3",
    role: "floating",
  },
  mon_final_crown_guard: {
    imageSrc: "./assets/monsters/transparent/mon-final-crown-guard-regenerated-v01.png",
    environment: "final-main-phase-3",
    role: "ground",
  },
  mon_final_last_shadow: {
    imageSrc: "./assets/monsters/transparent/mon-final-last-shadow-regenerated-v01.png",
    environment: "final-main-phase-3",
    role: "ground",
  },
  boss_final_demon_king: {
    imageSrc: "./assets/monsters/transparent/boss-final-demon-king-regenerated-v01.png",
    environment: "final-main-phase-3",
    role: "boss-tall",
  },
});

const DEBUG_ENEMY_NAMES = Object.freeze({
  mon_cinder_bat: "焦翼蝠",
  mon_lava_imp: "熔岩小鬼",
  mon_scorched_guard: "焦石斥候",
  boss_glen: "山寨頭目葛倫",
  mon_moss_rat: "青苔鼠",
  mon_cave_slug: "洞窟黏蟲",
  mon_cracked_golem: "裂石小魔像",
  mon_ash_imp: "灰燼小鬼",
  mon_lava_bat: "熔岩蝙蝠",
  mon_cinder_soldier: "燼火兵",
  boss_ash_guardian: "灰燼守衛",
  mon_ember_stalker: "餘燼潛獵者",
  mon_molten_shell: "熔殼岩獸",
  mon_cinder_brand_wisp: "燼印火靈",
  boss_cinder_seal_sentinel: "燼印鎮衛",
});

const urlParams = new URLSearchParams(window.location.search);
const isDebug = urlParams.get("debug") === "1";
shellEl.dataset.debug = isDebug ? "true" : "false";

const state = {
  model: null,
  actionLog: [],
  logExpanded: false,
  activeSubmenu: null,
  submenuAnchorActionId: null,
  resultOpen: false,
};

fixtureSelect.addEventListener("change", () => {
  loadFixture(fixtureSelect.value);
});

clearLogEl.addEventListener("click", () => {
  state.actionLog = [];
  renderActionLog();
});

toggleBattleLogEl.addEventListener("click", () => {
  state.logExpanded = !state.logExpanded;
  renderBattleLog();
});

resultNextActionEl.addEventListener("click", () => {
  activateResultNextAction();
});

window.addEventListener("resize", () => {
  if (state.activeSubmenu) {
    positionSubmenu();
  }
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
    state.actionLog = [];
    state.logExpanded = false;
    state.activeSubmenu = null;
    state.submenuAnchorActionId = null;
    state.resultOpen = false;
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
    const model = await runtimeClient.getScreen("combat_screen");
    state.model = model;
    state.actionLog = [];
    state.logExpanded = false;
    state.activeSubmenu = null;
    state.submenuAnchorActionId = null;
    state.resultOpen = Boolean(model.result_overlay);
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
    state.actionLog = [];
    state.logExpanded = false;
    state.activeSubmenu = null;
    state.submenuAnchorActionId = null;
    state.resultOpen = false;
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
  titleEl.textContent = model.title ?? "";
  subtitleEl.textContent = model.subtitle ?? "";
  renderResources(model.resource_strip ?? []);
  renderBattlefield(model);
  renderBattleLog();
  commandMessageEl.textContent = model.command_message ?? "";
  renderCommands(model.actions ?? []);
  renderSubmenu();
  renderResultOverlay();
  renderActionLog();
}

function renderResources(items) {
  const roundItem = items.find((item) => (item.label ?? "").includes("回合"));
  if (!roundItem) {
    resourceStripEl.hidden = true;
    resourceStripEl.replaceChildren();
    return;
  }

  resourceStripEl.hidden = false;
  resourceStripEl.replaceChildren(
    (() => {
      const el = document.createElement("div");
      el.className = "resource-item";
      el.dataset.tone = roundItem.tone ?? "neutral";
      el.textContent = roundItem.label ?? "";
      return el;
    })(),
  );
}

function renderBattlefield(model) {
  const player = model.player ?? {};
  const enemy = model.enemy ?? {};
  const urlEnemyId = isDebug ? urlParams.get("enemy_id") : null;
  if (urlEnemyId) {
    enemy.enemy_id = urlEnemyId;
    const debugName = DEBUG_ENEMY_NAMES[urlEnemyId];
    if (debugName) {
      if (urlEnemyId.startsWith("boss_")) {
        enemy.name = `${debugName} (Debug Boss)`;
      } else {
        enemy.name = `${debugName} (Debug)`;
      }
    } else {
      enemy.name = `${urlEnemyId} (Debug Fallback)`;
    }
  }
  enemyNameEl.textContent = enemy.name ?? "";
  enemyHpFillEl.style.setProperty("--meter-value", `${Math.max(0, Math.min(100, enemy.hp_percent ?? 0))}%`);
  enemyHpLabelEl.textContent = enemy.hp_label ?? "";
  renderEnemyMeta(enemy);
  playerNameEl.textContent = player.name ?? "";

  const enemyVisual = COMBAT_ENEMY_VISUALS[enemy.enemy_id];
  if (enemyVisual) {
    shellEl.dataset.enemyId = enemy.enemy_id;
    shellEl.dataset.enemyEnvironment = enemyVisual.environment;
    shellEl.dataset.enemyVisualRole = enemyVisual.role;
    if (enemyImageEl) {
      enemyImageEl.src = enemyVisual.imageSrc;
      enemyImageEl.style.display = "block";
    }
  } else {
    shellEl.dataset.enemyId = enemy.enemy_id ?? "unknown";
    shellEl.dataset.enemyEnvironment = enemy.asset_slot?.state === "placeholder" ? "asset-slot" : "unknown";
    shellEl.dataset.enemyVisualRole = "placeholder";
    if (enemyImageEl) {
      enemyImageEl.removeAttribute("src");
      enemyImageEl.style.display = "none";
    }
  }

  const focusRows = [
    ["HP", player.hp_label ?? ""],
    ["MP", player.mp_label ?? ""],
    ["狀態", player.status_label ?? ""],
    ["姿態", player.stance_label ?? ""],
  ];
  playerFocusStatsEl.replaceChildren(
    ...focusRows.map(([label, value]) => {
      const row = document.createElement("div");
      row.className = "focus-stat";

      const strong = document.createElement("strong");
      strong.textContent = label;

      const span = document.createElement("span");
      span.textContent = value;

      row.append(strong, span);
      return row;
    }),
  );
}

function renderEnemyMeta(enemy) {
  const rows = [
    ["屬性", enemy.attribute],
    ["狀態", enemy.status_label],
  ].filter(([, value]) => Boolean(value));

  enemyMetaEl.replaceChildren(
    ...rows.map(([label, value]) => {
      const item = document.createElement("span");
      item.textContent = `${label} ${value}`;
      return item;
    }),
  );
}

function renderBattleLog() {
  const lines = state.model?.battle_log ?? [];
  const visibleLines = state.logExpanded ? lines : lines.slice(-5);
  shellEl.dataset.logExpanded = String(state.logExpanded);
  logModeLabelEl.textContent = state.logExpanded ? "完整" : "最近 5 條";
  toggleBattleLogEl.textContent = state.logExpanded ? "收合" : "展開";

  if (visibleLines.length === 0) {
    battleLogEl.replaceChildren(createEmptyState("尚無 Battle Log。"));
    return;
  }

  battleLogEl.replaceChildren(
    ...visibleLines.map((line) => {
      const item = document.createElement("li");
      item.textContent = line;
      return item;
    }),
  );
}

function renderCommands(actions) {
  commandRowEl.replaceChildren(
    ...actions.map((action) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "command-button";
      button.dataset.actionId = action.action_id ?? "unavailable";
      button.dataset.payload = JSON.stringify(action.payload ?? {});
      button.dataset.disabledReason = action.disabled_reason ?? "";
      button.dataset.primary = String(Boolean(action.primary));
      button.dataset.active = "false";
      button.dataset.enabled = String(Boolean(action.enabled));
      button.setAttribute("aria-disabled", String(!action.enabled));
      button.disabled = state.resultOpen;
      button.title = action.enabled ? action.description ?? "" : action.disabled_reason ?? "";

      const label = document.createElement("strong");
      label.textContent = action.label ?? action.action_id;

      const description = document.createElement("span");
      description.textContent = action.description ?? "";

      button.append(label, description);
      button.addEventListener("click", () => activateAction(action, "command_bar", button));
      return button;
    }),
  );
  updateCommandActiveState();
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

async function activateAction(action, source, triggerEl = null) {
  if (state.resultOpen) {
    pushActionLog({
      action_id: action.action_id,
      payload: action.payload ?? {},
      source,
      dispatched: false,
      reason: "combat already resolved",
    });
    commandMessageEl.textContent = "戰鬥已結束，請確認結算。";
    return;
  }

  if (!action.enabled) {
    pushActionLog({
      action_id: action.action_id,
      payload: action.payload ?? {},
      source,
      dispatched: false,
      reason: action.disabled_reason ?? "disabled",
    });
    commandMessageEl.textContent = action.disabled_reason || "目前無法執行這個指令。";
    return;
  }

  if (action.action_id === "open_skill_menu" && state.activeSubmenu === "skill") {
    closeSubmenu("已收回技能選單。");
    return;
  }

  if (action.action_id === "open_item_menu" && state.activeSubmenu === "item") {
    closeSubmenu("已收回道具選單。");
    return;
  }

  pushActionLog({
    action_id: action.action_id,
    payload: action.payload ?? {},
    source,
    dispatched: true,
  });

  if (action.action_id === "open_skill_menu") {
    commandMessageEl.textContent = action.feedback_message ?? "已開啟技能選單。再次按技能可收回。";
    openSubmenu("skill", triggerEl);
    return;
  }

  if (action.action_id === "open_item_menu") {
    commandMessageEl.textContent = action.feedback_message ?? "已開啟道具選單。再次按道具可收回。";
    openSubmenu("item", triggerEl);
    return;
  }

  if (runtimeClient.isLiveMode()) {
    await dispatchRuntimeAction(action, source);
    return;
  }

  state.activeSubmenu = null;
  state.submenuAnchorActionId = null;
  renderSubmenu();
  commandMessageEl.textContent =
    action.feedback_message ?? `已送出 ${action.action_id}。static prototype 不會計算戰鬥結果。`;

  if (action.opens_result) {
    openResultOverlay(action);
  }
}

async function dispatchRuntimeAction(action, source) {
  try {
    const result = await runtimeClient.dispatchAction("combat_screen", action.action_id, action.payload ?? {});
    if (result.screen_model) {
      state.model = result.screen_model;
      state.activeSubmenu = null;
      state.submenuAnchorActionId = null;
      state.resultOpen = Boolean(result.screen_model.result_overlay);
      render();
    }
    if (result.message && !state.resultOpen) {
      commandMessageEl.textContent = result.message;
    }
    if (result.next_route) {
      window.setTimeout(() => {
        window.location.href = runtimeClient.nextRoute(result, "../town_hub/index.html");
      }, 140);
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
    commandMessageEl.textContent = reason;
  }
}

function openSubmenu(type, triggerEl = null) {
  state.activeSubmenu = type;
  state.submenuAnchorActionId =
    triggerEl?.dataset.actionId ?? (type === "skill" ? "open_skill_menu" : "open_item_menu");
  renderSubmenu();
}

function closeSubmenu(message) {
  state.activeSubmenu = null;
  state.submenuAnchorActionId = null;
  renderSubmenu();
  if (message) {
    commandMessageEl.textContent = message;
  }
}

function renderSubmenu() {
  const menu = getActiveMenu();
  if (!menu) {
    submenuPanelEl.hidden = true;
    submenuPanelEl.dataset.menuType = "none";
    submenuLabelEl.textContent = "";
    submenuTitleEl.textContent = "";
    submenuSummaryEl.textContent = "";
    submenuListEl.replaceChildren();
    submenuPanelEl.dataset.placement = "none";
    submenuPanelEl.style.removeProperty("--submenu-left");
    submenuPanelEl.style.removeProperty("--submenu-width");
    submenuPanelEl.style.removeProperty("--submenu-anchor-x");
    submenuPanelEl.style.removeProperty("--submenu-under-top");
    submenuPanelEl.style.removeProperty("--submenu-under-max-height");
    updateCommandActiveState();
    return;
  }

  submenuPanelEl.hidden = false;
  submenuPanelEl.dataset.menuType = state.activeSubmenu;
  submenuLabelEl.textContent = menu.label ?? "";
  submenuTitleEl.textContent = menu.title ?? "";
  submenuSummaryEl.textContent = menu.summary ?? "";

  const items = menu.items ?? [];
  if (items.length === 0) {
    submenuListEl.replaceChildren(createEmptyState(menu.empty_message ?? "沒有可用項目。"));
    positionSubmenu();
    updateCommandActiveState();
    return;
  }

  submenuListEl.replaceChildren(
    ...items.map((item) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "submenu-option";
      button.dataset.actionId = item.action_id ?? "unavailable";
      button.dataset.payload = JSON.stringify(item.payload ?? {});
      button.dataset.disabledReason = item.disabled_reason ?? "";
      button.setAttribute("aria-disabled", String(!item.enabled));
      button.title = item.enabled ? item.description ?? "" : item.disabled_reason ?? "";

      const title = document.createElement("strong");
      title.textContent = item.label ?? item.action_id;

      const meta = document.createElement("span");
      meta.textContent = item.meta ?? "";

      const description = document.createElement("small");
      description.textContent = item.enabled ? item.description ?? "" : item.disabled_reason ?? item.description ?? "";

      button.append(title, meta, description);
      button.addEventListener("click", () => activateSubmenuItem(item));
      return button;
    }),
  );
  positionSubmenu();
  updateCommandActiveState();
}

function renderResultOverlay() {
  const result = state.model?.result_overlay ?? null;
  shellEl.dataset.resultOpen = String(state.resultOpen && Boolean(result));

  if (!state.resultOpen || !result) {
    resultOverlayEl.hidden = true;
    resultOverlayEl.dataset.outcome = "none";
    resultLabelEl.textContent = "";
    resultTitleEl.textContent = "";
    resultStatusEl.textContent = "";
    resultSummaryEl.textContent = "";
    resultRewardTitleEl.textContent = "";
    resultLinesEl.replaceChildren();
    resultNextActionEl.textContent = "";
    resultNextActionEl.disabled = true;
    updateCommandActiveState();
    return;
  }

  resultOverlayEl.hidden = false;
  resultOverlayEl.dataset.outcome = result.outcome ?? "neutral";
  resultLabelEl.textContent = result.label ?? "戰鬥結算";
  resultTitleEl.textContent = result.title ?? "";
  resultStatusEl.textContent = result.status_summary ?? "";
  resultSummaryEl.textContent = result.battle_summary ?? "";
  resultRewardTitleEl.textContent = result.reward_title ?? "結果";
  resultLinesEl.replaceChildren(...(result.rows ?? []).map(createResultLine));

  const nextAction = result.next_action ?? {};
  resultNextActionEl.textContent = nextAction.label ?? "下一步";
  resultNextActionEl.title = nextAction.description ?? "";
  resultNextActionEl.disabled = !nextAction.action_id;
  updateCommandActiveState();
}

function openResultOverlay(action) {
  if (!state.model?.result_overlay) {
    commandMessageEl.textContent = "這個 static fixture 尚未提供 result_overlay。";
    return;
  }

  state.resultOpen = true;
  state.activeSubmenu = null;
  state.submenuAnchorActionId = null;
  renderSubmenu();
  renderResultOverlay();
  commandMessageEl.textContent =
    action.result_message ?? action.feedback_message ?? "戰鬥已結束，請確認結算。";
}

async function activateResultNextAction() {
  const nextAction = state.model?.result_overlay?.next_action ?? null;
  if (!state.resultOpen || !nextAction?.action_id) {
    return;
  }

  pushActionLog({
    action_id: nextAction.action_id,
    payload: nextAction.payload ?? {},
    source: "result_overlay",
    dispatched: true,
  });
  commandMessageEl.textContent = nextAction.feedback_message ?? `已送出 ${nextAction.action_id}。`;

  if (runtimeClient.isLiveMode()) {
    try {
      const result = await runtimeClient.dispatchAction("combat_screen", nextAction.action_id, nextAction.payload ?? {});
      window.setTimeout(() => {
        window.location.href = runtimeClient.nextRoute(result, nextAction.navigate_to ?? "../town_hub/index.html");
      }, 140);
    } catch (error) {
      pushActionLog({
        action_id: nextAction.action_id,
        payload: nextAction.payload ?? {},
        source: "result_overlay",
        dispatched: false,
        reason: error instanceof Error ? error.message : String(error),
      });
    }
    return;
  }

  if (nextAction.navigate_to) {
    window.setTimeout(() => {
      window.location.href = nextAction.navigate_to;
    }, 140);
  }
}

function createResultLine(row) {
  const item = document.createElement("div");
  item.className = "result-line";
  item.dataset.tone = row.tone ?? "neutral";

  const labelText = row.label ?? "";
  const isNumericLabel = /^\d+\.?$/.test(labelText.trim());
  if (isNumericLabel) {
    item.classList.add("result-line-list");
  } else {
    item.classList.add("result-line-kv");
  }

  const label = document.createElement("strong");
  label.textContent = labelText;

  const value = document.createElement("span");
  value.textContent = row.value ?? "";

  item.append(label, value);
  if (row.detail) {
    const detail = document.createElement("small");
    detail.textContent = row.detail;
    item.append(detail);
  }
  return item;
}

function positionSubmenu() {
  const anchorId =
    state.submenuAnchorActionId ?? (state.activeSubmenu === "skill" ? "open_skill_menu" : "open_item_menu");
  const anchorEl = commandRowEl.querySelector(`[data-action-id="${anchorId}"]`);
  if (!anchorEl || !combatFooterEl) {
    return;
  }

  const footerRect = combatFooterEl.getBoundingClientRect();
  const anchorRect = anchorEl.getBoundingClientRect();
  const commandRowRect = commandRowEl.getBoundingClientRect();
  const inset = 10;
  const preferredWidth = 560;
  const minWidth = 300;
  const availableWidth = Math.max(minWidth, footerRect.width - inset * 2);
  const width = Math.min(preferredWidth, availableWidth);
  const anchorCenter = anchorRect.left - footerRect.left + anchorRect.width / 2;
  const left = Math.max(inset, Math.min(anchorCenter - width / 2, footerRect.width - width - inset));
  const anchorX = Math.max(18, Math.min(anchorCenter - left, width - 18));

  const useStackedPlacement = window.innerWidth <= 1180;
  submenuPanelEl.dataset.placement = useStackedPlacement ? "under-command" : "above-command";
  submenuPanelEl.style.setProperty("--submenu-left", `${left}px`);
  submenuPanelEl.style.setProperty("--submenu-width", `${width}px`);
  submenuPanelEl.style.setProperty("--submenu-anchor-x", `${anchorX}px`);
  submenuPanelEl.style.setProperty("--submenu-under-top", `${commandRowRect.bottom - footerRect.top + 10}px`);
  submenuPanelEl.style.setProperty(
    "--submenu-under-max-height",
    `${Math.max(140, Math.min(220, window.innerHeight - commandRowRect.bottom - 22))}px`,
  );
}

function updateCommandActiveState() {
  commandRowEl.querySelectorAll(".command-button").forEach((button) => {
    const actionId = button.dataset.actionId;
    const isBaseDisabled = button.dataset.enabled !== "true";
    const isActive =
      (state.activeSubmenu === "skill" && actionId === "open_skill_menu") ||
      (state.activeSubmenu === "item" && actionId === "open_item_menu");
    button.dataset.active = String(isActive);
    button.disabled = state.resultOpen;
    button.setAttribute("aria-disabled", String(state.resultOpen || isBaseDisabled));
  });
}

function getActiveMenu() {
  if (state.activeSubmenu === "skill") {
    return state.model?.skill_menu ?? null;
  }

  if (state.activeSubmenu === "item") {
    return state.model?.item_menu ?? null;
  }

  return null;
}

async function activateSubmenuItem(item) {
  if (!item.enabled) {
    pushActionLog({
      action_id: item.action_id,
      payload: item.payload ?? {},
      source: `${state.activeSubmenu}_submenu`,
      dispatched: false,
      reason: item.disabled_reason ?? "disabled",
    });
    commandMessageEl.textContent = item.disabled_reason || "目前無法使用這個項目。";
    return;
  }

  pushActionLog({
    action_id: item.action_id,
    payload: item.payload ?? {},
    source: `${state.activeSubmenu}_submenu`,
    dispatched: true,
  });
  if (runtimeClient.isLiveMode()) {
    await dispatchRuntimeAction(item, `${state.activeSubmenu}_submenu`);
    return;
  }
  commandMessageEl.textContent =
    item.feedback_message ?? `已送出 ${item.action_id}。static prototype 不會計算戰鬥結果。`;
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

function createEmptyState(message) {
  const empty = document.createElement("div");
  empty.className = "empty-state";
  empty.textContent = message;
  return empty;
}

function renderLoadError(error) {
  state.resultOpen = false;
  titleEl.textContent = "Fixture 載入失敗";
  subtitleEl.textContent = "無法讀取 Combat Screen static fixture。";
  resourceStripEl.replaceChildren();
  enemyNameEl.textContent = "無法載入戰鬥畫面";
  enemyHpLabelEl.textContent = error instanceof Error ? error.message : String(error);
  enemyMetaEl.replaceChildren();
  playerNameEl.textContent = "";
  playerFocusStatsEl.replaceChildren();
  battleLogEl.replaceChildren();
  commandMessageEl.textContent = "";
  commandRowEl.replaceChildren(createEmptyState("沒有可用指令。"));
  closeSubmenu();
  renderResultOverlay();
}
