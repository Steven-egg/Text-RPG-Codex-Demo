from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
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
        SKILLS,
    )
except Exception as exc:  # pragma: no cover - protects CLI diagnostics.
    print(f"[ERROR] failed to import data modules: {exc}")
    raise SystemExit(1)


REGION_TOKENS = ("fire", "ice", "earth", "thunder", "final")

MONSTER_TYPE_TERMS: dict[str, tuple[str, ...]] = {
    "fae": ("小妖", "妖精", "花妖", "蕈妖", "葉妖"),
    "humanoid": ("者", "兵", "騎", "祭司", "法師", "船員", "弩手", "水手", "斥候"),
    "lost_oath": ("失誓", "誓騎", "誓者", "封根"),
    "plant_fungus": ("根", "樹", "藤", "孢", "菌", "蕈", "花", "苔"),
    "serpent": ("蛇", "蟒", "王蛇", "羽蛇", "蛇龍"),
    "beast": ("鼠", "犬", "豬", "熊", "蟹", "蝠", "獸", "獵蛛"),
    "spirit_undead": ("靈", "魂", "幽", "亡", "魄", "影"),
    "construct_stone": ("魔像", "石像", "石衛", "石僕", "晶童", "巨像", "偶"),
    "guard_role": ("守衛", "禁衛", "衛", "守", "看守", "守望"),
}

MATERIAL_OBJECT_TERMS: tuple[str, ...] = (
    "核心",
    "晶核",
    "靈核",
    "礦心",
    "囊",
    "根瘤",
    "根髓",
    "樹脂",
    "種子",
    "之種",
    "汁液",
    "莓",
    "琥珀",
    "碎晶",
    "晶片",
    "印片",
    "碎片",
    "片",
    "粉",
    "土",
    "纖維",
    "石",
)

WATCH_SUFFIXES: tuple[str, ...] = (
    "者",
    "衛",
    "靈",
    "妖",
    "小妖",
    "花妖",
    "精",
    "姬",
    "祭司",
    "騎",
    "蛇",
    "蟒",
    "王蛇",
    "魄",
    "僕",
    "童",
    "群",
    "獸",
    "蝠",
    "鼠",
    "兵",
    "法師",
    "巨像",
)

MATERIAL_RISK_TERMS: dict[str, str] = {
    "土": "土/粉/纖維類較像採集原料；若由怪物掉落，建議確認來源畫面感。",
    "粉": "土/粉/纖維類較像採集原料；若由怪物掉落，建議確認來源畫面感。",
    "纖維": "土/粉/纖維類較像採集原料；若由怪物掉落，建議確認來源畫面感。",
}


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


def region_from_id(data_id: str) -> str:
    parts = data_id.split("_")
    for token in REGION_TOKENS:
        if token in parts:
            return token
    if data_id.startswith(("mon_moss_", "mon_cave_", "mon_cracked_", "boss_glen")):
        return "fire"
    return "shared"


def include_region(data_id: str, selected_region: str | None) -> bool:
    if not selected_region:
        return True
    return region_from_id(data_id) == selected_region


def display_records(selected_region: str | None) -> dict[str, list[dict[str, str]]]:
    records: dict[str, list[dict[str, str]]] = {
        "dungeons": [],
        "monsters": [],
        "bosses": [],
        "materials": [],
        "quests": [],
        "items": [],
        "equipment": [],
        "skills": [],
        "magic_books": [],
    }

    for data_id, payload in DUNGEONS.items():
        if include_region(data_id, selected_region):
            records["dungeons"].append({"id": data_id, "name": payload["name"]})

    for data_id, payload in MONSTERS.items():
        if include_region(data_id, selected_region):
            bucket = "bosses" if payload.get("boss") else "monsters"
            records[bucket].append({"id": data_id, "name": payload["name"]})

    for data_id, name in MATERIALS.items():
        if include_region(data_id, selected_region):
            records["materials"].append({"id": data_id, "name": name})

    for data_id, payload in QUESTS.items():
        if include_region(data_id, selected_region):
            records["quests"].append(
                {"id": data_id, "name": payload["title"], "desc": payload["desc"]}
            )

    if not selected_region:
        for data_id, payload in ITEMS.items():
            records["items"].append({"id": data_id, "name": payload["name"], "desc": payload["desc"]})
        for data_id, payload in EQUIPMENT.items():
            records["equipment"].append(
                {"id": data_id, "name": payload["name"], "desc": payload["desc"]}
            )
        for data_id, payload in SKILLS.items():
            records["skills"].append({"id": data_id, "name": payload["name"], "desc": payload["desc"]})
        for data_id, payload in MAGIC_BOOKS.items():
            records["magic_books"].append({"id": data_id, "name": payload["name"]})

    return records


