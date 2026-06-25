from __future__ import annotations

from typing import Any
from data import EQUIPMENT, SHOP_INVENTORY, RECIPES, MATERIALS
from . import game


def workshop_screen_model(state: dict[str, Any], selected_region_id: str | None = None) -> dict[str, Any]:
    gold = state.get("gold", 0)
    stats = game.get_stats(state)

    player_data = {
        "name": state.get("name", ""),
        "job": state.get("job", ""),
        "level": state.get("level", 1),
        "current_hp": state.get("current_hp", 0),
        "max_hp": stats.get("max_hp", 0),
        "current_mp": state.get("current_mp", 0),
        "max_mp": stats.get("max_mp", 0),
        "gold": gold,
        "completed_quests": state.get("completed_quests", []),
        "inventory": state.get("inventory", {}),
        "equipment": state.get("equipment", {})
    }

    from data.regions import REGIONS, _is_unlocked
    region_id = selected_region_id or "border_fire"
    if region_id not in REGIONS or not _is_unlocked(state, REGIONS[region_id].get("unlock_key")):
        region_id = "border_fire"
    weapons_to_show = [
        w_id for w_id in SHOP_INVENTORY["weapon"]
        if EQUIPMENT.get(w_id, {}).get("region", "border_fire") == region_id
    ]

    weapons_list = []
    for item_id in weapons_to_show:
        if item_id in EQUIPMENT:
            eq = EQUIPMENT[item_id]
            weapons_list.append({
                "id": item_id,
                "name": eq["name"],
                "slot": eq["slot"],
                "subtype": eq["subtype"],
                "price": eq["price"],
                "jobs": eq["jobs"],
                "stats": eq["stats"],
                "desc": eq["desc"]
            })

    armors_to_show = [
        a_id for a_id in SHOP_INVENTORY["armor"]
        if EQUIPMENT.get(a_id, {}).get("region", "border_fire") == region_id
    ]

    armors_list = []
    for item_id in armors_to_show:
        if item_id in EQUIPMENT:
            eq = EQUIPMENT[item_id]
            armors_list.append({
                "id": item_id,
                "name": eq["name"],
                "slot": eq["slot"],
                "subtype": eq["subtype"],
                "price": eq["price"],
                "jobs": eq["jobs"],
                "stats": eq["stats"],
                "desc": eq["desc"]
            })

    weapons_details = {}
    for item_id, eq in EQUIPMENT.items():
        weapons_details[item_id] = {
            "id": item_id,
            "name": eq["name"],
            "slot": eq["slot"],
            "subtype": eq["subtype"],
            "price": eq["price"],
            "jobs": eq["jobs"],
            "stats": eq["stats"],
            "desc": eq["desc"]
        }

    upgrades_list = []
    whitelisted_recipes = [
        r_id for r_id, r in RECIPES.items()
        if r.get("region", "border_fire") == region_id
        and r.get("base_item")
        and EQUIPMENT.get(list(r["output"].keys())[0], {}).get("slot") != "accessory"
    ]
    for recipe_id in whitelisted_recipes:
        if recipe_id in RECIPES:
            r = RECIPES[recipe_id]
            output_id = list(r["output"].keys())[0]
            output_name = EQUIPMENT[output_id]["name"] if output_id in EQUIPMENT else r["name"]
            base_item = r.get("base_item")
            base_name = EQUIPMENT[base_item]["name"] if (base_item and base_item in EQUIPMENT) else ""

            materials_formatted = {}
            for mat_id, count in r.get("materials", {}).items():
                mat_name = MATERIALS.get(mat_id, mat_id)
                materials_formatted[mat_id] = {
                    "name": mat_name,
                    "required": count
                }

            output_stats = EQUIPMENT[output_id]["stats"] if output_id in EQUIPMENT else {}

            upgrades_list.append({
                "id": recipe_id,
                "name": r["name"],
                "output_id": output_id,
                "output_name": output_name,
                "base_item": base_item,
                "base_name": base_name,
                "materials": materials_formatted,
                "gold": r.get("gold", 0),
                "stats": output_stats,
                "desc": r.get("desc", ""),
                "unlock_quest": r.get("unlock", "")
            })

    return {
        "screen_id": "facility_workshop_screen",
        "facility_id": "workshop",
        "title": "邊境工坊 (Live)",
        "subtitle": "與遊戲核心同步的裝備交易服務，已開放武器與防具購買。",
        "player": player_data,
        "weapons": weapons_list,
        "weapons_details": weapons_details,
        "armors": armors_list,
        "upgrades": upgrades_list
    }
