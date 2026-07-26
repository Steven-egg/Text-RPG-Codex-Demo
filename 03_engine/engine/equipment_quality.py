"""Four-job v1 quality rules.

The module is deliberately data-only from the caller's perspective: a rolled
instance records the selected pattern and affix IDs, so no later reroll occurs.
"""
from __future__ import annotations

import random

QUALITY_ORDER = ("normal", "fine", "rare", "epic", "legendary")
QUALITY_LABELS = {
    "normal": "普通", "fine": "精良", "rare": "稀有", "epic": "史詩", "legendary": "傳說",
}
QUALITY_ENVELOPES = {"normal": 0.0, "fine": 0.10, "rare": 0.25, "epic": 0.45, "legendary": 0.70}
# Fine is the player-facing baseline for a rolled affix.  The later quality
# multipliers retain the approved envelope spacing without changing a pattern
# or adding another budget system: 1.00, 1.15, 1.35, and 1.60.
QUALITY_AFFIX_MULTIPLIERS = {
    "fine": 1.00,
    "rare": 1.15,
    "epic": 1.35,
    "legendary": 1.60,
}
QUALITY_SELL_MULTIPLIERS = {"normal": 1.0, "fine": 1.1, "rare": 1.4, "epic": 1.8, "legendary": 2.4}

CRAFT_QUALITY_WEIGHTS = {
    "border_fire": (("fine", 1.0),),
    "ice": (("fine", 0.80), ("rare", 0.20)),
    "earth": (("fine", 0.65), ("rare", 0.28), ("epic", 0.07)),
    "thunder": (("fine", 0.55), ("rare", 0.30), ("epic", 0.12), ("legendary", 0.03)),
    "final": (("fine", 0.55), ("rare", 0.30), ("epic", 0.12), ("legendary", 0.03)),
}

BOSS_QUALITY = {
    "boss_cinder_seal_sentinel": "fine",
    "boss_ice_wreck_captain": "fine", "boss_ice_frostroot_keeper": "fine", "boss_ice_outer_gatewarden": "fine", "boss_ice_final_seal_lord": "rare",
    "boss_earth_rootwarden": "rare", "boss_earth_quarry_colossus": "rare", "boss_earth_outer_grovekeeper": "rare", "boss_earth_deep_leyline_lord": "epic",
    "boss_thunder_plateau_beacon": "epic", "boss_thunder_channel_keeper": "epic", "boss_thunder_lower_array_warden": "epic", "boss_thunder_crown_storm_lord": "legendary",
    "boss_final_echo_vanguard": "epic", "boss_final_ruin_jailer": "epic", "boss_final_echo_warden": "epic", "boss_final_seal_core": "epic", "boss_final_demon_king": "legendary",
}

SUPPORTED_JOBS = {"劍士", "法師", "盜賊", "牧師"}

# Every slot has exactly two legal pre-built patterns.  Their affixes contain
# only v1 allowed effects; Rogue heads are the sole offensive armor exception.
PATTERNS = {
    "weapon": (("edge", "major_edge", "minor_precision"), ("tempo", "major_tempo", "minor_precision")),
    "head": (("ward", "major_guard", "minor_element_ward"), ("status", "major_status_guard", "minor_element_ward")),
    "body": (("guard", "major_guard", "minor_element_ward"), ("shell", "major_magic_guard", "minor_status_guard")),
    "accessory": (("ward", "major_magic_guard", "minor_element_ward"), ("status", "major_status_guard", "minor_guard")),
}
ROGUE_HEAD_PATTERNS = (("blade", "major_edge", "minor_precision"), ("venom", "major_tempo", "minor_precision"))
WARRIOR_PATTERNS = {
    "weapon": (
        ("charge_cap", "major_charge_skill_bonus", "minor_charge_cap"),
        ("charge_gain", "major_charge_skill_bonus", "minor_charge_gain"),
    ),
    "head": (("iron_guard", "major_guard", "minor_guard"), ("rune_guard", "major_magic_guard", "minor_region_ward")),
    "body": (("bulwark", "major_guard", "minor_guard"), ("barrier", "major_magic_guard", "minor_region_ward")),
    "accessory": (("seal", "major_guard", "minor_guard"), ("warding", "major_magic_guard", "minor_region_ward")),
}
MAGE_PATTERNS = {
    "weapon": (
        ("elemental", "major_arcane", "minor_elemental_magic_direct"),
        ("spellward", "major_arcane", "minor_magic_guard_weapon"),
    ),
    "head": (("spellward", "major_magic_guard", "minor_region_ward"), ("woven_wall", "major_guard", "minor_guard")),
    "body": (("spirit_robe", "major_magic_guard", "minor_region_ward"), ("armored_rune", "major_guard", "minor_guard")),
    "accessory": (("arcane_charm", "major_magic_guard", "minor_region_ward"), ("guard_ring", "major_guard", "minor_guard")),
}

