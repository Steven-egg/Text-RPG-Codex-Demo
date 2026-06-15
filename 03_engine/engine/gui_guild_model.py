from __future__ import annotations

from typing import Any
from data import DUNGEONS, EQUIPMENT, ITEMS, QUESTS
from . import game
from .formatting import item_name
from .gui_presentation import resource_strip


def guild_screen_model(state: dict[str, Any]) -> dict[str, Any]:
    unlocked_dungeons = []
    for d_id, d_data in DUNGEONS.items():
        if game.is_unlocked(state, d_data.get("unlock")):
            unlocked_dungeons.append((d_id, d_data))

    unlocked_quests = []
    for q_id, q_data in QUESTS.items():
        if game.quest_unlocked(state, q_id):
            unlocked_quests.append((q_id, q_data))

    task_rows = []
    task_details = {}
    reward_summaries = {}
    condition_rows = {}

    for d_id, d_data in unlocked_dungeons:
        cleared = d_id in state.get("cleared_dungeons", [])
        reported = state.get("flags", {}).get(f"guild_reported_{d_id}", False)

        if not cleared:
            status = "requirements_missing"
            status_label = "未通關"
            status_icon_id = "missing"
            desc = f"你尚未完成 {d_data['name']} 的探索路線。請前往世界地圖並挑戰通關後，再來工會登記回報。"
            notes = "未通關無法登記回報。"
            feedback = { "tone": "warning", "speaker": "莉娜", "text": f"你還沒有走完 {d_data['name']} 呢，通關後我再幫你登記。" }
            disabled_reason = f"需要完成 {d_data['name']} 探索路線。"
        elif not reported:
            status = "ready_to_submit"
            status_label = "可回報"
            status_icon_id = "ready"
            desc = f"你已成功通關 {d_data['name']} 的探索路線！可在工會櫃台登記回報，確認首次通關獎勵的領取狀態。"
            notes = f"回報將標記為已登記狀態。首次通關獎勵（工會積分 +{d_data['clear_guild']}）已於通關當下直接發放。"
            feedback = { "tone": "success", "speaker": "莉娜", "text": f"太棒了！已確認你的 {d_data['name']} 探索記錄，可以進行回報登記了。" }
            disabled_reason = None
        else:
            status = "completed"
            status_label = "已完成"
            status_icon_id = "completed"
            desc = f"你已通關並完成 {d_data['name']} 的探索回報。記錄已保存在工會名冊中。"
            notes = "首次通關獎勵已取得。此回報已結案。"
            feedback = { "tone": "info", "speaker": "莉娜", "text": f"這份 {d_data['name']} 通關回報已經登記完成了，幹得好！" }
            disabled_reason = "這個回報已完成"

        task_rows.append({
            "task_id": d_id,
            "title": f"{d_data['name']} 探索回報",
            "giver": "工會",
            "status": status,
            "status_label": status_label,
            "status_icon_id": status_icon_id,
            "enabled": True,
            "disabled_reason": None,
        })

        task_details[d_id] = {
            "task_id": d_id,
            "title": f"{d_data['name']} 探索回報",
            "giver": "工會",
            "description": desc,
            "status_label": status_label,
            "notes": notes,
            "disabled_reason": disabled_reason,
            "ready_feedback": feedback if not reported and cleared else None,
            "missing_feedback": feedback if not cleared else None,
            "completed_feedback": feedback if reported else None,
        }

        reward_summaries[d_id] = {
            "gold": None,
            "guild_points": d_data["clear_guild"],
            "items": [],
            "unlocks": [],
            "notes": f"首次通關獎勵已取得 (工會積分 +{d_data['clear_guild']})" if (reported or cleared) else f"首次通關獎勵尚未取得 (預期工會積分 +{d_data['clear_guild']})"
        }

        condition_rows[d_id] = [
            {
                "id": f"condition_{d_id}_clear",
                "condition_type": "dungeon_clear",
                "label": f"通關 {d_data['name']}",
                "required_value": "通關",
                "current_value": "已通關" if cleared else "未通關",
                "status": "met" if cleared else ("not_applicable" if reported else "missing"),
                "status_label": "已滿足" if cleared else "未滿足",
                "status_icon_id": "met" if cleared else "missing",
                "source": "runtime"
            }
        ]

    for q_id, q_data in unlocked_quests:
        cleared = q_id in state.get("completed_quests", [])
        ready = game.quest_ready(state, q_id)

        if cleared:
            status = "completed"
            status_label = "已完成"
            status_icon_id = "completed"
            desc = q_data.get("desc", "")
            notes = "此委託已完成。"
            feedback = { "tone": "info", "speaker": q_data.get("giver", "莉娜"), "text": "這份委託已經完成登記了，謝謝你！" }
            disabled_reason = "這個委託已完成"
        elif ready:
            status = "ready_to_submit"
            status_label = "可回報"
            status_icon_id = "ready"
            desc = q_data.get("desc", "")
            notes = "交付委託會消耗素材。"
            feedback = { "tone": "success", "speaker": q_data.get("giver", "莉娜"), "text": "你收集齊委託需求的物件了啊，可以進行回報登記了。" }
            disabled_reason = None
        else:
            status = "requirements_missing"
            status_label = "條件不足"
            status_icon_id = "missing"
            desc = q_data.get("desc", "")
            notes = "尚未滿足交付條件。"
            feedback = { "tone": "warning", "speaker": q_data.get("giver", "莉娜"), "text": "這份委託的需求還沒收集齊呢。" }
            disabled_reason = "尚未滿足交付條件"

        task_rows.append({
            "task_id": q_id,
            "title": q_data.get("title", q_id),
            "giver": q_data.get("giver", "工會"),
            "status": status,
            "status_label": status_label,
            "status_icon_id": status_icon_id,
            "enabled": True,
            "disabled_reason": None,
        })

        task_details[q_id] = {
            "task_id": q_id,
            "title": q_data.get("title", q_id),
            "giver": q_data.get("giver", "工會"),
            "description": desc,
            "status_label": status_label,
            "notes": notes,
            "disabled_reason": disabled_reason,
            "ready_feedback": feedback if status == "ready_to_submit" else None,
            "missing_feedback": feedback if status == "requirements_missing" else None,
            "completed_feedback": feedback if status == "completed" else None,
        }

        # Populate rewards
        reward_items = []
        for rit_id, rqty in q_data.get("reward", {}).get("items", {}).items():
            reward_items.append({
                "item_id": rit_id,
                "label": item_name(rit_id),
                "quantity": rqty
            })

        reward_unlocks = []
        for u_key in q_data.get("unlocks", []):
            if u_key == q_id:
                continue
            if u_key == "shop_synthesis_01":
                reward_unlocks.append("米菈合成屋")
            elif u_key == "item_escape_scroll":
                reward_unlocks.append("逃脫卷軸")
            elif u_key == "second_act_preview":
                reward_unlocks.append("第二幕預告")
            elif u_key == "unlock_act_2":
                reward_unlocks.append("第二幕入口")
            elif u_key == "unlock_ash_ravine":
                reward_unlocks.append("灰燼裂谷")
            elif u_key in DUNGEONS:
                reward_unlocks.append(DUNGEONS[u_key]["name"])
            elif u_key in ITEMS:
                reward_unlocks.append(ITEMS[u_key]["name"])
            elif u_key in EQUIPMENT:
                reward_unlocks.append(EQUIPMENT[u_key]["name"])
            else:
                reward_unlocks.append(u_key)

        reward_summaries[q_id] = {
            "gold": q_data.get("reward", {}).get("gold", 0) or None,
            "guild_points": q_data.get("reward", {}).get("guild", 0) or None,
            "items": reward_items,
            "unlocks": reward_unlocks,
            "notes": "已完成" if cleared else None
        }

        # Populate conditions
        conds = []
        for req_key, required_qty in q_data.get("turn_in", {}).items():
            if req_key.startswith("flag:"):
                flag_key = req_key.split(":", 1)[1]
                flag_val = state.get("flags", {}).get(flag_key)
                met = bool(flag_val)
                label = f"完成事件：{flag_key}"
                if flag_key == "boss_glen_defeated":
                    label = "擊敗山寨頭目葛倫"
                conds.append({
                    "id": f"condition_{q_id}_{flag_key}",
                    "condition_type": "flag_set",
                    "label": label,
                    "required_value": "達成",
                    "current_value": "已達成" if met else "未達成",
                    "status": "met" if met else ("not_applicable" if cleared else "missing"),
                    "status_label": "已滿足" if met else "未滿足",
                    "status_icon_id": "met" if met else "missing",
                    "source": "runtime"
                })
            else:
                owned_qty = state.get("inventory", {}).get(req_key, 0)
                met = owned_qty >= required_qty
                conds.append({
                    "id": f"condition_{q_id}_{req_key}",
                    "condition_type": "turn_in_item",
                    "label": f"交付 {item_name(req_key)}",
                    "required_value": f"x{required_qty}",
                    "current_value": f"x{owned_qty}",
                    "status": "met" if met else ("not_applicable" if cleared else "missing"),
                    "status_label": "已滿足" if met else "未滿足",
                    "status_icon_id": "met" if met else "missing",
                    "source": "runtime"
                })
        condition_rows[q_id] = conds

    all_count = len(task_rows)
    ready_count = sum(1 for row in task_rows if row["status"] == "ready_to_submit")
    completed_count = sum(1 for row in task_rows if row["status"] == "completed")

    task_filters = [
        { "id": "all", "label": "全部委託", "count": all_count, "enabled": True },
        { "id": "ready_to_submit", "label": "可回報", "count": ready_count, "enabled": True },
        { "id": "completed", "label": "已完成", "count": completed_count, "enabled": True }
    ]

    completed_quests = state.get("completed_quests", [])

    if "quest_boss_glen" not in completed_quests:
        glen_sighted = state.get("flags", {}).get("boss_glen_sighted")
        glen_accepted = state.get("flags", {}).get("boss_glen_investigation_accepted")
        glen_defeated = state.get("flags", {}).get("boss_glen_defeated")

        if glen_sighted:
            if not glen_accepted:
                story_hint_card = {
                    "id": "story_hint_boss_glen",
                    "title": "焦石礦坑深處的氣息",
                    "description": "你在焦石礦坑深處感受到一股強烈的氣息。回報工會以調查此事。",
                    "detail_description": "工會接到報告，焦石礦坑深處傳來異樣的震動與粗暴的笑聲，疑似山寨頭目葛倫的蹤跡。接下調查以獲得進一步的作戰地圖指示。",
                    "status": "story_hint",
                    "status_label": "主線線索",
                    "visible": True,
                    "enabled": True,
                    "disabled_reason": None,
                    "primary_action": "accept_boss_glen_investigation",
                    "action_label": "接下調查",
                    "condition_rows": [],
                    "reward_summary": None,
                    "notes": "接下調查後將會開啟正式 Boss 討伐任務。"
                }
            elif not glen_defeated:
                story_hint_card = {
                    "id": "story_hint_boss_glen_accepted",
                    "title": "焦石礦坑深處的氣息 (已接受)",
                    "description": "已確認焦石礦坑深處異常氣息。請回到焦石礦坑最深處挑戰山寨頭目葛倫，奪回被他搶走的「血跡地圖」並帶回工會回報。",
                    "detail_description": "已確認焦石礦坑深處異常氣息。請回到焦石礦坑最深處挑戰山寨頭目葛倫，奪回被他搶走的「血跡地圖」並帶回工會回報，以開啟前往灰燼裂谷的通道。",
                    "status": "story_hint",
                    "status_label": "主線線索",
                    "visible": True,
                    "enabled": False,
                    "disabled_reason": "已確認焦石礦坑深處異常氣息，請回到焦石礦坑最深處挑戰山寨頭目葛倫以取得「血跡地圖」。",
                    "primary_action": "unavailable",
                    "action_label": "調查中",
                    "condition_rows": [],
                    "reward_summary": None,
                    "notes": "請回到焦石礦坑最深處挑戰山寨頭目葛倫以取得「血跡地圖」。"
                }
            else:
                story_hint_card = {
                    "id": "story_hint_boss_glen_defeated",
                    "title": "山寨頭目葛倫已被擊敗",
                    "description": "你已成功擊敗山寨頭目葛倫並取得「血跡地圖」。請向工會提交以完成委託。",
                    "detail_description": "山寨頭目葛倫已被擊敗！請在右側的委託板上選擇「血跡地圖」任務並點擊「回報委託」，交回血跡地圖以解鎖前往灰燼裂谷的通道。",
                    "status": "story_hint",
                    "status_label": "主線線索",
                    "visible": True,
                    "enabled": False,
                    "disabled_reason": "請在委託清單中選擇「血跡地圖」任務進行回報。",
                    "primary_action": "unavailable",
                    "action_label": "請回報委託",
                    "condition_rows": [],
                    "reward_summary": None,
                    "notes": "提交「血跡地圖」任務後將會開啟前往灰燼裂谷的道路。"
                }
        else:
            story_hint_card = {
                "id": "story_hint_placeholder",
                "title": "目前沒有主線線索",
                "description": "暫無主線線索可詢問。",
                "detail_description": "這不是正式委託，不計入篩選數。",
                "status": "story_hint",
                "status_label": "主線線索",
                "visible": False,
                "enabled": False,
                "disabled_reason": "尚未開放。",
                "primary_action": "unavailable",
                "action_label": "無法使用",
                "condition_rows": [],
                "reward_summary": None
            }
    else:
        if "quest_ash_ravine_scout" not in completed_quests:
            story_hint_card = {
                "id": "story_hint_ash_ravine_unlocked",
                "title": "已解鎖灰燼裂谷通道",
                "description": "已解鎖前往灰燼裂谷的通道。請深入探索並收集特有素材以向工會回報。",
                "detail_description": "已確認血跡地圖的指引，前往灰燼裂谷的通道已開放。請前往世界地圖並探索「灰燼裂谷」進行偵查，收集委託所需的裂谷素材以向工會回報。",
                "status": "story_hint",
                "status_label": "主線進度",
                "visible": True,
                "enabled": False,
                "disabled_reason": "請前往世界地圖並探索灰燼裂谷以進行偵查。",
                "primary_action": "unavailable",
                "action_label": "進行中",
                "condition_rows": [],
                "reward_summary": None,
                "notes": "灰燼裂谷中溫度極高，遇到危險時請適時撤退。"
            }
        elif not state.get("flags", {}).get("ash_guardian_defeated"):
            story_hint_card = {
                "id": "story_hint_ash_guardian",
                "title": "灰燼裂谷終點的異動",
                "description": "灰燼裂谷偵查已登記。最深處傳來強烈震動，似乎有什麼東西甦醒了。",
                "detail_description": "根據你帶回的裂谷灰回報，工會推測裂谷終點的熱流深處有強大的守護者活動。請小隊整頓後再次前往「灰燼裂谷」終點調查並排除威脅，以開啟後續深入的補給路線。",
                "status": "story_hint",
                "status_label": "主線進度",
                "visible": True,
                "enabled": False,
                "disabled_reason": "請前往灰燼裂谷終點調查威脅反應。",
                "primary_action": "unavailable",
                "action_label": "進行中",
                "condition_rows": [],
                "reward_summary": None,
                "notes": "終點存在極具威脅的熱源反應，進入決戰前請準備充足的藥水。"
            }
        elif "quest_supply_upgrade" not in completed_quests:
            story_hint_card = {
                "id": "story_hint_supply_upgrade",
                "title": "工會補給路線升級",
                "description": "裂谷守護者已被討伐。工會正準備升級小隊的物資補給線。",
                "detail_description": "裂谷深處的威脅已清除，工會的補給隊伍現在可以著手擴展路線。請在右側的委託板選擇「補給線升級」，提交所需的工程素材，以開啟前往更深處「燼印深窟」的安全補給。",
                "status": "story_hint",
                "status_label": "主線進度",
                "visible": True,
                "enabled": False,
                "disabled_reason": "請在委託清單中選擇「補給線升級」任務進行回報。",
                "primary_action": "unavailable",
                "action_label": "請回報委託",
                "condition_rows": [],
                "reward_summary": None,
                "notes": "升級補給線能提升後續在極高溫地帶的生存保障。"
            }
        elif "quest_cinder_depths_scout" not in completed_quests:
            story_hint_card = {
                "id": "story_hint_cinder_depths",
                "title": "前往封印深處的偵查",
                "description": "前往燼印深窟的通道已開放。請深入該地帶進行初步偵查。",
                "detail_description": "隨著補給線延伸，工會已標記出通往「燼印深窟」的路徑。請在世界地圖前往該處偵查，帶回當地的礦石標本與結晶碎片以完成工會的深度評估。",
                "status": "story_hint",
                "status_label": "主線進度",
                "visible": True,
                "enabled": False,
                "disabled_reason": "請前往世界地圖並探索燼印深窟以進行偵查。",
                "primary_action": "unavailable",
                "action_label": "進行中",
                "condition_rows": [],
                "reward_summary": None,
                "notes": "該處屬於核心封印區域，請謹慎應對隨時可能發生的暴動。"
            }
        elif not state.get("flags", {}).get("cinder_seal_sentinel_defeated"):
            story_hint_card = {
                "id": "story_hint_cinder_sentinel",
                "title": "深窟封印核心的震動",
                "description": "已登記深窟的偵查報告。封印核心似乎有巨大物體正在甦醒。",
                "detail_description": "工會分析了你帶回的深窟岩石標本，確認底部結界核心的防禦機制已被觸發。請整理裝備，再次前往「燼印深窟」最深處挑戰核心的守護者，以解除當地的火之印記封印。",
                "status": "story_hint",
                "status_label": "主線進度",
                "visible": True,
                "enabled": False,
                "disabled_reason": "請前往燼印深窟終點挑戰核心守護者。",
                "primary_action": "unavailable",
                "action_label": "進行中",
                "condition_rows": [],
                "reward_summary": None,
                "notes": "這是解除該區域核心封印的最後一戰，請準備最精良的裝備。"
            }
        else:
            if game.can_ask_fire_mark_guild_inquiry(state):
                story_hint_card = {
                    "id": "story_hint_fire_mark_guild_inquiry",
                    "title": "火印碎片的疑問",
                    "description": "已收集三枚火之印記碎片。請向工會會長諾亞詢問關於印記碎片的奧秘。",
                    "detail_description": "你收集到了三枚共鳴的火之印記碎片。工會可能有相關的古代記錄，請向會長諾亞詢問這些碎片的來歷。",
                    "status": "story_hint",
                    "status_label": "主線線索",
                    "visible": True,
                    "enabled": True,
                    "disabled_reason": None,
                    "primary_action": "fire_mark_guild_inquiry",
                    "action_label": "詢問諾亞",
                    "condition_rows": [
                        {
                            "id": "cond_fire_mark_shards",
                            "condition_type": "item_requirement",
                            "label": "持有三枚火之印記碎片",
                            "required_value": "3 個",
                            "current_value": f"{state.get('inventory', {}).get('key_fire_mark_shard', 0)} 個",
                            "status": "met",
                            "status_label": "已滿足",
                            "status_icon_id": "met",
                            "source": "runtime"
                        }
                    ],
                    "reward_summary": None,
                    "notes": "詢問完成後將會獲得下一步前往神殿的指引。"
                }
            elif state.get("flags", {}).get("fire_mark_guild_inquiry_done"):
                story_hint_card = {
                    "id": "story_hint_fire_mark_guild_inquiry_done",
                    "title": "前往轉職神殿詢問賽恩",
                    "description": "諾亞建議前往大教堂。請至轉職神殿向賽恩祭司回報與詢問。",
                    "detail_description": "諾亞會長表示工會舊紀錄不足以判讀碎片的真正用途，建議前往神殿。請前往城鎮的「轉職神殿」向賽恩祭司回報，確認印記碎片的奧秘。",
                    "status": "story_hint",
                    "status_label": "主線進度",
                    "visible": True,
                    "enabled": False,
                    "disabled_reason": "請前往轉職神殿向賽恩祭司詢問。",
                    "primary_action": "unavailable",
                    "action_label": "請前往神殿",
                    "condition_rows": [],
                    "reward_summary": None,
                    "notes": "主線進展：詢問大教堂。"
                }
            else:
                story_hint_card = {
                    "id": "story_hint_cinder_seal_completed",
                    "title": "火之印記核心的凝聚",
                    "description": "已擊敗深窟守護者並取得碎片。請前往大教堂報告調查結果。",
                    "detail_description": "你已取得所有共鳴的火之印記碎片！這項重大進展需要神職人員的文獻知識。請小隊前往城鎮的「轉職神殿」向賽恩祭司回報，確認印記的核心狀態。",
                    "status": "story_hint",
                    "status_label": "主線進度",
                    "visible": True,
                    "enabled": False,
                    "disabled_reason": "主線第一幕已全部通關。",
                    "primary_action": "unavailable",
                    "action_label": "已完成",
                    "condition_rows": [],
                    "reward_summary": None,
                    "notes": "工會會長諾亞在此向米菈小隊的卓越冒險致以敬意！"
                }

    feedback_message = {
        "tone": "info",
        "speaker": "莉娜",
        "text": "歡迎來到冒險者工會！如果完成了迷宮探索，請在委託板進行回報登記哦。"
    }

    secondary_actions = [
        {
            "action_id": "back_to_town_hub",
            "label": "返回城鎮",
            "description": "離開工會，回到 Town Hub。",
            "enabled": True,
            "disabled_reason": None,
            "payload": {},
            "visual_role": "secondary"
        }
    ]

    selected_task_id = None
    # default selection: prefer first "ready_to_submit" task, otherwise first task
    ready_tasks = [t["task_id"] for t in task_rows if t["status"] == "ready_to_submit"]
    if ready_tasks:
        selected_task_id = ready_tasks[0]
    elif task_rows:
        selected_task_id = task_rows[0]["task_id"]

    # Calculate sellable materials
    sellable_materials = []
    for m_id, unit_price in game.GUILD_MATERIAL_BUY_PRICES.items():
        qty = state.get("inventory", {}).get(m_id, 0)
        if qty > 0:
            sellable_materials.append({
                "item_id": m_id,
                "title": game.item_name(m_id),
                "owned_count": qty,
                "unit_price": unit_price
            })

    return {
        "screen_id": "facility_guild_screen",
        "facility_id": "guild",
        "title": "冒險者工會 / 委託板 (Live)",
        "subtitle": "登記迷宮探索進度，記錄你的冒險足跡。",
        "npc": {
            "id": "guild_receptionist",
            "name": "莉娜",
            "role": "工會接待員，負責登記迷宮探索回報。"
        },
        "resource_strip": resource_strip(state),
        "task_filters": task_filters,
        "selected_filter_id": "all",
        "selected_task_id": selected_task_id,
        "task_rows": task_rows,
        "story_hint_card": story_hint_card,
        "task_details": task_details,
        "reward_summaries": reward_summaries,
        "condition_rows": condition_rows,
        "feedback_message": feedback_message,
        "secondary_actions": secondary_actions,
        "sellable_materials": sellable_materials
    }
