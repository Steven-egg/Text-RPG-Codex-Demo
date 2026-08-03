from __future__ import annotations

import random
from typing import Any, Mapping


FACILITY_GREETINGS = {
    "border_fire": {
        "guild": {
            "greeting": "諾亞從一堆文件中抬頭，對你點了點頭。",
            "welcome": "「歡迎回來。想挑戰新目標，還是要交付已完成的委託？」",
        },
        "weapon_workshop": {
            "ambiance": "伴隨著鐵錘敲擊砧台的節奏，這裡充滿了金屬與汗水的硬派氣息。",
            "quote": "葛雷抹了一把汗：「最好的防禦就是進攻。」",
        },
        "armor_workshop": {
            "ambiance": "布琳的手指滑過一排整齊的甲冑。",
            "quote": "「耐用、實惠，品質無可挑剔。每一件都經得起實戰檢驗。」",
        },
        "shop": {
            "welcome": "拉比把補給袋推到櫃台前。",
            "greeting": "「出發前帶上足夠的藥水，永遠不要低估迷宮的危險。」",
        },
        "synthesis": {
            "welcome": "米菈把配方卡排成一列：「先看你想做什麼，再決定要不要動手。」",
        },
        "magic_shop": {
            "welcome": "伊芙輕輕敲了敲書脊：「願星辰指引你的靈魂，冒險者。」",
        },
        "temple": {
            "welcome": "賽恩站在門前，像一塊懂得呼吸的石碑。",
        },
        "storage": {
            "locked": "工會旁的小倉庫還沒整理好，木箱上還掛著新的銅鎖。",
            "unlocked": "小倉庫裡擺放著幾個乾淨的木箱。關鍵道具與安置的印記不會存入此處。",
        },
        "inn": {
            "welcome": "旅店老闆擦亮櫃台上的銅鈴：「睡一晚，明天的路會比較像路。」",
            "reject": "旅館老闆搖搖頭：「先去工會看看有沒有簡單委託吧。」",
        },
    },
    "ice": {
        "guild": {
            "greeting": "霜潮的海霧滲進工會聯絡所，桌上的委託紙邊緣微微捲起。",
            "welcome": "「霜潮港隨時需要人手，看看今天的委託吧。」",
        },
        "weapon_workshop": {
            "ambiance": "伴隨著寒風打擊爐火的碎響，霜鐵在火光中呈現冷藍色的弧光。",
            "quote": "鐵匠將淬火的霜鐵抽出：「冰冷的鋒刃能凍結最狂野的傷口。」",
        },
        "armor_workshop": {
            "ambiance": "防寒披肩與厚皮甲掛在牆上，上面覆著細小的鹽霜。",
            "quote": "「鹽霧會侵蝕金屬，但在這片海岸，堅韌的護甲能救你的命。」",
        },
        "shop": {
            "welcome": "寒港補給鋪準備著長途航行用的乾糧與藥水。",
            "greeting": "「在海上和冰原，凍傷和乾渴一樣致命。多帶點補給吧。」",
        },
        "synthesis": {
            "welcome": "霜潮合成台旁堆著鹽布、浮木與藍石，熔劑在容器裡緩緩起泡。",
        },
        "magic_shop": {
            "welcome": "冰燈照亮潮濕 of 書頁，學徒正細心擦拭卷軸筒。",
        },
        "temple": {
            "welcome": "霜碑神殿的石牆覆著薄薄白霜，祭司低頭為長途冒險祈禱。",
        },
        "storage": {
            "locked": "霜潮港的倉庫被海風吹蝕，厚木門上鎖著一把生鏽的鐵鎖。",
            "unlocked": "海港倉庫裡飄著淡淡的魚腥與海鹽味，空間十分寬敞。",
        },
        "inn": {
            "welcome": "旅店掌櫃撥了撥壁爐裡的炭火：「海上回來的冷氣，只能靠這爐火驅散了。」",
            "reject": "旅館掌櫃抱歉地笑笑：「霜潮港的床位雖然簡陋，但也不能賒帳啊。」",
        },
    },
    "earth": {
        "guild": {
            "greeting": "根環的工會聯絡所被樹根環抱，委託板散著潮土氣味。",
            "welcome": "「大地的根脈指引冒險者，來看看能做些什麼。」",
        },
        "weapon_workshop": {
            "ambiance": "伴隨著地脈深處的悶響，石根工坊的重錘沉穩地敲在厚重的砧板上。",
            "quote": "石根鐵匠敲了敲砧台：「厚實的鐵，就跟腳下的大地一樣可靠。」",
        },
        "armor_workshop": {
            "ambiance": "藤片與厚實皮革的香氣瀰漫，老匠人正細心編織新的護甲。",
            "quote": "「大地的恩賜融入藤木與皮革，能吸收重擊的震動。」",
        },
        "shop": {
            "welcome": "林環補給鋪擺著乾燥草藥與清水囊。",
            "greeting": "「森林的迷宮比想像的更漫長，別讓草藥袋空著。」",
        },
        "synthesis": {
            "welcome": "根脈合成台的紋路像活著的年輪，散發出淡淡的草藥與古木香。",
        },
        "magic_shop": {
            "welcome": "苔光魔法商店的書架間浮著柔綠微光，古老紙卷散發木香。",
        },
        "temple": {
            "welcome": "古根神殿的石柱被苔與細根覆蓋，空氣中瀰漫著古老森林的寧靜。",
        },
        "storage": {
            "locked": "根環營地的倉庫由厚實的巨木板搭成，上面繞著緊繃的藤條鎖扣。",
            "unlocked": "巨木倉庫內部乾燥且陰涼，非常適合存放各種素材。",
        },
        "inn": {
            "welcome": "旅館掌櫃為你倒了一杯熱草藥茶：「大地的寧靜會帶走你骨子裡的疲憊。」",
            "reject": "旅館掌櫃搖了搖頭：「根脈的守護需要相應的報酬，先去賺點旅費吧。」",
        },
    },
    "thunder": {
        "guild": {
            "greeting": "雷脊工會聯絡所的銅線在風中輕鳴。",
            "welcome": "「雷鳴聲中委託不斷，挑選合適的委託吧。」",
        },
        "weapon_workshop": {
            "ambiance": "伴隨著導雷線的微弱嗡鳴，導雷工坊的火花帶著亮白電弧飛濺。",
            "quote": "導雷鐵匠擦拭著錘柄：「將雷電封入鋒刃，每一擊都是天罰。」",
        },
        "armor_workshop": {
            "ambiance": "雲銅護甲與絕緣襯料整齊排列，邊角隱隱有靜電吸附微塵。",
            "quote": "「雲銅能引導多餘的雷能，但你最好確保襯裡乾爽。」",
        },
        "shop": {
            "welcome": "雷脊補給鋪把防滑繩與藥水排成一列。",
            "greeting": "「雷脊的狂風會消耗體力，補給是走下去的唯一保障。」",
        },
        "synthesis": {
            "welcome": "雷玻合成台內有亮白光點一閃一閃，玻璃管道傳導著微弱能量。",
        },
        "magic_shop": {
            "welcome": "鳴塔魔法商店的書頁隨著遠處雷聲微微共鳴微震。",
        },
        "temple": {
            "welcome": "雷碑神殿的石階帶著雨後金屬氣味，高聳的尖塔直指雷雲。",
        },
        "storage": {
            "locked": "雷脊前哨的倉庫表面裝有銅製避雷導線，門鎖上閃爍著微弱電火花。",
            "unlocked": "避雷倉庫的架子裝有防靜電的木襯，確保存放物品的安全。",
        },
        "inn": {
            "welcome": "旅館掌櫃拉緊窗簾擋住雷光：「在雷脊，只有這裡能讓你做個安穩的夢。」",
            "reject": "旅館掌櫃指了指門口：「雷脊前哨不養閒人，先去工會找點活做吧。」",
        },
    },
    "final": {
        "guild": {
            "greeting": "前線工會指揮所的地圖上標著四元素回聲的位置。",
            "welcome": "「前線作戰吃緊，請挑選你能勝任的任務。」",
        },
        "weapon_workshop": {
            "ambiance": "伴隨著隨時準備拔營的緊迫感，終門武備所的熔爐正維持著最後的高溫。",
            "quote": "終門軍械官推開厚重圖紙：「我們只打造能帶你活過明天的武器。」",
        },
        "armor_workshop": {
            "ambiance": "每一件厚重的鋼甲都刻上了軍用編號，工匠正默默加固鉚釘。",
            "quote": "「沒有多餘的裝飾。在這裡，護甲就是你的第二條命。」",
        },
        "shop": {
            "welcome": "前線補給站把所有物資按撤退路線分箱。",
            "greeting": "「物資有限，但我保證這些都是最上等的軍規藥劑。」",
        },
        "synthesis": {
            "welcome": "封核合成台的光像被深處的黑暗拉扯，簡陋但功能完備。",
        },
        "magic_shop": {
            "welcome": "終門魔法書庫只開放最必要的卷冊，暗淡的守護結界在門口運作。",
        },
        "temple": {
            "welcome": "四印祈禱所中，四枚聖印的光彼此呼應，散發著神聖而肅穆的氣壓。",
        },
        "storage": {
            "locked": "前線倉庫是一座由軍隊嚴密看守的木板庫房，只有持有手令才能開啟。",
            "unlocked": "前線倉庫的物資擺放得井井有條，每個架子都有專人看管。",
        },
        "inn": {
            "welcome": "補給官指了指鋪著乾草的床鋪：「抓緊時間睡吧，下一場戰鬥隨時會開始。」",
            "reject": "補給官冷冷地看著你：「物資緊缺，我們沒辦法為沒有貢獻的人提供床位。」",
        },
    },
}


