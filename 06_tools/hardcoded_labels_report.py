from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
ENGINE_ROOT = ROOT / "03_engine" / "engine"

# Regex to capture Chinese characters within single/double quotes, supporting f/r prefixes
CHINESE_STRING_RE = re.compile(
    r'(?:f|r|fr|rf)?'
    r'(?:'
    r'"([^"\n]*[\u4e00-\u9fff]+[^"\n]*)"'
    r'|'
    r'\'([^\'\n]*[\u4e00-\u9fff]+[^\'\n]*)\''
    r')'
)

def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")

def scan_hardcoded_labels() -> dict[str, list[dict[str, Any]]]:
    results = {}
    
    for path in sorted(ENGINE_ROOT.glob("*.py")):
        file_key = rel(path)
        file_results = []
        
        try:
            lines = path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            lines = path.read_text().splitlines()
            
        for lineno, line in enumerate(lines, start=1):
            stripped = line.strip()
            # Skip pure comment lines
            if stripped.startswith("#"):
                continue
                
            # Strip trailing comments if they are not inside string literals
            if "#" in line:
                parts = line.split("#")
                before_comment = parts[0]
                # Simple quote balance check
                if (before_comment.count('"') % 2 == 0) and (before_comment.count("'") % 2 == 0):
                    line_to_scan = before_comment
                else:
                    line_to_scan = line
            else:
                line_to_scan = line
                
            matches = CHINESE_STRING_RE.findall(line_to_scan)
            for m in matches:
                found_str = m[0] if m[0] else m[1]
                if found_str:
                    file_results.append({
                        "line": lineno,
                        "string": found_str.strip(),
                        "code": stripped
                    })
                    
        if file_results:
            results[file_key] = file_results
            
    return results

def render_markdown(results: dict[str, list[dict[str, Any]]]) -> str:
    lines = ["# Hard-coded Chinese Labels Report", ""]
    
    total_count = sum(len(items) for items in results.values())
    lines.append(f"**Total Hard-coded Strings Found: {total_count}** across {len(results)} files.")
    lines.append("")
    
    for file_path, items in results.items():
        lines.append(f"## File: [{file_path.split('/')[-1]}](file:///{ROOT}/{file_path})")
        lines.append(f"Path: `{file_path}` ({len(items)} strings)")
        lines.append("")
        
        headers = ["Line", "Hard-coded Text", "Code Snippet"]
        rows = []
        for item in items:
            code = item["code"]
            if len(code) > 80:
                code = code[:77] + "..."
            rows.append([item["line"], item["string"], f"`{code}`"])
            
        lines.append(table(headers, rows))
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
    parser = argparse.ArgumentParser(description="Read-only hardcoded Chinese labels report.")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    return parser.parse_args()

def main() -> None:
    # Reconfigure stdout to use UTF-8 to prevent encoding errors on Windows cp950 consoles
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        
    args = parse_args()
    results = scan_hardcoded_labels()
    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(results))

if __name__ == "__main__":
    main()
