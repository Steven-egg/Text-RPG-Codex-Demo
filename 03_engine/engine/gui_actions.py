from __future__ import annotations

import shutil
from datetime import datetime
from typing import Any

from data import DUNGEONS, EQUIPMENT, ITEMS, JOBS

from . import game
from .formatting import item_name


JOB_IDS = ["warrior", "mage", "rogue", "cleric"]
JOB_ID_TO_KEY = dict(zip(JOB_IDS, JOBS.keys()))
JOB_KEY_TO_ID = {value: key for key, value in JOB_ID_TO_KEY.items()}
SAVE_BACKUP_PREFIX = "save.gui-backup"


class GuiActionError(Exception):
    def __init__(self, message: str, *, status: int = 400):
        super().__init__(message)
        self.status = status


class GuiRuntimeSession:
    def __init__(self) -> None:
        self.state: dict[str, Any] | None = None
        self._save_backup_created = False

    @property
    def state_loaded(self) -> bool:
        return self.state is not None

    def require_state(self) -> dict[str, Any]:
        if self.state is None:
            raise GuiActionError("No runtime state is loaded.", status=409)
        return self.state

    def new_game(self, name: str | None, job_id: str | None) -> dict[str, Any]:
        job_key = normalize_job_id(job_id)
        character_name = str(name or "").strip() or "GUI Adventurer"
        self.state = game.create_state(character_name, job_key)
        return action_response(
            "start_new_game",
            "New game session created. Save manually to persist it.",
            self.state,
            screen_id="town_hub",
            next_route="../town_hub/index.html?mode=live",
        )

    def load_demo_seed(self) -> dict[str, Any]:
        job_key = normalize_job_id("warrior")
        self.state = game.create_state("GUI Demo Adventurer", job_key)
        self.state["level"] = max(self.state.get("level", 1), 4)
        self.state["gold"] = max(self.state.get("gold", 0), 620)
        for unlock_key in ("dungeon_moss_cave", "dungeon_scorched_mine"):
            game.unlock(self.state, unlock_key)
        game.add_item(self.state, "item_potion_s", 3)
        game.add_item(self.state, "item_focus_drop", 1)
        game.add_item(self.state, "mat_moss_fiber", 3)
        game.add_item(self.state, "mat_cracked_stone", 3)
        stats = game.get_stats(self.state)
        self.state["current_hp"] = stats["max_hp"]
        self.state["current_mp"] = stats["max_mp"]
        return action_response(
            "load_demo_seed",
            "Demo seed loaded in memory. Save manually to persist it.",
            self.state,
            screen_id="town_hub",
            next_route="../town_hub/index.html?mode=live",
        )

    def load_game(self) -> dict[str, Any]:
        loaded = game.load_game()
        if loaded is None:
            raise GuiActionError("No valid save file is available.", status=404)
        self.state = loaded
        return action_response(
            "load_game",
            "Save loaded into the live GUI session.",
            self.state,
            screen_id="town_hub",
            next_route="../town_hub/index.html?mode=live",
        )

    def save_game(self, *, screen_id: str = "world_map") -> dict[str, Any]:
        state = self.require_state()
        self._backup_save_once()
        game.save_game(state)
        return action_response("save_game", "Runtime save written.", state, screen_id=screen_id)

    def dispatch(self, action_id: str, payload: dict[str, Any] | None = None, screen_id: str | None = None) -> dict[str, Any]:
        payload = payload or {}
        if action_id in {"start_new_game", "restart_game"}:
            response = self.new_game(payload.get("name"), payload.get("job_id"))
            response["action_id"] = action_id
            return response
        if action_id == "load_demo_seed":
            return self.load_demo_seed()
        if action_id == "load_game":
            return self.load_game()
        if action_id == "save_game":
            return self.save_game(screen_id=screen_id or "world_map")
        if action_id == "rest_at_inn":
            return self.rest_at_inn(payload)
        if action_id == "open_world_map":
            state = self.require_state()
            return action_response(
                action_id,
                "Opening live World Map.",
                state,
                screen_id="world_map",
                next_route="../world_map/index.html?mode=live",
            )
        if action_id == "back_to_town_hub":
            state = self.require_state()
            return action_response(
                action_id,
                "Returning to live Town Hub.",
                state,
                screen_id="town_hub",
                next_route="../town_hub/index.html?mode=live",
            )
        if action_id == "confirm_travel":
            state = self.require_state()
            dungeon_id = payload.get("dungeon_id") or payload.get("location_id")
            if dungeon_id not in DUNGEONS:
                raise GuiActionError("Unknown dungeon.", status=400)
            dungeon = DUNGEONS[dungeon_id]
            if not game.is_unlocked(state, dungeon.get("unlock")):
                raise GuiActionError("Dungeon is locked.", status=403)
            return action_response(
                action_id,
                f"Travel confirmed: {dungeon['name']}. Exploration bridge is a later slice.",
                state,
                screen_id=screen_id or "world_map",
                next_route="../dungeon_exploration/index.html?mode=live",
            )
        raise GuiActionError(f"Unknown GUI action: {action_id}", status=404)

    def rest_at_inn(self, payload: dict[str, Any]) -> dict[str, Any]:
        state = self.require_state()
        service_id = payload.get("service_id", "overnight_rest")
        cost = int(payload.get("cost", 30))
        if service_id != "overnight_rest":
            raise GuiActionError("Unknown inn service.", status=400)
        if cost != 30:
            raise GuiActionError("Inn cost mismatch.", status=400)
        if state.get("gold", 0) < cost:
            raise GuiActionError("Not enough gold for the inn.", status=409)
        stats = game.get_stats(state)
        state["gold"] -= cost
        state["current_hp"] = stats["max_hp"]
        state["current_mp"] = stats["max_mp"]
        return action_response("rest_at_inn", "Rested at the inn. Save manually to persist.", state, screen_id="town_hub")

    def screen_model(self, screen_id: str) -> dict[str, Any]:
        if screen_id == "start_screen":
            return start_screen_model(save_exists())
        state = self.require_state()
        if screen_id == "world_map":
            return world_map_model(state)
        if screen_id == "town_hub":
            return town_hub_model(state)
        if screen_id == "inn_screen":
            return inn_screen_model(state)
        raise GuiActionError(f"Unsupported live screen: {screen_id}", status=404)

    def session_info(self) -> dict[str, Any]:
        return {
            "ok": True,
            "save_exists": save_exists(),
            "state_loaded": self.state_loaded,
            "state_summary": state_summary(self.state) if self.state is not None else None,
        }

    def _backup_save_once(self) -> None:
        if self._save_backup_created or not save_exists():
            self._save_backup_created = True
            return
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        backup_path = game.SAVE_PATH.with_name(f"{SAVE_BACKUP_PREFIX}-{timestamp}.json")
        shutil.copy2(game.SAVE_PATH, backup_path)
        self._save_backup_created = True


