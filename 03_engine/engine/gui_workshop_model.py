from __future__ import annotations

from typing import Any
from data import EQUIPMENT, SHOP_INVENTORY, RECIPES
from . import game
from .equipment_refs import equipment_base_id, inventory_equipment_refs, resolve_equipment_ref
from .equipment_quality import QUALITY_LABELS
from .gui_presentation import equipment_affix_names, equipment_slot_comparison, equipment_stat_rows


def _shop_equipment_row(state: dict[str, Any], item_id: str) -> dict[str, Any]:
    eq = EQUIPMENT[item_id]
    equipped_same_base = any(
        equipment_base_id(state, reference_id) == item_id
        for reference_id in state.get("equipment", {}).values()
    )
    return {
        "id": item_id,
        "name": eq["name"],
        "slot": eq["slot"],
        "subtype": eq["subtype"],
        "price": eq["price"],
        "jobs": eq["jobs"],
        "stats": eq["stats"],
        "stat_rows": equipment_stat_rows(eq["stats"]),
        "desc": eq["desc"],
        "owned_count": game.equipment_ref_count(state, item_id, include_equipped=True),
        "equipped_same_base": equipped_same_base,
        "comparison": equipment_slot_comparison(state, item_id),
    }


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
            weapons_list.append(_shop_equipment_row(state, item_id))

    armors_to_show = [
        a_id for a_id in SHOP_INVENTORY["armor"]
        if EQUIPMENT.get(a_id, {}).get("region", "border_fire") == region_id
    ]

    armors_list = []
    for item_id in armors_to_show:
        if item_id in EQUIPMENT:
            armors_list.append(_shop_equipment_row(state, item_id))

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
            "stat_rows": equipment_stat_rows(eq["stats"]),
            "desc": eq["desc"]
        }

    upgrades_list = []
    workshop_recipes = game.workshop_recipe_ids(region_id)
    for recipe_id in workshop_recipes:
        if recipe_id in RECIPES:
            r = RECIPES[recipe_id]
            output_id = list(r["output"].keys())[0]
            output_name = EQUIPMENT[output_id]["name"] if output_id in EQUIPMENT else r["name"]
            base_item = r.get("base_item")
            base_name = EQUIPMENT[base_item]["name"] if (base_item and base_item in EQUIPMENT) else ""

            material_rows = game.recipe_material_requirements(state, r)
            materials_formatted = {
                row["id"]: {
                    "name": row["name"],
                    "owned": row["owned"],
                    "required": row["required"],
                    "missing": row["missing"],
                    "satisfied": row["satisfied"],
                }
                for row in material_rows
            }
            missing_materials = [row for row in material_rows if not row["satisfied"]]

            output_stats = EQUIPMENT[output_id]["stats"] if output_id in EQUIPMENT else {}
            output_jobs = EQUIPMENT[output_id].get("jobs", []) if output_id in EQUIPMENT else []
            unlocked = game.is_unlocked(state, r.get("unlock"))
            job_compatible = game.recipe_job_compatible(state, recipe_id)
            base_inventory_count = game.equipment_ref_count(state, base_item) if base_item else 0
            base_equipped = bool(base_item) and any(
                equipment_base_id(state, reference_id) == base_item
                for reference_id in state.get("equipment", {}).values()
            )

            upgrades_list.append({
                "id": recipe_id,
                "name": r["name"],
                "output_id": output_id,
                "output_name": output_name,
                "base_item": base_item,
                "base_name": base_name,
                "materials": materials_formatted,
                "missing_materials": missing_materials,
                "materials_satisfied": not missing_materials,
                "material_shortage_message": game.recipe_material_shortage_message(state, r),
                "gold": r.get("gold", 0),
                "stats": output_stats,
                "jobs": output_jobs,
                "desc": r.get("desc", ""),
                "unlocked": unlocked,
                "unlock_condition": game.recipe_unlock_condition(recipe_id),
                "locked_reason": game.recipe_locked_reason(state, recipe_id),
                "job_compatible": job_compatible,
                "job_blocked_reason": None if job_compatible else game.recipe_unavailable_reason(state, recipe_id),
                "base_inventory_count": base_inventory_count,
                "base_equipped": base_equipped,
                "base_owned_count": base_inventory_count + (1 if base_equipped else 0),
            })

    owned_equipment = []
    equipped_by_reference = {
        reference_id: slot
        for slot, reference_id in state.get("equipment", {}).items()
        if reference_id
    }
    for reference_id in [*inventory_equipment_refs(state), *equipped_by_reference]:
        resolved = resolve_equipment_ref(state, reference_id)
        if not resolved:
            continue
        base = resolved["base"]
        owned_equipment.append({
            "id": reference_id,
            "base_item_id": resolved["base_item_id"],
            "name": base["name"],
            "slot": base["slot"],
            "subtype": base["subtype"],
            "jobs": base["jobs"],
            "stats": resolved["effective_stats"],
            "stat_rows": equipment_stat_rows(resolved["effective_stats"]),
            "desc": base["desc"],
            "equipped_slot": equipped_by_reference.get(reference_id),
            "quality_label": QUALITY_LABELS.get(resolved["quality"], "普通"),
            "affix_names": equipment_affix_names(resolved),
            "comparison": equipment_slot_comparison(state, reference_id),
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
        "upgrades": upgrades_list,
        "owned_equipment": owned_equipment,
    }
