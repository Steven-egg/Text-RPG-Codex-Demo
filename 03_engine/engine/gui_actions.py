from __future__ import annotations

import random
import shutil
from copy import deepcopy
from datetime import datetime
from typing import Any

from data import (
    DUNGEONS,
    EQUIPMENT,
    ITEMS,
    JOBS,
    MAGIC_BOOKS,
    QUESTS,
    RECIPES,
    REGIONS,
    SHOP_INVENTORY,
    SKILLS,
    get_unlocked_regions,
)
from .equipment_refs import is_equipment_ref, resolve_equipment_ref

from . import game
from .formatting import item_name
from .story_beats import (
    boss_story_beat_id,
    region_story_beat_id,
    take_story_beat,
)
from .gui_shop_model import shop_screen_model
from .gui_magic_shop_model import magic_shop_screen_model
from .gui_workshop_model import workshop_screen_model
from .gui_storage_model import storage_screen_model
from .gui_presentation import resource_strip
from .gui_synthesis_model import synthesis_screen_model
from .gui_temple_model import temple_screen_model
from .gui_relic_preview_model import relic_preview_screen_model
from .gui_guild_model import guild_screen_model
from .gui_presentation_helpers import (
    JOB_IDS,
    JOB_ID_TO_KEY,
    JOB_KEY_TO_ID,
    save_exists,
    percent,
    state_summary,
    player_model,
    normalize_job_id,
)
from .gui_world_map_model import (
    WORLD_MAP_PRESENTATION,
    WORLD_MAP_ROUTE_SEGMENTS,
    WORLD_MAP_PREVIEW_LOCATIONS,
    REGION_ORDER,
    REGION_LABELS,
    REGION_TONES,
    REGION_TOKENS,
    REGION_X,
    REGION_TOWN_Y,
    DUNGEON_Y,
    REGION_ROUTE_ENABLED,
    REGION_GATE_DESTINATIONS,
    REGION_MAP_ASSETS,
    REGION_TOWN_ASSETS,
    REGION_TOWN_POSITIONS,
    REGION_GATE_POSITIONS,
    REGION_DUNGEON_LAYOUTS,
    region_town_location_id,
    region_route_status,
    region_runtime_unlocked,
    region_route_enabled,
    normalize_region_id,
    region_locked_reason,
    region_options_model,
    default_region_id,
    region_for_dungeon_id,
    active_dungeon_id_for_slot,
    region_gate_options_model,
    legacy_world_map_model,
    world_map_model,
)
from .gui_town_hub_model import (
    FACILITY_VISUALS,
    legacy_town_hub_model,
    facility_nodes,
    facility,
    town_hub_model,
    inn_screen_model,
)
from .gui_exploration_model import exploration_screen_model
from .gui_combat_model import (
    combat_item_rows,
    combat_skill_rows,
    result_overlay_model,
    combat_screen_model,
)

SAVE_BACKUP_PREFIX = "save.gui-backup"
STORAGE_UNLOCK_COST = game.STORAGE_UNLOCK_COST




class GuiActionError(Exception):
    def __init__(
        self,
        message: str,
        *,
        status: int = 400,
        result_status: str | None = None,
        blocked_reason: str | None = None,
    ):
        super().__init__(message)
        self.status = status
        self.result_status = result_status or ("blocked" if status in {403, 409} else "error")
        self.blocked_reason = blocked_reason or (message if self.result_status == "blocked" else None)


