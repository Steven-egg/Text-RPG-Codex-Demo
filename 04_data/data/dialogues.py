from __future__ import annotations

from typing import Any


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