def normalize_job_id(job_id: str | None) -> str:
    if job_id in JOB_ID_TO_KEY:
        return JOB_ID_TO_KEY[str(job_id)]
    if job_id in JOBS:
        return str(job_id)
    raise GuiActionError("Unknown job id.", status=400)


def save_exists() -> bool:
    return game.SAVE_PATH.exists()


def state_summary(state: dict[str, Any] | None) -> dict[str, Any] | None:
    if state is None:
        return None
    game.ensure_state_defaults(state)
    stats = game.get_stats(state)
    job_key = state.get("job")
    return {
        "name": state.get("name", ""),
        "job_id": JOB_KEY_TO_ID.get(job_key, str(job_key)),
        "job_label": str(job_key),
        "level": state.get("level", 1),
        "exp": state.get("exp", 0),
        "gold": state.get("gold", 0),
        "guild_points": state.get("guild_points", 0),
        "hp": {"current": state.get("current_hp", stats["max_hp"]), "max": stats["max_hp"]},
        "mp": {"current": state.get("current_mp", stats["max_mp"]), "max": stats["max_mp"]},
        "save_exists": save_exists(),
    }


def action_response(
    action_id: str,
    message: str,
    state: dict[str, Any],
    *,
    screen_id: str | None,
    next_route: str | None = None,
) -> dict[str, Any]:
    return {
        "ok": True,
        "action_id": action_id,
        "message": message,
        "state_summary": state_summary(state),
        "screen_model": build_screen_model(screen_id, state) if screen_id else None,
        "next_route": next_route,
    }


def build_screen_model(screen_id: str | None, state: dict[str, Any]) -> dict[str, Any] | None:
    if screen_id == "world_map":
        return world_map_model(state)
    if screen_id == "town_hub":
        return town_hub_model(state)
    if screen_id == "inn_screen":
        return inn_screen_model(state)
    return None


