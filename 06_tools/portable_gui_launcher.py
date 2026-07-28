from __future__ import annotations

import argparse
import posixpath
import threading
import webbrowser
from http import HTTPStatus
from http.server import ThreadingHTTPServer
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

from gui_runtime_bridge import GuiRuntimeBridgeHandler


APP_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = APP_ROOT.parent
PROTO_ROOT = APP_ROOT / "07_gui_prototype"
OVERLAY_ROOT = PACKAGE_ROOT / "assets-overlay" / "app" / "07_gui_prototype"
HOST = "127.0.0.1"
DEFAULT_PORT = 8010
START_PATH = "/start_screen/index.html?mode=live"
IMAGE_SUFFIXES = {".gif", ".jpeg", ".jpg", ".png", ".webp"}


class PortableGuiError(RuntimeError):
    pass


def overlay_path_for_request(path: str) -> Path | None:
    request_path = unquote(urlsplit(path).path)
    if ".." in PurePosixPath(request_path).parts:
        return None
    normalized = posixpath.normpath(request_path).lstrip("/")
    relative = PurePosixPath(normalized)
    if normalized in {"", "."} or ".." in relative.parts:
        return None
    if relative.suffix.casefold() not in IMAGE_SUFFIXES:
        return None
    candidate = (OVERLAY_ROOT / Path(*relative.parts)).resolve()
    try:
        candidate.relative_to(OVERLAY_ROOT.resolve())
    except ValueError:
        return None
    return candidate


class PortableGuiHandler(GuiRuntimeBridgeHandler):
    server_version = "ElementMazePortableGui/1"

    def do_GET(self) -> None:
        if urlsplit(self.path).path == "/favicon.ico":
            self.send_response(HTTPStatus.NO_CONTENT)
            self.end_headers()
            return
        super().do_GET()

    def translate_path(self, path: str) -> str:
        program_path = Path(super().translate_path(path))
        if program_path.is_file():
            return str(program_path)
        overlay_path = overlay_path_for_request(path)
        if overlay_path is not None and overlay_path.is_file():
            return str(overlay_path)
        return str(program_path)


def validate_layout() -> None:
    if not PROTO_ROOT.is_dir():
        raise PortableGuiError(f"GUI program root not found: {PROTO_ROOT}")
    if not (PROTO_ROOT / "start_screen" / "index.html").is_file():
        raise PortableGuiError("portable Start Screen is missing")
    if not OVERLAY_ROOT.is_dir():
        raise PortableGuiError(f"asset overlay not found: {OVERLAY_ROOT}")


def create_server(port: int = DEFAULT_PORT) -> ThreadingHTTPServer:
    validate_layout()
    return ThreadingHTTPServer((HOST, port), PortableGuiHandler)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Launch the portable Element Maze GUI in live runtime mode."
    )
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument(
        "--no-browser",
        action="store_true",
        help="Serve the live GUI without opening the default browser.",
    )
    parser.add_argument(
        "--smoke-test",
        action="store_true",
        help="Validate the portable GUI layout without starting a server.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        validate_layout()
    except PortableGuiError as exc:
        print(f"[ERROR] {exc}")
        return 1
    if args.smoke_test:
        print("[OK] portable GUI layout passed")
        print(f"program root: {PROTO_ROOT}")
        print(f"asset overlay: {OVERLAY_ROOT}")
        print(f"bind host: {HOST}")
        print(f"start path: {START_PATH}")
        return 0

    server = create_server(args.port)
    port = server.server_address[1]
    url = f"http://{HOST}:{port}{START_PATH}"
    print("Element Maze GUI (primary portable entrypoint)")
    print(f"Program root: {PROTO_ROOT}")
    print(f"Asset overlay: {OVERLAY_ROOT}")
    print(f"Start URL: {url}")
    print("Python runtime remains gameplay authority.")
    print("Press Ctrl+C to stop.")
    if not args.no_browser:
        threading.Timer(0.5, webbrowser.open, args=(url,)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping portable GUI runtime bridge.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
