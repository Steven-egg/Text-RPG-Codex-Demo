from __future__ import annotations

import os
import sys

try:
    from rich.console import Console, Group
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
except ImportError:
    Console = None
    Group = None
    Panel = None
    Table = None
    Text = None


_console = Console() if Console is not None else None


def setup_console() -> None:
    if os.name == "nt":
        os.system("chcp 65001 > nul")
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stdin.reconfigure(encoding="utf-8")
    except Exception:
        pass


def pause() -> None:
    input("\n按 Enter 繼續...")


def title(text: str) -> None:
    print("\n" + "=" * 56)
    print(text)
    print("=" * 56)


def menu(prompt: str, options: list[str], allow_back: bool = True) -> int:
    print()
    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")
    if allow_back:
        print("0. 返回")
    while True:
        raw = input(f"{prompt} > ").strip()
        if allow_back and raw == "0":
            return 0
        if raw.isdigit():
            choice = int(raw)
            if 1 <= choice <= len(options):
                return choice
        print("請輸入列表中的數字。")


def main_menu_panel(
    prompt: str,
    options: list[str],
    player_summary: str,
    allow_back: bool = False,
) -> int:
    if _console is None or Group is None or Panel is None or Table is None or Text is None:
        title("主選單")
        print(player_summary)
        return menu(prompt, options, allow_back=allow_back)

    table = Table.grid(padding=(0, 2))
    table.add_column(justify="right", style="bold cyan", no_wrap=True)
    table.add_column(style="bright_white")
    for idx, option in enumerate(options, start=1):
        table.add_row(f"{idx}.", option)
    if allow_back:
        table.add_row("0.", "返回")

    body = Group(
        Text(player_summary, style="bold bright_white"),
        Text(""),
        table,
    )
    _console.print()
    _console.print(
        Panel.fit(
            body,
            title="主選單",
            border_style="cyan",
            padding=(1, 2),
        )
    )
    while True:
        raw = input(f"{prompt} > ").strip()
        if allow_back and raw == "0":
            return 0
        if raw.isdigit():
            choice = int(raw)
            if 1 <= choice <= len(options):
                return choice
        print("請輸入列表中的數字。")


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")