def start_screen_model(has_save: bool) -> dict[str, Any]:
    actions = [
        {
            "action_id": "start_new_game",
            "label": "Start New Game",
            "description": "Create a live runtime session in memory.",
            "token": "NEW",
            "kind": "primary",
            "enabled": True,
            "opens_registration": True,
            "final_action_id": "start_new_game",
            "registration_entry": "new_game",
            "payload": {"entry": "new_game"},
        },
        {
            "action_id": "load_demo_seed",
            "label": "Load Demo Seed",
            "description": "Load a prepared in-memory state without writing save.json.",
            "token": "DEM",
            "kind": "secondary",
            "enabled": True,
            "payload": {},
        },
        {
            "action_id": "load_game",
            "label": "Load Save",
            "description": "Load the shared CLI/runtime save file.",
            "token": "LOD",
            "kind": "secondary",
            "enabled": has_save,
            "disabled_reason": None if has_save else "No save file is available.",
            "payload": {},
        },
    ]
    return {
        "screen_id": "start_screen",
        "screen_label": "Live Runtime",
        "title": "Element Maze",
        "hero_kicker": "Runtime-connected prototype",
        "hero_title": "Playable GUI Bridge",
        "hero_copy": "Start, load, or seed a Python runtime session. Static fixture mode remains available without ?mode=live.",
        "registration": registration_model(),
        "actions": actions,
    }


def registration_model() -> dict[str, Any]:
    return {
        "panel_label": "Adventurer Registration",
        "title": "Create Runtime Character",
        "chip": "LIVE",
        "name_label": "Name",
        "name_placeholder": "GUI Adventurer",
        "fallback_name": "GUI Adventurer",
        "job_label": "Job",
        "job_hint": "Jobs are generated from Python runtime data.",
        "default_job_id": "warrior",
        "feedback": "This creates an in-memory state. Use Save Game to persist it.",
        "back_label": "Back",
        "back_description": "Return to start actions",
        "confirm_label": "Create",
        "confirm_description": "Create live runtime state and open Town Hub",
        "jobs": [
            {"id": job_id, "index": f"{idx}.", "label": job_key, "summary": ", ".join(JOBS[job_key]["base_skills"])}
            for idx, (job_id, job_key) in enumerate(JOB_ID_TO_KEY.items(), start=1)
        ],
    }


def player_model(state: dict[str, Any]) -> dict[str, Any]:
    summary = state_summary(state) or {}
    hp = summary["hp"]
    mp = summary["mp"]
    return {
        "name": summary["name"],
        "class_label": summary["job_label"],
        "level_label": f"Lv{summary['level']}",
        "hp": {"label": f"HP {hp['current']}/{hp['max']}", "percent": percent(hp["current"], hp["max"])},
        "mp": {"label": f"MP {mp['current']}/{mp['max']}", "percent": percent(mp["current"], mp["max"])},
        "gold_label": f"{summary['gold']}G",
    }


def resource_strip(state: dict[str, Any]) -> list[dict[str, str]]:
    summary = state_summary(state) or {}
    hp = summary["hp"]
    mp = summary["mp"]
    return [
        {"id": "hero", "label": f"{summary['name']} / {summary['job_label']} Lv{summary['level']}", "tone": "primary"},
        {"id": "hp", "label": f"HP {hp['current']}/{hp['max']}", "tone": "healthy"},
        {"id": "mp", "label": f"MP {mp['current']}/{mp['max']}", "tone": "mana"},
        {"id": "gold", "label": f"{summary['gold']}G", "tone": "gold"},
        {"id": "guild_points", "label": f"Guild {summary['guild_points']}", "tone": "neutral"},
    ]


def world_map_model(state: dict[str, Any]) -> dict[str, Any]:
    locations = []
    positions = [(35, 22), (24, 48), (49, 42), (48, 67)]
    for index, (dungeon_id, dungeon) in enumerate(DUNGEONS.items()):
        unlocked = game.is_unlocked(state, dungeon.get("unlock"))
        x, y = positions[index] if index < len(positions) else (40 + index * 8, 50)
        locations.append(
            {
                "location_id": dungeon_id,
                "label": dungeon["name"],
                "description": f"{dungeon['recommended']} / {dungeon['steps']} steps",
                "detail_note": "Live runtime validates travel availability.",
                "position": {"x": x, "y": y},
                "tone": "fire" if "fire" in dungeon_id or "cinder" in dungeon_id else "nature",
                "icon_token": "DG",
                "unlocked": unlocked,
                "locked_reason": None if unlocked else "Locked by runtime state.",
                "favorite": index == 0,
                "status_label": "Open" if unlocked else "Locked",
                "recommended_level": dungeon["recommended"],
                "steps": f"{dungeon['steps']} steps",
                "attribute": dungeon["element"],
                "clear_state": "Cleared" if dungeon_id in state.get("cleared_dungeons", []) else "Uncleared",
                "exploration_rating": "Runtime",
                "boss": boss_label(dungeon.get("boss")),
                "preview_role": "cave",
                "primary_action": {
                    "action_id": "confirm_travel",
                    "label": "Travel",
                    "enabled": unlocked,
                    "disabled_reason": None if unlocked else "Dungeon is locked.",
                    "payload": {"dungeon_id": dungeon_id},
                },
            }
        )
    return {
        "screen_id": "world_map",
        "title": "World Map",
        "subtitle": "Live runtime map model.",
        "selected_location_id": locations[0]["location_id"] if locations else None,
        "current_location_id": "town_hub",
        "player": player_model(state),
        "menu_actions": [
            {"action_id": "open_world_map", "label": "Refresh Map", "description": "Reload live map state.", "enabled": True, "payload": {}},
            {"action_id": "save_game", "label": "Save Game", "description": "Write the shared runtime save.", "enabled": True, "payload": {}},
            {"action_id": "back_to_town_hub", "label": "Town Hub", "description": "Return to live town.", "enabled": True, "payload": {}},
            {"action_id": "back_to_start_screen", "label": "Start Screen", "description": "Return to start screen.", "enabled": True, "payload": {}},
        ],
        "route_segments": [],
        "locations": locations,
    }


