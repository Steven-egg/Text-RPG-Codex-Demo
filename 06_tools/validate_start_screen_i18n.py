from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "07_gui_prototype" / "shared" / "start-screen-locales.json"
PLACEHOLDER_RE = re.compile(r"\{([a-zA-Z0-9_]+)\}")


def main() -> None:
    with CATALOG_PATH.open(encoding="utf-8") as catalog_file:
        catalog = json.load(catalog_file)
    assert set(catalog) == {"zh-Hant", "en"}, "catalog must provide zh-Hant and en"
    base = catalog["zh-Hant"]
    assert isinstance(base, dict) and base, "zh-Hant catalog must be a non-empty object"
    for locale, messages in catalog.items():
        assert isinstance(messages, dict), f"{locale} catalog must be an object"
        missing = sorted(set(base) - set(messages))
        extra = sorted(set(messages) - set(base))
        assert not missing and not extra, f"{locale} key parity failed; missing={missing}, extra={extra}"
        for key in base:
            assert isinstance(base[key], str), f"zh-Hant value for {key} must be a string"
            assert isinstance(messages[key], str), f"{locale} value for {key} must be a string"
            expected = sorted(PLACEHOLDER_RE.findall(base[key]))
            actual = sorted(PLACEHOLDER_RE.findall(messages[key]))
            assert expected == actual, f"{locale} placeholder parity failed for {key}: {actual} != {expected}"
    print("Start Screen i18n catalog: JSON, key parity, and placeholder parity passed.")


if __name__ == "__main__":
    main()
