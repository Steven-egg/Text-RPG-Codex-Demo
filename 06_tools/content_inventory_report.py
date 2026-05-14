from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_ROOT = ROOT / "04_data"
ENGINE_ROOT = ROOT / "03_engine" / "engine"
if str(DATA_ROOT) not in sys.path:
    sys.path.insert(0, str(DATA_ROOT))

try:
    from data import (
        DUNGEONS,
        EQUIPMENT,
        ITEMS,
        JOB_SPECIALIZATIONS,
        JOBS,
        MAGIC_BOOKS,
        MATERIALS,
        MONSTERS,
        PROMOTIONS,
        QUESTS,
        RECIPES,
        RELICS,
        SHOP_INVENTORY,
        SKILLS,
    )
    from data.registry import (
        ENGINE_EVENT_UNLOCK_KEYS,
        INITIAL_UNLOCK_KEYS,
        KNOWN_FLAG_KEYS,
        STORY_UNLOCK_KEYS,
        SYSTEM_UNLOCK_KEYS,
    )
except Exception as exc:  # pragma: no cover - protects CLI diagnostics.
    print(f"[ERROR] failed to import data modules: {exc}")
    raise SystemExit(1)


FIRE_MARK_TOKENS = (
    "ash",
    "charred",
    "cinder",
    "fire",
    "flame",
    "heat",
    "lava",
    "scorched",
    "warm",
)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


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


def data_counts() -> dict[str, int]:
    return {
        "jobs": len(JOBS),
        "job_specializations": len(JOB_SPECIALIZATIONS),
        "materials": len(MATERIALS),
        "items": len(ITEMS),
        "equipment": len(EQUIPMENT),
        "skills": len(SKILLS),
        "magic_books": len(MAGIC_BOOKS),
        "recipes": len(RECIPES),
        "monsters": len(MONSTERS),
        "bosses": sum(1 for monster in MONSTERS.values() if monster.get("boss")),
        "dungeons": len(DUNGEONS),
        "quests": len(QUESTS),
        "shops": len(SHOP_INVENTORY),
        "promotions": len(PROMOTIONS),
        "relics": len(RELICS),
    }


def grouped_ids(data: dict[str, dict[str, Any]], field: str) -> dict[str, list[str]]:
    groups: dict[str, list[str]] = defaultdict(list)
    for data_id, payload in data.items():
        groups[str(payload.get(field))].append(data_id)
    return dict(sorted(groups.items()))


def all_data_ids() -> set[str]:
    ids = set()
    for data in (
        JOB_SPECIALIZATIONS,
        MATERIALS,
        ITEMS,
        EQUIPMENT,
        SKILLS,
        MAGIC_BOOKS,
        RECIPES,
        MONSTERS,
        DUNGEONS,
        QUESTS,
        PROMOTIONS,
        RELICS,
    ):
        ids.update(data)
    ids.update(KNOWN_FLAG_KEYS)
    ids.update(ENGINE_EVENT_UNLOCK_KEYS)
    ids.update(INITIAL_UNLOCK_KEYS)
    ids.update(STORY_UNLOCK_KEYS)
    ids.update(SYSTEM_UNLOCK_KEYS)
    return ids


def scan_engine_references(ids: set[str]) -> dict[str, list[str]]:
    references: dict[str, list[str]] = defaultdict(list)
    for path in sorted(ENGINE_ROOT.glob("*.py")):
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            lines = path.read_text().splitlines()
        for lineno, line in enumerate(lines, start=1):
            for data_id in ids:
                if data_id in line:
                    references[data_id].append(f"{rel(path)}:{lineno}")
    return dict(sorted(references.items()))


