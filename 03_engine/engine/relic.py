from __future__ import annotations

from data import (
    RELICS,
    get_facility_display_name,
    say,
    has_template,
)
from .display import (
    title,
    pause,
    action_menu_panel,
    render_panel,
)
from .formatting import item_name
from .state import (
    ICE_REGION_UNLOCK,
    FINAL_REGION_UNLOCK,
    is_unlocked,
    unlock,
    add_item,
    remove_item,
    check_and_normalize_region,
)

ELEMENTAL_SEAL_FLAGS = (
    "fire_seal_enshrined",
    "ice_seal_enshrined",
    "earth_seal_enshrined",
    "thunder_seal_enshrined",
)


def relic_unlock_met(state: dict, unlock_data: dict | None) -> bool:
    if not unlock_data:
        return True
    kind = unlock_data.get("kind")
    if kind == "level":
        return state.get("level", 0) >= unlock_data.get("value", 0)
    if kind == "unlock":
        return is_unlocked(state, unlock_data.get("key"))
    if kind == "quest":
        return unlock_data.get("key") in state.get("completed_quests", [])
    if kind == "flag":
        return bool(state.get("flags", {}).get(unlock_data.get("key")))
    if kind == "item":
        return state.get("inventory", {}).get(unlock_data.get("key"), 0) > 0
    return False


def relic_unlock_line(state: dict, unlock_data: dict | None) -> str:
    if not unlock_data:
        return "解鎖提示：目前無額外提示。"
    status = "已達成" if relic_unlock_met(state, unlock_data) else "未達成"
    return f"解鎖提示：{unlock_data['label']}（{status}）"


def preview_relic_entries() -> list[tuple[str, dict]]:
    return [
        (relic_id, relic)
        for relic_id, relic in RELICS.items()
        if relic.get("status") == "preview"
    ]


def find_preview_relic(identifier: str | None) -> tuple[str, dict] | None:
    if not identifier:
        return None
    for relic_id, relic in preview_relic_entries():
        if identifier in {relic_id, relic.get("name"), relic.get("seal_item_id"), relic.get("element_id")}:
            return relic_id, relic
    return None


def relic_source_required(relic: dict) -> int:
    required = relic.get("source_required", 1)
    return required if isinstance(required, int) and required > 0 else 1


def relic_source_count(state: dict, relic: dict) -> int:
    return state.get("inventory", {}).get(relic.get("source_item_id"), 0)


def relic_enshrined(state: dict, relic: dict) -> bool:
    return bool(state.get("flags", {}).get(relic.get("complete_flag")))


def relic_passive_choices(relic: dict) -> list[dict]:
    return [choice for choice in relic.get("passive_choices", []) if isinstance(choice, dict)]


def selected_relic_passive(state: dict, relic_id: str, relic: dict) -> dict | None:
    choice_id = state.get("relic_passives", {}).get(relic_id)
    return next((choice for choice in relic_passive_choices(relic) if choice.get("id") == choice_id), None)


def active_relic_passive_effects(state: dict) -> dict[str, int]:
    effects: dict[str, int] = {}
    for relic_id, relic in preview_relic_entries():
        if not relic_enshrined(state, relic):
            continue
        selected = selected_relic_passive(state, relic_id, relic)
        if not selected:
            continue
        for effect_id, value in selected.get("effect", {}).items():
            if isinstance(value, int):
                effects[effect_id] = effects.get(effect_id, 0) + value
    return effects


def select_relic_passive(state: dict, relic_identifier: str | None, choice_id: str | None) -> dict:
    found = find_preview_relic(relic_identifier)
    if not found:
        return {"status": "blocked", "changed": False, "message": "找不到指定的聖印資料。"}
    relic_id, relic = found
    if not relic_enshrined(state, relic):
        return {"status": "blocked", "changed": False, "relic_id": relic_id, "message": "必須先安置此聖印，才能選擇被動效果。"}
    selected = next((choice for choice in relic_passive_choices(relic) if choice.get("id") == choice_id), None)
    if not selected:
        return {"status": "blocked", "changed": False, "relic_id": relic_id, "message": "此聖印沒有指定的被動選項。"}
    state.setdefault("relic_passives", {})[relic_id] = selected["id"]
    return {
        "status": "selected",
        "changed": True,
        "relic_id": relic_id,
        "choice_id": selected["id"],
        "message": f"{relic['name']} 已選擇「{selected['label']}」。可隨時免費改選。",
    }


def relic_ready_to_enshrine(state: dict, relic: dict) -> bool:
    return (
        not relic_enshrined(state, relic)
        and relic_unlock_met(state, relic.get("unlock"))
        and relic_source_count(state, relic) >= relic_source_required(relic)
    )


def relic_disabled_reason(state: dict, relic: dict) -> str | None:
    if relic_enshrined(state, relic):
        return "聖印已安置。"
    if not relic_unlock_met(state, relic.get("unlock")):
        unlock_data = relic.get("unlock") or {}
        return f"尚未達成：{unlock_data.get('label', '前置條件')}。"
    source_item_id = relic.get("source_item_id", "")
    required = relic_source_required(relic)
    current = relic_source_count(state, relic)
    if current < required:
        return f"需要 {item_name(source_item_id)} x{required}（目前 {current}）。"
    return None


def ready_relic_names(state: dict) -> list[str]:
    return [
        relic["name"]
        for _relic_id, relic in preview_relic_entries()
        if relic_ready_to_enshrine(state, relic)
    ]