def get_dialogue(region_id: str, facility_id: str, key: str, default: str = "") -> str:
    """Helper to lookup regional facility greetings. Fallback to border_fire if missing."""
    if region_id in FACILITY_GREETINGS:
        facility = FACILITY_GREETINGS[region_id]
        if facility_id in facility:
            if key in facility[facility_id]:
                return facility[facility_id][key]

    if "border_fire" in FACILITY_GREETINGS:
        facility = FACILITY_GREETINGS["border_fire"]
        if facility_id in facility:
            if key in facility[facility_id]:
                return facility[facility_id][key]

    return default


class SafeFormatDict(dict):
    """Leave missing placeholders visible instead of crashing."""
    def __missing__(self, key: str) -> str:
        return "{" + key + "}"

def render_template(template: Any, context: Mapping[str, Any]) -> Any:
    """Render one template string or list of strings with safe fallback."""
    if isinstance(template, list):
        return [t.format_map(SafeFormatDict(context)) for t in template]
    return template.format_map(SafeFormatDict(context))

DEFAULT_CONTEXT: dict[str, Any] = {
    "player": "見習冒險者",
    "job": "冒險者",
    "npc": "諾亞",
    "facility": "轉職神殿",
    "region": "灰燼裂谷",
    "name": "火之印記",
    "boss": "灰燼守衛",
    "item": "火之印記碎片",
    "quest": "裂谷偵查委託",
    "amount": 0,
}

