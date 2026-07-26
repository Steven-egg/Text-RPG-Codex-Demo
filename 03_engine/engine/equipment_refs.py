"""Read-only equipment-reference helpers for the Phase 4B transition."""
from __future__ import annotations

from copy import deepcopy

from data import AFFIXES, EQUIPMENT
from .equipment_quality import affix_value_multiplier


def equipment_base_id(state: dict, reference_id: str | None) -> str | None:
    """Return the static EQUIPMENT base ID for static or instance references."""
    if reference_id in EQUIPMENT:
        return reference_id
    instance = state.get("equipment_instances", {}).get(reference_id)
    base_item_id = instance.get("base_item_id") if isinstance(instance, dict) else None
    return base_item_id if base_item_id in EQUIPMENT else None


def resolve_equipment_ref(state: dict, reference_id: str | None) -> dict | None:
    """Return detached base/effective data and never mutate global data."""
    base_item_id = equipment_base_id(state, reference_id)
    if not base_item_id:
        return None
    base = deepcopy(EQUIPMENT[base_item_id])
    instance = state.get("equipment_instances", {}).get(reference_id)
    affixes, affix_stats = _resolve_affixes(base, instance)
    effective_stats = deepcopy(base.get("stats", {}))
    for stat_key, value in affix_stats.items():
        effective_stats[stat_key] = effective_stats.get(stat_key, 0) + value
    return {
        "reference_id": reference_id,
        "base_item_id": base_item_id,
        "base": base,
        "instance": deepcopy(instance) if isinstance(instance, dict) else None,
        "affixes": affixes,
        "affix_stats": affix_stats,
        "effective_stats": effective_stats,
        "quality": (instance or {}).get("quality", "normal") if isinstance(instance, dict) else "normal",
    }


def _resolve_affixes(base: dict, instance: object) -> tuple[dict[str, dict], dict[str, float]]:
    """Resolve valid fixed affixes without normalizing or mutating state."""
    affixes: dict[str, dict] = {}
    increments: dict[str, float] = {}
    multiplier = affix_value_multiplier(instance.get("quality") if isinstance(instance, dict) else None)
    used_families: set[str] = set()
    for tier in ("major", "minor"):
        raw_id = instance.get(f"{tier}_affix_id") if isinstance(instance, dict) else None
        view = {"id": raw_id, "status": "none"}
        affix = AFFIXES.get(raw_id) if isinstance(raw_id, str) else None
        if raw_id is None:
            affixes[tier] = view
            continue
        if not affix:
            view["status"] = "invalid_id"
        elif affix["tier"] != tier:
            view["status"] = "invalid_tier"
        elif base["slot"] not in affix["slots"]:
            view["status"] = "invalid_slot"
        elif affix["family"] in used_families:
            view["status"] = "duplicate_family"
        else:
            effective_affix_stats = {
                stat_key: value * multiplier
                for stat_key, value in affix["stats"].items()
            }
            view.update({
                "name": affix["name"],
                "tier": affix["tier"],
                "family": affix["family"],
                "stats": effective_affix_stats,
                "status": "valid",
            })
            used_families.add(affix["family"])
            for stat_key, value in effective_affix_stats.items():
                increments[stat_key] = increments.get(stat_key, 0) + value
        affixes[tier] = view
    return affixes, increments


def is_equipment_ref(state: dict, reference_id: str | None) -> bool:
    return equipment_base_id(state, reference_id) is not None


def inventory_equipment_refs(state: dict, base_item_id: str | None = None) -> list[str]:
    return [
        reference_id
        for reference_id, quantity in state.get("inventory", {}).items()
        if quantity > 0
        and (base_item_id is None or equipment_base_id(state, reference_id) == base_item_id)
        and is_equipment_ref(state, reference_id)
    ]


def equipment_ref_count(state: dict, base_item_id: str, *, include_equipped: bool = False) -> int:
    count = sum(state.get("inventory", {}).get(reference_id, 0) for reference_id in inventory_equipment_refs(state, base_item_id))
    if include_equipped:
        count += sum(
            1 for reference_id in state.get("equipment", {}).values()
            if equipment_base_id(state, reference_id) == base_item_id
        )
    return count


def first_inventory_equipment_ref(state: dict, base_item_id: str) -> str | None:
    refs = inventory_equipment_refs(state, base_item_id)
    return refs[0] if refs else None


def equipped_reference_for_base(state: dict, base_item_id: str) -> str | None:
    return next(
        (reference_id for reference_id in state.get("equipment", {}).values()
         if equipment_base_id(state, reference_id) == base_item_id),
        None,
    )
