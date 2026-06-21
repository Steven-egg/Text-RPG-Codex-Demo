from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "04_data"
if str(DATA_ROOT) not in sys.path:
    sys.path.insert(0, str(DATA_ROOT))

try:
    from data import (
        DUNGEONS,
        EQUIPMENT,
        ITEMS,
        MAGIC_BOOKS,
        MATERIALS,
        MONSTERS,
        QUESTS,
        RECIPES,
        RELICS,
    )
except Exception as exc:
    print(f"[ERROR] failed to import data modules: {exc}")
    raise SystemExit(1)

REGION_TOKENS = ["ice", "earth", "thunder", "final", "fire"]

def get_region_of_id(data_id: str) -> str:
    parts = data_id.split("_")
    for token in REGION_TOKENS[:-1]:
        if token in parts:
            return token
    if "fire" in parts or "ash" in parts or "cinder" in parts:
        return "fire"
    if data_id.startswith((
        "mon_moss_", "mon_cave_", "mon_cracked_", "boss_glen", 
        "dungeon_moss_cave", "dungeon_scorched_mine", 
        "quest_cave_gathering", "quest_mine_scout", "quest_boss_glen"
    )):
        return "fire"
    return "shared"

# Expected counts from regional-data-template-v0.1.md
EXPECTED_TEMPLATES = {
    "ice": {
        "dungeons": 4,
        "quests": 5,
        "normal_monsters": 14,
        "bosses": 4,
        "shop_goods": 3,      # HP consumable, MP consumable, local accessory
        "magic_books": 6,
        "recipes": 2,
        "equipment": 7,
        "workshop_upgrades": 4,
    },
    "earth": {
        "dungeons": 4,
        "quests": 5,
        "normal_monsters": 14,
        "bosses": 4,
        "shop_goods": 3,
        "magic_books": 6,
        "recipes": 2,
        "equipment": 7,
        "workshop_upgrades": 4,
    },
    "thunder": {
        "dungeons": 4,
        "quests": 5,
        "normal_monsters": 14,
        "bosses": 4,
        "shop_goods": 3,
        "magic_books": 6,
        "recipes": 2,
        "equipment": 7,
        "workshop_upgrades": 4,
    },
    "final": {
        "dungeons": 4,
        "quests": 5,
        "normal_monsters": 14,
        "bosses": 4,
        "shop_goods": 3,
        "magic_books": 6,
        "recipes": 4,         # Final synthesis has 4 recipes
        "equipment": 7,
        "workshop_upgrades": 6, # Final workshop upgrades is 6
    },
    "fire": {
        "dungeons": 4,
        "quests": 8,
        "normal_monsters": 12,
        "bosses": 3,
        "shop_goods": 0,      # Legacy fire uses default border town shops
        "magic_books": 0,
        "recipes": 0,
        "equipment": 0,
        "workshop_upgrades": 0,
    }
}

def generate_report() -> dict[str, Any]:
    stats = {
        r: {
            "dungeons": [],
            "quests": [],
            "normal_monsters": [],
            "bosses": [],
            "shop_goods": [],
            "magic_books": [],
            "recipes": [],
            "equipment": [],
            "workshop_upgrades": [],
        }
        for r in REGION_TOKENS
    }
    
    # 1. Dungeons
    for d_id in DUNGEONS:
        reg = get_region_of_id(d_id)
        if reg in stats:
            stats[reg]["dungeons"].append(d_id)
            
    # 2. Quests
    for q_id in QUESTS:
        reg = get_region_of_id(q_id)
        if reg in stats:
            stats[reg]["quests"].append(q_id)
            
    # 3. Monsters & Bosses
    for m_id, monster in MONSTERS.items():
        reg = get_region_of_id(m_id)
        if reg in stats:
            if monster.get("boss"):
                stats[reg]["bosses"].append(m_id)
            else:
                stats[reg]["normal_monsters"].append(m_id)
                
    # 4. Shop Goods (Consumables in ITEMS, accessories in EQUIPMENT)
    for i_id, item in ITEMS.items():
        reg = get_region_of_id(i_id)
        if reg in stats and item.get("price", 0) > 0:
            stats[reg]["shop_goods"].append(i_id)
            
    for eq_id, eq in EQUIPMENT.items():
        reg = get_region_of_id(eq_id)
        if reg in stats and eq.get("slot") == "accessory" and eq.get("price", 0) > 0:
            stats[reg]["shop_goods"].append(eq_id)
            
    # 5. Magic Books
    for b_id in MAGIC_BOOKS:
        reg = get_region_of_id(b_id)
        if reg in stats:
            stats[reg]["magic_books"].append(b_id)
            
    # 6. Recipes & Workshop Upgrades
    for r_id, recipe in RECIPES.items():
        reg = get_region_of_id(r_id)
        if reg in stats:
            if recipe.get("base_item"):
                stats[reg]["workshop_upgrades"].append(r_id)
            else:
                stats[reg]["recipes"].append(r_id)
                
    # 7. Equipment (weapons/armors under region, excluding accessories)
    for eq_id, eq in EQUIPMENT.items():
        reg = get_region_of_id(eq_id)
        if reg in stats and eq.get("slot") != "accessory":
            stats[reg]["equipment"].append(eq_id)

    report = {}
    for reg in REGION_TOKENS:
        reg_stats = stats[reg]
        expected = EXPECTED_TEMPLATES.get(reg, {})
        reg_report = {}
        for category, items in reg_stats.items():
            exp_count = expected.get(category, 0)
            act_count = len(items)
            pct = (act_count / exp_count * 100) if exp_count > 0 else 100.0
            reg_report[category] = {
                "actual": act_count,
                "expected": exp_count,
                "percentage": round(pct, 1),
                "items": sorted(items)
            }
        report[reg] = reg_report
        
    return report

def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Region Slot Coverage Report", ""]
    
    for reg in REGION_TOKENS:
        lines.append(f"## Region: {reg.upper()}")
        lines.append("")
        
        headers = ["Slot Category", "Actual Count", "Expected Template", "Coverage %", "Landed IDs"]
        rows = []
        reg_report = report[reg]
        
        total_act = 0
        total_exp = 0
        
        for category, data in reg_report.items():
            act = data["actual"]
            exp = data["expected"]
            pct = f"{data['percentage']}%" if exp > 0 else "-"
            items_str = ", ".join(data["items"][:5])
            if len(data["items"]) > 5:
                items_str += f" (+{len(data['items'])-5} more)"
            rows.append([category, act, exp, pct, items_str or "_None._"])
            
            total_act += act
            total_exp += exp
            
        lines.append(table(headers, rows))
        
        overall_pct = (total_act / total_exp * 100) if total_exp > 0 else 100.0
        lines.append("")
        lines.append(f"**Overall Slot Coverage for {reg.upper()}: {total_act}/{total_exp} ({overall_pct:.1f}%)**")
        lines.append("")
        lines.append("---")
        lines.append("")
        
    return "\n".join(lines)

def table(headers: list[str], rows: list[list[Any]]) -> str:
    if not rows:
        return "_None._"
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        cells = []
        for value in row:
            text = str(value).replace("\n", " ").replace("|", "\\|")
            cells.append(text)
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read-only region slot coverage report.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    report = generate_report()
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(report))

if __name__ == "__main__":
    main()