STORY_BEATS: dict[str, dict[str, Any]] = {
    "prologue.new_game": {
        "kind": "prologue",
        "title": "邊境的第一步",
        "lines": [
            "諾亞替{player}別上見習徽章，正式登記為{job}。",
            "元素迷宮的異動正從邊境蔓延，工會需要有人查明源頭。",
            "你的旅程，從火之地的第一份委託開始。",
        ],
        "dismiss_label": "踏上旅程",
        "tone": "neutral",
    },
    "region.enter.ice": {
        "kind": "region_transition",
        "title": "霜潮海岸",
        "lines": [
            "火之聖印在寒風中微微發亮，替你穩住通往北境的航路。",
            "霜潮港外，冰封迷宮正吞沒失去聯絡的船隊。",
            "第二道元素封印，就沉睡在白霧深處。",
        ],
        "dismiss_label": "進入霜潮",
        "tone": "neutral",
    },
    "region.enter.earth": {
        "kind": "region_transition",
        "title": "根環林地",
        "lines": [
            "穿過融雪後的山徑，潮濕土壤傳來低沉而規律的震動。",
            "古樹的根脈封住舊路，也把地底的異常牢牢纏在其中。",
            "大地的封印正在森林最深處等待回應。",
        ],
        "dismiss_label": "踏入林地",
        "tone": "neutral",
    },
    "region.enter.thunder": {
        "kind": "region_transition",
        "title": "雷脊高原",
        "lines": [
            "雲層壓得很低，遠方的導雷塔在暴風中接連熄滅。",
            "每一道雷光都照出通往冠峰的殘破石階。",
            "第四道元素封印，就在風暴中心。",
        ],
        "dismiss_label": "登上雷脊",
        "tone": "warning",
    },
    "region.enter.final": {
        "kind": "region_transition",
        "title": "終門前線",
        "lines": [
            "四枚元素聖印彼此共鳴，終於撐開通往迷宮核心的道路。",
            "前線之外沒有城鎮，只有被黑霧包圍的最後一道門。",
            "魔王與元素迷宮的主封印，都在門後等你。",
        ],
        "dismiss_label": "前往終門",
        "tone": "warning",
    },
    "boss.before.boss_cinder_seal_sentinel": {
        "kind": "boss_before",
        "title": "燼印鎮衛",
        "lines": [
            "三枚火之印記碎片同時發熱，深窟的赤紅刻紋逐一亮起。",
            "鎮衛從封印前站起，拒絕讓未受承認的人再向前一步。",
            "要追查火之印記的真相，必須先證明你能承受它的火焰。",
        ],
        "dismiss_label": "迎戰鎮衛",
        "tone": "warning",
    },
    "boss.after.boss_cinder_seal_sentinel": {
        "kind": "boss_after",
        "title": "三枚火印碎片",
        "lines": [
            "鎮衛的鎧甲化為餘燼，胸口的刻印凝成第三枚碎片。",
            "三枚碎片短暫共鳴，卻還沒有成為完整的聖印。",
            "先帶回工會與神殿，查明這股火焰真正的用途。",
        ],
        "dismiss_label": "帶回碎片",
        "tone": "victory",
    },
    "boss.before.boss_ice_final_seal_lord": {
        "kind": "boss_before",
        "title": "寒封之主",
        "lines": [
            "冰壁後方傳來沉重回音，整座迷宮像在同一次呼吸中凍結。",
            "寒封之主守著失控的冰之核心，不容任何熱量靠近。",
            "只有擊穿這場永冬，霜潮的航路才會重開。",
        ],
        "dismiss_label": "破除寒封",
        "tone": "warning",
    },
    "boss.after.boss_ice_final_seal_lord": {
        "kind": "boss_after",
        "title": "冰印源核",
        "lines": [
            "寒封之主倒下後，冰層的裂紋凝成一枚清澈源核。",
            "失控寒氣暫時退去，但冰之聖印尚未完成安置。",
            "帶著這份印記線索回城，讓工會與神殿確認下一步。",
        ],
        "dismiss_label": "帶回冰核",
        "tone": "victory",
    },
    "boss.before.boss_earth_deep_leyline_lord": {
        "kind": "boss_before",
        "title": "地脈領主",
        "lines": [
            "巨根在你身後閉合，地底脈動化成震耳欲聾的怒吼。",
            "地脈領主盤踞核心，將每一道侵入者的腳步傳遍岩層。",
            "想讓森林恢復呼吸，就得先平息大地的暴走。",
        ],
        "dismiss_label": "平息地脈",
        "tone": "warning",
    },
    "boss.after.boss_earth_deep_leyline_lord": {
        "kind": "boss_after",
        "title": "地脈源核",
        "lines": [
            "領主沉入岩層，狂亂的根脈終於停止收縮。",
            "地脈深處留下沉穩源核，但大地聖印尚未完成安置。",
            "先把這份印記線索帶回城，森林才有機會真正恢復。",
        ],
        "dismiss_label": "帶回地核",
        "tone": "victory",
    },
    "boss.before.boss_thunder_crown_storm_lord": {
        "kind": "boss_before",
        "title": "冠峰風暴領主",
        "lines": [
            "最後一座導雷塔被強光貫穿，冠峰在雷聲中裂開。",
            "風暴領主立於雲海中央，將失序雷霆全部引向你的腳下。",
            "這是抵達終門前，最後一道元素試煉。",
        ],
        "dismiss_label": "穿越風暴",
        "tone": "warning",
    },
    "boss.after.boss_thunder_crown_storm_lord": {
        "kind": "boss_after",
        "title": "雷印源核",
        "lines": [
            "風暴領主消散，積壓已久的雷雲從冠峰兩側退開。",
            "雷光凝成最後一枚源核，但雷之聖印尚未完成安置。",
            "把印記線索帶回城後，四種元素才可能完整共鳴。",
        ],
        "dismiss_label": "帶回雷核",
        "tone": "victory",
    },
    "boss.before.boss_final_demon_king": {
        "kind": "boss_before",
        "title": "魔王御前",
        "lines": [
            "王座前的黑霧凝成身影，四枚聖印同時發出警告。",
            "魔王正以迷宮主封印汲取元素之力，讓所有道路屈從於它。",
            "這一戰將決定迷宮是否再次吞沒艾爾姆。",
        ],
        "dismiss_label": "迎戰魔王",
        "tone": "warning",
    },
    "boss.after.boss_final_demon_king": {
        "kind": "boss_after",
        "title": "王座沉寂",
        "lines": [
            "魔王的身影在四印光芒中崩解，王座上的黑霧不再流動。",
            "迷宮深處仍有回音，但支撐主封印的惡意已經消失。",
            "你終於為艾爾姆爭回一條能夠回家的路。",
        ],
        "dismiss_label": "走向封印",
        "tone": "victory",
    },
    "boss.before.boss_glen": {
        "kind": "boss_before",
        "title": "礦坑深處的守門者",
        "lines": [
            "焦石礦坑的異常源頭現身了：格倫擋在熔岩裂隙前。",
            "你已自動承接調查與討伐，不必返回公會，可立刻挑戰。",
        ],
        "dismiss_label": "準備迎戰",
        "tone": "warning",
    },
    "guidance.promotion_preview": {
        "kind": "region_transition",
        "title": "轉職前瞻",
        "lines": [
            "正式轉職需達 Lv18，並完成 Ice 區域的回報任務。",
            "此處先可查看路線與條件；尚未達成前不會進行轉職。",
        ],
        "dismiss_label": "查看條件",
        "tone": "neutral",
    },
    "guidance.relic_preview": {
        "kind": "region_transition",
        "title": "四元素聖印",
        "lines": [
            "Fire、Ice、Earth、Thunder 聖印記錄主線進度與調查線索。",
            "目前僅提供前瞻，聖印效果尚未實裝，請勿視為戰鬥加成。",
        ],
        "dismiss_label": "查看聖印",
        "tone": "neutral",
    },
    "ending.main_story_clear": {
        "kind": "ending",
        "title": "元素迷宮・主線完成",
        "lines": [
            "灰燼、寒霜、根脈與雷光彼此呼應，重新穩住迷宮的主封印。",
            "迷宮沒有消失，卻不再飢渴地扭曲每一條道路。",
            "{player}回到工會，成為第一位關閉元素迷宮主封印的冒險者。",
            "新的探索仍會開始，但艾爾姆今晚終於能安穩點燈。",
        ],
        "dismiss_label": "返回標題",
        "tone": "ending",
    },
}

