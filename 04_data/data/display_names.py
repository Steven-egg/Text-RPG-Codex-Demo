from __future__ import annotations


CORE_NPC_KEYS = (
    "noah",
    "rabi",
    "eve",
    "gray",
    "bryn",
    "mira",
    "sion",
    "innkeeper",
)


CORE_FACILITY_KEYS = (
    "guild",
    "weapon_workshop",
    "armor_workshop",
    "shop",
    "synthesis",
    "magic_shop",
    "temple",
    "relic",
    "storage",
    "inn",
)


NPC_DISPLAY_NAMES = {
    "border_fire": {
        "noah": "諾亞",
        "rabi": "拉比",
        "eve": "伊芙",
        "gray": "格雷",
        "bryn": "布琳",
        "mira": "米菈",
        "sion": "賽恩",
        "innkeeper": "旅館老闆",
    },
    "ice": {
        "noah": "諾亞",
        "rabi": "拉比",
        "eve": "伊芙",
        "gray": "格雷",
        "bryn": "布琳",
        "mira": "米菈",
        "sion": "賽恩",
        "innkeeper": "霜潮旅店掌櫃",
    },
    "earth": {
        "noah": "諾亞",
        "rabi": "拉比",
        "eve": "伊芙",
        "gray": "格雷",
        "bryn": "布琳",
        "mira": "米菈",
        "sion": "賽恩",
        "innkeeper": "根環旅店掌櫃",
    },
    "thunder": {
        "noah": "諾亞",
        "rabi": "拉比",
        "eve": "伊芙",
        "gray": "格雷",
        "bryn": "布琳",
        "mira": "米菈",
        "sion": "賽恩",
        "innkeeper": "雷脊旅店掌櫃",
    },
    "final": {
        "noah": "諾亞",
        "rabi": "拉比",
        "eve": "伊芙",
        "gray": "格雷",
        "bryn": "布琳",
        "mira": "米菈",
        "sion": "賽恩",
        "innkeeper": "前線補給官",
    },
}


FACILITY_DISPLAY_NAMES = {
    "border_fire": {
        "guild": "冒險者工會",
        "weapon_workshop": "鐵刃工坊",
        "armor_workshop": "堅甲工坊",
        "shop": "旅人小鋪",
        "synthesis": "米菈合成屋",
        "magic_shop": "星燈魔法商店",
        "temple": "轉職神殿",
        "relic": "聖物調查",
        "storage": "倉庫",
        "inn": "旅館",
    },
    "ice": {
        "guild": "霜潮工會聯絡所",
        "weapon_workshop": "霜鐵工坊",
        "armor_workshop": "鹽霧護具鋪",
        "shop": "寒港補給鋪",
        "synthesis": "霜潮合成台",
        "magic_shop": "冰燈魔法商店",
        "temple": "霜碑神殿",
        "relic": "冰印調查台",
        "storage": "港口倉庫",
        "inn": "霜潮旅店",
    },
    "earth": {
        "guild": "根環工會聯絡所",
        "weapon_workshop": "石根工坊",
        "armor_workshop": "藤甲護具鋪",
        "shop": "林環補給鋪",
        "synthesis": "根脈合成台",
        "magic_shop": "苔光魔法商店",
        "temple": "古根神殿",
        "relic": "地印調查台",
        "storage": "林環倉庫",
        "inn": "根環旅店",
    },
    "thunder": {
        "guild": "雷脊工會聯絡所",
        "weapon_workshop": "導雷工坊",
        "armor_workshop": "雲銅護具鋪",
        "shop": "雷脊補給鋪",
        "synthesis": "雷玻合成台",
        "magic_shop": "鳴塔魔法商店",
        "temple": "雷碑神殿",
        "relic": "雷印調查台",
        "storage": "雷脊倉庫",
        "inn": "雷脊旅店",
    },
    "final": {
        "guild": "前線工會指揮所",
        "weapon_workshop": "終門武備所",
        "armor_workshop": "終門護具所",
        "shop": "前線補給站",
        "synthesis": "封核合成台",
        "magic_shop": "終門魔法書庫",
        "temple": "四印祈禱所",
        "relic": "四印調查台",
        "storage": "前線倉庫",
        "inn": "前線休息棚",
    },
}