REGION_WARD_AFFIXES = {
    "border_fire": "minor_quality_fire_ward",
    "fire": "minor_quality_fire_ward",
    "ice": "minor_quality_ice_ward",
    "earth": "minor_quality_earth_ward",
    "thunder": "minor_quality_thunder_ward",
    "final": "minor_quality_final_ward",
}


def supports_quality_job(job: str) -> bool:
    return job in SUPPORTED_JOBS


def affix_value_multiplier(quality: object) -> float:
    """Return the fixed quality multiplier for an affix's live stat value.

    Normal and legacy instances retain their original affix values.  Unknown
    persisted values likewise fail safe to the unmodified value.
    """
    return QUALITY_AFFIX_MULTIPLIERS.get(quality, 1.0)


def roll_craft_quality(region_id: str, rng: random.Random | None = None) -> str:
    roll = (rng or random).random()
    total = 0.0
    for quality, chance in CRAFT_QUALITY_WEIGHTS.get(region_id, CRAFT_QUALITY_WEIGHTS["border_fire"]):
        total += chance
        if roll < total:
            return quality
    return CRAFT_QUALITY_WEIGHTS.get(region_id, CRAFT_QUALITY_WEIGHTS["border_fire"])[-1][0]


def pattern_for(base: dict, job: str, quality: str, rng: random.Random | None = None) -> tuple[str | None, str | None, str | None]:
    if quality == "normal":
        return None, None, None
    if job == "劍士":
        patterns = WARRIOR_PATTERNS.get(base.get("slot"), ())
    elif job == "法師":
        patterns = MAGE_PATTERNS.get(base.get("slot"), ())
    else:
        patterns = ROGUE_HEAD_PATTERNS if job == "盜賊" and base.get("slot") == "head" else PATTERNS.get(base.get("slot"), ())
    if not patterns:
        return None, None, None
    pattern_id, major, minor = (rng or random).choice(patterns)
    if minor == "minor_region_ward":
        minor = REGION_WARD_AFFIXES.get(base.get("region"), "minor_quality_fire_ward")
    if quality == "fine":
        return pattern_id, major, None
    if quality == "rare":
        return pattern_id, major, None
    return pattern_id, major, minor


def sell_price(base_price: int, quality: str) -> int:
    return int(base_price * 0.5 * QUALITY_SELL_MULTIPLIERS[quality])


def filter_tags(base: dict, instance: dict | None) -> set[str]:
    tags: set[str] = set(base.get("jobs", ()))
    stats = dict(base.get("stats", {}))
    if instance:
        for key in ("major_affix_id", "minor_affix_id"):
            affix_id = instance.get(key)
            if affix_id:
                tags.add(affix_id)
    if any(key in stats for key in ("attack", "magic_attack", "crit", "agility", "effect_accuracy")):
        tags.add("attack")
    if any(key in stats for key in ("defense", "magic_defense")):
        tags.add("defense")
    if any(key.endswith("_resist") for key in stats):
        tags.add("resist")
    return tags