def suffix_hits(names: list[str], suffixes: tuple[str, ...]) -> list[dict[str, Any]]:
    counts: Counter[str] = Counter()
    examples: dict[str, list[str]] = defaultdict(list)
    for name in names:
        for suffix in suffixes:
            if name.endswith(suffix):
                counts[suffix] += 1
                if len(examples[suffix]) < 6:
                    examples[suffix].append(name)
    return [
        {"suffix": suffix, "count": count, "examples": examples[suffix]}
        for suffix, count in counts.most_common()
    ]


def term_hits(names: list[str], terms: tuple[str, ...]) -> list[dict[str, Any]]:
    counts: Counter[str] = Counter()
    examples: dict[str, list[str]] = defaultdict(list)
    for name in names:
        for term in terms:
            if term in name:
                counts[term] += 1
                if len(examples[term]) < 6:
                    examples[term].append(name)
    return [
        {"term": term, "count": count, "examples": examples[term]}
        for term, count in counts.most_common()
    ]


def monster_type_hits(monster_records: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows = []
    for group, terms in MONSTER_TYPE_TERMS.items():
        matched = []
        for record in monster_records:
            name = record["name"]
            if any(term in name for term in terms):
                matched.append(f"{record['id']}:{name}")
        rows.append({"group": group, "count": len(matched), "examples": matched[:8]})
    return rows


def duplicate_names(records: dict[str, list[dict[str, str]]]) -> list[dict[str, Any]]:
    buckets: dict[str, list[str]] = defaultdict(list)
    for category, items in records.items():
        for item in items:
            buckets[item["name"]].append(f"{category}.{item['id']}")
    return [
        {"name": name, "locations": locations}
        for name, locations in sorted(buckets.items())
        if len(locations) > 1
    ]


def check_region_id_drift() -> list[str]:
    drifts = []
    region_tokens = ["ice", "earth", "thunder", "final"]

    # 1. Check dungeon element vs ID
    for dungeon_id, dungeon in DUNGEONS.items():
        element = dungeon.get("element", "").lower()
        for r in region_tokens:
            if element == r:
                expected_prefix = f"dungeon_{r}_"
                if not dungeon_id.startswith(expected_prefix):
                    drifts.append(f"Dungeon `{dungeon_id}` has element `{dungeon.get('element')}` but ID does not start with `{expected_prefix}`")

    # 2. Check monster element vs ID
    for monster_id, monster in MONSTERS.items():
        element = monster.get("element", "").lower()
        for r in region_tokens:
            if element == r:
                if monster.get("boss"):
                    expected_prefix = f"boss_{r}_"
                else:
                    expected_prefix = f"mon_{r}_"
                if not monster_id.startswith(expected_prefix):
                    drifts.append(f"Monster `{monster_id}` (boss={monster.get('boss')}) has element `{monster.get('element')}` but ID does not start with `{expected_prefix}`")

    # 3. Check ID pattern for anything containing region tokens
    tables = [
        ("dungeon", DUNGEONS),
        ("quest", QUESTS),
        ("mon", {k: v for k, v in MONSTERS.items() if not v.get("boss")}),
        ("boss", {k: v for k, v in MONSTERS.items() if v.get("boss")}),
        ("mat", MATERIALS),
        ("recipe", RECIPES),
        ("book", MAGIC_BOOKS),
        ("eq", EQUIPMENT),
        ("skill", SKILLS),
    ]

    for prefix, data in tables:
        for data_id in data:
            parts = data_id.split("_")
            found_regions = [r for r in region_tokens if r in parts]
            if not found_regions:
                continue

            allowed_prefixes = [prefix]
            if prefix == "eq":
                allowed_prefixes = ["weapon", "armor", "acc", "special"]
            elif prefix == "mat":
                allowed_prefixes = ["mat", "key"]

            matched = False
            for r in found_regions:
                for p in allowed_prefixes:
                    if data_id.startswith(f"{p}_{r}_"):
                        matched = True
                        break
                if matched:
                    break

            if not matched:
                drifts.append(f"ID `{data_id}` contains region tokens {found_regions} but does not match pattern `prefix_region_*` for any of them")
    return drifts


def naming_warnings(records: dict[str, list[dict[str, str]]]) -> list[str]:
    warnings = []

    monster_names = [record["name"] for record in records["monsters"]]
    for row in suffix_hits(monster_names, WATCH_SUFFIXES):
        if row["count"] >= 3:
            warnings.append(
                f"Monster suffix `{row['suffix']}` appears {row['count']} times: "
                + ", ".join(row["examples"])
            )

    material_names = [record["name"] for record in records["materials"]]
    for term, message in MATERIAL_RISK_TERMS.items():
        matched = [name for name in material_names if term in name]
        if matched:
            warnings.append(f"Material term `{term}`: {message} Examples: {', '.join(matched[:8])}")

    duplicates = duplicate_names(records)
    if duplicates:
        warnings.append(f"Duplicate display names found: {len(duplicates)}")

    drifts = check_region_id_drift()
    for drift in drifts:
        warnings.append(f"Region ID prefix drift: {drift}")

    return warnings


def build_report(selected_region: str | None) -> dict[str, Any]:
    records = display_records(selected_region)
    monster_records = records["monsters"] + records["bosses"]
    monster_names = [record["name"] for record in monster_records]
    material_names = [record["name"] for record in records["materials"]]

    return {
        "region": selected_region or "all",
        "counts": {category: len(items) for category, items in records.items() if items},
        "monster_suffixes": suffix_hits(monster_names, WATCH_SUFFIXES),
        "monster_type_groups": monster_type_hits(monster_records),
        "material_terms": term_hits(material_names, MATERIAL_OBJECT_TERMS),
        "duplicates": duplicate_names(records),
        "warnings": naming_warnings(records),
    }


def rows_from_hits(items: list[dict[str, Any]], key: str) -> list[list[Any]]:
    return [[item[key], item["count"], ", ".join(item["examples"])] for item in items if item["count"]]


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Naming Inventory Report",
        "",
        f"Region: `{report['region']}`",
        "",
        "## Counts",
        "",
        table(["category", "count"], [[key, value] for key, value in report["counts"].items()]),
        "",
        "## Monster Suffixes",
        "",
        table(["suffix", "count", "examples"], rows_from_hits(report["monster_suffixes"], "suffix")),
        "",
        "## Monster Type Groups",
        "",
        table(
            ["group", "count", "examples"],
            [
                [row["group"], row["count"], ", ".join(row["examples"])]
                for row in report["monster_type_groups"]
                if row["count"]
            ],
        ),
        "",
        "## Material Terms",
        "",
        table(["term", "count", "examples"], rows_from_hits(report["material_terms"], "term")),
        "",
        "## Duplicate Display Names",
        "",
        table(
            ["name", "locations"],
            [[row["name"], ", ".join(row["locations"])] for row in report["duplicates"]],
        ),
        "",
        "## Warnings",
        "",
    ]
    if report["warnings"]:
        lines.extend(f"- {warning}" for warning in report["warnings"])
    else:
        lines.append("_None._")
    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read-only naming inventory report.")
    parser.add_argument(
        "--region",
        choices=REGION_TOKENS,
        help="Limit report to one region inferred from runtime IDs.",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = build_report(args.region)
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(report))


if __name__ == "__main__":
    main()
