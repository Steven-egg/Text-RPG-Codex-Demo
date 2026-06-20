from __future__ import annotations

from .crafting import RECIPES
from .dungeons import DUNGEONS, EVENT_WEIGHTS
from .items import EQUIPMENT, ITEMS
from .jobs import JOBS
from .job_specializations import JOB_SPECIALIZATIONS
from .materials import MATERIALS
from .monsters import MONSTERS
from .promotions import PROMOTIONS
from .relics import RELICS
from .quests import QUESTS
from .shops import SHOP_INVENTORY
from .skills import MAGIC_BOOKS, SKILLS


DATA_REGISTRY = {
    "jobs": JOBS,
    "job_specializations": JOB_SPECIALIZATIONS,
    "materials": MATERIALS,
    "items": ITEMS,
    "equipment": EQUIPMENT,
    "skills": SKILLS,
    "magic_books": MAGIC_BOOKS,
    "recipes": RECIPES,
    "monsters": MONSTERS,
    "dungeons": DUNGEONS,
    "event_weights": EVENT_WEIGHTS,
    "quests": QUESTS,
    "shop_inventory": SHOP_INVENTORY,
    "promotions": PROMOTIONS,
    "relics": RELICS,
}


INITIAL_UNLOCK_KEYS = {
    "dungeon_moss_cave",
}


ENGINE_EVENT_UNLOCK_KEYS = {
    "item_armor_piercer",
    "recipe_piercing_bundle",
    "recipe_heat_charm",
}


STORY_UNLOCK_KEYS = {
    "second_act_preview",
    "unlock_act_2",
    "unlock_ash_ravine",
    "unlock_ice_region",
    "unlock_earth_region_preview",
}


SYSTEM_UNLOCK_KEYS = {
    "shop_synthesis_01",
}


KNOWN_FLAG_KEYS = {
    "ash_guardian_defeated",
    "boss_glen_defeated",
    "boss_glen_investigation_accepted",
    "boss_glen_sighted",
    "cinder_seal_sentinel_defeated",
    "fire_mark_church_bridge_done",
    "fire_mark_church_lookup_done",
    "fire_mark_guild_inquiry_done",
    "ice_final_boss_defeated",
    "ice_frostroot_keeper_defeated",
    "ice_outer_gatewarden_defeated",
    "ice_relic_marker_resolved",
    "ice_wreck_captain_defeated",
}


def all_item_like_ids() -> set[str]:
    return set(ITEMS) | set(EQUIPMENT) | set(MATERIALS)


def all_sellable_ids() -> set[str]:
    return set(ITEMS) | set(EQUIPMENT)


def all_skill_ids() -> set[str]:
    return set(SKILLS)


def all_job_ids() -> set[str]:
    return set(JOBS)


def all_job_specialization_ids() -> set[str]:
    return set(JOB_SPECIALIZATIONS)


def all_monster_ids() -> set[str]:
    return set(MONSTERS)


def all_dungeon_ids() -> set[str]:
    return set(DUNGEONS)


def all_recipe_ids() -> set[str]:
    return set(RECIPES)


def all_quest_ids() -> set[str]:
    return set(QUESTS)


def all_material_ids() -> set[str]:
    return set(MATERIALS)


def all_promotion_ids() -> set[str]:
    return set(PROMOTIONS)


def all_relic_ids() -> set[str]:
    return set(RELICS)


def promotion_previews_for_job(job_id: str) -> list[tuple[str, dict]]:
    return [
        (promotion_id, promotion)
        for promotion_id, promotion in PROMOTIONS.items()
        if promotion.get("source_job") == job_id and promotion.get("status") == "preview"
    ]


def job_specialization_previews_for_job(job_id: str) -> list[tuple[str, dict]]:
    return [
        (specialization_id, specialization)
        for specialization_id, specialization in JOB_SPECIALIZATIONS.items()
        if specialization.get("source_job") == job_id and specialization.get("status") == "preview"
    ]


def relic_previews() -> list[tuple[str, dict]]:
    return [
        (relic_id, relic)
        for relic_id, relic in RELICS.items()
        if relic.get("status") == "preview"
    ]


def all_unlock_sources() -> set[str]:
    sources = set()
    sources.update(INITIAL_UNLOCK_KEYS)
    sources.update(ENGINE_EVENT_UNLOCK_KEYS)
    sources.update(STORY_UNLOCK_KEYS)
    sources.update(SYSTEM_UNLOCK_KEYS)
    sources.update(DUNGEONS.keys())
    sources.update(QUESTS.keys())
    sources.update(RECIPES.keys())

    for item in ITEMS.values():
        if item.get("unlock"):
            sources.add(item["unlock"])

    for equipment in EQUIPMENT.values():
        if equipment.get("unlock"):
            sources.add(equipment["unlock"])

    for quest in QUESTS.values():
        sources.update(quest.get("unlocks", []))

    return sources


def all_unlock_producers() -> set[str]:
    producers = set()
    producers.update(INITIAL_UNLOCK_KEYS)
    producers.update(ENGINE_EVENT_UNLOCK_KEYS)
    producers.update(STORY_UNLOCK_KEYS)
    producers.update(SYSTEM_UNLOCK_KEYS)

    for quest in QUESTS.values():
        producers.update(quest.get("unlocks", []))

    # Completed quest ids are valid unlock checks because is_unlocked()
    # accepts keys from either state["unlocked"] or completed_quests.
    producers.update(QUESTS.keys())
    return producers