DIALOGUE_TEMPLATES: dict[str, dict[str, Any]] = {
    # Generic templates from dialogue_templates_demo.py
    "greeting.generic": {
        "label": "一般歡迎語",
        "variables": ["npc", "player"],
        "templates": [
            "{npc}抬頭看向{player}：「回來了啊。」",
            "{npc}整理著文件：「今天也要出發嗎？」",
            "{npc}點了點頭：「準備好了就開始吧。」",
            "{npc}：「一路辛苦了，有什麼需要就說。」",
        ],
    },
    "guide.investigate": {
        "label": "調查引導",
        "variables": ["name", "facility"],
        "templates": [
            "如果想調查{name}，可以去{facility}看看。",
            "關於{name}，{facility}那邊或許會有線索。",
            "有人建議先到{facility}確認{name}的狀況。",
            "{name}不是一般東西，最好去{facility}問清楚。",
        ],
    },
    "guide.go_region": {
        "label": "前往區域引導",
        "variables": ["region"],
        "templates": [
            "最近{region}不太平靜，可以去看看。",
            "有冒險者從{region}帶回了奇怪的消息。",
            "下一步，應該先確認{region}那邊的狀況。",
            "如果要追線索，{region}會是目前最合理的方向。",
        ],
    },
    "guide.find_npc": {
        "label": "尋找 NPC",
        "variables": ["npc"],
        "templates": [
            "可以去找{npc}問問。",
            "{npc}應該知道一些情況。",
            "這件事，最好先和{npc}確認。",
            "去問問{npc}吧，別自己亂猜。",
        ],
    },
    "warning.boss": {
        "label": "Boss 警告",
        "variables": ["boss", "region"],
        "templates": [
            "聽說{region}深處有個大家伙，名字叫{boss}。",
            "挑戰{boss}之前，最好先把補給準備好。",
            "不少冒險者都在{boss}面前吃過虧。",
            "如果在{region}遇到{boss}，別硬撐。",
        ],
    },
    "warning.item": {
        "label": "重要道具提醒",
        "variables": ["item", "facility"],
        "templates": [
            "{item}先別亂丟，{facility}那邊可能用得上。",
            "如果找到{item}，記得帶去{facility}確認。",
            "{item}看起來不像普通素材，先留著比較好。",
        ],
    },
    "lore.region": {
        "label": "區域世界觀",
        "variables": ["region"],
        "templates": [
            "很久以前，{region}不是現在這個樣子。",
            "關於{region}，老冒險者通常不太願意多談。",
            "{region}的異常，可能比表面看起來更麻煩。",
            "那片{region}，最近連風向都變得奇怪。",
        ],
    },
    "quest.brief": {
        "label": "任務重點提示",
        "variables": ["quest", "region"],
        "templates": [
            "{quest}的重點在{region}，先從那裡查起。",
            "這次{quest}不要拖太久，{region}的情況正在變化。",
            "如果要處理{quest}，{region}會是第一個要確認的地方。",
        ],
    },
    "quest.after_clear": {
        "label": "任務完成回應",
        "variables": ["npc", "quest"],
        "templates": [
            "{npc}：「{quest}完成得不錯。」",
            "{npc}鬆了口氣：「這樣一來，局勢就穩一些了。」",
            "{npc}：「辛苦了，這件事我會登記下來。」",
        ],
    },
    "shop.welcome": {
        "label": "商店歡迎語",
        "variables": ["npc", "facility"],
        "templates": [
            "{npc}把商品排開：「出發前補給一下吧。」",
            "{npc}：「{facility}今天也有新鮮補給。」",
            "{npc}笑著說：「需要什麼就自己看。」",
        ],
    },
    "shop.no_gold": {
        "label": "金幣不足",
        "variables": [],
        "templates": [
            "金幣不足。",
            "錢不夠，先去探索賺點金幣吧。",
            "目前金幣不夠購買這項物品。",
        ],
    },
    "system.save": {
        "label": "存檔訊息",
        "variables": [],
        "templates": [
            "已存檔。",
            "存檔完成。",
            "目前進度已保存。",
        ],
    },
    "combat.exp_gain": {
        "label": "獲得經驗",
        "variables": ["amount"],
        "templates": [
            "獲得經驗 {amount}。",
            "戰鬥經驗 +{amount}。",
            "累積了 {amount} 點經驗。",
        ],
    },

    # Migrated Dungeon Event Templates from cli_helpers.py
    "dungeon.event.material": {
        "label": "找到素材",
        "variables": ["item_name", "qty"],
        "templates": [
            "你找到 {item_name} x{qty}。"
        ],
    },
    "dungeon.event.treasure_gold": {
        "label": "找到金幣寶箱",
        "variables": ["gold"],
        "templates": [
            "你打開一只舊木箱，取得 {gold}G。"
        ],
    },
    "dungeon.event.treasure_item": {
        "label": "找到道具寶箱",
        "variables": ["item_name"],
        "templates": [
            "你找到 {item_name} x1。"
        ],
    },
    "dungeon.event.trap_dodge": {
        "label": "避開陷阱",
        "variables": [],
        "templates": [
            "你察覺地面異樣，及時避開了陷阱。"
        ],
    },
    "dungeon.event.trap_hit_fire": {
        "label": "踩到火陷阱",
        "variables": ["damage"],
        "templates": [
            "熱風從裂縫噴出，你受到 {damage} 點火傷害。"
        ],
    },
    "dungeon.event.trap_hit_default": {
        "label": "踩到一般陷阱",
        "variables": ["damage"],
        "templates": [
            "碎石從腳邊滑落，你受到 {damage} 點傷害。"
        ],
    },
    "dungeon.event.special_moss_cave": {
        "label": "苔石洞窟特殊事件",
        "variables": [],
        "templates": [
            "牆上刻著舊工會標記：別把小魔晶賣掉。你取得小魔晶 x1。"
        ],
    },
    "dungeon.event.special_default_main": {
        "label": "預設特殊事件主提示",
        "variables": [],
        "templates": [
            "你發現有人故意遮住通往深處的舊路標。拉比的情報看來沒錯。"
        ],
    },
    "dungeon.event.special_default_loot": {
        "label": "預設特殊事件取得道具",
        "variables": [],
        "templates": [
            "路標後方還卡著熔岩碎片 x1。"
        ],
    },

    # Migrated Quest Complete Dialogues from cli_helpers.py
    "quest_complete.quest_cave_gathering": {
        "label": "洞窟採集委託完成對話",
        "variables": [],
        "templates": [
            ["米菈合成屋開放了。拉比也整理了新的旅途補給。"]
        ],
    },
    "quest_complete.quest_magic_crystal": {
        "label": "魔晶研究委託完成對話",
        "variables": [],
        "templates": [
            ["伊芙記下小魔晶的光色。火花術書現在折價 50G。"]
        ],
    },
    "quest_complete.quest_mine_scout": {
        "label": "焦石礦坑偵查委託完成對話",
        "variables": [],
        "templates": [
            ["拉比壓低聲音：焦石礦坑深處很熱，抗火斗篷的配方已交給米菈。"]
        ],
    },
    "quest_complete.quest_boss_glen": {
        "label": "葛倫討伐委託完成對話",
        "variables": [],
        "templates": [
            [
                "諾亞看著血跡地圖，表情第一次變得猶豫。第二幕的元素迷宮露出了入口。",
                "下一步很明確：前往「迷宮探索」中的灰燼裂谷，先帶回少量裂谷素材完成偵查。"
            ]
        ],
    },
    "quest_complete.quest_ash_ravine_scout": {
        "label": "灰燼裂谷偵查委託完成對話",
        "variables": [],
        "templates": [
            ["諾亞收起裂谷灰與焦黑鐵片：這些足夠證明灰燼裂谷值得深入調查，但現在還不是挑戰守衛的時候。"]
        ],
    },
    "quest_complete.quest_supply_upgrade": {
        "label": "補給線升級委託完成對話",
        "variables": [],
        "templates": [
            ["諾亞點頭：旅人小鋪已能販售中藥水。接下來的長戰鬥，記得把補給準備好。"]
        ],
    },
    "quest_complete.quest_cinder_depths_scout": {
        "label": "燼印深窟偵查委託完成對話",
        "variables": [],
        "templates": [
            ["諾亞攤開偵查圖：深窟最底層有一座燼印鎮衛。若要第三枚火之印記碎片，只能親自擊敗它。"]
        ],
    },
    # Narrative Story Dialogues
    "prologue.welcome": {
        "label": "開局諾亞致歡迎詞對話",
        "variables": ["player", "job"],
        "templates": [
            "\n諾亞替你別上見習徽章：「歡迎來到艾爾姆，{player}。今天開始，你就是{job}了。」"
        ],
    },
    "quest.fire_mark_guild_inquiry": {
        "label": "詢問三枚印記碎片的事宜",
        "variables": [],
        "templates": [
            [
                "你把三枚火之印記碎片放在諾亞面前。",
                "碎片彼此靠近時，裂紋裡浮起微弱的紅光，像在回應同一個呼吸。",
                "",
                "諾亞仔細翻過工會的舊紀錄，最後搖了搖頭：",
                "「三枚碎片的反應已經很明顯，但工會沒有足夠資料判讀它真正的用途。」",
                "「去教堂問問吧。教會保存的舊文獻，也許能解釋這些印記碎片代表什麼。」",
                "",
                "正式火之印記流程尚未開放；你已記下下一步該詢問教會。"
            ]
        ],
    },
    "quest.fire_mark_church_bridge": {
        "label": "攜帶碎片前往神殿與賽恩對話",
        "variables": [],
        "templates": [
            [
                "賽恩聽完諾亞的轉介，視線落在三枚火之印記碎片上。",
                "碎片的紅光在神殿石階間一明一滅，像是在尋找尚未打開的門。",
                "「工會看不懂它，是因為這不是委託紀錄裡的東西。」賽恩低聲說。",
                "「它不普通，但我還不能斷言它是什麼。我要花點時間查閱舊文獻。」",
                "「先把碎片收好。等我整理出線索，再回神殿找我。」",
                "",
                "你記下賽恩的囑咐：先保管碎片，稍後再回神殿詢問查閱結果。"
            ]
        ],
    },
    "quest.fire_mark_church_lookup": {
        "label": "回到神殿詢問賽恩查閱結果",
        "variables": [],
        "templates": [
            [
                "賽恩把翻開的舊文獻推到石桌中央，頁面上畫著三道分裂的火印。",
                "「查到了。這三枚碎片不是完整的火之印記，而是它尚未完成的核心。」",
                "「它記錄了火的資格，卻還沒有承載力量。現在啟用，只會把印記燒毀。」",
                "",
                "賽恩用封蠟與灰白布帶暫時封住碎片的共鳴，又把它們交還給你。",
                "「去神殿後側的聖物調查台吧。那裡能讓碎片承接成真正的火之聖印。」",
                "",
                "已確認：未完成的火之印記核心。",
                "下一步：前往聖物調查台合成並安置火之聖印。聖印被動效果尚未開放。"
            ]
        ],
    },
    # Facility Lock & Region Lock Warnings
    "facility.synthesis.locked": {
        "label": "合成店鋪鎖定提示",
        "variables": ["mira"],
        "templates": [
            "{mira}的店門半掩著。先完成工會任務「洞窟採集」吧。"
        ],
    },
    "region.locked.ice": {
        "label": "極寒區域鎖定提示",
        "variables": [],
        "templates": [
            "Ice Region unlocks after the Fire Seal route is complete."
        ],
    },
    "region.locked.earth": {
        "label": "大地區域鎖定提示",
        "variables": [],
        "templates": [
            "Earth Region unlocks after completing Ice Region quests."
        ],
    },
    "region.locked.thunder": {
        "label": "雷霆區域鎖定提示",
        "variables": [],
        "templates": [
            "Thunder Region unlocks after completing Earth Region quests."
        ],
    },
    "region.locked.final": {
        "label": "魔王前線鎖定提示",
        "variables": [],
        "templates": [
            "Final Region requires all four enshrined elemental seals."
        ],
    },
    "region.locked.default": {
        "label": "預設區域鎖定提示",
        "variables": [],
        "templates": [
            "This region is locked."
        ],
    },
}

_dialogue_rng = random.Random()


def has_template(key: str) -> bool:
    """Check if a template key exists in the registry."""
    return key in DIALOGUE_TEMPLATES


def say(key: str, *, rng: random.Random | None = None, **context: Any) -> Any:
    """Pick a template, format it, and return the rendered string or list of strings."""
    active_rng = rng or _dialogue_rng
    group = DIALOGUE_TEMPLATES.get(key)
    if not group:
        return f"{{missing dialogue template: {key}}}"
    templates = group.get("templates") or []
    if not templates:
        return f"{{empty dialogue template: {key}}}"
    merged = {**DEFAULT_CONTEXT, **context}
    return render_template(active_rng.choice(templates), merged)