def town_hub_model(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "screen_id": "town_hub",
        "title": "Live Town Hub",
        "subtitle": "Resource strip and key actions are backed by Python runtime state.",
        "resource_strip": resource_strip(state),
        "town_guidance": [
            "Live mode: actions are validated by Python runtime.",
            "Use World Map to continue the playable loop, or rest at the inn from this hub.",
        ],
        "selected_facility_id": "guild",
        "facility_nodes": facility_nodes(state),
        "navigation_actions": [
            {"action_id": "open_world_map", "label": "World Map", "description": "Open live World Map.", "enabled": True, "payload": {}},
            {"action_id": "save_game", "label": "Save Game", "description": "Write the shared runtime save.", "enabled": True, "payload": {}},
        ],
    }


def facility_nodes(state: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        facility("guild", "Guild", "Quest board and material turn-in are later bridge slices.", "guild", "open_facility", enabled=False),
        facility("inn", "Inn", "Spend 30G to restore HP/MP.", "bed", "rest_at_inn", payload={"service_id": "overnight_rest", "cost": 30}),
        facility("travel_shop", "Travel Shop", "Buying and selling are later bridge slices.", "shop", "open_facility", enabled=False),
        facility("workshop", "Workshop", "Equipment buying and upgrades are later bridge slices.", "hammer", "open_facility", enabled=False),
        facility("synthesis", "Synthesis", "Crafting is a later bridge slice.", "alchemy", "open_facility", enabled=False),
        facility("magic_shop", "Magic Shop", "Learning magic is a later bridge slice.", "magic", "open_facility", enabled=False),
        facility("temple", "Temple", "Preview-only for now; story mutation needs explicit action.", "temple", "open_facility", enabled=False),
        facility("relic_preview", "Relic Preview", "Preview-only for now.", "relic", "open_facility", enabled=False),
        facility("storage", "Storage", "Storage transfer is a later bridge slice.", "storage", "open_facility", enabled=False),
    ]


def facility(
    facility_id: str,
    label: str,
    description: str,
    icon_role: str,
    action_id: str,
    *,
    payload: dict[str, Any] | None = None,
    enabled: bool = True,
) -> dict[str, Any]:
    return {
        "facility_id": facility_id,
        "label": label,
        "description": description,
        "visual_group": facility_id,
        "visual_anchor": facility_id,
        "icon_role": icon_role,
        "enabled": enabled,
        "disabled_reason": None if enabled else "This live action is scheduled for a later slice.",
        "badges": [],
        "primary_action": action_id,
        "payload": payload or {"facility_id": facility_id},
    }


def inn_screen_model(state: dict[str, Any]) -> dict[str, Any]:
    summary = state_summary(state) or {}
    return {
        "screen_id": "inn_screen",
        "title": "Live Inn",
        "subtitle": "Runtime-backed rest action.",
        "resource_strip": resource_strip(state),
        "service": {
            "service_id": "overnight_rest",
            "label": "Overnight Rest",
            "cost": 30,
            "enabled": summary.get("gold", 0) >= 30,
            "disabled_reason": None if summary.get("gold", 0) >= 30 else "Not enough gold.",
            "payload": {"service_id": "overnight_rest", "cost": 30},
        },
    }


def boss_label(boss_id: str | None) -> str:
    if not boss_id:
        return "-"
    monster = game.MONSTERS.get(boss_id)
    return monster["name"] if monster else boss_id


def percent(current: int, maximum: int) -> int:
    if maximum <= 0:
        return 0
    return max(0, min(100, round(current / maximum * 100)))


def inventory_preview(state: dict[str, Any]) -> list[dict[str, Any]]:
    entries = []
    for item_id, qty in state.get("inventory", {}).items():
        data = ITEMS.get(item_id) or EQUIPMENT.get(item_id) or {}
        entries.append({"item_id": item_id, "label": data.get("name", item_name(item_id)), "quantity": qty})
    return entries
