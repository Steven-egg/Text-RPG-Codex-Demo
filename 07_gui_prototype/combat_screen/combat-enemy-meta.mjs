export function combatEnemyMetaRows(enemy = {}) {
  const traitValue = [enemy.trait_label, enemy.trait_status_label].filter(Boolean).join(" · ");
  return [
    ["屬性", enemy.attribute],
    ["種族", enemy.race_label],
    ["特性", traitValue],
    ["狀態", enemy.status_label],
  ].filter(([, value]) => Boolean(value));
}
