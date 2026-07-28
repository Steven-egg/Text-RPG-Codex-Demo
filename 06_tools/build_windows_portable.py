from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

import build_release_assets as release_assets


ROOT = Path(__file__).resolve().parents[1]
FORMAT_VERSION = 1
PACKAGE_NAME = "ElementMaze"
ZIP_FILENAME = "ElementMaze-Windows-Portable.zip"
DIST_ROOT = Path("dist")
STAGING_PARENT = DIST_ROOT / "windows-portable"
PACKAGE_RELATIVE = STAGING_PARENT / PACKAGE_NAME
ZIP_RELATIVE = DIST_ROOT / ZIP_FILENAME
ASSET_OUTPUT = Path("dist/assets-overlay")
ASSET_MANIFEST = Path("dist/manifests/assets-manifest.json")
PORTABLE_MANIFEST_NAME = "windows-portable-manifest.json"
GUI_ENTRYPOINT = "啟動 Element Maze GUI.bat"
CLI_ENTRYPOINT = "文字核心版 Text Core.bat"
IMAGE_SUFFIXES = {".gif", ".jpeg", ".jpg", ".png", ".webp"}
GUI_PROGRAM_SUFFIXES = {".css", ".html", ".js", ".json", ".mjs"}
FORBIDDEN_SEGMENTS = {
    ".antigravity",
    ".codex",
    ".git",
    "__pycache__",
    "cache",
    "dist",
    "old",
    "worktrees",
}
FORBIDDEN_NAMES = {"save.json"}
FIXED_ZIP_TIMESTAMP = (1980, 1, 1, 0, 0, 0)


class WindowsPortableError(RuntimeError):
    pass


@dataclass(frozen=True)
class BuildSummary:
    mode: str
    source_revision: str
    program_file_count: int
    asset_file_count: int
    runtime_file_count: int
    release_ready: bool
    package_path: Path | None
    zip_path: Path | None


