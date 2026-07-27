import assert from "node:assert/strict";

import { combatEnemyMetaRows } from "../07_gui_prototype/combat_screen/combat-enemy-meta.mjs";


assert.deepEqual(
  combatEnemyMetaRows({
    attribute: "無",
    race_label: "構裝",
    trait_label: "可破裝甲",
    trait_status_label: "剩餘 1 次",
    status_label: "無",
  }),
  [
    ["屬性", "無"],
    ["種族", "構裝"],
    ["特性", "可破裝甲 · 剩餘 1 次"],
    ["狀態", "無"],
  ],
);

assert.deepEqual(
  combatEnemyMetaRows({attribute: "火", status_label: "灼熱外殼"}),
  [
    ["屬性", "火"],
    ["狀態", "灼熱外殼"],
  ],
);

console.log("combat GUI enemy meta render contracts passed");