class GuiRuntimeSession:
    def __init__(self) -> None:
        self.state: dict[str, Any] | None = None
        self.exploration: dict[str, Any] | None = None
        self.combat: dict[str, Any] | None = None
        self.current_region_id = "border_fire"
        self._save_backup_created = False

    @property
    def state_loaded(self) -> bool:
        return self.state is not None

    def require_state(self) -> dict[str, Any]:
        if self.state is None:
            raise GuiActionError("未載入遊戲核心狀態。", status=409)
        return self.state

    def set_current_region(self, requested_region_id: str | None = None) -> str:
        state = self.require_state()
        self.current_region_id = normalize_region_id(state, requested_region_id or self.current_region_id)
        if "flags" not in state:
            state["flags"] = {}
        state["flags"]["current_region_id"] = self.current_region_id
        return self.current_region_id

    def new_game(self, name: str | None, job_id: str | None) -> dict[str, Any]:
        job_key = normalize_job_id(job_id)
        character_name = str(name or "").strip() or "見習冒險者"
        self.state = game.create_state(character_name, job_key)
        self.current_region_id = "border_fire"
        self._clear_live_run()
        story_beat = take_story_beat(
            self.state,
            "prologue.new_game",
            context={"player": character_name, "job": job_key},
        )
        return action_response(
            "start_new_game",
            "新的冒險者名冊已建立。可在世界地圖主選單進行存檔。",
            self.state,
            screen_id="town_hub",
            next_route="../town_hub/index.html?mode=live",
            story_beat=story_beat,
        )

    def load_demo_seed(self) -> dict[str, Any]:
        job_key = normalize_job_id("warrior")
        self.state = game.create_state("GUI Demo Adventurer", job_key)
        self.current_region_id = "border_fire"
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
        self._clear_live_run()
        return action_response(
            "load_demo_seed",
            "Demo 初始存檔已載入記憶體。請手動存檔以儲存進度。",
            self.state,
            screen_id="town_hub",
            next_route="../town_hub/index.html?mode=live",
        )

    def load_game(self) -> dict[str, Any]:
        loaded = game.load_game()
        if loaded is None:
            raise GuiActionError(
                "無可用的有效存檔資料。",
                status=404,
                result_status="blocked",
                blocked_reason="無可用的有效存檔資料。",
            )
        self.state = loaded
        saved_region = loaded.get("flags", {}).get("current_region_id")
        self.current_region_id = normalize_region_id(loaded, saved_region)
        self._clear_live_run()
        return action_response(
            "load_game",
            "存檔已成功載入 Live 遊戲會話中。",
            self.state,
            screen_id="town_hub",
            next_route="../town_hub/index.html?mode=live",
            selected_region_id=self.current_region_id,
        )

    def save_game(self, *, screen_id: str = "world_map") -> dict[str, Any]:
        state = self.require_state()
        if "flags" not in state:
            state["flags"] = {}
        state["flags"]["current_region_id"] = self.current_region_id
        self._backup_save_once()
        game.save_game(state)
        if screen_id == "town_hub":
            screen_model = town_hub_model(state, selected_region_id=self.current_region_id)
        elif screen_id in {"guild_screen", "facility_guild_screen"}:
            screen_model = self.guild_screen_model()
        else:
            screen_model = world_map_model(state, self.current_region_id)
        return self._live_response("save_game", "Saved.", screen_model=screen_model)

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
        if action_id == "view_status":
            state = self.require_state()
            model = world_map_model(state, self.current_region_id)
            model["utility_preview"] = {
                "type": "status",
                "title": "角色狀態摘要",
                "data": get_status_preview_data(state)
            }
            return self._live_response(
                action_id,
                "已開啟角色狀態摘要。",
                screen_model=model,
            )
        if action_id == "open_inventory":
            state = self.require_state()
            model = world_map_model(state, self.current_region_id)
            model["utility_preview"] = {
                "type": "inventory",
                "title": "背包 / 裝備",
                "data": get_inventory_preview_data(state)
            }
            return self._live_response(
                action_id,
                "已開啟背包 / 裝備。",
                screen_model=model,
            )
        if action_id == "open_bestiary":
            state = self.require_state()
            model = world_map_model(state, self.current_region_id)
            model["utility_preview"] = {
                "type": "bestiary",
                "title": "魔物圖鑑摘要",
                "data": get_bestiary_preview_data(state)
            }
            return self._live_response(
                action_id,
                "已開啟魔物圖鑑摘要。",
                screen_model=model,
            )
        if action_id == "buy_item":
            return self.buy_item(payload, screen_id=screen_id)
        if action_id == "buy_equipment":
            return self.buy_equipment(payload, screen_id=screen_id)
        if action_id == "equip_weapon":
            return self.equip_weapon(payload, screen_id=screen_id)
        if action_id == "learn_magic_book":
            return self.learn_magic_book(payload, screen_id=screen_id)
        if action_id == "craft_recipe":
            return self.craft_recipe(payload, screen_id=screen_id)
        if action_id == "rest_at_inn":
            return self.rest_at_inn(payload, screen_id=screen_id)
        if action_id == "unlock_storage":
            return self.unlock_storage(payload, screen_id=screen_id)
        if action_id == "deposit_item":
            return self.deposit_item(payload, screen_id=screen_id)
        if action_id == "withdraw_item":
            return self.withdraw_item(payload, screen_id=screen_id)
        if action_id == "equip_equipment":
            return self.equip_equipment(payload, screen_id=screen_id)
        if action_id == "upgrade_equipment":
            return self.upgrade_equipment(payload, screen_id=screen_id)
        if action_id == "accept_boss_glen_investigation":
            return self.accept_boss_glen_investigation(payload, screen_id=screen_id)
        if action_id == "fire_mark_guild_inquiry":
            return self.fire_mark_guild_inquiry(payload, screen_id=screen_id)
        if action_id == "sell_guild_material":
            return self.sell_guild_material(payload, screen_id=screen_id)
        if action_id in {"submit_quest", "report_dungeon_clear"}:
            return self.report_dungeon_clear(payload, screen_id=screen_id)
        if action_id == "fire_mark_church_bridge":
            return self.fire_mark_church_bridge(payload, screen_id=screen_id)
        if action_id == "fire_mark_church_lookup":
            return self.fire_mark_church_lookup(payload, screen_id=screen_id)
        if action_id == "temple_pray":
            return self.temple_pray(payload, screen_id=screen_id)
        if action_id == "claim_promotion":
            return self.claim_promotion(payload, screen_id=screen_id)
        if action_id == "attune_relic":
            return self.attune_relic(payload, screen_id=screen_id)
        if action_id == "select_relic_passive":
            return self.select_relic_passive(payload, screen_id=screen_id)
        if action_id == "travel_region":
            return self.travel_region(payload)
        if action_id == "open_world_map":
            state = self.require_state()
            region_id = self.set_current_region(payload.get("region_id"))
            return self._live_response(
                action_id,
                "Opening world map.",
                screen_model=world_map_model(state, region_id),
                next_route="../world_map/index.html?mode=live",
            )
            return action_response(
                action_id,
                "正在開啟世界地圖...",
                state,
                screen_id="world_map",
                next_route="../world_map/index.html?mode=live",
            )
        if action_id == "back_to_town_hub":
            state = self.require_state()
            region_id = self.set_current_region(payload.get("region_id"))
            self._clear_live_run()
            return self._live_response(
                action_id,
                "正在返回城鎮...",
                screen_model=town_hub_model(state, selected_region_id=region_id),
                next_route="../town_hub/index.html?mode=live",
            )
        if action_id in {"return_to_exploration", "back_to_exploration"}:
            state = self.require_state()
            exploration = self.require_exploration()
            ending_story_beat = None
            if state.pop("_ending_pending", False):
                ending_story_beat = take_story_beat(
                    state,
                    "ending.main_story_clear",
                    context={"player": state.get("name", "見習冒險者")},
                )
            self.combat = None
            exploration["status"] = "exploring"

            dungeon_id = exploration["dungeon_id"]
            dungeon = DUNGEONS[dungeon_id]
            total_steps = dungeon["steps"]
            current_step = exploration["current_step"]

            if current_step >= total_steps:
                # Check if the boss was defeated to record the defeat event log
                boss_id = dungeon.get("boss")
                if boss_id == "boss_glen" and not game.boss_defeated(state, boss_id):
                    newly_accepted = game.activate_boss_glen_investigation(state)
                    if newly_accepted and ending_story_beat is None:
                        ending_story_beat = take_story_beat(state, "boss.before.boss_glen")
                boss_defeated = game.boss_defeated(state, boss_id)

                if boss_defeated and not exploration.get("boss_defeat_logged"):
                    exploration["boss_defeat_logged"] = True
                    boss_name = game.MONSTERS[boss_id]["name"]
                    defeat_msg = f"你成功擊敗了守護者 {boss_name}！取得戰利品。請使用「離開迷宮」返回地圖回報工會。"
                    exploration["last_message"] = defeat_msg
                    exploration.setdefault("events", []).append(defeat_msg)

                if not exploration.get("cleared_marked"):
                    exploration["cleared_marked"] = True
                    first_clear = dungeon_id not in state.get("cleared_dungeons", [])
                    if first_clear:
                        state.setdefault("cleared_dungeons", []).append(dungeon_id)
                        state["guild_points"] = state.get("guild_points", 0) + dungeon["clear_guild"]
                        msg = f"你走完了 {dungeon['name']} 的探索路線！首次通關，工會積分 +{dungeon['clear_guild']}。"
                    else:
                        msg = f"你走完了 {dungeon['name']} 的探索路線！"

                    # 終點守護者提示
                    if boss_id:
                        boss_name = game.MONSTERS[boss_id]["name"]
                        if game.boss_available_at_dungeon_end(state, dungeon_id, boss_id):
                            msg += f" 終點傳來強烈的氣息……可挑戰守護者 {boss_name}。出發前請確認 HP、藥水與火抗。"
                        else:
                            if boss_defeated:
                                msg += f" 守護者 {boss_name} 已被擊敗。"
                            else:
                                msg += f" {boss_name} 尚未滿足挑戰條件，先處理工會委託線索。"
                    exploration["last_message"] = msg
                    exploration.setdefault("events", []).append(msg)
                exploration["status"] = "resolved"

            return self._live_response(
                action_id,
                "正在返回探索...",
                screen_model=exploration_screen_model(self),
                next_route="../dungeon_exploration/index.html?mode=live",
                story_beat=ending_story_beat,
            )
        if action_id == "confirm_travel":
            return self.confirm_travel(payload)
        if action_id == "advance_step":
            return self.advance_step(payload)
        if action_id == "challenge_boss":
            return self.challenge_boss(payload)
        if action_id == "retreat":
            if screen_id == "combat_screen" or self.combat is not None:
                return self.combat_retreat()
            return self.retreat_from_exploration()
        if action_id in {"basic_attack", "defend", "use_item", "use_skill"}:
            return self.dispatch_combat_action(action_id, payload)
        raise GuiActionError(f"Unknown GUI action: {action_id}", status=404)

    def travel_region(self, payload: dict[str, Any]) -> dict[str, Any]:
        state = self.require_state()
        region_id = str(payload.get("region_id") or "")
        if region_id not in REGION_ORDER:
            raise GuiActionError("Unknown region.", status=400)
        if not region_route_enabled(state, region_id):
            raise GuiActionError(region_locked_reason(region_id), status=403)
        previous_region_id = self.current_region_id
        self.set_current_region(region_id)
        self._clear_live_run()
        story_beat = None
        if region_id != previous_region_id:
            story_beat = take_story_beat(state, region_story_beat_id(region_id))
        return self._live_response(
            "travel_region",
            f"Traveling to {REGION_LABELS[region_id]}.",
            screen_model=world_map_model(state, self.current_region_id),
            next_route="../world_map/index.html?mode=live",
            story_beat=story_beat,
        )

    def confirm_travel(self, payload: dict[str, Any]) -> dict[str, Any]:
        state = self.require_state()
        dungeon_id = payload.get("dungeon_id") or payload.get("location_id")
        if dungeon_id not in DUNGEONS:
            raise GuiActionError("Unknown dungeon.", status=400)
        dungeon = DUNGEONS[dungeon_id]
        if not game.is_unlocked(state, dungeon.get("unlock")):
            raise GuiActionError("Dungeon is locked.", status=403)
        try:
            game.configure_run_supplies(state, payload.get("supplies", {}))
        except ValueError as error:
            raise GuiActionError(str(error), status=409) from error
        self.current_region_id = normalize_region_id(state, payload.get("region_id") or region_for_dungeon_id(dungeon_id))
        game.clamp_vitals(state)
        run_log = {"gold": 0, "items": {}, "dungeon_id": dungeon_id}
        if state.get("equipment", {}).get("special") == "special_focus_pouch":
            game.add_loot(state, "item_focus_drop", 1, run_log)
            opening_event = "集中藥袋發出微光，出發前多整理出一瓶集中滴露。"
        else:
            opening_event = f"已抵達 {dungeon['name']} 入口。"
        self.exploration = {
            "dungeon_id": dungeon_id,
            "current_step": 0,
            "run_log": run_log,
            "events": [opening_event],
            "last_message": "已成功進入迷宮。請點擊前進一步開始探索。",
            "status": "exploring",
        }
        self.combat = None
        return self._live_response(
            "confirm_travel",
            f"已進入迷宮：{dungeon['name']}。",
            screen_model=exploration_screen_model(self),
            next_route="../dungeon_exploration/index.html?mode=live",
        )

    def advance_step(self, payload: dict[str, Any]) -> dict[str, Any]:
        state = self.require_state()
        exploration = self.require_exploration()
        if self.combat is not None:
            raise GuiActionError("A combat encounter is already active.", status=409)
        dungeon = DUNGEONS[exploration["dungeon_id"]]
        if state.get("current_hp", 0) <= 0:
            return self.resolve_defeat("You collapsed before taking the next step.")
        exploration["current_step"] = min(exploration["current_step"] + 1, dungeon["steps"])
        monster_id = random.choice(dungeon["monsters"])
        self.start_combat(monster_id)
        exploration["status"] = "combat"
        exploration["last_message"] = f"第 {exploration['current_step']} 步：遭遇 {game.MONSTERS[monster_id]['name']}。"
        exploration.setdefault("events", []).append(exploration["last_message"])
        return self._live_response(
            "advance_step",
            f"遭遇魔物：{game.MONSTERS[monster_id]['name']}。",
            screen_model=combat_screen_model(self),
            next_route="../combat_screen/index.html?mode=live",
        )

    def challenge_boss(self, payload: dict[str, Any]) -> dict[str, Any]:
        state = self.require_state()
        exploration = self.require_exploration()
        if self.combat is not None:
            raise GuiActionError("A combat encounter is already active.", status=409)
        dungeon_id = exploration["dungeon_id"]
        dungeon = DUNGEONS[dungeon_id]
        boss_id = dungeon.get("boss")
        if not boss_id:
            raise GuiActionError("This dungeon does not have a boss.", status=400)
        if not game.boss_available_at_dungeon_end(state, dungeon_id, boss_id):
            raise GuiActionError("Boss challenge conditions are not met.", status=403)
        if state.get("current_hp", 0) <= 0:
            return self.resolve_defeat("You collapsed before challenging the boss.")

        self.start_combat(boss_id, boss=True)
        exploration["status"] = "combat"
        exploration["last_message"] = f"決戰：開始挑戰守護者 {game.MONSTERS[boss_id]['name']}！"
        exploration.setdefault("events", []).append(exploration["last_message"])
        story_beat = take_story_beat(state, boss_story_beat_id(boss_id, "before"))
        return self._live_response(
            "challenge_boss",
            f"決戰開始：{game.MONSTERS[boss_id]['name']}！",
            screen_model=combat_screen_model(self),
            next_route="../combat_screen/index.html?mode=live",
            story_beat=story_beat,
        )

    def retreat_from_exploration(self) -> dict[str, Any]:
        state = self.require_state()
        exploration = self.require_exploration()
        exploration["status"] = "resolved"
        exploration["last_message"] = "已撤退並回到世界地圖。"
        self.combat = None
        self._clear_live_run()
        return self._live_response(
            "retreat",
            "已撤退並回到世界地圖。",
            screen_model=world_map_model(state, self.current_region_id),
            next_route="../world_map/index.html?mode=live",
        )

    def start_combat(self, monster_id: str, boss: bool = False) -> None:
        if monster_id not in game.MONSTERS:
            raise GuiActionError("Unknown monster.", status=400)
        enemy = deepcopy(game.MONSTERS[monster_id])
        self.combat = {
            "enemy_id": monster_id,
            "enemy": enemy,
            "enemy_hp": enemy["hp"],
            "player_buffs": {},
            "enemy_buffs": {},
            "turn": 1,
            "boss": boss,
            "boss_marker": False,
            "battle_log": [f"遭遇 {enemy['name']}。敵人屬性：{enemy['element']} / HP {enemy['hp']}/{enemy['hp']}。"],
            "last_action_summary": "尚未行動。",
            "outcome": None,
            "result_overlay": None,
        }

    def dispatch_combat_action(self, action_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        state = self.require_state()
        combat = self.require_combat()
        if combat.get("outcome"):
            raise GuiActionError("Combat is already resolved.", status=409)

        enemy = combat["enemy"]
        enemy["current_hp"] = combat["enemy_hp"]
        player_buffs = combat["player_buffs"]
        enemy_buffs = combat["enemy_buffs"]
        defending = False
        action_result = game.CombatActionResult()

        if action_id == "basic_attack":
            action_result = game.player_attack(state, enemy, combat["enemy_hp"], None, player_buffs, enemy_buffs)
            combat["enemy_hp"] -= action_result.damage
        elif action_id == "defend":
            defending = True
            events = []
            if player_buffs.get("defense_up", 0) > 0:
                stats = game.get_stats(state, player_buffs)
                state["current_mp"] = min(stats["max_mp"], state["current_mp"] + 2)
                events.append("你穩住姿勢，符文讓你回復 MP 2。")
            events.append("你採取防禦姿態。")
            action_result = game.CombatActionResult(events=events, summary=["你採取防禦姿態。"])
        elif action_id == "use_item":
            item_id = payload.get("item_id")
            action_result = self.use_combat_item(str(item_id) if item_id else "")
            if action_result.outcome == "escaped":
                return self.resolve_retreat(action_result.summary or action_result.events)
            combat["enemy_hp"] -= action_result.damage
        elif action_id == "use_skill":
            skill_id = payload.get("skill_id")
            if not skill_id or skill_id not in state.get("learned_skills", []):
                raise GuiActionError("未學會該技能或無效技能。", status=400)
            skill = SKILLS.get(skill_id)
            if not skill:
                raise GuiActionError("技能資料不存在。", status=400)
            if state.get("current_mp", 0) < skill["mp"]:
                raise GuiActionError(
                    "MP 不足，無法使用技能。",
                    status=409,
                    result_status="blocked",
                    blocked_reason="MP 不足，無法使用技能。",
                )
            runtime_skill = dict(skill)
            if skill_id in {"skill_star_fracture", "skill_sigil_mage"}:
                selected_element = payload.get("element")
                learned_elements = {
                    known_skill.get("element")
                    for known_skill_id in state.get("learned_skills", [])
                    if (known_skill := SKILLS.get(known_skill_id)) and known_skill.get("element") in {"火", "冰", "自然", "雷"}
                }
                if selected_element not in learned_elements:
                    raise GuiActionError("未學會所選元素，無法施展此技能。", status=409)
                runtime_skill["element"] = selected_element
            state["current_mp"] -= skill["mp"]
            stats = game.get_stats(state, player_buffs)
            if skill["kind"] == "damage":
                action_result = game.execute_skill(state, enemy, skill_id, runtime_skill, player_buffs, enemy_buffs)
                combat["enemy_hp"] -= action_result.damage
            elif skill["kind"] == "heal":
                before = state["current_hp"]
                state["current_hp"] = min(stats["max_hp"], state["current_hp"] + skill["amount"])
                healed = state["current_hp"] - before
                line = f"你使用 {skill['name']}，回復 {healed} HP。"
                action_result = game.CombatActionResult(events=[line], summary=[line])
            elif skill["kind"] == "buff":
                player_buffs[skill["buff"]] = skill["duration"]
                line = f"你使用 {skill['name']}。{skill['desc']}"
                action_result = game.CombatActionResult(events=[line], summary=[line])
                if skill_id in {"skill_blood_blade_strike", "skill_blood_armor_shield", "skill_holy_veil_barrier", "skill_holy_eclipse_cast"}:
                    player_buffs.pop(skill["buff"], None)
                    action_result = game.execute_skill(state, enemy, skill_id, runtime_skill, player_buffs, enemy_buffs)
            elif skill["kind"] == "debuff":
                enemy_buffs[skill["debuff"]] = skill["duration"]
                if skill.get("damage_percent") is not None:
                    enemy_buffs.setdefault("_debuff_data", {})[skill["debuff"]] = {
                        "damage_percent": skill["damage_percent"],
                        "damage_scope": skill.get("damage_scope"),
                    }
                line = f"你使用 {skill['name']}。{skill['desc']}"
                action_result = game.CombatActionResult(events=[line], summary=[line])
                if skill_id == "skill_sigil_mage":
                    action_result = game.execute_skill(state, enemy, skill_id, runtime_skill, player_buffs, enemy_buffs)
            elif skill["kind"] == "dot":
                game.apply_dot(enemy_buffs, skill["name"], skill["duration"], skill["multiplier"], "magic", skill.get("element", "無"))
                line = f"{skill['name']} 必定附加，持續 {skill['duration']} 回合。"
                action_result = game.CombatActionResult(events=[line], summary=[line])
            elif skill["kind"] == "regen":
                player_buffs["regeneration"] = skill["duration"]
                player_buffs["_regen_data"] = {"amount": skill["amount"], "multiplier": skill["multiplier"]}
                line = f"{skill['name']} 必定附加，持續 {skill['duration']} 回合。"
                action_result = game.CombatActionResult(events=[line], summary=[line])
            else:
                raise GuiActionError("不支援的技能類型。", status=400)

        if action_result.outcome == "cancel":
            if action_id == "use_skill":
                state["current_mp"] += skill["mp"]
            raise GuiActionError(action_result.summary[0], status=409)

        turn_events = list(action_result.events)
        if action_result.free_action:
            combat["mp_item_used_turn"] = True
            game.record_battle_events(combat["battle_log"], combat["turn"], turn_events)
            combat["last_action_summary"] = " / ".join(action_result.summary[:2])
            return self._live_response(action_id, action_result.summary[0], screen_model=combat_screen_model(self))
        if combat["enemy_hp"] <= 0:
            turn_events.append(f"{enemy['name']}倒下。")
            game.record_battle_events(combat["battle_log"], combat["turn"], turn_events)
            return self.resolve_victory(action_result.summary + [f"{enemy['name']}倒下。"])

        combat["boss_marker"], enemy_events = game.dispatch_enemy_turn(
            combat["enemy_id"],
            enemy,
            combat["enemy_hp"],
            state,
            player_buffs,
            enemy_buffs,
            defending,
            combat["turn"],
            combat.get("boss_marker", False),
        )
        enemy_events.extend(player_buffs.pop("_shield_absorb_logs", []))
        reflect_damage = player_buffs.pop("_reflect_damage_queue", 0)
        if reflect_damage:
            combat["enemy_hp"] = max(0, combat["enemy_hp"] - reflect_damage)
        # Pass the live enemy so periodic enemy DoT effects are resolved and
        # included in the bridge battle log just like the CLI combat path.
        effect_events, dot_damage = game.tick_effects(state, player_buffs, enemy_buffs, enemy)
        combat["enemy_hp"] -= dot_damage
        turn_events.extend(enemy_events)
        turn_events.extend(effect_events)
        game.record_battle_events(combat["battle_log"], combat["turn"], turn_events)
        summary = game.combat_summary_lines(action_result.summary, enemy_events, effect_events)
        combat["last_action_summary"] = " / ".join(summary[:2]) if summary else "回合結束。"
        combat["turn"] += 1
        combat["mp_item_used_turn"] = False

        if combat["enemy_hp"] <= 0:
            return self.resolve_victory(effect_events + [f"{enemy['name']}倒下了。"])
        if state.get("current_hp", 0) <= 0:
            return self.resolve_defeat("You were defeated in combat.")

        return self._live_response(
            action_id,
            combat["last_action_summary"],
            screen_model=combat_screen_model(self),
        )

    def use_combat_item(self, item_id: str) -> game.CombatActionResult:
        state = self.require_state()
        combat = self.require_combat()
        enemy = combat["enemy"]
        enemy_buffs = combat["enemy_buffs"]
        if game.combat_item_quantity(state, item_id) <= 0:
            raise GuiActionError("Item is not available.", status=409)
        if item_id in game.COMBAT_MP_RECOVERY and combat.get("mp_item_used_turn"):
            raise GuiActionError("本回合已使用 MP 藥水。", status=409, blocked_reason="本回合已使用 MP 藥水。")
        if item_id in game.COMBAT_HP_RECOVERY:
            stats = game.get_stats(state)
            before = state["current_hp"]
            state["current_hp"] = min(stats["max_hp"], state["current_hp"] + game.combat_recovery_amount(state, item_id))
            game.consume_combat_item(state, item_id)
            line = f"使用{ITEMS[item_id]['name']}，回復 {state['current_hp'] - before} HP。"
            return game.CombatActionResult(events=[line], summary=[line])
        if item_id in game.COMBAT_MP_RECOVERY:
            stats = game.get_stats(state)
            before = state["current_mp"]
            state["current_mp"] = min(stats["max_mp"], state["current_mp"] + game.combat_recovery_amount(state, item_id))
            game.consume_combat_item(state, item_id)
            line = f"使用{ITEMS[item_id]['name']}，回復 {state['current_mp'] - before} MP。"
            return game.CombatActionResult(events=[line], summary=[line], free_action=True)
        if item_id == "item_herb_antidote":
            game.consume_combat_item(state, item_id)
            state.setdefault("_clear_burn", True)
            line = "你嚼下解毒草，灼熱感稍微退去。"
            return game.CombatActionResult(events=[line], summary=[line])
        if item_id in game.COMBAT_THROWABLE_IDS:
            return game.use_combat_throwable(state, item_id, enemy, enemy_buffs)
        raise GuiActionError("Unsupported combat item.", status=400)

    def combat_retreat(self) -> dict[str, Any]:
        state = self.require_state()
        combat = self.require_combat()
        enemy = combat["enemy"]
        if combat.get("boss"):
            raise GuiActionError(
                "Boss 戰不可逃跑。",
                status=409,
                blocked_reason="Boss 戰不可逃跑。",
            )
        if game.try_escape(state, enemy):
            return self.resolve_retreat(["你成功脫離戰鬥。"])
        action_result = game.CombatActionResult(events=["逃跑失敗。"], summary=["逃跑失敗。"])
        combat["boss_marker"], enemy_events = game.dispatch_enemy_turn(
            combat["enemy_id"],
            enemy,
            combat["enemy_hp"],
            state,
            combat["player_buffs"],
            combat["enemy_buffs"],
            False,
            combat["turn"],
            combat.get("boss_marker", False),
        )
        effect_events, dot_damage = game.tick_effects(state, combat["player_buffs"], combat["enemy_buffs"], enemy)
        combat["enemy_hp"] -= dot_damage
        turn_events = list(action_result.events) + enemy_events + effect_events
        game.record_battle_events(combat["battle_log"], combat["turn"], turn_events)
        summary = game.combat_summary_lines(action_result.summary, enemy_events, effect_events)
        combat["last_action_summary"] = " / ".join(summary[:2]) if summary else "逃跑失敗。"
        combat["turn"] += 1
        if combat["enemy_hp"] <= 0:
            return self.resolve_victory(effect_events + [f"{enemy['name']}倒下了。"])
        if state.get("current_hp", 0) <= 0:
            return self.resolve_defeat("You were defeated while retreating.")
        return self._live_response("retreat", combat["last_action_summary"], screen_model=combat_screen_model(self))

    def resolve_victory(self, summary_lines: list[str]) -> dict[str, Any]:
        state = self.require_state()
        combat = self.require_combat()
        enemy = combat["enemy"]
        enemy_id = combat["enemy_id"]
        run_log = self.current_run_log()
        story_beat = None

        # 記錄升級前狀態與 Level
        level_before = state.get("level", 1)

        # 登錄圖鑑並判斷是否為首次登錄
        newly_registered = game.try_register_bestiary(state, enemy_id)

        # 獲得經驗值與 Level Up 處理
        dungeon_id = self.exploration.get("dungeon_id") if self.exploration else None
        exp_reward = game.gain_exp(state, enemy["exp"], dungeon_id)
        enemy["exp"] = exp_reward["awarded_exp"]
        level_after = state.get("level", 1)
        level_up_occurred = level_after > level_before

        # 獲得金幣
        gold = random.randint(*enemy["gold"])
        game.add_gold(state, gold, run_log)

        reward_lines = []
        reward_lines.append(f"獲得金幣：+{gold}G")

        # 處理 EXP 顯示
        if level_up_occurred:
            reward_lines.append(f"🎉 等級提升！升級為 Lv{level_after}，HP/MP 已恢復全滿！")
        else:
            reward_lines.append(f"獲得經驗：+{enemy['exp']} EXP (目前 {state['exp']}/{game.exp_to_next(level_after)})")

        # 處理掉落素材
        if exp_reward["reason"]:
            reward_lines.append(f"經驗衰減：{exp_reward['reason']}，原始 {exp_reward['base_exp']} EXP 的 20%。")

        drops_found = []
        for item_id, chance, qty in enemy["drops"]:
            stats = game.get_stats(state)
            final_chance = chance + stats.get("rare_drop", 0) / 100
            if random.random() <= final_chance:
                game.add_loot(state, item_id, qty, run_log)
                drops_found.append(f"{item_name(item_id)} x{qty}")

        if drops_found:
            reward_lines.append("掉落物品：" + "、".join(drops_found))
        else:
            reward_lines.append("掉落物品：無")

        # 處理圖鑑登錄狀態提示
        if newly_registered:
            reward_lines.append(f"📖 圖鑑登錄：已將 {enemy['name']} 登錄至魔物圖鑑！")
        else:
            reward_lines.append(f"📖 圖鑑提示：{enemy['name']} 的資料已存在於圖鑑中。")

        if enemy_id == "mon_lava_imp":
            game.unlock(state, "recipe_heat_charm")
            reward_lines.append("🔑 解鎖配方：[暖石墜]。")

        # 處理 Boss 擊敗與劇情物品掉落
        if combat.get("boss"):
            story_beat = game.clear_dungeon_boss(state, enemy_id, run_log)
            if enemy_id == "boss_glen":
                reward_lines.append("🔑 取得戰利品：血跡地圖 x1、火之印記碎片 x1、熔岩碎片 x2。")
            elif enemy_id in {"boss_ash_guardian", "boss_cinder_seal_sentinel"}:
                reward_lines.append("🔑 取得戰利品：火之印記碎片 x1。")

        if combat.get("boss") and enemy_id.startswith("boss_ice_"):
            reward_lines.append("Ice Boss proof recovered. Return to the Guild if a quest is ready.")

        combat["outcome"] = "victory"
        combat["last_action_summary"] = " / ".join(summary_lines[:2]) if summary_lines else f"擊敗 {enemy['name']}。"
        combat["result_overlay"] = result_overlay_model(
            "victory",
            "戰鬥勝利",
            f"擊敗 {enemy['name']}。",
            combat["last_action_summary"],
            reward_lines + [game.run_loot_summary(run_log)],
        )
        return self._live_response(
            "basic_attack",
            "Victory.",
            screen_model=combat_screen_model(self),
            story_beat=story_beat,
        )

    def resolve_retreat(self, summary_lines: list[str]) -> dict[str, Any]:
        combat = self.require_combat()
        combat["outcome"] = "retreat"
        combat["last_action_summary"] = " / ".join(summary_lines[:2]) if summary_lines else "你撤出戰鬥。"

        reward_lines = [
            "撤退安全無恙。",
            game.run_loot_summary(self.current_run_log())
        ]

        combat["result_overlay"] = result_overlay_model(
            "retreat",
            "撤退成功",
            "你撤回通往城鎮的路線。",
            combat["last_action_summary"],
            reward_lines,
        )
        game.record_battle_events(combat["battle_log"], combat["turn"], summary_lines or ["你撤出戰鬥。"])
        return self._live_response("retreat", "Retreated from combat.", screen_model=combat_screen_model(self))

    def resolve_defeat(self, message: str) -> dict[str, Any]:
        state = self.require_state()
        run_log = self.current_run_log()
        lost_gold = game.math.ceil(run_log.get("gold", 0) * 0.5)
        state["gold"] = max(0, state.get("gold", 0) - lost_gold)
        lost_items = []
        for item_id, qty in run_log.get("items", {}).items():
            if game.is_key_item(item_id) or item_id in game.EQUIPMENT:
                continue
            lose_qty = game.math.ceil(qty * 0.5)
            if lose_qty > 0 and state.get("inventory", {}).get(item_id, 0) > 0:
                actual = min(lose_qty, state["inventory"].get(item_id, 0))
                game.remove_item(state, item_id, actual)
                lost_items.append(f"{item_name(item_id)} x{actual}")
        stats = game.get_stats(state)
        state["current_hp"] = max(1, game.math.ceil(stats["max_hp"] * 0.25))
        state["current_mp"] = game.math.ceil(stats["max_mp"] * 0.25)
        if self.combat is None:
            self.start_combat(DUNGEONS[self.require_exploration()["dungeon_id"]]["monsters"][0])
        combat = self.require_combat()
        combat["outcome"] = "defeat"
        combat["last_action_summary"] = message

        reward_lines = [
            f"扣減本趟所獲金幣的 50% ({lost_gold}G)。",
            "散落丟失本趟一般掉落的 50%：" + "、".join(lost_items) if lost_items else "本趟素材大致都保住了。",
            "公會救援隊收取了救援代價，已平安把你帶回據點城鎮艾爾姆。"
        ]

        combat["result_overlay"] = result_overlay_model(
            "defeat",
            "戰鬥失敗",
            "工會救援隊把你帶回艾爾姆。",
            message,
            reward_lines,
        )
        combat.setdefault("battle_log", []).append("戰鬥結束：你倒下了。")
        defeat_screen_model = combat_screen_model(self)
        self._clear_live_run()
        return self._live_response("defeat", "Defeated. Returned by rescue.", screen_model=defeat_screen_model)

    def require_exploration(self) -> dict[str, Any]:
        if self.exploration is None:
            raise GuiActionError("No live exploration is active.", status=409)
        return self.exploration

    def require_combat(self) -> dict[str, Any]:
        if self.combat is None:
            raise GuiActionError("No live combat is active.", status=409)
        return self.combat

    def current_run_log(self) -> dict[str, Any]:
        if self.exploration is None:
            return {"gold": 0, "items": {}}
        return self.exploration.setdefault("run_log", {"gold": 0, "items": {}})

    def _live_response(
        self,
        action_id: str,
        message: str,
        *,
        screen_model: dict[str, Any] | None,
        next_route: str | None = None,
        story_beat: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return {
            "ok": True,
            "status": "success",
            "action_id": action_id,
            "message": message,
            "state_summary": state_summary(self.state),
            "screen_model": screen_model,
            "next_route": next_route,
            "next_screen_id": screen_model.get("screen_id") if screen_model else None,
            "story_beat": story_beat,
        }

    def _clear_live_run(self) -> None:
        self.exploration = None
        self.combat = None

    def rest_at_inn(self, payload: dict[str, Any], *, screen_id: str | None = None) -> dict[str, Any]:
        state = self.require_state()
        service_id = payload.get("service_id", "overnight_rest")
        cost_payload = payload.get("cost", 30)
        if isinstance(cost_payload, bool):
            raise GuiActionError("旅店費用必須是數字。", status=400)
        try:
            cost = int(cost_payload)
        except (TypeError, ValueError) as exc:
            raise GuiActionError("旅店費用必須是數字。", status=400) from exc
        if service_id != "overnight_rest":
            raise GuiActionError("未知的旅店服務。", status=400)
        if cost != 30:
            raise GuiActionError("旅店費用不符合。", status=400)
        if state.get("gold", 0) < cost:
            raise GuiActionError(
                "身上金幣不足，無法在旅店住宿。",
                status=409,
                result_status="blocked",
                blocked_reason="身上金幣不足，無法在旅店住宿。",
            )
        stats = game.get_stats(state)
        state["gold"] -= cost
        state["current_hp"] = stats["max_hp"]
        state["current_mp"] = stats["max_mp"]
        response = action_response(
            "rest_at_inn",
            "已在旅店住宿休整完畢，HP/MP 已恢復全滿。請記得進行存檔以儲存進度。",
            state,
            screen_id="inn_screen" if screen_id == "inn_screen" else "town_hub",
        )
        if response.get("screen_model"):
            response["screen_model"]["feedback_message"] = response["message"]
        return response

    def unlock_storage(self, payload: dict[str, Any], *, screen_id: str | None = None) -> dict[str, Any]:
        state = self.require_state()
        if state.get("storage_unlocked", False):
            raise GuiActionError("保管箱已經解鎖。", status=409)
        cost = STORAGE_UNLOCK_COST
        if state.get("gold", 0) < cost:
            raise GuiActionError(
                "身上的金幣不足以支付開啟保管箱的會費。",
                status=409,
                result_status="blocked",
                blocked_reason="身上金幣不足以支付解鎖費用",
            )
        state["gold"] -= cost
        state["storage_unlocked"] = True

        response = self._live_response(
            "unlock_storage",
            "解鎖成功！這就幫米菈小隊開啟專屬的保管箱空間！",
            screen_model=self.storage_screen_model(),
        )
        return response

    def deposit_item(self, payload: dict[str, Any], *, screen_id: str | None = None) -> dict[str, Any]:
        state = self.require_state()
        if not state.get("storage_unlocked", False):
            raise GuiActionError("倉庫尚未開啟。", status=409)

        item_id = payload.get("item_id")
        quantity = payload.get("quantity", 1)

        if type(quantity) is not int or isinstance(quantity, bool):
            raise GuiActionError("轉移數量必須為整數。", status=400)
        if quantity <= 0:
            raise GuiActionError("轉移數量必須大於 0。", status=400)

        if not item_id:
            raise GuiActionError("未指定要存入的物品。", status=400)

        if item_id.startswith("key_"):
            raise GuiActionError("貴重道具無法存入倉庫。", status=409)

        owned = state.get("inventory", {}).get(item_id, 0)
        if owned < quantity:
            raise GuiActionError("背包中的物品數量不足。", status=409)

        if not game.storage_has_room_for(state, item_id):
            raise GuiActionError("倉庫容量已達上限，無法新增其他種類物品。", status=409)

        if game.remove_item(state, item_id, quantity):
            game.add_storage_item(state, item_id, quantity)
        else:
            raise GuiActionError("物品轉移失敗，背包內物品數量異常。", status=409)

        response = self._live_response(
            "deposit_item",
            f"成功將 {game.item_name(item_id)} x{quantity} 放入保管箱。",
            screen_model=self.storage_screen_model(),
        )
        return response

    def withdraw_item(self, payload: dict[str, Any], *, screen_id: str | None = None) -> dict[str, Any]:
        state = self.require_state()
        if not state.get("storage_unlocked", False):
            raise GuiActionError("倉庫尚未開啟。", status=409)

        item_id = payload.get("item_id")
        quantity = payload.get("quantity", 1)

        if type(quantity) is not int or isinstance(quantity, bool):
            raise GuiActionError("轉移數量必須為整數。", status=400)
        if quantity <= 0:
            raise GuiActionError("轉移數量必須大於 0。", status=400)

        if not item_id:
            raise GuiActionError("未指定要取出的物品。", status=400)

        in_storage = state.get("storage", {}).get(item_id, 0)
        if in_storage < quantity:
            raise GuiActionError("倉庫中的物品數量不足。", status=409)

        if game.remove_storage_item(state, item_id, quantity):
            game.add_item(state, item_id, quantity)
        else:
            raise GuiActionError("物品轉移失敗，倉庫內物品數量異常。", status=409)

        response = self._live_response(
            "withdraw_item",
            f"成功從保管箱取出 {game.item_name(item_id)} x{quantity} 到背包。",
            screen_model=self.storage_screen_model(),
        )
        return response

    def buy_equipment(self, payload: dict[str, Any], *, screen_id: str | None = None) -> dict[str, Any]:
        state = self.require_state()
        item_id = payload.get("item_id")

        if not item_id or item_id not in EQUIPMENT:
            raise GuiActionError("裝備不存在。", status=400)

        if item_id not in SHOP_INVENTORY["weapon"] and item_id not in SHOP_INVENTORY["armor"]:
            raise GuiActionError("此商店不販售該裝備。", status=400)

        eq = EQUIPMENT[item_id]
        if state.get("job") not in eq["jobs"]:
            raise GuiActionError(
                f"{state.get('job')}無法使用這件裝備，先別買比較好。",
                status=409,
                result_status="blocked",
                blocked_reason="職業不合",
            )

        price = eq["price"]
        if state.get("gold", 0) < price:
            raise GuiActionError(
                "金幣不足，無法購買該裝備。",
                status=409,
                result_status="blocked",
                blocked_reason="金幣不足",
            )

        state["gold"] -= price
        game.add_item(state, item_id, 1)

        response = action_response(
            "buy_equipment",
            f"成功購買 {eq['name']}！獲得 {eq['name']} x1，扣除金幣 {price}G。",
            state,
            screen_id="workshop_screen",
        )
        if response.get("screen_model"):
            is_weapon = eq["slot"] == "weapon"
            speaker = "葛雷" if is_weapon else "布琳"
            text = (
                f"「金幣收下了，祝你在焦石礦坑好運！這是你的 {eq['name']}。」"
                if is_weapon
                else f"「耐用、實惠，這是你的 {eq['name']}。穿戴後再去冒險吧。」"
            )
            response["screen_model"]["feedback_message"] = {
                "tone": "success",
                "speaker": speaker,
                "text": text
            }
        return response

    def equip_weapon(self, payload: dict[str, Any], *, screen_id: str | None = None) -> dict[str, Any]:
        state = self.require_state()
        item_id = payload.get("item_id")

        resolved = resolve_equipment_ref(state, item_id)
        if not resolved:
            raise GuiActionError("武器不存在。", status=400)

        eq = resolved["base"]
        if eq["slot"] != "weapon":
            raise GuiActionError("該裝備不是武器，無法裝備在武器欄位。", status=400)

        if state.get("job") not in eq["jobs"]:
            raise GuiActionError(
                f"{state.get('job')}無法裝備此武器。",
                status=409,
                result_status="blocked",
                blocked_reason="職業不符",
            )

        if state.get("equipment", {}).get("weapon") == item_id:
            raise GuiActionError(
                "目前已裝備此武器，無需重複裝備。",
                status=409,
                result_status="blocked",
                blocked_reason="已裝備此武器",
            )

        if state.get("inventory", {}).get(item_id, 0) <= 0:
            raise GuiActionError(
                "背包中沒有這件武器，無法裝備。",
                status=409,
                result_status="blocked",
                blocked_reason="背包中無此武器",
            )

        success = game.equip_item(state, item_id, quiet=True)
        if not success:
            raise GuiActionError("裝備武器失敗。", status=400)

        response = action_response(
            "equip_weapon",
            f"已裝備 {eq['name']}。",
            state,
            screen_id="workshop_screen",
        )
        if response.get("screen_model"):
            response["screen_model"]["feedback_message"] = {
                "tone": "success",
                "speaker": "葛雷",
                "text": f"「已經為你換上 {eq['name']} 了。舊的裝備幫你收入背包裡。」"
            }
        return response

    def equip_equipment(self, payload: dict[str, Any], *, screen_id: str | None = None) -> dict[str, Any]:
        state = self.require_state()
        item_id = payload.get("item_id")

        resolved = resolve_equipment_ref(state, item_id)
        if not resolved:
            raise GuiActionError("裝備不存在。", status=400)

        eq = resolved["base"]
        slot = eq["slot"]

        if state.get("job") not in eq["jobs"]:
            raise GuiActionError(
                f"{state.get('job')}無法裝備此裝備。",
                status=409,
                result_status="blocked",
                blocked_reason="職業不符",
            )

        if state.get("equipment", {}).get(slot) == item_id:
            raise GuiActionError(
                "目前已裝備此物品，無需重複裝備。",
                status=409,
                result_status="blocked",
                blocked_reason="已裝備此裝備",
            )

        if state.get("inventory", {}).get(item_id, 0) <= 0:
            raise GuiActionError(
                "背包中沒有這件裝備，無法裝備。",
                status=409,
                result_status="blocked",
                blocked_reason="背包中無此裝備",
            )

        success = game.equip_item(state, item_id, quiet=True)
        if not success:
            raise GuiActionError("裝備穿戴失敗。", status=400)

        response = action_response(
            "equip_equipment",
            f"已裝備 {eq['name']}。",
            state,
            screen_id="workshop_screen",
        )
        if response.get("screen_model"):
            speaker = "葛雷" if slot == "weapon" else "布琳"
            response["screen_model"]["feedback_message"] = {
                "tone": "success",
                "speaker": speaker,
                "text": f"「已經為你換上 {eq['name']}。舊的裝備幫你收入背包裡。」"
            }
        return response

    def upgrade_equipment(self, payload: dict[str, Any], *, screen_id: str | None = None) -> dict[str, Any]:
        state = self.require_state()
        recipe_id = payload.get("recipe_id")

        whitelisted_recipes = {"recipe_iron_sword_plus_1", "recipe_leather_armor_plus_1"}
        if recipe_id not in whitelisted_recipes:
            raise GuiActionError("非白名單配方。", status=400)

        if not recipe_id or recipe_id not in RECIPES:
            raise GuiActionError("配方不存在。", status=400)

        recipe = RECIPES[recipe_id]

        if not game.recipe_available(state, recipe_id):
            raise GuiActionError(
                "配方尚未解鎖，無法進行強化。",
                status=409,
                result_status="blocked",
                blocked_reason="配方未解鎖",
            )

        if state.get("gold", 0) < recipe["gold"]:
            raise GuiActionError(
                "金幣不足，無法進行強化。",
                status=409,
                result_status="blocked",
                blocked_reason="金幣不足",
            )

        if not game.can_pay_items(state, recipe["materials"]):
            raise GuiActionError(
                "材料不足，無法進行強化。",
                status=409,
                result_status="blocked",
                blocked_reason="材料不足",
            )

        base_item = recipe.get("base_item")
        if base_item and not game.owns_item_or_equipped(state, base_item):
            raise GuiActionError(
                "缺少基底裝備，無法進行強化。",
                status=409,
                result_status="blocked",
                blocked_reason="缺少基底裝備",
            )

        result = game.craft_recipe_message(state, recipe_id)
        if not result.startswith("完成："):
            raise GuiActionError(result, status=400)

        response = action_response(
            "upgrade_equipment",
            f"成功強化 {recipe['name']}！",
            state,
            screen_id="workshop_screen",
        )
        if response.get("screen_model"):
            response["screen_model"]["feedback_message"] = {
                "tone": "success",
                "speaker": "布琳",
                "text": f"「太棒了！你的 {recipe['name']} 已經強化完成囉！」"
            }
        return response

    def buy_item(self, payload: dict[str, Any], *, screen_id: str | None = None) -> dict[str, Any]:
        state = self.require_state()
        item_id = payload.get("item_id")

        if not item_id or (item_id not in ITEMS and item_id not in EQUIPMENT):
            raise GuiActionError("商品不存在。", status=400)

        if item_id not in SHOP_INVENTORY["travel"]:
            raise GuiActionError("此商店不販售該商品。", status=400)

        item = ITEMS.get(item_id) or EQUIPMENT.get(item_id)

        if not game.is_shop_item_available(state, item_id):
            raise GuiActionError("商品尚未解鎖或不可購買。", status=409)

        if item_id in EQUIPMENT:
            if state.get("job") not in item["jobs"]:
                raise GuiActionError(
                    "職業不符，無法購買該裝備。",
                    status=409,
                    result_status="blocked",
                    blocked_reason="職業不符",
                )

        price = item["price"]
        if state.get("gold", 0) < price:
            raise GuiActionError(
                "金幣不足，無法購買該商品。",
                status=409,
                result_status="blocked",
                blocked_reason="金幣不足，無法購買該商品。",
            )

        state["gold"] -= price
        game.add_item(state, item_id, 1)

        response = action_response(
            "buy_item",
            f"成功購買 {item['name']}！獲得 {item['name']} x1，扣除金幣 {price}G。",
            state,
            screen_id="shop_screen",
        )
        if response.get("screen_model"):
            response["screen_model"]["feedback_message"] = {
                "tone": "success",
                "speaker": "特里",
                "text": f"「非常感謝！這是你的 {item['name']}，請拿好！」"
            }
        return response

    def learn_magic_book(self, payload: dict[str, Any], *, screen_id: str | None = None) -> dict[str, Any]:
        state = self.require_state()
        book_id = payload.get("book_id")

        if not book_id or book_id not in MAGIC_BOOKS:
            raise GuiActionError("魔法書不存在。", status=400)

        book = MAGIC_BOOKS[book_id]
        skill_id = book["skill"]
        if skill_id not in SKILLS:
            raise GuiActionError("技能資料不存在。", status=400)

        if skill_id in state.get("learned_skills", []):
            raise GuiActionError(
                "你已經學會這本書的技能。",
                status=409,
                result_status="blocked",
                blocked_reason="已學會此法術",
            )

        if state.get("job") not in book["jobs"]:
            raise GuiActionError(
                f"{state.get('job')}無法理解這本魔法書的核心術式。",
                status=409,
                result_status="blocked",
                blocked_reason="職業不符",
            )

        if state.get("level", 1) < book["level"]:
            raise GuiActionError(
                f"等級不足，需要 Lv{book['level']}。",
                status=409,
                result_status="blocked",
                blocked_reason=f"等級不足 Lv{book['level']}",
            )

        price = game.magic_book_price(state, book_id)
        if state.get("gold", 0) < price:
            raise GuiActionError(
                "金幣不足，無法學習該魔法。",
                status=409,
                result_status="blocked",
                blocked_reason="金幣不足",
            )

        if not game.can_pay_items(state, book["materials"]):
            raise GuiActionError(
                "素材不足，無法學習該魔法。",
                status=409,
                result_status="blocked",
                blocked_reason="素材不足",
            )

        state["gold"] -= price
        game.pay_items(state, book["materials"])
        state.setdefault("learned_skills", []).append(skill_id)

        skill = SKILLS[skill_id]
        response = action_response(
            "learn_magic_book",
            f"你成功研讀了《{book['name']}》！扣除金幣 {price}G 與素材，已永久學會法術「{skill['name']}」！",
            state,
            screen_id="magic_shop_screen",
        )
        if response.get("screen_model"):
            response["screen_model"]["feedback_message"] = {
                "tone": "success",
                "speaker": "伊芙",
                "text": f"「術式編織成功！星辰奧秘已永久融入你的靈魂，你學會了高深的傳承技能【{skill['name']}】！」"
            }
        return response

    def craft_recipe(self, payload: dict[str, Any], *, screen_id: str | None = None) -> dict[str, Any]:
        state = self.require_state()
        recipe_id = payload.get("recipe_id")
        mira_recipes = {"recipe_fire_cloak", "recipe_focus_pouch", "recipe_heat_charm", "recipe_piercing_bundle", "recipe_rending_spike"}
        if recipe_id not in mira_recipes:
            raise GuiActionError("非白名單配方。", status=403)

        if not game.recipe_available(state, recipe_id):
            raise GuiActionError(
                "配方尚未解鎖。",
                status=403,
                result_status="blocked",
                blocked_reason="配方尚未解鎖。",
            )

        result = game.craft_recipe_message(state, recipe_id)
        if result == "金幣不足。":
            raise GuiActionError(
                "金幣不足。",
                status=409,
                result_status="blocked",
                blocked_reason="金幣不足。",
            )
        elif result == "素材不足。":
            raise GuiActionError(
                "素材不足。",
                status=409,
                result_status="blocked",
                blocked_reason="素材不足。",
            )
        elif result.startswith("需要"):
            raise GuiActionError(
                result,
                status=409,
                result_status="blocked",
                blocked_reason=result,
            )

        screen_to_use = screen_id or "synthesis_screen"
        return action_response("craft_recipe", result, state, screen_id=screen_to_use)

    def guild_screen_model(self) -> dict[str, Any]:
        return guild_screen_model(self.require_state(), selected_region_id=self.current_region_id)

    def storage_screen_model(self) -> dict[str, Any]:
        return storage_screen_model(self.require_state())

    def accept_boss_glen_investigation(self, payload: dict[str, Any], screen_id: str | None = None) -> dict[str, Any]:
        state = self.require_state()
        if not game.accept_boss_glen_investigation(state):
            if not state.get("flags", {}).get(game.BOSS_GLEN_SIGHTED_FLAG):
                raise GuiActionError("尚未在焦石礦坑深處感受到強烈氣息。", status=409)
            if state.get("flags", {}).get(game.BOSS_GLEN_INVESTIGATION_ACCEPTED_FLAG):
                raise GuiActionError("已接下調查。", status=409)
            raise GuiActionError("Boss Glen investigation cannot be accepted.", status=409)
        return self._live_response(
            "accept_boss_glen_investigation",
            "你接下了焦石礦坑深處強烈氣息的調查任務。",
            screen_model=self.guild_screen_model(),
        )

    def fire_mark_guild_inquiry(self, payload: dict[str, Any], screen_id: str | None = None) -> dict[str, Any]:
        state = self.require_state()
        state.setdefault("flags", {})
        if not game.can_ask_fire_mark_guild_inquiry(state):
            raise GuiActionError(
                "不符合詢問條件或已詢問過關於印記碎片的事。",
                status=409,
                result_status="blocked",
                blocked_reason="不符合詢問條件或已詢問過",
            )
        game.fire_mark_guild_inquiry(state)
        return self._live_response(
            "fire_mark_guild_inquiry",
            "已向工會會長詢問關於三枚火之印記碎片的事。會長建議前往大教堂詢問賽恩祭司。",
            screen_model=self.guild_screen_model(),
        )

    def sell_guild_material(self, payload: dict[str, Any], screen_id: str | None = None) -> dict[str, Any]:
        state = self.require_state()
        item_id = payload.get("item_id")
        quantity = payload.get("quantity")
        confirm = payload.get("confirm", False)

        if not item_id or item_id not in game.GUILD_MATERIAL_BUY_PRICES:
            raise GuiActionError("此物品非登記收購素材。", status=400)

        # Validate positive integer
        if isinstance(quantity, bool) or not isinstance(quantity, int) or quantity <= 0:
            raise GuiActionError("數量必須為正整數。", status=400)

        owned = state.get("inventory", {}).get(item_id, 0)
        if quantity > owned:
            raise GuiActionError("持有素材數量不足。", status=409)

        if not confirm:
            raise GuiActionError("出售已取消。", status=400)

        # Perform transaction
        unit_price = game.GUILD_MATERIAL_BUY_PRICES[item_id]
        total_gold = quantity * unit_price

        game.remove_item(state, item_id, quantity)
        state["gold"] = state.get("gold", 0) + total_gold

        material_name = game.item_name(item_id)
        msg = f"成功出售 {material_name} x{quantity}，獲得 {total_gold}G。"

        return self._live_response(
            "sell_guild_material",
            msg,
            screen_model=self.guild_screen_model(),
        )

    def report_dungeon_clear(self, payload: dict[str, Any], *, screen_id: str | None = None) -> dict[str, Any]:
        state = self.require_state()
        task_id = payload.get("task_id") or payload.get("dungeon_id")
        if not task_id:
            raise GuiActionError("未指定有效的任務或迷宮 ID。", status=400)

        if task_id in QUESTS:
            quest = QUESTS[task_id]
            cleared = task_id in state.get("completed_quests", [])
            ready = game.quest_ready(state, task_id)

            if cleared:
                raise GuiActionError(f"{quest['title']} 已經完成過了。", status=409)
            if not ready:
                raise GuiActionError(f"{quest['title']} 的交付條件尚未滿足。", status=409)

            # Perform actual quest completion
            game.pay_items(state, quest["turn_in"])
            reward = quest["reward"]
            state["gold"] += reward.get("gold", 0)
            guild_gain = reward.get("guild", 0)
            if state["equipment"].get("special") == "special_trial_badge":
                import math
                guild_gain = math.ceil(guild_gain * 1.05)
            state["guild_points"] += guild_gain
            for item_id, qty in reward.get("items", {}).items():
                game.add_item(state, item_id, qty)
            for key in quest.get("unlocks", []):
                game.unlock(state, key)
            state["completed_quests"].append(task_id)

            msg = f"委託「{quest['title']}」完成！獲得 {reward.get('gold', 0)}G，工會積分 +{guild_gain}。"
            if task_id == "quest_cave_gathering":
                msg += " 米菈合成屋已開放！"

            return self._live_response(
                "submit_quest",
                msg,
                screen_model=self.guild_screen_model(),
            )

        elif task_id in DUNGEONS:
            dungeon = DUNGEONS[task_id]
            cleared = task_id in state.get("cleared_dungeons", [])
            reported = state.get("flags", {}).get(f"guild_reported_{task_id}", False)

            if not cleared:
                raise GuiActionError(f"尚未通關 {dungeon['name']}，無法登記回報。", status=409)
            if reported:
                raise GuiActionError(f"{dungeon['name']} 的探索回報已經登記過了。", status=409)

            state.setdefault("flags", {})[f"guild_reported_{task_id}"] = True

            return self._live_response(
                "report_dungeon_clear",
                f"已成功登記 {dungeon['name']} 的探索回報！首次通關獎勵（工會積分）已於通關當下登記完畢。",
                screen_model=self.guild_screen_model(),
            )
        else:
            raise GuiActionError("未指定有效的任務或迷宮 ID。", status=400)

    def temple_screen_model(self) -> dict[str, Any]:
        return temple_screen_model(self.require_state())

    def relic_preview_screen_model(self) -> dict[str, Any]:
        return relic_preview_screen_model(self.require_state())

    def exploration_screen_model(self) -> dict[str, Any]:
        return exploration_screen_model(self)

    def combat_screen_model(self) -> dict[str, Any]:
        return combat_screen_model(self)

    def fire_mark_church_bridge(self, payload: dict[str, Any], screen_id: str | None = None) -> dict[str, Any]:
        state = self.require_state()
        if not game.should_show_fire_mark_church_bridge(state):
            raise GuiActionError("不符合向賽恩展示印記碎片的條件。", status=409)
        game.fire_mark_church_bridge(state)
        msg = (
            "賽恩聽完諾亞的轉介，視線落在三枚火之印記碎片上。\n"
            "碎片的紅光在神殿石階間一明一滅，像是在尋找尚未打開的門。\n"
            "「工會看不懂它，是因為這不是委託紀錄裡的東西。」賽恩低聲說。\n"
            "「它不普通，但我還不能斷言它是什麼。我要花點時間查閱舊文獻。」\n"
            "「先將碎片收好。等我整理出線索，再回神殿找我。」\n\n"
            "已確認：保管碎片，稍後再回神殿詢問大祭司查閱結果。"
        )
        return self._live_response(
            "fire_mark_church_bridge",
            msg,
            screen_model=self.temple_screen_model()
        )

    def fire_mark_church_lookup(self, payload: dict[str, Any], screen_id: str | None = None) -> dict[str, Any]:
        state = self.require_state()
        if not game.should_show_fire_mark_church_lookup(state):
            raise GuiActionError("不符合詢問火之印記核心的條件。", status=409)
        game.fire_mark_church_lookup(state)
        msg = (
            "賽恩把翻開的舊文獻推到石桌中央，頁面上畫著三道分裂的火印。\n"
            "「查到了。這三枚碎片不是完整的火之印記，而是它尚未完成的核心。」\n"
            "「它記錄了火的資格，卻還沒有承載力量。現在啟用，只會把印記燒毀。」\n"
            "賽恩用封蠟與灰白布帶暫時封住碎片的共鳴，又把它們交還給你。\n"
            "「去神殿後側的聖物調查台吧。那裡能讓碎片承接成真正的火之聖印。」\n\n"
            "已確認：未完成的火之印記核心。下一步是前往聖物調查台合成並安置火之聖印；聖印被動效果尚未開放。"
        )
        return self._live_response(
            "fire_mark_church_lookup",
            msg,
            screen_model=self.temple_screen_model()
        )

    def temple_pray(self, payload: dict[str, Any], screen_id: str | None = None) -> dict[str, Any]:
        state = self.require_state()
        cost = 30
        if state.get("gold", 0) < cost:
            raise GuiActionError("身上金幣不足以進行祈福。", status=409)
        state["gold"] = max(0, state["gold"] - cost)
        msg = "你汲取了微光閃爍的泉水進行祈福！獲得了 [月華庇護] (抗性 +10%，探索裝扮預覽，效果依後續版本開放為準)。"
        return self._live_response(
            "temple_pray",
            msg,
            screen_model=self.temple_screen_model()
        )

    def claim_promotion(self, payload: dict[str, Any], screen_id: str | None = None) -> dict[str, Any]:
        from data import PROMOTIONS, SKILLS
        state = self.require_state()
        class_id = payload.get("class_id")
        if not class_id or class_id not in PROMOTIONS:
            raise GuiActionError("無效的轉職 ID。", status=400)

        promo = PROMOTIONS[class_id]
        if promo.get("source_job") != state.get("job"):
            raise GuiActionError("職業不符，無法晉升此方向。", status=409)

        if state.get("promotion_id"):
            raise GuiActionError("角色已選定晉升方向，無法重複晉升。", status=409)
        if payload.get("confirmed") is not True:
            raise GuiActionError("晉升不可逆，請先確認宣誓。", status=409)

        # 驗證條件
        lv_satisfied = state.get("level", 1) >= 18
        quest_satisfied = "quest_ice_return_handoff" in state.get("completed_quests", [])
        if not (lv_satisfied and quest_satisfied):
            raise GuiActionError("未達成晉升的等級或任務要求條件。", status=409)

        # 執行晉升
        state["promotion_id"] = class_id

        # 學習技能
        learned = state.setdefault("learned_skills", [])
        if promo["active_skill_id"] not in learned:
            learned.append(promo["active_skill_id"])
        if promo["passive_skill_id"] not in learned:
            learned.append(promo["passive_skill_id"])

        msg = f"宣誓晉升成功！您已正式成為【{promo['name']}】。解鎖新主動技能及被動特性！"
        return self._live_response(
            "claim_promotion",
            msg,
            screen_model=self.temple_screen_model()
        )

    def attune_relic(self, payload: dict[str, Any], screen_id: str | None = None) -> dict[str, Any]:
        state = self.require_state()
        relic_identifier = payload.get("relic_id") or payload.get("relic_name") or payload.get("element_id")
        result = game.enshrine_relic(state, str(relic_identifier) if relic_identifier else None)
        return self._live_response("attune_relic", result["message"], screen_model=self.relic_preview_screen_model())

    def select_relic_passive(self, payload: dict[str, Any], screen_id: str | None = None) -> dict[str, Any]:
        state = self.require_state()
        relic_identifier = payload.get("relic_id") or payload.get("relic_name") or payload.get("element_id")
        result = game.select_relic_passive(state, str(relic_identifier) if relic_identifier else None, payload.get("choice_id"))
        if result["status"] == "blocked":
            raise GuiActionError(result["message"], status=409, result_status="blocked", blocked_reason=result["message"])
        return self._live_response("select_relic_passive", result["message"], screen_model=self.relic_preview_screen_model())

    def screen_model(self, screen_id: str) -> dict[str, Any]:
        if screen_id == "start_screen":
            return start_screen_model(save_exists())
        state = self.require_state()
        if screen_id == "world_map":
            return world_map_model(state, self.current_region_id)
        if screen_id == "town_hub":
            return town_hub_model(state, selected_region_id=self.current_region_id)
        if screen_id == "inn_screen":
            return inn_screen_model(state)
        if screen_id in {"guild_screen", "facility_guild_screen"}:
            return self.guild_screen_model()
        if screen_id in {"shop_screen", "facility_shop_screen"}:
            return shop_screen_model(state, selected_region_id=self.current_region_id)
        if screen_id in {"workshop_screen", "facility_workshop_screen"}:
            return workshop_screen_model(state, selected_region_id=self.current_region_id)
        if screen_id in {"magic_shop_screen", "facility_magic_shop_screen"}:
            return magic_shop_screen_model(state, selected_region_id=self.current_region_id)
        if screen_id in {"synthesis_screen", "facility_synthesis_screen"}:
            return synthesis_screen_model(state, selected_region_id=self.current_region_id)
        if screen_id in {"storage_screen", "facility_storage_screen"}:
            return self.storage_screen_model()
        if screen_id in {"temple_screen", "facility_temple_screen"}:
            return self.temple_screen_model()
        if screen_id in {"relic_preview_screen", "facility_relic_preview_screen"}:
            return self.relic_preview_screen_model()
        if screen_id == "dungeon_exploration":
            return exploration_screen_model(self)
        if screen_id == "combat_screen":
            return combat_screen_model(self)
        raise GuiActionError(f"未支援的 Live 畫面：{screen_id}", status=404)

    def session_info(self) -> dict[str, Any]:
        return {
            "ok": True,
            "status": "success",
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



def action_response(
    action_id: str,
    message: str,
    state: dict[str, Any],
    *,
    screen_id: str | None,
    next_route: str | None = None,
    selected_region_id: str | None = None,
    story_beat: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "ok": True,
        "status": "success",
        "action_id": action_id,
        "message": message,
        "state_summary": state_summary(state),
        "screen_model": build_screen_model(screen_id, state, selected_region_id=selected_region_id) if screen_id else None,
        "next_route": next_route,
        "next_screen_id": screen_id,
        "story_beat": story_beat,
    }


def build_screen_model(
    screen_id: str | None,
    state: dict[str, Any],
    *,
    selected_region_id: str | None = None,
) -> dict[str, Any] | None:
    if screen_id == "world_map":
        return world_map_model(state, selected_region_id)
    if screen_id == "town_hub":
        return town_hub_model(state, selected_region_id=selected_region_id)
    if screen_id == "inn_screen":
        return inn_screen_model(state)
    if screen_id in {"guild_screen", "facility_guild_screen"}:
        return guild_screen_model(state, selected_region_id=selected_region_id)
    if screen_id in {"shop_screen", "facility_shop_screen"}:
        return shop_screen_model(state, selected_region_id=selected_region_id)
    if screen_id in {"workshop_screen", "facility_workshop_screen"}:
        return workshop_screen_model(state, selected_region_id=selected_region_id)
    if screen_id in {"magic_shop_screen", "facility_magic_shop_screen"}:
        return magic_shop_screen_model(state, selected_region_id=selected_region_id)
    if screen_id in {"synthesis_screen", "facility_synthesis_screen"}:
        return synthesis_screen_model(state, selected_region_id=selected_region_id)
    if screen_id in {"temple_screen", "facility_temple_screen"}:
        return temple_screen_model(state)
    if screen_id in {"relic_preview_screen", "facility_relic_preview_screen"}:
        return relic_preview_screen_model(state)
    return None


def start_screen_model(has_save: bool) -> dict[str, Any]:
    if has_save:
        actions = [
            {
                "action_id": "load_game",
                "label": "繼續冒險（Continue）",
                "description": "",
                "token": "續",
                "kind": "primary",
                "enabled": True,
                "disabled_reason": None,
                "payload": {"entry": "load_game"},
            },
            {
                "action_id": "restart_game",
                "label": "重新開始（New Game）",
                "description": "",
                "token": "重",
                "kind": "secondary",
                "enabled": True,
                "disabled_reason": None,
                "opens_registration": True,
                "final_action_id": "restart_game",
                "registration_entry": "restart_game",
                "registration_title": "重新登錄冒險者",
                "registration_feedback": "這會建立一份新的 live runtime 狀態；需要存檔時請到 World Map 主選單執行存檔。",
                "confirm_label": "確認重新開始",
                "payload": {"entry": "restart_game"},
            },
        ]
        hero_copy = "既有名冊仍封存在公會櫃台。你可以重新出發，也可以讀取最近一次的冒險足跡。"
    else:
        actions = [
            {
                "action_id": "start_new_game",
                "label": "開始新冒險（New Game）",
                "description": "",
                "token": "新",
                "kind": "primary",
                "enabled": True,
                "disabled_reason": None,
                "opens_registration": True,
                "final_action_id": "start_new_game",
                "registration_entry": "new_game",
                "registration_title": "建立冒險者名冊",
                "registration_feedback": "輸入名字並選擇初始職業；空白名字會使用「見習冒險者」。",
                "confirm_label": "確認開始",
                "payload": {"entry": "new_game"},
            }
        ]
        hero_copy = "城門外的礦道仍在發熱，公會只留下新的登錄名冊。你可以從這裡建立一段新的冒險。"
    return {
        "screen_id": "start_screen",
        "layout_family": "entry",
        "presentation": {"has_save": has_save},
        "screen_label": "開始畫面",
        "title": "《元素迷宮：邊境冒險者》",
        "hero_kicker": "邊境公會記錄",
        "hero_title": "元素迷宮",
        "hero_copy": hero_copy,
        "registration": registration_model(),
        "actions": actions,
    }


def registration_model() -> dict[str, Any]:
    job_summaries = {
        "劍士": "穩定近戰，適合承受壓力。",
        "法師": "使用魔法，重視 MP 與爆發。",
        "盜賊": "行動靈活，適合快速探索。",
        "牧師": "能恢復與支援，續航較佳。",
    }
    return {
        "panel_label": "冒險者登錄",
        "title": "建立冒險者名冊",
        "chip": "REG",
        "name_label": "冒險者名字",
        "name_placeholder": "見習冒險者",
        "fallback_name": "見習冒險者",
        "job_label": "初始職業",
        "job_hint": "對照 CLI 的四個初始職業，由 Python runtime 建立角色。",
        "default_job_id": "warrior",
        "feedback": "輸入名字並選擇初始職業；空白名字會使用「見習冒險者」。",
        "back_label": "返回",
        "back_description": "回到開始畫面",
        "confirm_label": "確認開始",
        "confirm_description": "建立 live runtime 狀態後開啟 Town Hub",
        "jobs": [
            {
                "id": job_id,
                "index": f"{idx}.",
                "label": job_key,
                "summary": job_summaries.get(job_key, "依照 Python runtime 職業資料建立。"),
            }
            for idx, (job_id, job_key) in enumerate(JOB_ID_TO_KEY.items(), start=1)
        ],
    }







def inventory_preview(state: dict[str, Any]) -> list[dict[str, Any]]:
    entries = []
    for item_id, qty in state.get("inventory", {}).items():
        data = ITEMS.get(item_id) or EQUIPMENT.get(item_id) or {}
        entries.append({"item_id": item_id, "label": data.get("name", item_name(item_id, state)), "quantity": qty})
    return entries


def get_status_preview_data(state: dict[str, Any]) -> dict[str, Any]:
    stats = game.get_stats(state)
    slot_names = {"weapon": "武器", "head": "頭部", "body": "身體", "accessory": "飾品", "special": "特殊"}
    equipment = []
    for slot, label in slot_names.items():
        item_id = state.get("equipment", {}).get(slot)
        equipment.append({
            "slot_label": label,
            "item_name": item_name(item_id, state) if item_id else "無",
            "item_id": item_id
        })
    skills = []
    for skill_id in state.get("learned_skills", []):
        skill = game.SKILLS.get(skill_id, {})
        skills.append({
            "name": skill.get("name", skill_id),
            "mp": skill.get("mp", 0),
            "desc": skill.get("desc", "")
        })
    return {
        "name": state.get("name", ""),
        "job_label": state.get("job", ""),
        "level": state.get("level", 1),
        "exp": state.get("exp", 0),
        "exp_next": game.exp_to_next(state.get("level", 1)),
        "gold": state.get("gold", 0),
        "guild_points": state.get("guild_points", 0),
        "hp_current": state.get("current_hp", stats["max_hp"]),
        "hp_max": stats["max_hp"],
        "mp_current": state.get("current_mp", stats["max_mp"]),
        "mp_max": stats["max_mp"],
        "attack": stats.get("attack", 0),
        "magic_attack": stats.get("magic_attack", 0),
        "defense": stats.get("defense", 0),
        "agility": stats.get("agility", 0),
        "crit": stats.get("crit", 0),
        "fire_resist": stats.get("fire_resist", 0),
        "equipment": equipment,
        "skills": skills
    }


def get_inventory_preview_data(state: dict[str, Any]) -> list[dict[str, Any]]:
    counts = {}
    equipped_set = set()

    for slot, item_id in state.get("equipment", {}).items():
        if item_id:
            counts[item_id] = counts.get(item_id, 0) + 1
            equipped_set.add(item_id)

    for item_id, qty in state.get("inventory", {}).items():
        if qty > 0:
            counts[item_id] = counts.get(item_id, 0) + qty

    entries = []
    for item_id in sorted(counts.keys()):
        qty = counts[item_id]
        category = "其他"
        if is_equipment_ref(state, item_id):
            category = "裝備"
            is_equipped = item_id in equipped_set
            name = f"{item_name(item_id, state)}（已裝備）" if is_equipped else item_name(item_id, state)
        else:
            name = item_name(item_id)
            item_data = ITEMS.get(item_id, {})
            kind = item_data.get("kind")
            if kind == "consumable":
                category = "補給品"
            elif kind in {"battle", "special"}:
                category = "戰術道具"
            elif item_id.startswith("key_"):
                category = "關鍵道具"
            elif item_id.startswith("mat_"):
                category = "素材"

        entries.append({
            "item_id": item_id,
            "name": name,
            "quantity": qty,
            "category": category,
            "desc": game.item_usage_summary(item_id)
        })
    return entries


def get_bestiary_preview_data(state: dict[str, Any]) -> list[dict[str, Any]]:
    entries = []
    for monster_id in state.get("bestiary", []):
        monster = game.MONSTERS.get(monster_id)
        if monster:
            drops_formatted = []
            for item_id, chance, qty in monster.get("drops", []):
                drops_formatted.append(f"{item_name(item_id)} ({int(chance*100)}%機率 x{qty})")
            drops_str = "、".join(drops_formatted) if drops_formatted else "無"

            entries.append({
                "monster_id": monster_id,
                "name": monster["name"],
                "level": monster["level"],
                "hp": monster["hp"],
                "element": monster["element"],
                "exp": monster["exp"],
                "gold_range": f"{monster['gold'][0]} - {monster['gold'][1]}G" if isinstance(monster["gold"], tuple) else f"{monster['gold']}G",
                "drops": drops_str
            })
    return entries
