"""Dialogue Template System Prototype for Element Maze.

目的：
- 不把 NPC 對話做成每句 hardcode key。
- 使用「情境模板 + 少量變數」產生短句。
- NPC 對話只講重點：去哪裡、調查什麼、Boss/道具/區域重要提示。
- 任務條件細節，例如素材數量、持有數、等級限制，交給 Quest UI 顯示。

Codex 可參考整合方向：
1. 先把 DIALOGUE_TEMPLATES 搬到 data/dialogue_templates.py 或 json。
2. 在 game.py 需要提示時呼叫 say("guide.investigate", name="火之印記", facility="轉職神殿")。
3. 不急著替換所有 print；先替換 NPC 歡迎、任務引導、Boss 警告、商店歡迎。
"""

from __future__ import annotations

import random
import re
from typing import Any, Mapping

PLACEHOLDER_RE = re.compile(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}")

DIALOGUE_TEMPLATES: dict[str, dict[str, Any]] = {
    "greeting.generic": {
        "label": "一般歡迎語",
        "purpose": "NPC 開場或玩家回到設施時使用。",
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
        "purpose": "提示玩家調查某個重點名稱，並前往某設施。",
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
        "purpose": "提示玩家下一步要去的區域或地城。",
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
        "purpose": "提示玩家去找某個 NPC，不講任務細節。",
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
        "purpose": "只在有重要戰鬥風險時提示玩家。",
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
        "purpose": "提醒玩家某個道具很重要，但不列系統條件。",
        "variables": ["item", "facility"],
        "templates": [
            "{item}先別亂丟，{facility}那邊可能用得上。",
            "如果找到{item}，記得帶去{facility}確認。",
            "{item}看起來不像普通素材，先留著比較好。",
        ],
    },
    "lore.region": {
        "label": "區域世界觀",
        "purpose": "補一點氣氛，不負責交代數量條件。",
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
        "purpose": "NPC 只講任務方向，不重複素材數量與條件。",
        "variables": ["quest", "region"],
        "templates": [
            "{quest}的重點在{region}，先從那裡查起。",
            "這次{quest}不要拖太久，{region}的情況正在變化。",
            "如果要處理{quest}，{region}會是第一個要確認的地方。",
        ],
    },
    "quest.after_clear": {
        "label": "任務完成回應",
        "purpose": "完成任務後的簡短回饋。",
        "variables": ["npc", "quest"],
        "templates": [
            "{npc}：「{quest}完成得不錯。」",
            "{npc}鬆了口氣：「這樣一來，局勢就穩一些了。」",
            "{npc}：「辛苦了，這件事我會登記下來。」",
        ],
    },
    "shop.welcome": {
        "label": "商店歡迎語",
        "purpose": "進入商店時的短句。",
        "variables": ["npc", "facility"],
        "templates": [
            "{npc}把商品排開：「出發前補給一下吧。」",
            "{npc}：「{facility}今天也有新鮮補給。」",
            "{npc}笑著說：「需要什麼就自己看。」",
        ],
    },
    "shop.no_gold": {
        "label": "金幣不足",
        "purpose": "系統式商店訊息，短而清楚。",
        "variables": [],
        "templates": [
            "金幣不足。",
            "錢不夠，先去探索賺點金幣吧。",
            "目前金幣不夠購買這項物品。",
        ],
    },
    "system.save": {
        "label": "存檔訊息",
        "purpose": "系統提示，不需要角色語氣。",
        "variables": [],
        "templates": [
            "已存檔。",
            "存檔完成。",
            "目前進度已保存。",
        ],
    },
    "combat.exp_gain": {
        "label": "獲得經驗",
        "purpose": "戰鬥結果摘要。",
        "variables": ["amount"],
        "templates": [
            "獲得經驗 {amount}。",
            "戰鬥經驗 +{amount}。",
            "累積了 {amount} 點經驗。",
        ],
    },
}

DEFAULT_CONTEXT: dict[str, Any] = {
    "player": "見習冒險者",
    "npc": "諾亞",
    "facility": "轉職神殿",
    "region": "灰燼裂谷",
    "name": "火之印記",
    "boss": "灰燼守衛",
    "item": "火之印記碎片",
    "quest": "裂谷偵查委託",
    "amount": 42,
}


def placeholders(template: str) -> set[str]:
    """Return variable names required by a template."""
    return set(PLACEHOLDER_RE.findall(template))


class SafeFormatDict(dict):
    """Leave missing placeholders visible instead of crashing."""

    def __missing__(self, key: str) -> str:
        return "{" + key + "}"


def render_template(template: str, context: Mapping[str, Any]) -> str:
    """Render one template string with safe fallback for missing variables."""
    return template.format_map(SafeFormatDict(context))


def say(key: str, *, rng: random.Random | None = None, **context: Any) -> str:
    """Pick a random template group and render it.

    Example:
        say("guide.investigate", name="火之印記", facility="轉職神殿")
    """
    rng = rng or random
    group = DIALOGUE_TEMPLATES.get(key)
    if not group:
        return f"{{missing dialogue template: {key}}}"
    templates = group.get("templates") or []
    if not templates:
        return f"{{empty dialogue template: {key}}}"
    merged = {**DEFAULT_CONTEXT, **context}
    return render_template(rng.choice(templates), merged)


def demo() -> None:
    rng = random.Random(7)
    examples = [
        ("greeting.generic", {}),
        ("guide.investigate", {"name": "火之印記", "facility": "轉職神殿"}),
        ("guide.go_region", {"region": "燼印深窟"}),
        ("warning.boss", {"boss": "燼印鎮衛", "region": "燼印深窟"}),
        ("quest.brief", {"quest": "補給線升級", "region": "灰燼裂谷"}),
        ("shop.welcome", {"npc": "拉比", "facility": "旅人小鋪"}),
        ("combat.exp_gain", {"amount": 120}),
    ]
    for key, ctx in examples:
        print(f"[{key}] {say(key, rng=rng, **ctx)}")


if __name__ == "__main__":
    demo()
