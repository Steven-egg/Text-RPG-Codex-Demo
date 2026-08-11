from __future__ import annotations

import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
for module_root in (ROOT / "04_data", ROOT / "03_engine", ROOT / "06_tools"):
    module_path = str(module_root)
    if module_path not in sys.path:
        sys.path.insert(0, module_path)

from engine import game  # noqa: E402
import gui_runtime_bridge as bridge  # noqa: E402


def main() -> None:
    original_save_path = game.SAVE_PATH
    original_test_root = bridge.TEST_SAVE_ROOT
    try:
        bridge.TEST_SAVE_ROOT.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=bridge.TEST_SAVE_ROOT) as temporary_directory:
            bridge.TEST_SAVE_ROOT = Path(temporary_directory)
            first_path = bridge.configure_test_profile("ice-entry", reset=True)
            fixture_path = bridge.TEST_PROFILE_ROOT / "ice-entry.json"
            assert first_path.read_bytes() == fixture_path.read_bytes()
            assert game.SAVE_PATH == first_path

            first_path.write_text('{"changed": true}', encoding="utf-8")
            retained_path = bridge.configure_test_profile("ice-entry")
            assert retained_path.read_text(encoding="utf-8") == '{"changed": true}'

            reset_path = bridge.configure_test_profile("ice-entry", reset=True)
            assert reset_path.read_bytes() == fixture_path.read_bytes()
    finally:
        bridge.TEST_SAVE_ROOT = original_test_root
        game.set_save_path(original_save_path)

    print("test save profiles ok")


if __name__ == "__main__":
    main()
