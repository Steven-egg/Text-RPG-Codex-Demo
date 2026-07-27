from __future__ import annotations

"""Declarative configuration for the stdout-only S10 balance measurement."""

S10_VERSION = "s10-entry-endgame-v1"
S10_TARGETS = {
    "normal": (3, 5),
    "boss": (10, 15),
}

# `loadout_region` selects the existing B4 regional loadout for every job.
# Per-job overrides stay explicit and empty until an owner selects one.
S10_SCENARIOS = (
    {"region": "fire", "checkpoint": "entry", "target_type": "normal", "enemy_id": "mon_ember_stalker", "loadout_region": "fire", "relic_count": 0, "loadout_overrides": {}},
    {"region": "fire", "checkpoint": "endgame", "target_type": "boss", "enemy_id": "boss_cinder_seal_sentinel", "loadout_region": "fire", "relic_count": 0, "loadout_overrides": {}},
    {"region": "ice", "checkpoint": "entry", "target_type": "normal", "enemy_id": "mon_ice_outer_guard", "loadout_region": "fire", "relic_count": 0, "loadout_overrides": {}},
    {"region": "ice", "checkpoint": "endgame", "target_type": "boss", "enemy_id": "boss_ice_final_seal_lord", "loadout_region": "ice", "relic_count": 1, "loadout_overrides": {}},
    {"region": "earth", "checkpoint": "entry", "target_type": "normal", "enemy_id": "mon_earth_leyline_guard", "loadout_region": "ice", "relic_count": 1, "loadout_overrides": {}},
    {"region": "earth", "checkpoint": "endgame", "target_type": "boss", "enemy_id": "boss_earth_deep_leyline_lord", "loadout_region": "earth", "relic_count": 2, "loadout_overrides": {}},
    {"region": "thunder", "checkpoint": "entry", "target_type": "normal", "enemy_id": "mon_thunder_array_guard", "loadout_region": "earth", "relic_count": 2, "loadout_overrides": {}},
    {"region": "thunder", "checkpoint": "endgame", "target_type": "boss", "enemy_id": "boss_thunder_crown_storm_lord", "loadout_region": "thunder", "relic_count": 3, "loadout_overrides": {}},
    {"region": "final", "checkpoint": "entry", "target_type": "normal", "enemy_id": "mon_final_core_guard", "loadout_region": "thunder", "relic_count": 3, "loadout_overrides": {}},
    {"region": "final", "checkpoint": "endgame", "target_type": "boss", "enemy_id": "boss_final_demon_king", "loadout_region": "final", "relic_count": 4, "loadout_overrides": {}},
)

class S10SupplyProfilesDict(dict):
    def get_profile(self, key: str, region_id: str = "fire") -> dict:
        if key == "none":
            return {
                "sustain_hp": {"item_id": None, "quantity": 0},
                "emergency_hp": {"item_id": None, "quantity": 0},
                "mp": {"item_id": None, "quantity": 0},
                "throwable": {"item_id": None, "quantity": 0},
                "escape": {"item_id": None, "quantity": 0},
            }
        
        # boss_standard 依各區實際合法五槽補給 (item_potion_m 已移除)
        if region_id == "fire":
            return {
                "sustain_hp": {"item_id": "item_potion_s", "quantity": 3},
                "emergency_hp": {"item_id": "item_potion_s", "quantity": 1},
                "mp": {"item_id": "item_focus_drop", "quantity": 1},
                "throwable": {"item_id": "item_armor_piercer", "quantity": 1},
                "escape": {"item_id": None, "quantity": 0},
            }
        elif region_id == "ice":
            return {
                "sustain_hp": {"item_id": "item_potion_s", "quantity": 3},
                "emergency_hp": {"item_id": "item_ice_potion_01", "quantity": 1},
                "mp": {"item_id": "item_ice_potion_02", "quantity": 1},
                "throwable": {"item_id": "item_throw_fire", "quantity": 1},
                "escape": {"item_id": None, "quantity": 0},
            }
        elif region_id == "earth":
            return {
                "sustain_hp": {"item_id": "item_potion_s", "quantity": 3},
                "emergency_hp": {"item_id": "item_earth_potion_01", "quantity": 1},
                "mp": {"item_id": "item_earth_potion_02", "quantity": 1},
                "throwable": {"item_id": "item_throw_ice", "quantity": 1},
                "escape": {"item_id": None, "quantity": 0},
            }
        elif region_id == "thunder":
            return {
                "sustain_hp": {"item_id": "item_potion_s", "quantity": 3},
                "emergency_hp": {"item_id": "item_thunder_potion_01", "quantity": 1},
                "mp": {"item_id": "item_thunder_potion_02", "quantity": 1},
                "throwable": {"item_id": "item_throw_earth", "quantity": 1},
                "escape": {"item_id": None, "quantity": 0},
            }
        else:  # final
            return {
                "sustain_hp": {"item_id": "item_potion_s", "quantity": 3},
                "emergency_hp": {"item_id": "item_final_potion_01", "quantity": 1},
                "mp": {"item_id": "item_final_potion_02", "quantity": 1},
                "throwable": {"item_id": "item_throw_thunder", "quantity": 1},
                "escape": {"item_id": None, "quantity": 0},
            }

    def __getitem__(self, key):
        return self.get_profile(key, "fire")

    def __contains__(self, key):
        return key in ("none", "boss_standard")

    def keys(self):
        return ["none", "boss_standard"]


S10_SUPPLY_PROFILES = S10SupplyProfilesDict()


def scenario_config_id(scenario: dict) -> str:
    return f"{S10_VERSION}:{scenario['region']}:{scenario['checkpoint']}"


def supply_profile_for(scenario: dict) -> str:
    return "boss_standard" if scenario["target_type"] == "boss" else "none"


def supplies_for_job(scenario: dict, job_key: str) -> dict:
    """Return the legal S10 supply profile, including explicit job overrides."""
    profile = S10_SUPPLY_PROFILES.get_profile(supply_profile_for(scenario), scenario["region"])
    supplies = {slot: dict(selection) for slot, selection in profile.items()}
    if scenario["region"] == "fire" and scenario["target_type"] == "boss" and job_key == "rogue":
        supplies["throwable"] = {"item_id": "item_rending_spike", "quantity": 2}
    return supplies
