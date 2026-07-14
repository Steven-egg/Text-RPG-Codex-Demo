from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "06_tools" / "relic_passive_playtest.py"
SPEC = importlib.util.spec_from_file_location("relic_passive_playtest", MODULE_PATH)
assert SPEC and SPEC.loader
playtest = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(playtest)


def main() -> None:
    state = playtest.build_playtest_state("cleric", 25)
    assert state["job"] == "牧師"
    assert state["level"] == 25
    assert state["gold"] == 9_999
    assert all(state["flags"].get(flag) for flag in playtest.SEAL_FLAGS)
    assert state["current_hp"] == playtest.get_stats(state)["max_hp"]
    assert state["current_mp"] == playtest.get_stats(state)["max_mp"]
    assert state["inventory"]["item_potion_s"] >= 10
    assert playtest.normalize_job("rogue") == "盜賊"
    try:
        playtest.build_playtest_state("unknown", 25)
    except ValueError:
        pass
    else:
        raise AssertionError("unknown job must be rejected")
    for level in (0, 100):
        try:
            playtest.build_playtest_state("cleric", level)
        except ValueError:
            pass
        else:
            raise AssertionError(f"level {level} must be rejected")
    print("Relic passive playtest seed checks ok!")


if __name__ == "__main__":
    main()