FACILITY_SHORT_DESCRIPTIONS = {
    "border_fire": {
        "guild": "諾亞從一堆文件中抬頭，對你點了點頭。",
        "weapon_workshop": "格雷把新磨好的鐵刃放回架上。",
        "armor_workshop": "布琳敲了敲護甲邊緣，確認鉚釘穩固。",
        "shop": "拉比把補給袋推到櫃台前。",
        "synthesis": "米菈整理著素材瓶，等你挑選配方。",
        "magic_shop": "伊芙翻開星燈旁的魔法書目錄。",
        "temple": "賽恩站在門前，像一塊懂得呼吸的石碑。",
        "relic": "聖物調查台安靜地映出四元素的微光。",
        "storage": "工會旁的小倉庫掛著新銅鎖。",
        "inn": "旅館老闆擦著木杯，示意你可以休息。",
    },
    "ice": {
        "guild": "霜潮的海霧滲進工會聯絡所，桌上的委託紙邊緣微微捲起。",
        "weapon_workshop": "霜鐵在爐中泛著冷藍色光。",
        "armor_workshop": "鹽霧護具鋪掛滿防寒披肩與硬皮甲。",
        "shop": "寒港補給鋪準備著長途航行用的乾糧與藥水。",
        "synthesis": "霜潮合成台旁堆著鹽布、浮木與藍石。",
        "magic_shop": "冰燈照亮潮濕的書頁。",
        "temple": "霜碑神殿的石牆覆著薄薄白霜。",
        "relic": "冰印調查台映出霜潮與沉船的輪廓。",
        "storage": "港口倉庫裡傳來繩索收緊的聲音。",
        "inn": "霜潮旅店的爐火把濕冷空氣烘得稍微柔和。",
    },
    "earth": {
        "guild": "根環的工會聯絡所被樹根環抱，委託板散著潮土氣味。",
        "weapon_workshop": "石根工坊的鐵砧下壓著古老礦石。",
        "armor_workshop": "藤甲護具鋪把皮革與藤片編成護甲。",
        "shop": "林環補給鋪擺著乾燥草藥與清水囊。",
        "synthesis": "根脈合成台的紋路像活著的年輪。",
        "magic_shop": "苔光魔法商店的書架間浮著柔綠微光。",
        "temple": "古根神殿的石柱被苔與細根覆蓋。",
        "relic": "地印調查台低低震動，像遠處地脈的回聲。",
        "storage": "林環倉庫被厚木門與藤索固定。",
        "inn": "根環旅店飄著草藥湯與木柴香。",
    },
    "thunder": {
        "guild": "雷脊工會聯絡所的銅線在風中輕鳴。",
        "weapon_workshop": "導雷工坊的工具旁閃過細小電弧。",
        "armor_workshop": "雲銅護具鋪檢查著每一片絕緣襯料。",
        "shop": "雷脊補給鋪把防滑繩與藥水排成一列。",
        "synthesis": "雷玻合成台內有亮白光點一閃一閃。",
        "magic_shop": "鳴塔魔法商店的書頁隨著雷聲微震。",
        "temple": "雷碑神殿的石階帶著雨後金屬氣味。",
        "relic": "雷印調查台映出高塔與雲路。",
        "storage": "雷脊倉庫的門閂纏著導電銅線。",
        "inn": "雷脊旅店用厚帆布擋住山風。",
    },
    "final": {
        "guild": "前線工會指揮所的地圖上標著四元素回聲的位置。",
        "weapon_workshop": "終門武備所只留下最可靠的工具與刃具。",
        "armor_workshop": "終門護具所反覆檢查每一件護甲。",
        "shop": "前線補給站把所有物資按撤退路線分箱。",
        "synthesis": "封核合成台的光像被深處的黑暗拉扯。",
        "magic_shop": "終門魔法書庫只開放最必要的卷冊。",
        "temple": "四印祈禱所中，四枚聖印的光彼此呼應。",
        "relic": "四印調查台正對著魔王城方向。",
        "storage": "前線倉庫的每個木箱都寫著歸隊編號。",
        "inn": "前線休息棚短暫隔開遠方的戰鼓聲。",
    },
}


def _regional_lookup(source: dict[str, dict[str, str]], region_id: str, key: str) -> str:
    if region_id in source and key in source[region_id]:
        return source[region_id][key]
    if key in source.get("border_fire", {}):
        return source["border_fire"][key]
    return key


def get_npc_display_name(region_id: str, key: str) -> str:
    return _regional_lookup(NPC_DISPLAY_NAMES, region_id, key)


def get_facility_display_name(region_id: str, key: str) -> str:
    return _regional_lookup(FACILITY_DISPLAY_NAMES, region_id, key)


def get_facility_short_description(region_id: str, key: str) -> str:
    return _regional_lookup(FACILITY_SHORT_DESCRIPTIONS, region_id, key)
