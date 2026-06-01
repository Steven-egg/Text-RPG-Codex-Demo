from __future__ import annotations

import random
import shutil
from copy import deepcopy
from datetime import datetime
from typing import Any

from data import DUNGEONS, EQUIPMENT, ITEMS, JOBS

from . import game
from .formatting import item_name


JOB_IDS = ["warrior", "mage", "rogue", "cleric"]
JOB_ID_TO_KEY = dict(zip(JOB_IDS, JOBS.keys()))
JOB_KEY_TO_ID = {value: key for key, value in JOB_ID_TO_KEY.items()}
SAVE_BACKUP_PREFIX = "save.gui-backup"
FACILITY_VISUALS = {
    "guild": {"visual_group": "guild", "visual_anchor": "top_center_guild_hall"},
    "inn": {"visual_group": "rest", "visual_anchor": "left_inn"},
    "travel_shop": {"visual_group": "shop", "visual_anchor": "mid_left_market"},
    "workshop": {"visual_group": "workshop", "visual_anchor": "right_workshop_group"},
    "synthesis": {"visual_group": "alchemy", "visual_anchor": "bottom_left_alchemy"},
    "magic_shop": {"visual_group": "magic", "visual_anchor": "right_arcane_shop"},
    "temple": {"visual_group": "temple", "visual_anchor": "bottom_center_temple"},
    "relic_preview": {"visual_group": "archive", "visual_anchor": "bottom_right_archive"},
    "storage": {"visual_group": "storage", "visual_anchor": "far_bottom_right_depot"},
}
WORLD_MAP_PRESENTATION = {
    "dungeon_moss_cave": {
        "location_id": "moss_cave",
        "position": {"x": 24, "y": 48},
        "tone": "nature",
        "icon_token": "葉",
        "preview_role": "cave",
        "description": "潮濕陰暗的洞窟，布滿青苔與藤蔓，棲息著各種小型魔物。",
        "detail_note": "適合作為早期探索地點，live mode 會交由 Python runtime 驗證前往條件。",
        "exploration_rating": "低風險",
    },
    "dungeon_scorched_mine": {
        "location_id": "ember_quarry",
        "position": {"x": 49, "y": 42},
        "tone": "fire",
        "icon_token": "火",
        "preview_role": "quarry",
        "description": "黑色岩壁間冒著餘燼，舊礦道仍殘留火元素的熱度。",
        "detail_note": "推薦攜帶回復道具。live mode 會交由 Python runtime 驗證前往條件。",
        "exploration_rating": "中等風險",
    },
    "dungeon_ash_ravine": {
        "location_id": "ash_valley",
        "position": {"x": 48, "y": 67},
        "tone": "fire",
        "icon_token": "火",
        "preview_role": "valley",
        "description": "裂谷底部流動著暗紅熔脈，空氣裡混著鐵鏽與焦土味。",
        "detail_note": "比焦石礦坑更危險，適合裝備更新後挑戰。",
        "exploration_rating": "高風險",
    },
    "dungeon_cinder_seal_depths": {
        "location_id": "cinder_depths",
        "position": {"x": 64, "y": 82},
        "tone": "fire",
        "icon_token": "燼",
        "preview_role": "plateau",
        "description": "深處的岩層帶著燼印反光，火印線索在洞壁間若隱若現。",
        "detail_note": "目前由 runtime unlock 狀態決定是否可前往。",
        "exploration_rating": "高風險",
    },
}
WORLD_MAP_ROUTE_SEGMENTS = [
    {"id": "town_to_cave", "from": "border_town", "to": "moss_cave", "points": [[35, 22], [29, 34], [24, 48]]},
    {"id": "cave_to_quarry", "from": "moss_cave", "to": "ember_quarry", "points": [[24, 48], [37, 44], [49, 42]]},
    {"id": "quarry_to_valley", "from": "ember_quarry", "to": "ash_valley", "points": [[49, 42], [49, 55], [48, 67]]},
    {"id": "valley_to_depths", "from": "ash_valley", "to": "cinder_depths", "points": [[48, 67], [56, 77], [64, 82]]},
    {"id": "town_to_frost", "from": "border_town", "to": "frost_pass", "points": [[35, 22], [50, 15], [66, 18]]},
    {"id": "quarry_to_forest", "from": "ember_quarry", "to": "mist_forest", "points": [[49, 42], [62, 38], [75, 38]]},
    {"id": "forest_to_tower", "from": "mist_forest", "to": "moon_tower", "points": [[75, 38], [72, 49], [70, 57]]},
    {"id": "cave_to_ruins", "from": "moss_cave", "to": "drowned_ruins", "points": [[24, 48], [23, 64], [26, 78]]},
]
WORLD_MAP_PREVIEW_LOCATIONS = [
    {
        "location_id": "frost_pass",
        "label": "冰封峽谷",
        "description": "北方山脈被冰雪封住，峽谷入口覆著厚重霜霧。",
        "detail_note": "尚未解鎖。這裡只提供地圖瀏覽與 blocked action。",
        "position": {"x": 66, "y": 18},
        "tone": "ice",
        "icon_token": "冰",
        "locked_reason": "尚未取得北境通行線索",
        "attribute": "冰 / 山脈",
        "preview_role": "frost",
    },
    {
        "location_id": "mist_forest",
        "label": "遺忘森林",
        "description": "林間常年飄著薄霧，路徑會在日落後改變方向。",
        "detail_note": "尚未解鎖。未來可接故事線索或公會委託。",
        "position": {"x": 75, "y": 38},
        "tone": "nature",
        "icon_token": "森",
        "locked_reason": "需要完成青苔洞窟後續調查",
        "attribute": "自然 / 幻霧",
        "preview_role": "forest",
    },
    {
        "location_id": "moon_tower",
        "label": "影月塔",
        "description": "高塔矗立在灰白岩脊上，塔頂會在夜裡反射紫色月光。",
        "detail_note": "尚未解鎖。這裡只提供地圖瀏覽與 blocked action。",
        "position": {"x": 70, "y": 57},
        "tone": "arcane",
        "icon_token": "月",
        "locked_reason": "需要影月塔入口鑰印",
        "attribute": "秘法 / 月影",
        "preview_role": "tower",
    },
    {
        "location_id": "drowned_ruins",
        "label": "沉沒遺跡",
        "description": "海岸旁的古代遺跡半沉在潮水裡，退潮時才露出入口。",
        "detail_note": "尚未解鎖。可檢查低亮度地點和鎖定狀態。",
        "position": {"x": 26, "y": 78},
        "tone": "water",
        "icon_token": "潮",
        "locked_reason": "尚未取得潮汐時刻表",
        "attribute": "水 / 遺跡",
        "preview_role": "ruins",
    },
]


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
        self._save_backup_created = False

    @property
    def state_loaded(self) -> bool:
        return self.state is not None

    def require_state(self) -> dict[str, Any]:
        if self.state is None:
            raise GuiActionError("未載入遊戲核心狀態。", status=409)
        return self.state

    def new_game(self, name: str | None, job_id: str | None) -> dict[str, Any]:
        job_key = normalize_job_id(job_id)
        character_name = str(name or "").strip() or "見習冒險者"
        self.state = game.create_state(character_name, job_key)
        self._clear_live_run()
        return action_response(
            "start_new_game",
            "新的冒險者名冊已建立。可在世界地圖主選單進行存檔。",
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
        self._clear_live_run()
        return action_response(
            "load_game",
            "存檔已成功載入 Live 遊戲會話中。",
            self.state,
            screen_id="town_hub",
            next_route="../town_hub/index.html?mode=live",
        )

    def save_game(self, *, screen_id: str = "world_map") -> dict[str, Any]:
        state = self.require_state()
        self._backup_save_once()
        game.save_game(state)
        return action_response("save_game", "存檔寫入成功。", state, screen_id=screen_id)

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
            model = world_map_model(state)
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
            model = world_map_model(state)
            model["utility_preview"] = {
                "type": "inventory",
                "title": "背包唯讀摘要",
                "data": get_inventory_preview_data(state)
            }
            return self._live_response(
                action_id,
                "已開啟背包唯讀摘要。",
                screen_model=model,
            )
        if action_id == "open_bestiary":
            state = self.require_state()
            model = world_map_model(state)
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
        if action_id == "rest_at_inn":
            return self.rest_at_inn(payload, screen_id=screen_id)
        if action_id == "open_world_map":
            state = self.require_state()
            return action_response(
                action_id,
                "正在開啟世界地圖...",
                state,
                screen_id="world_map",
                next_route="../world_map/index.html?mode=live",
            )
        if action_id == "back_to_town_hub":
            state = self.require_state()
            self._clear_live_run()
            return action_response(
                action_id,
                "正在返回城鎮...",
                state,
                screen_id="town_hub",
                next_route="../town_hub/index.html?mode=live",
            )
        if action_id in {"return_to_exploration", "back_to_exploration"}:
            state = self.require_state()
            exploration = self.require_exploration()
            self.combat = None
            exploration["status"] = "exploring"
            return self._live_response(
                action_id,
                "正在返回探索...",
                screen_model=self.exploration_screen_model(),
                next_route="../dungeon_exploration/index.html?mode=live",
            )
        if action_id == "confirm_travel":
            return self.confirm_travel(payload)
        if action_id == "advance_step":
            return self.advance_step(payload)
        if action_id == "retreat":
            if screen_id == "combat_screen" or self.combat is not None:
                return self.combat_retreat()
            return self.retreat_from_exploration()
        if action_id in {"basic_attack", "defend", "use_item"}:
            return self.dispatch_combat_action(action_id, payload)
        raise GuiActionError(f"Unknown GUI action: {action_id}", status=404)

    def confirm_travel(self, payload: dict[str, Any]) -> dict[str, Any]:
        state = self.require_state()
        dungeon_id = payload.get("dungeon_id") or payload.get("location_id")
        if dungeon_id not in DUNGEONS:
            raise GuiActionError("Unknown dungeon.", status=400)
        dungeon = DUNGEONS[dungeon_id]
        if not game.is_unlocked(state, dungeon.get("unlock")):
            raise GuiActionError("Dungeon is locked.", status=403)
        game.clamp_vitals(state)
        run_log = {"gold": 0, "items": {}}
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
            screen_model=self.exploration_screen_model(),
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
            screen_model=self.combat_screen_model(),
            next_route="../combat_screen/index.html?mode=live",
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
            screen_model=world_map_model(state),
            next_route="../world_map/index.html?mode=live",
        )

    def start_combat(self, monster_id: str) -> None:
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
            "boss": False,
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

        turn_events = list(action_result.events)
        if combat["enemy_hp"] <= 0:
            turn_events.append(f"{enemy['name']}倒下。")
            game.record_battle_events(combat["battle_log"], combat["turn"], turn_events)
            return self.resolve_victory(action_result.summary + [f"{enemy['name']}倒下。"])

        enemy_events = game.monster_action(combat["enemy_id"], enemy, state, player_buffs, defending)
        effect_events = game.tick_effects(state, player_buffs, enemy_buffs)
        turn_events.extend(enemy_events)
        turn_events.extend(effect_events)
        game.record_battle_events(combat["battle_log"], combat["turn"], turn_events)
        summary = game.combat_summary_lines(action_result.summary, enemy_events, effect_events)
        combat["last_action_summary"] = " / ".join(summary[:2]) if summary else "回合結束。"
        combat["turn"] += 1

        if state.get("current_hp", 0) <= 0:
            return self.resolve_defeat("You were defeated in combat.")

        return self._live_response(
            action_id,
            combat["last_action_summary"],
            screen_model=self.combat_screen_model(),
        )

    def use_combat_item(self, item_id: str) -> game.CombatActionResult:
        state = self.require_state()
        combat = self.require_combat()
        enemy = combat["enemy"]
        enemy_buffs = combat["enemy_buffs"]
        if state.get("inventory", {}).get(item_id, 0) <= 0:
            raise GuiActionError("Item is not available.", status=409)
        if item_id == "item_potion_s":
            stats = game.get_stats(state)
            before = state["current_hp"]
            state["current_hp"] = min(stats["max_hp"], state["current_hp"] + 35)
            game.remove_item(state, item_id, 1)
            line = f"使用小藥水，回復 {state['current_hp'] - before} HP。"
            return game.CombatActionResult(events=[line], summary=[line])
        if item_id == "item_potion_m":
            stats = game.get_stats(state)
            before = state["current_hp"]
            state["current_hp"] = min(stats["max_hp"], state["current_hp"] + 70)
            game.remove_item(state, item_id, 1)
            line = f"使用中藥水，回復 {state['current_hp'] - before} HP。"
            return game.CombatActionResult(events=[line], summary=[line])
        if item_id == "item_focus_drop":
            stats = game.get_stats(state)
            before = state["current_mp"]
            state["current_mp"] = min(stats["max_mp"], state["current_mp"] + 12)
            game.remove_item(state, item_id, 1)
            line = f"使用集中滴露，回復 {state['current_mp'] - before} MP。"
            return game.CombatActionResult(events=[line], summary=[line])
        if item_id == "item_herb_antidote":
            game.remove_item(state, item_id, 1)
            state.setdefault("_clear_burn", True)
            line = "你嚼下解毒草，灼熱感稍微退去。"
            return game.CombatActionResult(events=[line], summary=[line])
        if item_id == "item_armor_piercer":
            game.remove_item(state, item_id, 1)
            enemy_buffs["defense_down"] = max(enemy_buffs.get("defense_down", 0), 3)
            damage = max(8, game.math.ceil(enemy["hp"] * 0.08))
            line = f"破甲釘命中敵人的護具縫隙，造成 {damage} 傷害，敵方防禦下降。"
            return game.CombatActionResult(damage=damage, events=[line], summary=[line])
        if item_id == "item_escape_scroll":
            game.remove_item(state, item_id, 1)
            return game.CombatActionResult(events=["卷軸化成白光，你撤回迷宮入口。"], summary=["卷軸化成白光，你撤回迷宮入口。"], outcome="escaped")
        raise GuiActionError("Unsupported combat item.", status=400)

    def combat_retreat(self) -> dict[str, Any]:
        state = self.require_state()
        combat = self.require_combat()
        enemy = combat["enemy"]
        if game.try_escape(state, enemy):
            return self.resolve_retreat(["你成功脫離戰鬥。"])
        action_result = game.CombatActionResult(events=["逃跑失敗。"], summary=["逃跑失敗。"])
        enemy_events = game.monster_action(combat["enemy_id"], enemy, state, combat["player_buffs"], False)
        effect_events = game.tick_effects(state, combat["player_buffs"], combat["enemy_buffs"])
        turn_events = list(action_result.events) + enemy_events + effect_events
        game.record_battle_events(combat["battle_log"], combat["turn"], turn_events)
        summary = game.combat_summary_lines(action_result.summary, enemy_events, effect_events)
        combat["last_action_summary"] = " / ".join(summary[:2]) if summary else "逃跑失敗。"
        combat["turn"] += 1
        if state.get("current_hp", 0) <= 0:
            return self.resolve_defeat("You were defeated while retreating.")
        return self._live_response("retreat", combat["last_action_summary"], screen_model=self.combat_screen_model())

    def resolve_victory(self, summary_lines: list[str]) -> dict[str, Any]:
        state = self.require_state()
        combat = self.require_combat()
        enemy = combat["enemy"]
        enemy_id = combat["enemy_id"]
        run_log = self.current_run_log()
        game.try_register_bestiary(state, enemy_id)
        game.gain_exp(state, enemy["exp"])
        gold = random.randint(*enemy["gold"])
        game.add_gold(state, gold, run_log)
        reward_lines = [f"獲得 {gold}G。"]
        for item_id, chance, qty in enemy["drops"]:
            stats = game.get_stats(state)
            final_chance = chance + stats.get("rare_drop", 0) / 100
            if random.random() <= final_chance:
                game.add_loot(state, item_id, qty, run_log)
                reward_lines.append(f"取得 {item_name(item_id)} x{qty}。")
        if enemy_id == "mon_scorched_guard":
            game.unlock(state, "item_armor_piercer")
            game.unlock(state, "recipe_piercing_bundle")
        if enemy_id == "mon_lava_imp":
            game.unlock(state, "recipe_heat_charm")
        combat["outcome"] = "victory"
        combat["last_action_summary"] = " / ".join(summary_lines[:2]) if summary_lines else f"擊敗 {enemy['name']}。"
        combat["result_overlay"] = result_overlay_model(
            "victory",
            "戰鬥勝利",
            f"擊敗 {enemy['name']}。",
            combat["last_action_summary"],
            reward_lines + [game.run_loot_summary(run_log)],
        )
        return self._live_response("basic_attack", "Victory.", screen_model=self.combat_screen_model())

    def resolve_retreat(self, summary_lines: list[str]) -> dict[str, Any]:
        combat = self.require_combat()
        combat["outcome"] = "retreat"
        combat["last_action_summary"] = " / ".join(summary_lines[:2]) if summary_lines else "你撤出戰鬥。"
        combat["result_overlay"] = result_overlay_model(
            "retreat",
            "撤退成功",
            "你撤回通往城鎮的路線。",
            combat["last_action_summary"],
            [game.run_loot_summary(self.current_run_log())],
        )
        game.record_battle_events(combat["battle_log"], combat["turn"], summary_lines or ["你撤出戰鬥。"])
        return self._live_response("retreat", "Retreated from combat.", screen_model=self.combat_screen_model())

    def resolve_defeat(self, message: str) -> dict[str, Any]:
        state = self.require_state()
        run_log = self.current_run_log()
        lost_gold = game.math.floor(run_log.get("gold", 0) * 0.3)
        state["gold"] = max(0, state.get("gold", 0) - lost_gold)
        lost_items = []
        for item_id, qty in run_log.get("items", {}).items():
            lose_qty = game.math.floor(qty * 0.3)
            if lose_qty > 0 and state.get("inventory", {}).get(item_id, 0) > 0:
                actual = min(lose_qty, state["inventory"].get(item_id, 0))
                game.remove_item(state, item_id, actual)
                lost_items.append(f"{item_name(item_id)} x{actual}")
        stats = game.get_stats(state)
        state["current_hp"] = max(1, stats["max_hp"] // 2)
        state["current_mp"] = max(0, stats["max_mp"] // 2)
        if self.combat is None:
            self.start_combat(DUNGEONS[self.require_exploration()["dungeon_id"]]["monsters"][0])
        combat = self.require_combat()
        combat["outcome"] = "defeat"
        combat["last_action_summary"] = message
        combat["result_overlay"] = result_overlay_model(
            "defeat",
            "戰鬥失敗",
            "工會救援隊把你帶回艾爾姆。",
            message,
            [f"失去本趟金幣 {lost_gold}G。", "散落素材：" + "、".join(lost_items) if lost_items else "素材大致都保住了。"],
        )
        combat.setdefault("battle_log", []).append("戰鬥結束：你倒下了。")
        return self._live_response("defeat", "Defeated. Returned by rescue.", screen_model=self.combat_screen_model())

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
        if screen_id == "dungeon_exploration":
            return self.exploration_screen_model()
        if screen_id == "combat_screen":
            return self.combat_screen_model()
        raise GuiActionError(f"未支援的 Live 畫面：{screen_id}", status=404)

    def exploration_screen_model(self) -> dict[str, Any]:
        state = self.require_state()
        exploration = self.require_exploration()
        dungeon = DUNGEONS[exploration["dungeon_id"]]
        stats = game.get_stats(state)
        current_step = exploration.get("current_step", 0)
        total_steps = dungeon["steps"]
        status = exploration.get("status", "exploring")
        return {
            "screen_id": "dungeon_exploration",
            "title": "迷宮探索",
            "subtitle": "正在進行迷宮探索，冒險的下一步正等待著你。",
            "resource_strip": [
                {"id": "hp", "label": f"HP {state['current_hp']}/{stats['max_hp']}", "tone": "hp" if state["current_hp"] > stats["max_hp"] * 0.35 else "warning"},
                {"id": "mp", "label": f"MP {state['current_mp']}/{stats['max_mp']}", "tone": "mp"},
                {"id": "gold", "label": f"{state.get('gold', 0)}G", "tone": "gold"},
            ],
            "dungeon": {
                "dungeon_id": exploration["dungeon_id"],
                "name": dungeon["name"],
                "summary": f"屬性：{dungeon['element']} / 推薦等級：{dungeon['recommended']}",
                "recommended_level": dungeon["recommended"],
                "player_level": f"Lv{state.get('level', 1)}",
                "attribute": dungeon["element"],
                "route_length": f"{total_steps} 步",
                "clear_state": "已通關" if exploration["dungeon_id"] in state.get("cleared_dungeons", []) else "未通關",
                "boss_state": boss_label(dungeon.get("boss")),
            },
            "run_status": {
                "current_step": current_step,
                "total_steps": total_steps,
                "step_note": exploration.get("last_message", "已抵達入口，準備前進。"),
                "status_label": "戰鬥中" if status == "combat" else "探索中",
                "risk_label": "普通",
                "supply_label": f"HP {state['current_hp']}/{stats['max_hp']}",
                "next_node": "下一步",
            },
            "run_rewards": run_reward_rows(exploration.get("run_log", {})),
            "event_preview": exploration.get("events", [])[-5:],
            "narrative_message": exploration.get("last_message", ""),
            "actions": [
                {
                    "action_id": "advance_step",
                    "label": "前進一步",
                    "description": "前進探索下一步。",
                    "enabled": status == "exploring",
                    "disabled_reason": None if status == "exploring" else "戰鬥中無法執行此動作。",
                    "primary": True,
                    "payload": {"dungeon_id": exploration["dungeon_id"], "current_step": current_step},
                },
                {
                    "action_id": "retreat",
                    "label": "撤退",
                    "description": "撤離當前迷宮並返回地圖。",
                    "enabled": status == "exploring",
                    "disabled_reason": None if status == "exploring" else "請先結束戰鬥。",
                    "primary": False,
                    "payload": {"dungeon_id": exploration["dungeon_id"]},
                },
            ],
        }

    def combat_screen_model(self) -> dict[str, Any]:
        state = self.require_state()
        combat = self.require_combat()
        enemy = combat["enemy"]
        stats = game.get_stats(state, combat["player_buffs"])
        enemy_hp = max(0, combat["enemy_hp"])
        resolved = combat.get("outcome") is not None
        usable_items = combat_item_rows(state)
        return {
            "screen_id": "combat_screen",
            "title": "戰鬥",
            "subtitle": "迎擊眼前的強敵，取得勝利以推進探索。",
            "resource_strip": [{"label": f"第 {combat['turn']} 回合", "tone": "neutral"}],
            "player": {
                "name": state.get("name", ""),
                "class_label": state.get("job", ""),
                "level_label": f"Lv{state.get('level', 1)}",
                "hp_label": f"{state['current_hp']} / {stats['max_hp']}",
                "mp_label": f"{state['current_mp']} / {stats['max_mp']}",
                "status_label": game.buff_summary(combat["player_buffs"]),
                "stance_label": "戰鬥結束" if resolved else "可行動",
            },
            "enemy": {
                "enemy_id": combat["enemy_id"],
                "name": enemy["name"],
                "hp_label": f"HP {enemy_hp} / {enemy['hp']}",
                "hp_percent": percent(enemy_hp, enemy["hp"]),
                "attribute": enemy["element"],
                "status_label": game.buff_summary(combat["enemy_buffs"]),
            },
            "command_message": combat.get("last_action_summary", ""),
            "skill_menu": {
                "label": "技能選擇",
                "title": "技能",
                "summary": "技能系統準備中。",
                "empty_message": "當前無法使用技能。",
                "items": [],
            },
            "item_menu": {
                "label": "道具選擇",
                "title": "道具",
                "summary": f"目標：{enemy['name']} / 狀態 {game.buff_summary(combat['enemy_buffs'])}。",
                "empty_message": "沒有可用道具。",
                "items": usable_items,
            },
            "battle_log": combat.get("battle_log", []),
            "result_overlay": combat.get("result_overlay"),
            "actions": [
                {
                    "action_id": "basic_attack",
                    "label": "攻擊",
                    "description": "進行普通攻擊。",
                    "enabled": not resolved,
                    "disabled_reason": None if not resolved else "戰鬥已結束。",
                    "primary": True,
                    "payload": {"enemy_id": combat["enemy_id"]},
                },
                {
                    "action_id": "open_skill_menu",
                    "label": "技能",
                    "description": "職業特殊技能。",
                    "enabled": False,
                    "disabled_reason": "此 live slice 尚未開放技能。",
                    "primary": False,
                    "payload": {"source": "combat_screen"},
                },
                {
                    "action_id": "open_item_menu",
                    "label": "道具",
                    "description": "使用攜帶的戰鬥道具。",
                    "enabled": not resolved and bool(usable_items),
                    "disabled_reason": None if usable_items else "沒有可用道具。",
                    "primary": False,
                    "payload": {"source": "combat_screen"},
                },
                {
                    "action_id": "defend",
                    "label": "防禦",
                    "description": "採取防禦姿態降低下回合所受傷害。",
                    "enabled": not resolved,
                    "disabled_reason": None if not resolved else "戰鬥已結束。",
                    "primary": False,
                    "payload": {},
                },
                {
                    "action_id": "retreat",
                    "label": "逃跑",
                    "description": "嘗試逃離當前戰鬥。",
                    "enabled": not resolved,
                    "disabled_reason": None if not resolved else "戰鬥已結束。",
                    "primary": False,
                    "payload": {"enemy_id": combat["enemy_id"]},
                },
            ],
        }

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
        "status": "success",
        "action_id": action_id,
        "message": message,
        "state_summary": state_summary(state),
        "screen_model": build_screen_model(screen_id, state) if screen_id else None,
        "next_route": next_route,
        "next_screen_id": screen_id,
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
    locations = [
        {
            "location_id": "border_town",
            "label": "邊境城鎮 艾爾姆",
            "description": "旅程的據點，公會、旅店與工坊都集中在城牆內。",
            "detail_note": "目前所在城鎮。可從這裡返回 Town Hub live screen。",
            "position": {"x": 35, "y": 22},
            "tone": "town",
            "icon_token": "城",
            "unlocked": True,
            "locked_reason": None,
            "favorite": False,
            "status_label": "目前據點",
            "recommended_level": "安全",
            "steps": "0 步",
            "attribute": "城鎮 / 無",
            "clear_state": "可返回",
            "exploration_rating": "整備中",
            "boss": "無",
            "preview_role": "town",
            "primary_action": {
                "action_id": "back_to_town_hub",
                "label": "返回城鎮",
                "enabled": True,
                "disabled_reason": None,
                "payload": {"location_id": "border_town"},
            },
        }
    ]
    unlocked_location_ids = {"border_town"}
    for dungeon_id, dungeon in DUNGEONS.items():
        presentation = WORLD_MAP_PRESENTATION.get(
            dungeon_id,
            {
                "location_id": dungeon_id,
                "position": {"x": 50, "y": 50},
                "tone": "fire" if "fire" in dungeon_id or "cinder" in dungeon_id else "nature",
                "icon_token": "地",
                "preview_role": "cave",
                "description": f"{dungeon['recommended']} / {dungeon['steps']} 步",
                "detail_note": "Live 模式將由遊戲核心驗證前往條件。",
                "exploration_rating": "核心驗證",
            },
        )
        unlocked = game.is_unlocked(state, dungeon.get("unlock"))
        location_id = presentation["location_id"]
        if unlocked:
            unlocked_location_ids.add(location_id)
        locations.append(
            {
                "location_id": location_id,
                "label": dungeon["name"],
                "description": presentation["description"],
                "detail_note": presentation["detail_note"],
                "position": presentation["position"],
                "tone": presentation["tone"],
                "icon_token": presentation["icon_token"],
                "unlocked": unlocked,
                "locked_reason": None if unlocked else "尚未由 runtime 解鎖。",
                "favorite": dungeon_id in {"dungeon_moss_cave", "dungeon_scorched_mine", "dungeon_ash_ravine"},
                "status_label": "可探索" if unlocked else "尚未解鎖",
                "recommended_level": dungeon["recommended"],
                "steps": f"{dungeon['steps']} 步",
                "attribute": dungeon["element"],
                "clear_state": "已通關" if dungeon_id in state.get("cleared_dungeons", []) else "未通關",
                "exploration_rating": presentation["exploration_rating"],
                "boss": boss_label(dungeon.get("boss")),
                "preview_role": presentation["preview_role"],
                "primary_action": {
                    "action_id": "confirm_travel",
                    "label": "確認前往",
                    "enabled": unlocked,
                    "disabled_reason": None if unlocked else "尚未由 runtime 解鎖。",
                    "payload": {"dungeon_id": dungeon_id, "location_id": location_id},
                },
            }
        )
    for location in WORLD_MAP_PREVIEW_LOCATIONS:
        locations.append(
            {
                **location,
                "unlocked": False,
                "favorite": False,
                "status_label": "尚未解鎖",
                "recommended_level": "未知",
                "steps": "未知",
                "clear_state": "鎖定",
                "exploration_rating": "無資料",
                "boss": "未知",
                "primary_action": {
                    "action_id": "confirm_travel",
                    "label": "確認前往",
                    "enabled": False,
                    "disabled_reason": location["locked_reason"],
                    "payload": {"location_id": location["location_id"]},
                },
            }
        )
    route_segments = [
        {
            "id": route["id"],
            "status": "open" if route["from"] in unlocked_location_ids and route["to"] in unlocked_location_ids else "locked",
            "points": route["points"],
        }
        for route in WORLD_MAP_ROUTE_SEGMENTS
    ]
    return {
        "screen_id": "world_map",
        "layout_family": "navigation_map",
        "title": "世界地圖",
        "subtitle": "Live 模式使用遊戲核心狀態；畫面結構與靜態原型保持一致。",
        "selected_location_id": next((location["location_id"] for location in locations if location["location_id"] != "border_town" and location["unlocked"]), "border_town"),
        "current_location_id": "border_town",
        "player": player_model(state),
        "menu_actions": [
            {"action_id": "view_status", "label": "查看狀態", "description": "查看冒險者的能力數值與目前裝備。", "enabled": True, "payload": {}},
            {"action_id": "open_bestiary", "label": "怪物圖鑑", "description": "查看冒險中已登錄的魔物資訊。", "enabled": True, "payload": {}},
            {"action_id": "open_inventory", "label": "背包 / 裝備", "description": "查看背包內持有的道具、裝備與素材。", "enabled": True, "payload": {}},
            {"action_id": "save_game", "label": "存檔", "description": "透過遊戲核心寫入目前的進度。", "enabled": True, "payload": {}},
            {"action_id": "open_settings", "label": "設定", "description": "調整遊戲設定。", "enabled": True, "payload": {}},
            {"action_id": "back_to_start_screen", "label": "回到標題", "description": "返回遊戲開始標題畫面。", "enabled": True, "payload": {}},
        ],
        "route_segments": route_segments,
        "locations": locations,
    }


def town_hub_model(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "screen_id": "town_hub",
        "layout_family": "hub",
        "title": "艾爾姆城鎮 (Live)",
        "subtitle": "角色資源狀態與核心行為皆與 Python 遊戲引擎同步。",
        "resource_strip": resource_strip(state),
        "town_guidance": [
            "Live 模式：所有冒險行為皆經由 Python 核心驗證。",
            "可前往世界地圖繼續冒險，或在城鎮旅店進行休整。",
        ],
        "selected_facility_id": "guild",
        "facility_nodes": facility_nodes(state),
        "navigation_actions": [
            {"action_id": "open_world_map", "label": "前往世界地圖", "description": "離開城鎮，選擇下一個目的地。", "enabled": True, "payload": {}},
        ],
    }


def facility_nodes(state: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        facility("guild", "冒險者工會", "委託板與物資交付功能將在後續版本開放。", "guild", "open_facility", enabled=False),
        facility(
            "inn",
            "旅店",
            "前往旅店，提供金幣休整並回復狀態。",
            "bed",
            "open_facility",
            payload={"facility_id": "inn", "target_screen_id": "inn_screen"},
            target_screen_id="inn_screen",
            navigation_route="../inn_screen/index.html",
        ),
        facility("travel_shop", "旅人小鋪", "道具交易功能將在後續版本開放。", "shop", "open_facility", enabled=False),
        facility("workshop", "鐵刃 / 堅甲工坊", "裝備購買與強化功能將在後續版本開放。", "hammer", "open_facility", enabled=False),
        facility("synthesis", "米菈合成屋", "煉金合成配方將在後續版本開放。", "alchemy", "open_facility", enabled=False),
        facility("magic_shop", "星燈魔法商店", "魔法書購買與學習將在後續版本開放。", "magic", "open_facility", enabled=False),
        facility("temple", "轉職神殿", "神殿目前僅供預覽；轉職與故事線索解鎖需特定條件。", "temple", "open_facility", enabled=False),
        facility("relic_preview", "聖物調查", "聖物調查目前僅供預覽。", "relic", "open_facility", enabled=False),
        facility("storage", "城鎮倉庫", "倉庫轉移與物件存放功能將在後續版本開放。", "storage", "open_facility", enabled=False),
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
    target_screen_id: str | None = None,
    navigation_route: str | None = None,
) -> dict[str, Any]:
    visual = FACILITY_VISUALS.get(facility_id, {})
    return {
        "facility_id": facility_id,
        "label": label,
        "description": description,
        "visual_group": visual.get("visual_group", facility_id),
        "visual_anchor": visual.get("visual_anchor", facility_id),
        "icon_role": icon_role,
        "enabled": enabled,
        "disabled_reason": None if enabled else "此設施的 Live 模式功能將在後續版本開放。",
        "badges": [],
        "primary_action": action_id,
        "payload": payload or {"facility_id": facility_id},
        "target_screen_id": target_screen_id,
        "navigation_route": navigation_route,
    }


def inn_screen_model(state: dict[str, Any]) -> dict[str, Any]:
    summary = state_summary(state) or {}
    return {
        "screen_id": "inn_screen",
        "layout_family": "dialogue_node",
        "title": "艾爾姆旅店 (Live)",
        "subtitle": "與遊戲核心同步的休息休整服務。",
        "resource_strip": resource_strip(state),
        "feedback_message": None,
        "service": {
            "service_id": "overnight_rest",
            "label": "住宿休息",
            "description": "支付 30G 住宿費用，並由遊戲核心回復所有生命值與魔力值。",
            "cost": 30,
            "enabled": summary.get("gold", 0) >= 30,
            "disabled_reason": None if summary.get("gold", 0) >= 30 else "身上金幣不足。",
            "action_id": "rest_at_inn",
            "payload": {"service_id": "overnight_rest", "cost": 30},
        },
        "actions": [
            {
                "action_id": "rest_at_inn",
                "label": "休息休整",
                "description": "支付 30G 費用以完全回復狀態。",
                "enabled": summary.get("gold", 0) >= 30,
                "disabled_reason": None if summary.get("gold", 0) >= 30 else "身上金幣不足。",
                "payload": {"service_id": "overnight_rest", "cost": 30},
            }
        ],
        "navigation_actions": [
            {
                "action_id": "back_to_town_hub",
                "label": "返回城鎮",
                "description": "離開旅店返回城鎮廣場。",
                "enabled": True,
                "payload": {"from": "inn_screen"},
            }
        ],
    }


def run_reward_rows(run_log: dict[str, Any]) -> list[dict[str, str]]:
    rows = []
    gold = int(run_log.get("gold", 0) or 0)
    if gold:
        rows.append({"label": "金幣", "value": f"{gold}G"})
    for item_id, qty in run_log.get("items", {}).items():
        rows.append({"label": item_name(item_id), "value": f"x{qty}"})
    return rows


def combat_item_rows(state: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    for item_id in ["item_potion_s", "item_potion_m", "item_focus_drop", "item_herb_antidote", "item_armor_piercer", "item_escape_scroll"]:
        qty = state.get("inventory", {}).get(item_id, 0)
        if qty <= 0:
            continue
        item = ITEMS.get(item_id, {})
        rows.append(
            {
                "action_id": "use_item",
                "label": item.get("name", item_name(item_id)),
                "meta": f"x{qty}",
                "description": item.get("desc", ""),
                "enabled": True,
                "disabled_reason": None,
                "payload": {"item_id": item_id},
            }
        )
    return rows


def result_overlay_model(outcome: str, title: str, status: str, summary: str, rows: list[str]) -> dict[str, Any]:
    if outcome in ("victory", "retreat"):
        next_action = {
            "action_id": "back_to_exploration",
            "label": "返回探索",
            "description": "回到探索畫面繼續前進。",
            "payload": {"from": f"combat_result_{outcome}"},
            "feedback_message": "正在返回探索...",
            "navigate_to": "../dungeon_exploration/index.html?mode=live",
        }
    else:
        next_action = {
            "action_id": "back_to_town_hub",
            "label": "回到城鎮",
            "description": "返回城鎮廣場進行休整。",
            "payload": {"from": f"combat_result_{outcome}"},
            "feedback_message": "正在返回城鎮...",
            "navigate_to": "../town_hub/index.html?mode=live",
        }
    return {
        "outcome": outcome,
        "label": "戰鬥結束",
        "title": title,
        "status_summary": status,
        "battle_summary": summary,
        "reward_title": "結算",
        "rows": [
            {"label": f"{index}.", "value": row, "tone": "danger" if outcome == "defeat" and index == 1 else "neutral"}
            for index, row in enumerate(rows, start=1)
        ],
        "next_action": next_action,
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


def get_status_preview_data(state: dict[str, Any]) -> dict[str, Any]:
    stats = game.get_stats(state)
    slot_names = {"weapon": "武器", "head": "頭部", "body": "身體", "accessory": "飾品", "special": "特殊"}
    equipment = []
    for slot, label in slot_names.items():
        item_id = state.get("equipment", {}).get(slot)
        equipment.append({
            "slot_label": label,
            "item_name": item_name(item_id) if item_id else "無",
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
    entries = []
    for item_id, qty in sorted(state.get("inventory", {}).items()):
        category = "其他"
        if item_id in EQUIPMENT:
            category = "裝備"
        else:
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
            "name": item_name(item_id),
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
