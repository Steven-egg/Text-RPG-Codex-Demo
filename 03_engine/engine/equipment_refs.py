"""Read-only equipment-reference helpers for the Phase 4B transition."""
from __future__ import annotations

from copy import deepcopy

from data import EQUIPMENT


def equipment_base_id(state: dict, reference_id: str | None) -> str | None:
    """Return the static EQUIPMENT base ID for static or instance references."""
    if reference_id in EQUIPMENT:
        return reference_id
    instance = state.get("equipment_instances", {}).get(reference_id)
    base_item_id = instance.get("base_item_id") if isinstance(instance, dict) else None
    return base_item_id if base_item_id in EQUIPMENT else None


def resolve_equipment_ref(state: dict, reference_id: str | None) -> dict | None:
    """Return detached display data and never mutate global EQUIPMENT."""
    base_item_id = equipment_base_id(state, reference_id)
    if not base_item_id:
        return None
    instance = state.get("equipment_instances", {}).get(reference_id)
    return {
        "reference_id": reference_id,
        "base_item_id": base_item_id,
        "base": deepcopy(EQUIPMENT[base_item_id]),
        "instance": deepcopy(instance) if isinstance(instance, dict) else None,
    }


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