def unlock_maps() -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    producers: dict[str, list[str]] = defaultdict(list)
    consumers: dict[str, list[str]] = defaultdict(list)

    for key in INITIAL_UNLOCK_KEYS:
        producers[key].append("registry.initial")
    for key in ENGINE_EVENT_UNLOCK_KEYS:
        producers[key].append("registry.engine_event")
    for key in STORY_UNLOCK_KEYS:
        producers[key].append("registry.story")
    for key in SYSTEM_UNLOCK_KEYS:
        producers[key].append("registry.system")

    for quest_id, quest in QUESTS.items():
        producers[quest_id].append(f"QUESTS.{quest_id}.completed_quest")
        for key in quest.get("unlocks", []):
            producers[key].append(f"QUESTS.{quest_id}.unlocks")

    for dungeon_id, dungeon in DUNGEONS.items():
        consumers[dungeon.get("unlock")].append(f"DUNGEONS.{dungeon_id}.unlock")

    for item_id, item in ITEMS.items():
        if item.get("unlock"):
            consumers[item["unlock"]].append(f"ITEMS.{item_id}.unlock")

    for equipment_id, equipment in EQUIPMENT.items():
        if equipment.get("unlock"):
            consumers[equipment["unlock"]].append(f"EQUIPMENT.{equipment_id}.unlock")

    for recipe_id, recipe in RECIPES.items():
        consumers[recipe.get("unlock")].append(f"RECIPES.{recipe_id}.unlock")

    for promotion_id, promotion in PROMOTIONS.items():
        for idx, requirement in enumerate(promotion.get("requirements", [])):
            if requirement.get("kind") == "unlock":
                consumers[requirement.get("key")].append(
                    f"PROMOTIONS.{promotion_id}.requirements[{idx}]"
                )

    for relic_id, relic in RELICS.items():
        unlock = relic.get("unlock")
        if unlock and unlock.get("kind") == "unlock":
            consumers[unlock.get("key")].append(f"RELICS.{relic_id}.unlock")

    return dict(sorted(producers.items())), dict(sorted(consumers.items()))


def boss_defeated_flags(boss_id: str) -> list[str]:
    body = boss_id.removeprefix("boss_")
    return sorted(
        flag
        for flag in KNOWN_FLAG_KEYS
        if flag.endswith("_defeated") and (body in flag or boss_id in flag)
    )


def dungeon_rows() -> list[list[Any]]:
    rows = []
    for dungeon_id, dungeon in DUNGEONS.items():
        rows.append(
            [
                dungeon_id,
                dungeon["unlock"],
                len(dungeon["monsters"]),
                len(dungeon["materials"]),
                dungeon.get("boss") or "-",
                "drift" if dungeon["unlock"] != dungeon_id else "same-as-id",
            ]
        )
    return rows


def boss_rows(engine_refs: dict[str, list[str]]) -> list[list[Any]]:
    rows = []
    boss_to_dungeon = {
        dungeon.get("boss"): dungeon_id for dungeon_id, dungeon in DUNGEONS.items() if dungeon.get("boss")
    }
    for boss_id, monster in MONSTERS.items():
        if not monster.get("boss"):
            continue
        rows.append(
            [
                boss_id,
                boss_to_dungeon.get(boss_id, "-"),
                monster["level"],
                len(monster.get("drops", [])),
                ", ".join(boss_defeated_flags(boss_id)) or "-",
                len(engine_refs.get(boss_id, [])),
            ]
        )
    return rows


def quest_rows() -> list[list[Any]]:
    rows = []
    for quest_id, quest in QUESTS.items():
        turn_in = ", ".join(quest.get("turn_in", {}).keys()) or "-"
        unlocks = ", ".join(quest.get("unlocks", [])) or "-"
        self_unlock = "yes" if quest_id in quest.get("unlocks", []) else "no"
        rows.append([quest_id, turn_in, unlocks, self_unlock])
    return rows


