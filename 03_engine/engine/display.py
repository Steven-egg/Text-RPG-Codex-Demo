from __future__ import annotations

import os
import sys

try:
    from rich.align import Align
    from rich.console import Console, Group
    from rich.panel import Panel
    from rich.table import Table
    from rich.text import Text
except ImportError:
    Align = None
    Console = None
    Group = None
    Panel = None
    Table = None
    Text = None


_console = Console() if Console is not None else None


def rich_available() -> bool:
    return _console is not None and Group is not None and Panel is not None and Table is not None and Text is not None


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


def _panel_group(lines: list[str]):
    if Group is None or Text is None:
        return None
    body_lines = lines or [""]
    return Group(*(Text(line) for line in body_lines))


def render_panel(panel_title: str, lines: list[str], border_style: str = "cyan") -> None:
    if not rich_available():
        title(panel_title)
        for line in lines:
            print(line)
        return

    _console.print()
    _console.print(
        Panel.fit(
            _panel_group(lines),
            title=panel_title,
            border_style=border_style,
            padding=(1, 2),
        )
    )


def action_menu_panel(
    prompt: str,
    options: list[str],
    panel_title: str,
    header_lines: list[str] | None = None,
    hint_lines: list[str] | None = None,
    allow_back: bool = True,
    border_style: str = "cyan",
) -> int:
    if not rich_available():
        title(panel_title)
        for line in header_lines or []:
            print(line)
        if hint_lines:
            print()
            for line in hint_lines:
                print(f"提示：{line}")
        return menu(prompt, options, allow_back=allow_back)

    table = Table.grid(padding=(0, 2))
    table.add_column(justify="right", style="bold cyan", no_wrap=True)
    table.add_column(style="bright_white")
    for idx, option in enumerate(options, start=1):
        table.add_row(f"{idx}.", option)
    if allow_back:
        table.add_row("0.", "返回")

    body_items = []
    for line in header_lines or []:
        body_items.append(Text(line, style="bold bright_white"))
    if hint_lines:
        if body_items:
            body_items.append(Text(""))
        for line in hint_lines:
            body_items.append(Text(f"提示：{line}", style="yellow"))
    if body_items:
        body_items.append(Text(""))
    body_items.append(table)

    _console.print()
    _console.print(
        Panel.fit(
            Group(*body_items),
            title=panel_title,
            border_style=border_style,
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


def main_menu_panel(
    prompt: str,
    options: list[str],
    player_summary: str,
    allow_back: bool = False,
    hint_lines: list[str] | None = None,
) -> int:
    return action_menu_panel(
        prompt,
        options,
        "主選單",
        header_lines=[player_summary],
        hint_lines=hint_lines,
        allow_back=allow_back,
        border_style="cyan",
    )


def start_screen_panel(has_save: bool) -> int:
    prompt = "選擇行動"
    options = ["重新開始", "載入進度"] if has_save else ["開始新冒險"]
    hint = "偵測到既有存檔。" if has_save else "未偵測到存檔，將建立新角色。"

    clear_screen()
    if not rich_available() or Align is None:
        title("《元素迷宮：邊境冒險者》")
        print("邊境冒險者登入")
        print()
        print(hint)
        return menu(prompt, options, allow_back=False)

    table = Table.grid(padding=(0, 2))
    table.add_column(justify="right", style="bold cyan", no_wrap=True)
    table.add_column(style="bright_white")
    for idx, option in enumerate(options, start=1):
        table.add_row(f"{idx}.", option)

    body = Group(
        Text("《元素迷宮：邊境冒險者》", style="bold bright_white", justify="center"),
        Text("邊境冒險者登入", style="cyan", justify="center"),
        Text(""),
        Text(hint, style="yellow", justify="center"),
        Text(""),
        Align.center(table),
    )
    _console.print(
        Align.center(
            Panel(
                body,
                border_style="cyan",
                padding=(2, 6),
                width=max(54, min(88, _console.size.width - 4)),
            )
        )
    )
    while True:
        raw = input(f"{prompt} > ").strip()
        if raw.isdigit():
            choice = int(raw)
            if 1 <= choice <= len(options):
                return choice
        print("請輸入列表中的數字。")


def save_prompt_panel() -> int:
    prompt = "要讀取舊存檔嗎"
    options = ["讀取存檔", "重新開始"]

    if _console is None or Group is None or Panel is None or Table is None or Text is None:
        title("找到存檔")
        return menu(prompt, options, allow_back=False)

    table = Table.grid(padding=(0, 2))
    table.add_column(justify="right", style="bold cyan", no_wrap=True)
    table.add_column(style="bright_white")
    for idx, option in enumerate(options, start=1):
        table.add_row(f"{idx}.", option)

    body = Group(
        Text("偵測到既有存檔。", style="bold bright_white"),
        Text(""),
        table,
    )
    _console.print()
    _console.print(
        Panel.fit(
            body,
            title="找到存檔",
            border_style="cyan",
            padding=(1, 2),
        )
    )
    while True:
        raw = input(f"{prompt} > ").strip()
        if raw.isdigit():
            choice = int(raw)
            if 1 <= choice <= len(options):
                return choice
        print("請輸入列表中的數字。")


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")