def relative_posix(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def has_forbidden_segment(path: PurePosixPath | Path) -> bool:
    return any(part.casefold() in FORBIDDEN_SEGMENTS for part in path.parts)


def validate_relative_path(path: str, label: str) -> PurePosixPath:
    if "\\" in path:
        raise WindowsPortableError(f"{label} must use forward slashes: {path}")
    relative = PurePosixPath(path)
    if relative.is_absolute() or not relative.parts or ".." in relative.parts:
        raise WindowsPortableError(f"unsafe {label}: {path}")
    if has_forbidden_segment(relative):
        raise WindowsPortableError(f"forbidden path segment in {label}: {path}")
    if relative.name.casefold() in FORBIDDEN_NAMES:
        raise WindowsPortableError(f"forbidden file in {label}: {path}")
    return relative


def ensure_regular_file(path: Path, label: str) -> None:
    if path.is_symlink():
        raise WindowsPortableError(f"symlinks are not allowed in {label}: {path}")
    if not path.is_file():
        raise WindowsPortableError(f"missing {label}: {path}")


def select_program_sources(root: Path = ROOT) -> tuple[Path, ...]:
    root = root.resolve()
    selected: set[Path] = set()
    fixed = (
        root / "element_maze.py",
        root / "requirements.txt",
        root / "06_tools" / "gui_runtime_bridge.py",
        root / "06_tools" / "portable_gui_launcher.py",
    )
    for path in fixed:
        ensure_regular_file(path, "program source")
        selected.add(path)

    for relative_root in (Path("03_engine/engine"), Path("04_data/data")):
        source_root = root / relative_root
        if not source_root.is_dir():
            raise WindowsPortableError(f"missing runtime source directory: {source_root}")
        for path in source_root.rglob("*.py"):
            if path.is_symlink():
                raise WindowsPortableError(f"symlink in runtime source: {path}")
            relative = path.relative_to(root)
            if not has_forbidden_segment(relative):
                selected.add(path)

    gui_root = root / "07_gui_prototype"
    if not gui_root.is_dir():
        raise WindowsPortableError(f"missing GUI source directory: {gui_root}")
    for path in gui_root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if path.is_symlink():
            raise WindowsPortableError(f"symlink in GUI source: {path}")
        if has_forbidden_segment(relative):
            continue
        if path.name.casefold().endswith(".meta.json"):
            continue
        if path.suffix.casefold() in GUI_PROGRAM_SUFFIXES:
            selected.add(path)

    paths = tuple(sorted(selected, key=lambda path: relative_posix(path, root)))
    if any(path.suffix.casefold() in IMAGE_SUFFIXES for path in paths):
        raise WindowsPortableError("program selection unexpectedly contains an image")
    return paths


def validate_runtime_source(runtime_source: Path) -> tuple[Path, tuple[Path, ...], str]:
    source = runtime_source.resolve()
    if not source.is_dir():
        raise WindowsPortableError(f"runtime source is not a directory: {source}")
    python_exe = source / "python.exe"
    ensure_regular_file(python_exe, "runtime python.exe")
    license_files = tuple(
        sorted(
            (
                path
                for path in source.rglob("*")
                if path.is_file() and path.name.casefold().startswith(("license", "copying"))
            ),
            key=lambda path: relative_posix(path, source),
        )
    )
    if not license_files:
        raise WindowsPortableError("runtime source must include redistributable license material")
    completed = subprocess.run(
        [str(python_exe), "-I", "-c", "import sys; print(sys.version.split()[0])"],
        cwd=source,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        timeout=30,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise WindowsPortableError(f"runtime python.exe is not usable: {detail}")
    version = completed.stdout.strip()
    if not version:
        raise WindowsPortableError("runtime python.exe did not report a version")
    return source, license_files, version


def iter_runtime_files(source: Path) -> Iterable[tuple[Path, PurePosixPath]]:
    for path in sorted(source.rglob("*"), key=lambda item: item.as_posix()):
        if not path.is_file():
            continue
        if path.is_symlink():
            raise WindowsPortableError(f"symlink in runtime source: {path}")
        relative = PurePosixPath(path.relative_to(source).as_posix())
        if has_forbidden_segment(relative):
            continue
        if relative.name.casefold() in FORBIDDEN_NAMES:
            continue
        if relative.suffix.casefold() in IMAGE_SUFFIXES:
            continue
        validate_relative_path(relative.as_posix(), "runtime path")
        yield path, relative


def copy_program_payload(root: Path, app_root: Path) -> int:
    sources = select_program_sources(root)
    for source in sources:
        relative = source.resolve().relative_to(root.resolve())
        destination = app_root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    return len(sources)


def copy_runtime_payload(source: Path, runtime_root: Path) -> int:
    count = 0
    for path, relative in iter_runtime_files(source):
        destination = runtime_root / Path(*relative.parts)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, destination)
        count += 1
    if not (runtime_root / "python.exe").is_file():
        raise WindowsPortableError("copied runtime does not contain python.exe")
    return count


def load_asset_manifest(path: Path) -> dict[str, Any]:
    ensure_regular_file(path, "S4 asset manifest")
    raw = path.read_text(encoding="utf-8")
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise WindowsPortableError(f"invalid S4 asset manifest: {exc}") from exc
    if not isinstance(payload, dict) or not isinstance(payload.get("files"), list):
        raise WindowsPortableError("invalid S4 asset manifest contract")
    paths = [entry.get("path") for entry in payload["files"] if isinstance(entry, dict)]
    if len(paths) != len(payload["files"]) or not all(isinstance(path, str) for path in paths):
        raise WindowsPortableError("invalid S4 asset manifest file entries")
    if paths != sorted(paths) or len(paths) != len(set(paths)):
        raise WindowsPortableError("S4 asset manifest paths are not deterministic")
    for path in paths:
        relative = validate_relative_path(path, "asset manifest path")
        if relative.parts[:1] == ("05_assets",) or relative.suffix.casefold() not in IMAGE_SUFFIXES:
            raise WindowsPortableError(f"nonportable S4 asset manifest path: {path}")
    return payload


def copy_assets_into_package(root: Path, package_root: Path) -> tuple[int, str]:
    asset_source = root / ASSET_OUTPUT / "app"
    manifest_source = root / ASSET_MANIFEST
    payload = load_asset_manifest(manifest_source)
    paths = [entry["path"] for entry in payload["files"]]
    asset_destination = package_root / "assets-overlay" / "app"
    for path in paths:
        relative = validate_relative_path(path, "asset path")
        source = asset_source / Path(*relative.parts)
        ensure_regular_file(source, "S4 release asset")
        destination = asset_destination / Path(*relative.parts)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
    manifest_destination = package_root / "manifests" / "assets-manifest.json"
    manifest_destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(manifest_source, manifest_destination)
    return len(paths), sha256_file(manifest_destination)


def launcher_text(gui: bool) -> str:
    if gui:
        label = "啟動 Element Maze GUI（主要入口）"
        script = "app\\06_tools\\portable_gui_launcher.py"
    else:
        label = "文字核心版 Text Core"
        script = "app\\element_maze.py"
    return (
        "@echo off\r\n"
        "chcp 65001 >nul\r\n"
        "setlocal\r\n"
        "cd /d \"%~dp0\"\r\n"
        f"echo {label}\r\n"
        f"\"%~dp0app\\runtime\\python.exe\" -B \"%~dp0{script}\"\r\n"
        "if errorlevel 1 (\r\n"
        "  echo.\r\n"
        "  echo Element Maze failed to start.\r\n"
        ")\r\n"
        "pause\r\n"
    )


def release_text(source_revision: str, release_ready: bool, runtime_label: str) -> str:
    readiness = (
        "Release-ready runtime provenance was explicitly asserted by the builder operator."
        if release_ready
        else "LOCAL VALIDATION ONLY: runtime redistributability was not asserted; do not publish this ZIP."
    )
    return (
        "Element Maze - Windows Portable\n"
        "================================\n\n"
        f"PRIMARY: {GUI_ENTRYPOINT}\n"
        f"Text-only alternative: {CLI_ENTRYPOINT}\n\n"
        "The GUI always starts in live mode on 127.0.0.1. Python remains gameplay authority.\n"
        "Program files and compressed GUI images are intentionally stored separately.\n\n"
        f"Source revision: {source_revision}\n"
        f"Runtime label: {runtime_label}\n"
        f"{readiness}\n"
    )


def write_package_shell(
    package_root: Path,
    source_revision: str,
    release_ready: bool,
    runtime_label: str,
) -> None:
    (package_root / GUI_ENTRYPOINT).write_text(launcher_text(True), encoding="utf-8", newline="")
    (package_root / CLI_ENTRYPOINT).write_text(launcher_text(False), encoding="utf-8", newline="")
    (package_root / "RELEASE.txt").write_text(
        release_text(source_revision, release_ready, runtime_label),
        encoding="utf-8",
        newline="\n",
    )


def program_manifest_entries(package_root: Path) -> list[dict[str, Any]]:
    included_roots = [package_root / "app"]
    included_files = [
        package_root / GUI_ENTRYPOINT,
        package_root / CLI_ENTRYPOINT,
        package_root / "RELEASE.txt",
    ]
    files = list(included_files)
    for root in included_roots:
        files.extend(path for path in root.rglob("*") if path.is_file())
    entries = []
    for path in sorted(files, key=lambda item: relative_posix(item, package_root)):
        relative = relative_posix(path, package_root)
        validate_relative_path(relative, "program manifest path")
        if relative.startswith("app/") and path.suffix.casefold() in IMAGE_SUFFIXES:
            raise WindowsPortableError(f"image leaked into app payload: {relative}")
        entries.append(
            {"bytes": path.stat().st_size, "path": relative, "sha256": sha256_file(path)}
        )
    return entries


def manifest_payload(
    package_root: Path,
    source_revision: str,
    asset_manifest_sha256: str,
    asset_file_count: int,
    runtime_file_count: int,
    runtime_version: str,
    runtime_label: str,
    release_ready: bool,
) -> dict[str, Any]:
    return {
        "asset_file_count": asset_file_count,
        "asset_manifest_sha256": asset_manifest_sha256,
        "entrypoints": {"cli": CLI_ENTRYPOINT, "gui_primary": GUI_ENTRYPOINT},
        "format_version": FORMAT_VERSION,
        "program_files": program_manifest_entries(package_root),
        "release_ready": release_ready,
        "runtime": {
            "file_count": runtime_file_count,
            "label": runtime_label,
            "python_version": runtime_version,
            "redistributable_asserted": release_ready,
        },
        "source_revision": source_revision,
        "zip_filename": ZIP_FILENAME,
    }


def validate_staging_paths(root: Path) -> tuple[Path, Path, Path, Path]:
    dist_root = (root / DIST_ROOT).resolve()
    staging_parent = (root / STAGING_PARENT).resolve()
    package_root = (root / PACKAGE_RELATIVE).resolve()
    zip_path = (root / ZIP_RELATIVE).resolve()
    temp_root = (staging_parent / f".{PACKAGE_NAME}.building").resolve()
    if package_root.parent != staging_parent or temp_root.parent != staging_parent:
        raise WindowsPortableError("unsafe Windows portable staging path")
    if zip_path.parent != dist_root:
        raise WindowsPortableError("unsafe Windows portable ZIP path")
    return staging_parent, package_root, zip_path, temp_root


def clear_known_path(path: Path, expected: Path) -> None:
    if path.resolve() != expected.resolve():
        raise WindowsPortableError(f"refusing to clear unexpected path: {path}")
    if path.exists():
        shutil.rmtree(path)


def run_packaged_checks(package_root: Path, require_release_dependencies: bool = False) -> None:
    python_exe = package_root / "app" / "runtime" / "python.exe"
    commands: tuple[list[str], ...] = (
        [str(python_exe), "-B", "app/element_maze.py", "--smoke-test"],
        [str(python_exe), "-B", "app/06_tools/portable_gui_launcher.py", "--smoke-test"],
    )
    if require_release_dependencies:
        commands += ([str(python_exe), "-B", "-I", "-c", "import rich"],)
    for command in commands:
        completed = subprocess.run(
            command,
            cwd=package_root,
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=120,
        )
        if completed.returncode != 0:
            detail = completed.stderr.strip() or completed.stdout.strip()
            raise WindowsPortableError(f"packaged runtime check failed: {detail}")


def package_files(package_root: Path) -> list[Path]:
    return sorted(
        (path for path in package_root.rglob("*") if path.is_file()),
        key=lambda path: relative_posix(path, package_root),
    )


def write_deterministic_zip(package_root: Path, zip_path: Path) -> None:
    temp_zip = zip_path.with_suffix(zip_path.suffix + ".building")
    if temp_zip.exists():
        temp_zip.unlink()
    try:
        with zipfile.ZipFile(temp_zip, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for path in package_files(package_root):
                relative = relative_posix(path, package_root)
                validate_relative_path(relative, "ZIP entry")
                entry_name = f"{PACKAGE_NAME}/{relative}"
                info = zipfile.ZipInfo(entry_name, FIXED_ZIP_TIMESTAMP)
                info.compress_type = zipfile.ZIP_DEFLATED
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                archive.writestr(info, path.read_bytes(), compresslevel=9)
        temp_zip.replace(zip_path)
    finally:
        if temp_zip.exists():
            temp_zip.unlink()


def load_portable_manifest(package_root: Path) -> tuple[dict[str, Any], bytes]:
    path = package_root / "manifests" / PORTABLE_MANIFEST_NAME
    ensure_regular_file(path, "Windows portable manifest")
    raw = path.read_bytes()
    try:
        payload = json.loads(raw.decode("utf-8"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise WindowsPortableError(f"invalid Windows portable manifest: {exc}") from exc
    if not isinstance(payload, dict) or raw != canonical_json(payload).encode("utf-8"):
        raise WindowsPortableError("Windows portable manifest is not deterministic canonical JSON")
    return payload, raw


def verify_package(root: Path = ROOT) -> BuildSummary:
    root = root.resolve()
    # Verification also re-enters the S4 verifier; the portable builder never
    # maintains a second image-selection or transform implementation.
    release_assets.verify_release(root, ASSET_OUTPUT, ASSET_MANIFEST)
    _staging_parent, package_root, zip_path, _temp_root = validate_staging_paths(root)
    payload, _raw = load_portable_manifest(package_root)
    required = {
        "asset_file_count",
        "asset_manifest_sha256",
        "entrypoints",
        "format_version",
        "program_files",
        "release_ready",
        "runtime",
        "source_revision",
        "zip_filename",
    }
    if set(payload) != required or payload["format_version"] != FORMAT_VERSION:
        raise WindowsPortableError("Windows portable manifest keys/version do not match contract")
    if payload["zip_filename"] != ZIP_FILENAME:
        raise WindowsPortableError("Windows portable manifest ZIP filename mismatch")
    if payload["source_revision"] != release_assets.git_revision(root):
        raise WindowsPortableError("Windows portable manifest source revision does not match HEAD")
    expected_entrypoints = {"cli": CLI_ENTRYPOINT, "gui_primary": GUI_ENTRYPOINT}
    if payload["entrypoints"] != expected_entrypoints:
        raise WindowsPortableError("Windows portable entrypoints do not match contract")

    asset_manifest = package_root / "manifests" / "assets-manifest.json"
    repository_asset_manifest = root / ASSET_MANIFEST
    if asset_manifest.read_bytes() != repository_asset_manifest.read_bytes():
        raise WindowsPortableError("packaged S4 asset manifest differs from verified dist manifest")
    if sha256_file(asset_manifest) != payload["asset_manifest_sha256"]:
        raise WindowsPortableError("packaged S4 asset manifest SHA-256 mismatch")
    asset_payload = load_asset_manifest(asset_manifest)
    asset_paths = [entry["path"] for entry in asset_payload["files"]]
    if len(asset_paths) != payload["asset_file_count"]:
        raise WindowsPortableError("portable asset file count mismatch")
    actual_assets = sorted(
        relative_posix(path, package_root / "assets-overlay" / "app")
        for path in (package_root / "assets-overlay" / "app").rglob("*")
        if path.is_file()
    )
    if actual_assets != asset_paths:
        raise WindowsPortableError("portable assets do not exactly match the S4 manifest")

    entries = payload["program_files"]
    if not isinstance(entries, list):
        raise WindowsPortableError("program_files must be an array")
    paths = [entry.get("path") for entry in entries if isinstance(entry, dict)]
    if len(paths) != len(entries) or paths != sorted(paths) or len(paths) != len(set(paths)):
        raise WindowsPortableError("program_files are not a unique sorted list")
    expected_program_paths = [entry["path"] for entry in program_manifest_entries(package_root)]
    if paths != expected_program_paths:
        raise WindowsPortableError("program file set differs from manifest")
    for entry in entries:
        if set(entry) != {"bytes", "path", "sha256"}:
            raise WindowsPortableError("invalid program file manifest entry")
        path = package_root / Path(*validate_relative_path(entry["path"], "program path").parts)
        if path.stat().st_size != entry["bytes"] or sha256_file(path) != entry["sha256"]:
            raise WindowsPortableError(f"program file hash/size mismatch: {entry['path']}")
    if not (package_root / "app" / "runtime" / "python.exe").is_file():
        raise WindowsPortableError("portable package is missing app/runtime/python.exe")
    if any(path.suffix.casefold() in IMAGE_SUFFIXES for path in (package_root / "app").rglob("*")):
        raise WindowsPortableError("portable app payload contains image files")

    allowed_package_paths = set(paths)
    allowed_package_paths.update(
        f"assets-overlay/app/{path}" for path in asset_paths
    )
    allowed_package_paths.update(
        {"manifests/assets-manifest.json", f"manifests/{PORTABLE_MANIFEST_NAME}"}
    )
    actual_package_paths = {relative_posix(path, package_root) for path in package_files(package_root)}
    if actual_package_paths != allowed_package_paths:
        missing = sorted(allowed_package_paths - actual_package_paths)
        extra = sorted(actual_package_paths - allowed_package_paths)
        raise WindowsPortableError(f"portable package file set mismatch; missing={missing}, extra={extra}")

    if not zip_path.is_file():
        raise WindowsPortableError(f"missing Windows portable ZIP: {zip_path}")
    expected_zip_entries = [f"{PACKAGE_NAME}/{relative_posix(path, package_root)}" for path in package_files(package_root)]
    with zipfile.ZipFile(zip_path) as archive:
        names = archive.namelist()
        if names != expected_zip_entries:
            raise WindowsPortableError("ZIP entries are not an exact deterministic sorted package set")
        for info, expected_name in zip(archive.infolist(), expected_zip_entries, strict=True):
            relative = expected_name.removeprefix(f"{PACKAGE_NAME}/")
            validate_relative_path(relative, "ZIP entry")
            if info.filename != expected_name or info.date_time != FIXED_ZIP_TIMESTAMP:
                raise WindowsPortableError(f"nondeterministic ZIP entry: {info.filename}")
            source = package_root / Path(*PurePosixPath(relative).parts)
            if hashlib.sha256(archive.read(info)).hexdigest() != sha256_file(source):
                raise WindowsPortableError(f"ZIP content mismatch: {info.filename}")

    run_packaged_checks(package_root, bool(payload["release_ready"]))
    runtime = payload.get("runtime", {})
    return BuildSummary(
        "verify",
        payload["source_revision"],
        len(entries),
        len(asset_paths),
        int(runtime.get("file_count", 0)),
        bool(payload["release_ready"]),
        package_root,
        zip_path,
    )


def dry_run(
    root: Path,
    runtime_source: Path,
    release_ready: bool,
) -> BuildSummary:
    asset_summary = release_assets.dry_run_release(root)
    program_count = len(select_program_sources(root))
    source, _licenses, _version = validate_runtime_source(runtime_source)
    runtime_count = sum(1 for _ in iter_runtime_files(source))
    return BuildSummary(
        "dry-run",
        asset_summary.source_revision,
        program_count + runtime_count + 3,
        asset_summary.included_count,
        runtime_count,
        release_ready,
        None,
        None,
    )


def build_package(
    root: Path = ROOT,
    runtime_source: Path | None = None,
    runtime_label: str = "user-supplied-runtime",
    release_ready: bool = False,
) -> BuildSummary:
    root = root.resolve()
    if runtime_source is None:
        raise WindowsPortableError("build requires an explicit --runtime-source")
    if not runtime_label.strip() or any(char in runtime_label for char in "\\/\r\n"):
        raise WindowsPortableError("runtime label must be a short portable label, not a path")
    source, _licenses, runtime_version = validate_runtime_source(runtime_source)

    # S4 remains the only authority for image selection and transforms.
    release_assets.build_release(root, ASSET_OUTPUT, ASSET_MANIFEST)
    asset_summary = release_assets.verify_release(root, ASSET_OUTPUT, ASSET_MANIFEST)

    staging_parent, package_root, zip_path, temp_root = validate_staging_paths(root)
    staging_parent.mkdir(parents=True, exist_ok=True)
    clear_known_path(temp_root, temp_root)
    temp_root.mkdir(parents=True)
    try:
        app_root = temp_root / "app"
        app_root.mkdir()
        copy_program_payload(root, app_root)
        runtime_count = copy_runtime_payload(source, app_root / "runtime")
        asset_count, asset_manifest_hash = copy_assets_into_package(root, temp_root)
        if asset_count != asset_summary.included_count:
            raise WindowsPortableError("S4 asset count changed during portable staging")
        source_revision = release_assets.git_revision(root)
        write_package_shell(temp_root, source_revision, release_ready, runtime_label)
        manifest = manifest_payload(
            temp_root,
            source_revision,
            asset_manifest_hash,
            asset_count,
            runtime_count,
            runtime_version,
            runtime_label,
            release_ready,
        )
        manifest_path = temp_root / "manifests" / PORTABLE_MANIFEST_NAME
        manifest_path.write_text(canonical_json(manifest), encoding="utf-8", newline="\n")
        run_packaged_checks(temp_root, release_ready)
        clear_known_path(package_root, package_root)
        temp_root.replace(package_root)
        write_deterministic_zip(package_root, zip_path)
    except Exception:
        if temp_root.exists():
            clear_known_path(temp_root, temp_root)
        raise
    return verify_package(root)


def print_summary(summary: BuildSummary) -> None:
    print(f"[OK] Windows portable {summary.mode} passed")
    print(f"source_revision: {summary.source_revision}")
    print(f"program files: {summary.program_file_count}")
    print(f"runtime files: {summary.runtime_file_count}")
    print(f"asset files: {summary.asset_file_count}")
    print(f"release-ready: {'yes' if summary.release_ready else 'no (local validation only)'}")
    if summary.package_path is not None:
        print(f"package: {summary.package_path}")
    if summary.zip_path is not None:
        print(f"ZIP: {summary.zip_path}")
    if summary.mode == "dry-run":
        print("no files written")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a deterministic offline Element Maze Windows portable ZIP."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--verify", action="store_true")
    parser.add_argument(
        "--runtime-source",
        type=Path,
        help="Explicit directory containing a self-contained python.exe and license files.",
    )
    parser.add_argument("--runtime-label", default="user-supplied-runtime")
    parser.add_argument(
        "--redistributable-runtime",
        action="store_true",
        help="Assert that the supplied runtime is licensed for redistribution.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.verify:
            summary = verify_package(ROOT)
        else:
            if args.runtime_source is None:
                raise WindowsPortableError("--runtime-source is required for dry-run and build")
            if args.dry_run:
                summary = dry_run(ROOT, args.runtime_source, args.redistributable_runtime)
            else:
                summary = build_package(
                    ROOT,
                    args.runtime_source,
                    args.runtime_label,
                    args.redistributable_runtime,
                )
        print_summary(summary)
    except (WindowsPortableError, release_assets.ReleaseAssetError, OSError, subprocess.SubprocessError) as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