def preview_rows() -> list[list[Any]]:
    rows = []
    rows.extend(["promotion", data_id, payload.get("source_job"), payload.get("status")] for data_id, payload in PROMOTIONS.items())
    rows.extend(["job_specialization", data_id, payload.get("source_job"), payload.get("status")] for data_id, payload in JOB_SPECIALIZATIONS.items())
    rows.extend(["relic", data_id, payload.get("unlock", {}).get("key", "-"), payload.get("status")] for data_id, payload in RELICS.items())
    return rows


def fire_mark_related() -> dict[str, list[str]]:
    groups = {
        "materials": MATERIALS,
        "items": ITEMS,
        "equipment": EQUIPMENT,
        "skills": SKILLS,
        "magic_books": MAGIC_BOOKS,
        "recipes": RECIPES,
        "monsters": MONSTERS,
        "dungeons": DUNGEONS,
        "quests": QUESTS,
        "flags": {flag: {} for flag in KNOWN_FLAG_KEYS},
        "relics": RELICS,
        "promotions": PROMOTIONS,
    }
    related = {}
    for group, data in groups.items():
        matched = []
        for data_id, payload in data.items():
            text = f"{data_id} {json.dumps(payload, ensure_ascii=False)}".lower()
            parts = set(re.split(r"[^a-z0-9]+", text))
            if "fire_mark" in text or any(token in parts for token in FIRE_MARK_TOKENS):
                matched.append(data_id)
        related[group] = sorted(matched)
    return related


def naming_findings() -> list[str]:
    findings = []

    key_materials = sorted(data_id for data_id in MATERIALS if data_id.startswith("key_"))
    if key_materials:
        findings.append(f"Key items live in MATERIALS: {', '.join(key_materials)}")

    mixed_dungeon_unlocks = [
        f"{dungeon_id} uses {dungeon['unlock']}"
        for dungeon_id, dungeon in DUNGEONS.items()
        if dungeon["unlock"] != dungeon_id
    ]
    if mixed_dungeon_unlocks:
        findings.append("Dungeon unlock keys are mixed: " + "; ".join(mixed_dungeon_unlocks))

    self_unlocking = [
        quest_id for quest_id, quest in QUESTS.items() if quest_id in quest.get("unlocks", [])
    ]
    if self_unlocking:
        findings.append("Quests self-unlock for display/completion shortcuts: " + ", ".join(self_unlocking))

    equipment_slot_mismatch = []
    for equipment_id, equipment in EQUIPMENT.items():
        slot = equipment["slot"]
        if equipment_id.startswith("armor_") and slot not in {"head", "body"}:
            equipment_slot_mismatch.append(f"{equipment_id} -> {slot}")
        if equipment_id.startswith("acc_") and slot != "accessory":
            equipment_slot_mismatch.append(f"{equipment_id} -> {slot}")
        if equipment_id.startswith("special_") and slot != "special":
            equipment_slot_mismatch.append(f"{equipment_id} -> {slot}")
    if equipment_slot_mismatch:
        findings.append("Equipment id prefixes do not always match slots: " + "; ".join(equipment_slot_mismatch))

    for equipment_id, equipment in EQUIPMENT.items():
        if equipment.get("subtype") == "副武器":
            findings.append(f"Pseudo offhand equipment uses existing slot: {equipment_id} -> {equipment['slot']}")

    story_without_data_consumer = sorted(STORY_UNLOCK_KEYS - set(unlock_maps()[1]))
    if story_without_data_consumer:
        findings.append("Story unlock keys with no data-table consumer: " + ", ".join(story_without_data_consumer))

    return findings


