from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
for module_root in (ROOT / "04_data", ROOT / "03_engine"):
    module_path = str(module_root)
    if module_path not in sys.path:
        sys.path.insert(0, module_path)

from engine.game import *  # Re-exported for compatibility with older quick tests.
from engine.game import main


if __name__ == "__main__":
    main()
