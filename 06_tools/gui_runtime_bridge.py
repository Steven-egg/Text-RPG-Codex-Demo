from __future__ import annotations

import argparse
import json
import mimetypes
import re
import shutil
import sys
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse


ROOT = Path(__file__).resolve().parents[1]
PROTO_ROOT = ROOT / "07_gui_prototype"

for module_root in (ROOT / "04_data", ROOT / "03_engine"):
    module_path = str(module_root)
    if module_path not in sys.path:
        sys.path.insert(0, module_path)

from engine.gui_actions import GuiActionError, GuiRuntimeSession  # noqa: E402
from engine import game  # noqa: E402


SESSION = GuiRuntimeSession()
TEST_PROFILE_ROOT = ROOT / "06_tools" / "fixtures" / "saves"
TEST_SAVE_ROOT = ROOT / ".test-saves"
PROFILE_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def configure_test_profile(profile_id: str, *, reset: bool = False) -> Path:
    """Activate an isolated mutable copy of a committed test-save fixture."""
    if not PROFILE_ID_PATTERN.fullmatch(profile_id):
        raise ValueError("測試 profile 名稱只能使用小寫英數與連字號。")
    fixture_path = TEST_PROFILE_ROOT / f"{profile_id}.json"
    if not fixture_path.is_file():
        raise ValueError(f"找不到測試 profile：{profile_id}")
    TEST_SAVE_ROOT.mkdir(parents=True, exist_ok=True)
    save_path = TEST_SAVE_ROOT / f"{profile_id}.json"
    if reset or not save_path.exists():
        shutil.copy2(fixture_path, save_path)
    game.set_save_path(save_path)
    return save_path


class GuiRuntimeBridgeHandler(SimpleHTTPRequestHandler):
    server_version = "ElementMazeGuiRuntimeBridge/0.1"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(PROTO_ROOT), **kwargs)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/api/session":
            self.write_json(SESSION.session_info())
            return
        if parsed.path.startswith("/api/screen/"):
            screen_id = unquote(parsed.path.rsplit("/", 1)[-1])
            try:
                screen_model = SESSION.screen_model(screen_id)
                self.write_json(
                    {
                        "ok": True,
                        "status": "success",
                        "screen_model": screen_model,
                        "next_screen_id": screen_model.get("screen_id"),
                    }
                )
            except GuiActionError as error:
                self.write_error_json(
                    error.status,
                    str(error),
                    result_status=error.result_status,
                    blocked_reason=error.blocked_reason,
                )
            return
        if parsed.path == "/":
            self.path = "/start_screen/index.html"
        return super().do_GET()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        try:
            payload = self.read_json()
            if parsed.path == "/api/session/new":
                self.write_json(SESSION.new_game(payload.get("name"), payload.get("job_id")))
                return
            if parsed.path == "/api/session/load":
                self.write_json(SESSION.load_game())
                return
            if parsed.path == "/api/session/demo-seed":
                self.write_json(SESSION.load_demo_seed())
                return
            if parsed.path == "/api/save":
                self.write_json(SESSION.save_game())
                return
            if parsed.path == "/api/action":
                action_id = str(payload.get("action_id", ""))
                action_payload = payload.get("payload") if isinstance(payload.get("payload"), dict) else {}
                screen_id = payload.get("screen_id")
                self.write_json(SESSION.dispatch(action_id, action_payload, screen_id=screen_id))
                return
            self.write_error_json(HTTPStatus.NOT_FOUND, "Unknown API endpoint.")
        except GuiActionError as error:
            self.write_error_json(
                error.status,
                str(error),
                result_status=error.result_status,
                blocked_reason=error.blocked_reason,
            )
        except json.JSONDecodeError:
            self.write_error_json(HTTPStatus.BAD_REQUEST, "Invalid JSON payload.")

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def guess_type(self, path: str) -> str:
        if path.endswith(".js"):
            return "text/javascript"
        return mimetypes.guess_type(path)[0] or "application/octet-stream"

    def read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        raw = self.rfile.read(length).decode("utf-8")
        data = json.loads(raw)
        return data if isinstance(data, dict) else {}

    def write_json(self, data: dict, status: int | HTTPStatus = HTTPStatus.OK) -> None:
        encoded = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(int(status))
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def write_error_json(
        self,
        status: int | HTTPStatus,
        message: str,
        *,
        result_status: str | None = None,
        blocked_reason: str | None = None,
    ) -> None:
        status_code = int(status)
        response_status = result_status or ("blocked" if status_code in {403, 409} else "error")
        data = {
            "ok": False,
            "status": response_status,
            "error": message,
        }
        if response_status == "blocked":
            data["blocked_reason"] = blocked_reason or message
        self.write_json(data, status=status)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Serve GUI prototype files with a local runtime bridge API.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8010)
    parser.add_argument(
        "--test-profile",
        metavar="PROFILE",
        help="載入 06_tools/fixtures/saves 的測試 profile，進度會寫入 .test-saves。",
    )
    parser.add_argument(
        "--reset-test-profile",
        action="store_true",
        help="啟動時以 fixture 重設指定的測試 profile。",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.reset_test_profile and not args.test_profile:
        raise SystemExit("--reset-test-profile 必須與 --test-profile 一起使用。")
    if args.test_profile:
        try:
            test_save_path = configure_test_profile(args.test_profile, reset=args.reset_test_profile)
        except ValueError as error:
            raise SystemExit(str(error)) from error
    else:
        test_save_path = None
    if not PROTO_ROOT.exists():
        raise SystemExit(f"Prototype root not found: {PROTO_ROOT}")
    server = ThreadingHTTPServer((args.host, args.port), GuiRuntimeBridgeHandler)
    print("Element Maze GUI runtime bridge")
    print(f"Static root: {PROTO_ROOT}")
    print(f"Start URL: http://{args.host}:{args.port}/start_screen/index.html?mode=live")
    if test_save_path is not None:
        print(f"Test profile save: {test_save_path}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping GUI runtime bridge.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
