from __future__ import annotations

from typing import Any
from data import DUNGEONS, MONSTERS
from . import game
from .gui_presentation_helpers import run_reward_rows, boss_label
from .gui_presentation import display_hit_points, display_resource


def exploration_screen_model(session: Any) -> dict[str, Any]:
    state = session.require_state()
    exploration = session.require_exploration()
    dungeon = DUNGEONS[exploration["dungeon_id"]]
    stats = game.get_stats(state)
    current_step = exploration.get("current_step", 0)
    total_steps = dungeon["steps"]
    status = exploration.get("status", "exploring")

    if exploration["dungeon_id"] == "dungeon_scorched_mine" and current_step >= total_steps:
        game.activate_boss_glen_investigation(state)

    boss_id = dungeon.get("boss")
    boss_action = None
    boss_is_available = boss_id and game.boss_available_at_dungeon_end(
        state, exploration["dungeon_id"], boss_id
    )
    if boss_id and current_step >= total_steps and boss_is_available:
        boss_name = MONSTERS[boss_id]["name"]
        is_enabled = status in ("exploring", "resolved") and current_step >= total_steps
        disabled_reason = None
        if status == "combat":
            is_enabled = False
            disabled_reason = "戰鬥中無法執行此動作。"
        elif boss_id == "boss_glen":
            if not state.get("flags", {}).get(game.BOSS_GLEN_INVESTIGATION_ACCEPTED_FLAG):
                is_enabled = False
                disabled_reason = "先回工會確認這股氣息。"

        boss_action = {
            "action_id": "challenge_boss",
            "label": f"挑戰 {boss_name}",
            "description": f"決戰迷宮守護者 {boss_name}。",
            "enabled": is_enabled,
            "disabled_reason": disabled_reason,
            "primary": is_enabled,
            "payload": {"dungeon_id": exploration["dungeon_id"], "boss_id": boss_id},
        }

    actions = [
        {
            "action_id": "advance_step",
            "label": "前進一步",
            "description": "前進探索下一步。",
            "enabled": status == "exploring" and current_step < total_steps,
            "disabled_reason": (
                "戰鬥中無法執行此動作。" if status == "combat" else (
                    "已抵達終點，請挑戰守護者或離開返回地圖。" if current_step >= total_steps else None
                )
            ),
            "primary": not (boss_action and boss_action["enabled"]),
            "payload": {"dungeon_id": exploration["dungeon_id"], "current_step": current_step},
        }
    ]
    if boss_action:
        actions.append(boss_action)
    actions.append({
        "action_id": "retreat",
        "label": "離開迷宮" if current_step >= total_steps else "撤退",
        "description": "返回世界地圖。" if current_step >= total_steps else "撤離當前迷宮並返回地圖。",
        "enabled": status != "combat",
        "disabled_reason": None if status != "combat" else "請先結束戰鬥。",
        "primary": not (boss_action and boss_action["enabled"]),
        "payload": {"dungeon_id": exploration["dungeon_id"]},
    })

    # Generate narrative guidance message
    glen_sighted = state.get("flags", {}).get("boss_glen_sighted")
    glen_accepted = state.get("flags", {}).get("boss_glen_investigation_accepted")
    glen_defeated = state.get("flags", {}).get("boss_glen_defeated")

    if exploration["dungeon_id"] == "dungeon_scorched_mine":
        if current_step >= total_steps:
            if glen_defeated:
                narrative_msg = "山寨頭目葛倫已被擊敗。焦石礦坑深處的熱度逐漸退去，你可以隨時離開迷宮返回城鎮。"
            elif glen_accepted:
                narrative_msg = "已確認焦石礦坑最深處葛倫的藏身處。準備好迎接激烈的首領戰了嗎？"
            else:
                narrative_msg = "你感覺到一股強大的敵意就在前方！但似乎需要先回工會回報，以了解如何開啟挑戰。"
        else:
            if glen_accepted:
                narrative_msg = "你正在前往焦石礦坑最深處。葛倫的嘍囉們在四處游蕩，請保持警惕，準備決戰。"
            elif glen_sighted:
                narrative_msg = "已確認焦石礦坑深處異常氣息，請先撤退回到工會接受葛倫的調查委託。"
            else:
                narrative_msg = "焦石礦坑內部瀰漫著焦油的氣息，山賊嘍囉隱蔽在礦道陰影中。小心前進。"
    elif exploration["dungeon_id"] == "dungeon_ash_ravine":
        ash_defeated = state.get("flags", {}).get("ash_guardian_defeated")
        ash_scouted = "quest_ash_ravine_scout" in state.get("completed_quests", [])
        if current_step >= total_steps:
            if ash_defeated:
                narrative_msg = "灰燼裂谷終點的熱度逐漸退去，古老守護者已歸於灰燼。你可以安全離開迷宮。"
            elif ash_scouted:
                narrative_msg = "已確認灰燼裂谷最深處的熱能波動。古老的巨影在熱風中蠢蠢欲動，準備好迎接決戰了嗎？"
            else:
                narrative_msg = "裂谷深處熱浪滾滾，你隱約感受到強烈的震動與不尋常的熱源。請收集好裂谷素材，先撤退回工會登記偵查回報。"
        else:
            if ash_scouted:
                narrative_msg = "你再次深入灰燼裂谷。周圍的溫度比上次更高，元素守衛的甦醒震動愈加強烈。"
            else:
                narrative_msg = "灰燼裂谷中熱浪襲人，四周散落著焦黑的鐵片。小心前進，收集工會所需的偵查素材。"
    elif exploration["dungeon_id"] == "dungeon_cinder_seal_depths":
        cinder_defeated = state.get("flags", {}).get("cinder_seal_sentinel_defeated")
        cinder_scouted = "quest_cinder_depths_scout" in state.get("completed_quests", [])
        if current_step >= total_steps:
            if cinder_defeated:
                narrative_msg = "結界核心已解除封印，古老的鎮衛碎裂為塵土。第一幕的主線探索已告一段落。"
            elif cinder_scouted:
                narrative_msg = "燼印深窟的最底層，結界核心傳來沉重的機械甦醒聲。做好萬全準備發起挑戰！"
            else:
                narrative_msg = "深窟底層的火印微弱共鳴，前方氣流異常混亂。似乎需要先回工會，將此處的偵查結果報告給諾亞。"
        else:
            if cinder_scouted:
                narrative_msg = "你正在深入封印的核心地帶。空氣中的火元素粒子異常活躍，準備迎擊最終的守護者。"
            else:
                narrative_msg = "深窟內部分佈著交錯的紅石礦脈，古老結界的氣息若隱若現。小心前進，收集深窟偵查素材。"
    else:
        if current_step >= total_steps:
            narrative_msg = f"你已抵達 {dungeon['name']} 的最深處。前方沒有路了，整理收穫後即可離開迷宮。"
        else:
            narrative_msg = f"你正在探索 {dungeon['name']}。注意維持小隊的 HP 與 MP，小心前方的未知遭遇。"

    boss_defeated = game.boss_defeated(state, boss_id)

    hp_ratio = state["current_hp"] / stats["max_hp"] if stats["max_hp"] > 0 else 1.0
    if hp_ratio > 0.6:
        squad_status = "良好"
    elif hp_ratio > 0.25:
        squad_status = "警告"
    else:
        squad_status = "危急"

    # Determine dynamic boss label and availability wording
    boss_state_label = "-"
    if boss_id:
        if boss_id == "boss_glen":
            if state.get("flags", {}).get("boss_glen_defeated"):
                boss_state_label = "山寨頭目葛倫 (已擊敗)"
            elif state.get("flags", {}).get("boss_glen_investigation_accepted"):
                boss_state_label = "山寨頭目葛倫 (可挑戰)"
            elif state.get("flags", {}).get("boss_glen_sighted"):
                boss_state_label = "山寨頭目葛倫 (未接受調查)"
            else:
                boss_state_label = "深處有異動 (需要完成偵查)"
        elif boss_id == "boss_ash_guardian":
            if state.get("flags", {}).get("ash_guardian_defeated"):
                boss_state_label = "灰燼守衛 (已擊敗)"
            elif "quest_ash_ravine_scout" in state.get("completed_quests", []):
                boss_state_label = "灰燼守衛 (可挑戰)"
            else:
                boss_state_label = "深處有異動 (需要完成偵查)"
        elif boss_id == "boss_cinder_seal_sentinel":
            if state.get("flags", {}).get("cinder_seal_sentinel_defeated"):
                boss_state_label = "燼印鎮衛 (已擊敗)"
            elif "quest_cinder_depths_scout" in state.get("completed_quests", []):
                boss_state_label = "燼印鎮衛 (可挑戰)"
            else:
                boss_state_label = "深處有異動 (需要完成偵查)"
        else:
            label = boss_label(boss_id)
            if game.boss_defeated(state, boss_id):
                boss_state_label = f"{label} (defeated)"
            elif game.boss_available_at_dungeon_end(state, exploration["dungeon_id"], boss_id):
                boss_state_label = f"{label} (available)"
            else:
                boss_state_label = f"{label} (locked)"

    return {
        "screen_id": "dungeon_exploration",
        "title": "迷宮探索",
        "subtitle": "正在進行迷宮探索，冒險的下一步正等待著你。",
        "resource_strip": [
            {"id": "hp", "label": f"HP {display_hit_points(state['current_hp'])}/{display_hit_points(stats['max_hp'])}", "tone": "hp" if state["current_hp"] > stats["max_hp"] * 0.35 else "warning"},
            {"id": "mp", "label": f"MP {display_resource(state['current_mp'])}/{display_resource(stats['max_mp'])}", "tone": "mp"},
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
            "boss_state": boss_state_label,
        },
        "run_status": {
            "current_step": current_step,
            "total_steps": total_steps,
            "step_note": exploration.get("last_message", "已抵達入口，準備前進。"),
            "status_label": "已通關" if boss_defeated else ("戰鬥中" if status == "combat" else "探索中"),
            "risk_label": "無" if boss_defeated else ("極高 (首領)" if current_step >= total_steps else "中等"),
            "supply_label": squad_status,
            "next_node": "下一步",
        },
        "run_rewards": run_reward_rows(exploration.get("run_log", {})),
        "event_preview": exploration.get("events", [])[-5:],
        "narrative_message": narrative_msg,
        "actions": actions,
    }
