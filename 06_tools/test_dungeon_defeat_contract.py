"""Focused regression for dungeon defeat settlement."""
from __future__ import annotations

import math
import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
for module_root in (ROOT / "03_engine", ROOT / "04_data"):
    sys.path.insert(0, str(module_root))

from data import JOBS  # noqa: E402
from engine.dungeon import handle_defeat  # noqa: E402
from engine.state import add_item, create_state, get_stats  # noqa: E402


def main() -> None:
    state = create_state("Defeat QA", next(iter(JOBS)))
    add_item(state, "item_potion_s", 1)
    starting_gold = state["gold"]
    starting_potions = state["inventory"]["item_potion_s"]

    with patch("engine.dungeon.render_panel"), patch("engine.dungeon.pause"):
        handle_defeat(state, {"gold": 10, "items": {"item_potion_s": 1}})

    stats = get_stats(state)
    assert state["gold"] == starting_gold - 5
    assert state["inventory"].get("item_potion_s", 0) == starting_potions - 1
    assert state["current_hp"] == max(1, math.ceil(stats["max_hp"] * 0.25))
    assert state["current_mp"] == math.ceil(stats["max_mp"] * 0.25)
    print("dungeon defeat contract ok")


if __name__ == "__main__":
    main()
