from __future__ import annotations

from .jobs import JOBS
from .job_specializations import JOB_SPECIALIZATIONS
from .materials import MATERIALS
from .items import ITEMS, EQUIPMENT
from .skills import SKILLS, MAGIC_BOOKS
from .crafting import RECIPES
from .monsters import MONSTERS
from .dungeons import DUNGEONS, EVENT_WEIGHTS
from .quests import QUESTS
from .shops import SHOP_INVENTORY
from .promotions import PROMOTIONS
from .relics import RELICS
from .regions import REGIONS, get_region_by_dungeon, get_region_by_quest, get_unlocked_regions
from .display_names import (
    CORE_FACILITY_KEYS,
    CORE_NPC_KEYS,
    FACILITY_DIALOGUES,
    FACILITY_DISPLAY_NAMES,
    NPC_DISPLAY_NAMES,
    get_facility_dialogue,
    get_facility_display_name,
    get_npc_display_name,
)
from .dialogues import FACILITY_GREETINGS, get_dialogue
from .registry import DATA_REGISTRY

__all__ = [
    "JOBS",
    "JOB_SPECIALIZATIONS",
    "MATERIALS",
    "ITEMS",
    "EQUIPMENT",
    "SKILLS",
    "MAGIC_BOOKS",
    "RECIPES",
    "MONSTERS",
    "DUNGEONS",
    "EVENT_WEIGHTS",
    "QUESTS",
    "SHOP_INVENTORY",
    "PROMOTIONS",
    "RELICS",
    "REGIONS",
    "NPC_DISPLAY_NAMES",
    "FACILITY_DISPLAY_NAMES",
    "FACILITY_DIALOGUES",
    "FACILITY_GREETINGS",
    "CORE_NPC_KEYS",
    "CORE_FACILITY_KEYS",
    "get_unlocked_regions",
    "get_region_by_dungeon",
    "get_region_by_quest",
    "get_npc_display_name",
    "get_facility_display_name",
    "get_facility_dialogue",
    "get_dialogue",
    "DATA_REGISTRY",
]
