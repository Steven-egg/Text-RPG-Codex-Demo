from __future__ import annotations

import os
import sys


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


def clear_screen() -> None:
    os.system("cls" if os.name == "nt" else "clear")