def all_elemental_seals_enshrined(state: dict) -> bool:
    flags = state.get("flags", {})
    return all(flags.get(flag) for flag in ELEMENTAL_SEAL_FLAGS)


def unlock_final_region_from_relics(state: dict) -> bool:
    if not all_elemental_seals_enshrined(state):
        return False
    if is_unlocked(state, FINAL_REGION_UNLOCK):
        return False
    unlock(state, FINAL_REGION_UNLOCK)
    return True


def enshrine_relic(state: dict, identifier: str | None) -> dict:
    found = find_preview_relic(identifier)
    if not found:
        return {
            "status": "blocked",
            "changed": False,
            "message": "找不到指定的聖印資料。",
        }

    relic_id, relic = found
    if relic_enshrined(state, relic):
        return {
            "status": "complete",
            "changed": False,
            "relic_id": relic_id,
            "message": relic["complete_text"],
        }

    disabled_reason = relic_disabled_reason(state, relic)
    if disabled_reason:
        return {
            "status": "blocked",
            "changed": False,
            "relic_id": relic_id,
            "message": disabled_reason,
        }

    source_item_id = relic["source_item_id"]
    required = relic_source_required(relic)
    if not remove_item(state, source_item_id, required):
        return {
            "status": "blocked",
            "changed": False,
            "relic_id": relic_id,
            "message": f"需要 {item_name(source_item_id)} x{required}。",
        }

    seal_item_id = relic["seal_item_id"]
    add_item(state, seal_item_id, 1)
    state.setdefault("flags", {})[relic["complete_flag"]] = True

    unlocked_lines = []
    if relic.get("element_id") == "fire" and not is_unlocked(state, ICE_REGION_UNLOCK):
        unlock(state, ICE_REGION_UNLOCK)
        unlocked_lines.append("極寒區域路線已開放。")
    if unlock_final_region_from_relics(state):
        unlocked_lines.append("四聖印已安置，魔王城前線路線已開放。")

    message_lines = [
        relic["ready_text"],
        f"取得並安置：{item_name(seal_item_id)} x1。",
        "可至轉職神殿選擇或免費改選聖印被動效果。",
    ]
    message_lines.extend(unlocked_lines)
    return {
        "status": "enshrined",
        "changed": True,
        "relic_id": relic_id,
        "message": "\n".join(message_lines),
    }


def relic_passive_menu(state: dict) -> None:
    enshrined = [
        (relic_id, relic)
        for relic_id, relic in preview_relic_entries()
        if relic_enshrined(state, relic)
    ]
    if not enshrined:
        render_panel("聖印被動", ["尚未安置任何聖印。"], border_style="yellow")
        return
    options = []
    for relic_id, relic in enshrined:
        selected = selected_relic_passive(state, relic_id, relic)
        current = selected["label"] if selected else "尚未選擇"
        options.append(f"{relic['name']} / 目前：{current}")
    choice = action_menu_panel("聖印被動", options, "轉職神殿", header_lines=["每枚已安置聖印可選一項被動，可免費改選。"], allow_back=True, border_style="yellow")
    if not choice:
        return
    relic_id, relic = enshrined[choice - 1]
    passive_options = relic_passive_choices(relic)
    passive_choice = action_menu_panel(
        relic["name"],
        [f"{entry['label']} / {entry['summary']}" for entry in passive_options],
        "轉職神殿",
        header_lines=["選擇後可隨時免費改選。"],
        allow_back=True,
        border_style="yellow",
    )
    if passive_choice:
        result = select_relic_passive(state, relic_id, passive_options[passive_choice - 1]["id"])
        render_panel("聖印被動結果", result["message"].splitlines(), border_style="yellow")


def relic_preview_menu(state: dict, region_id: str = "border_fire") -> None:
    region_id = check_and_normalize_region(state, region_id)
    facility_name = get_facility_display_name(region_id, "relic")
    title(facility_name)
    previews = [relic for _relic_id, relic in preview_relic_entries()]
    if not previews:
        print("目前沒有可預覽的聖物線索。")
        pause()
        return

    print("四元素聖印可在此合成或安置；聖印被動效果尚未開放。")
    for relic in previews:
        complete = relic_enshrined(state, relic)
        ready = relic_ready_to_enshrine(state, relic)
        print(f"\n{relic['name']}")
        print(relic["summary"])
        print(f"來源：{relic['source']}")
        print(relic_unlock_line(state, relic.get("unlock")))
        print(f"源證：{item_name(relic['source_item_id'])} {relic_source_count(state, relic)}/{relic_source_required(relic)}")
        print("狀態：" + ("已安置" if complete else ("可安置" if ready else "待調查")))
        print(f"效果預告：{relic['effect_preview']}")
    ready_entries = [
        (relic_id, relic)
        for relic_id, relic in preview_relic_entries()
        if relic_ready_to_enshrine(state, relic)
    ]
    if ready_entries:
        options = [relic["action_label"] for _relic_id, relic in ready_entries]
        choice = action_menu_panel(
            "聖印安置",
            options,
            facility_name,
            header_lines=["選擇可安置的聖印。此操作不會啟用任何戰鬥效果。"],
            allow_back=True,
            border_style="yellow",
        )
        if choice:
            relic_id, _relic = ready_entries[choice - 1]
            result = enshrine_relic(state, relic_id)
            render_panel("聖印安置結果", result["message"].splitlines(), border_style="yellow")
    else:
        print("\n目前沒有可安置的聖印。")
    print("\n這裡不會裝備、啟用、強化聖物，也不會提供戰鬥加成。")
    pause()