def build_report() -> dict[str, Any]:
    engine_refs = scan_engine_references(all_data_ids())
    unlock_producers, unlock_consumers = unlock_maps()
    produced_keys = set(unlock_producers)
    consumed_keys = set(unlock_consumers)
    produced_without_data_consumer = sorted(
        key
        for key in produced_keys - consumed_keys
        if key not in QUESTS
        if not all(".completed_quest" in source for source in unlock_producers[key])
    )
    completed_quest_without_data_consumer = sorted(
        key
        for key in produced_keys - consumed_keys
        if any(".completed_quest" in source for source in unlock_producers[key])
    )
    return {
        "counts": data_counts(),
        "runtime_tables": [
            "jobs",
            "materials",
            "items",
            "equipment",
            "skills",
            "magic_books",
            "recipes",
            "monsters",
            "dungeons",
            "quests",
            "shop_inventory",
        ],
        "preview_tables": ["promotions", "job_specializations", "relics"],
        "groups": {
            "item_kinds": grouped_ids(ITEMS, "kind"),
            "equipment_slots": grouped_ids(EQUIPMENT, "slot"),
            "skill_kinds": grouped_ids(SKILLS, "kind"),
        },
        "dungeons": dungeon_rows(),
        "bosses": boss_rows(engine_refs),
        "quests": quest_rows(),
        "previews": preview_rows(),
        "unlock_producers": unlock_producers,
        "unlock_consumers": unlock_consumers,
        "produced_without_data_consumer": produced_without_data_consumer,
        "completed_quest_without_data_consumer": completed_quest_without_data_consumer,
        "consumed_without_producer": sorted(consumed_keys - produced_keys),
        "engine_hardcoded_refs": {
            key: refs for key, refs in engine_refs.items() if refs
        },
        "fire_mark_related": fire_mark_related(),
        "naming_findings": naming_findings(),
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Content Inventory Report", ""]

    lines.extend(
        [
            "## Counts",
            "",
            table(["category", "count"], [[key, value] for key, value in report["counts"].items()]),
            "",
            "## Runtime vs Preview",
            "",
            table(
                ["mode", "tables"],
                [
                    ["runtime", ", ".join(report["runtime_tables"])],
                    ["preview-only", ", ".join(report["preview_tables"])],
                ],
            ),
            "",
            "## Data Groups",
            "",
            table(
                ["group", "value", "ids"],
                [
                    [group, value, ", ".join(ids)]
                    for group, values in report["groups"].items()
                    for value, ids in values.items()
                ],
            ),
            "",
            "## Dungeons",
            "",
            table(["id", "unlock", "monster_count", "material_count", "boss", "unlock_style"], report["dungeons"]),
            "",
            "## Bosses",
            "",
            table(["id", "dungeon", "level", "data_drop_count", "defeated_flags", "engine_ref_count"], report["bosses"]),
            "",
            "## Quests",
            "",
            table(["id", "turn_in_keys", "unlocks", "self_unlock"], report["quests"]),
            "",
            "## Preview Content",
            "",
            table(["type", "id", "source_or_unlock", "status"], report["previews"]),
            "",
            "## Unlock Drift",
            "",
            table(
                ["finding", "keys"],
                [
                    ["produced_without_data_consumer", ", ".join(report["produced_without_data_consumer"]) or "-"],
                    [
                        "completed_quest_without_data_consumer",
                        ", ".join(report["completed_quest_without_data_consumer"]) or "-",
                    ],
                    ["consumed_without_producer", ", ".join(report["consumed_without_producer"]) or "-"],
                ],
            ),
            "",
            "## Fire Mark Related IDs",
            "",
            table(
                ["category", "ids"],
                [[category, ", ".join(ids) or "-"] for category, ids in report["fire_mark_related"].items()],
            ),
            "",
            "## Naming And Governance Findings",
            "",
        ]
    )

    findings = report["naming_findings"]
    if findings:
        lines.extend(f"- {finding}" for finding in findings)
    else:
        lines.append("_None._")

    lines.extend(
        [
            "",
            "## Engine Hardcoded ID References",
            "",
            table(
                ["id", "locations"],
                [[data_id, ", ".join(refs[:8])] for data_id, refs in report["engine_hardcoded_refs"].items()],
            ),
            "",
        ]
    )
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Read-only content/data inventory report.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = build_report()
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(report))


if __name__ == "__main__":
    main()
