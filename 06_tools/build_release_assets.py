from __future__ import annotations

import argparse
import ast
import hashlib
import io
import json
import re
import shutil
import subprocess
import sys
import tokenize
from collections import Counter
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
FORMAT_VERSION = 1
ASSET_ROOT = "app"
JPEG_QUALITY = 82
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
GUI_SOURCE_SUFFIXES = {".html", ".css", ".js", ".json"}
DEFAULT_OUTPUT = Path("dist/assets-overlay")
DEFAULT_MANIFEST = Path("dist/manifests/assets-manifest.json")

QUOTED_IMAGE_RE = re.compile(
    r"(?P<quote>[\"'`])"
    r"(?P<value>[^\"'`\r\n]*?\.(?:png|jpe?g|webp|gif)"
    r"(?:[?#][^\"'`\r\n]*)?)"
    r"(?P=quote)",
    re.IGNORECASE,
)
UNQUOTED_URL_RE = re.compile(
    r"url\(\s*(?P<value>[^\"')\r\n]*?\.(?:png|jpe?g|webp|gif)"
    r"(?:[?#][^\"')\r\n]*)?)\s*\)",
    re.IGNORECASE,
)
UNQUOTED_HTML_RE = re.compile(
    r"(?:src|href|poster)\s*=\s*"
    r"(?P<value>[^\s>\"']+?\.(?:png|jpe?g|webp|gif)(?:[?#][^\s>\"']*)?)",
    re.IGNORECASE,
)


try:
    from PIL import Image, UnidentifiedImageError
except Exception as exc:  # pragma: no cover - runtime dependency failure.
    Image = None  # type: ignore[assignment]
    UnidentifiedImageError = OSError  # type: ignore[assignment]
    PIL_IMPORT_ERROR: Exception | None = exc
else:
    PIL_IMPORT_ERROR = None


class ReleaseAssetError(RuntimeError):
    pass


@dataclass(frozen=True)
class LiteralReference:
    source: Path
    line: int
    literal: str


@dataclass(frozen=True)
class ReferenceIssue:
    kind: str
    reference: LiteralReference
    detail: str


@dataclass(frozen=True)
class AssetSelection:
    assets: tuple[Path, ...]
    source_files_scanned: int
    literal_references_scanned: int
    old_count: int
    unreferenced_count: int


@dataclass(frozen=True)
class ImageMetadata:
    size: tuple[int, int]
    has_alpha: bool
    format: str | None


@dataclass(frozen=True)
class ReleaseArtifact:
    source: Path
    path: str
    source_data: bytes
    release_data: bytes
    transform: str

    def manifest_entry(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "source_sha256": sha256_bytes(self.source_data),
            "release_sha256": sha256_bytes(self.release_data),
            "source_bytes": len(self.source_data),
            "release_bytes": len(self.release_data),
            "transform": self.transform,
        }


@dataclass(frozen=True)
class ReleaseSummary:
    source_revision: str
    included_count: int
    old_count: int
    unreferenced_count: int
    source_bytes: int
    release_bytes: int | None
    transforms: dict[str, int]


def relative_posix(path: Path, root: Path) -> str:
    return path.resolve().relative_to(root.resolve()).as_posix()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def has_old_segment(path: str | PurePosixPath | Path) -> bool:
    if isinstance(path, Path):
        parts = path.parts
    else:
        parts = PurePosixPath(str(path).replace("\\", "/")).parts
    return any(part.casefold() == "old" for part in parts)


def canonical_key(path: Path, root: Path) -> str:
    return relative_posix(path, root).casefold()


def discover_source_files(root: Path) -> tuple[Path, ...]:
    sources: set[Path] = set()
    gui_root = root / "07_gui_prototype"
    if gui_root.exists():
        sources.update(
            path
            for path in gui_root.rglob("*")
            if path.is_file() and path.suffix.lower() in GUI_SOURCE_SUFFIXES
        )
    engine_root = root / "03_engine" / "engine"
    if engine_root.exists():
        sources.update(path for path in engine_root.glob("gui_*.py") if path.is_file())
    return tuple(sorted(sources, key=lambda path: relative_posix(path, root)))


def is_runtime_source(path: Path, root: Path) -> bool:
    relative = path.resolve().relative_to(root.resolve())
    if has_old_segment(relative):
        return False
    # Asset-review metadata is scanned by discovery but is not loaded by the
    # static or live GUI, so it cannot authorize portable runtime assets.
    if path.suffix.lower() == ".json" and path.name.lower().endswith(".meta.json"):
        return False
    return True


def blank_span(chars: list[str], start: int, end: int) -> None:
    for index in range(start, end):
        if chars[index] not in "\r\n":
            chars[index] = " "


def mask_web_comments(text: str, suffix: str) -> str:
    chars = list(text)
    index = 0
    quote: str | None = None
    escaped = False
    while index < len(chars):
        char = chars[index]
        if quote is not None:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            index += 1
            continue
        if char in {"\"", "'", "`"}:
            quote = char
            index += 1
            continue
        if text.startswith("/*", index):
            end = text.find("*/", index + 2)
            end = len(text) if end < 0 else end + 2
            blank_span(chars, index, end)
            index = end
            continue
        if suffix == ".js" and text.startswith("//", index):
            end = text.find("\n", index + 2)
            end = len(text) if end < 0 else end
            blank_span(chars, index, end)
            index = end
            continue
        if suffix == ".html" and text.startswith("<!--", index):
            end = text.find("-->", index + 4)
            end = len(text) if end < 0 else end + 3
            blank_span(chars, index, end)
            index = end
            continue
        index += 1
    return "".join(chars)


def looks_like_image_literal(value: str) -> bool:
    path_part = re.split(r"[?#]", value.strip(), maxsplit=1)[0]
    return PurePosixPath(path_part.replace("\\", "/")).suffix.lower() in IMAGE_SUFFIXES


def extract_python_references(source: Path, text: str) -> list[LiteralReference]:
    references: list[LiteralReference] = []
    try:
        tokens = tokenize.generate_tokens(io.StringIO(text).readline)
        for token in tokens:
            if token.type != tokenize.STRING:
                continue
            try:
                value = ast.literal_eval(token.string)
            except (SyntaxError, ValueError):
                continue
            if isinstance(value, str) and looks_like_image_literal(value):
                references.append(LiteralReference(source, token.start[0], value))
    except (IndentationError, tokenize.TokenError) as exc:
        raise ReleaseAssetError(f"cannot tokenize live Python source {source}: {exc}") from exc
    return references


def extract_web_references(source: Path, text: str) -> list[LiteralReference]:
    masked = mask_web_comments(text, source.suffix.lower())
    matches: dict[tuple[int, str], LiteralReference] = {}
    patterns = [QUOTED_IMAGE_RE, UNQUOTED_URL_RE]
    if source.suffix.lower() == ".html":
        patterns.append(UNQUOTED_HTML_RE)
    for pattern in patterns:
        for match in pattern.finditer(masked):
            value = match.group("value").strip()
            if not looks_like_image_literal(value):
                continue
            line = masked.count("\n", 0, match.start("value")) + 1
            matches[(match.start("value"), value)] = LiteralReference(source, line, value)
    return [matches[key] for key in sorted(matches)]


def extract_literal_references(source: Path) -> list[LiteralReference]:
    try:
        text = source.read_text(encoding="utf-8-sig")
    except UnicodeError as exc:
        raise ReleaseAssetError(f"live source is not UTF-8: {source}") from exc
    if source.suffix.lower() == ".py":
        return extract_python_references(source, text)
    return extract_web_references(source, text)


def image_inventory(root: Path) -> tuple[dict[str, Path], tuple[Path, ...], tuple[Path, ...]]:
    gui_root = root / "07_gui_prototype"
    images = tuple(
        sorted(
            (
                path
                for path in gui_root.rglob("*")
                if path.is_file() and path.suffix.lower() in IMAGE_SUFFIXES
            ),
            key=lambda path: relative_posix(path, root),
        )
    )
    by_key: dict[str, Path] = {}
    for path in images:
        key = canonical_key(path, root)
        if key in by_key:
            raise ReleaseAssetError(
                "case-insensitive asset path collision: "
                f"{relative_posix(by_key[key], root)} and {relative_posix(path, root)}"
            )
        by_key[key] = path
    old = tuple(path for path in images if has_old_segment(path.relative_to(root)))
    usable = tuple(path for path in images if not has_old_segment(path.relative_to(root)))
    return by_key, old, usable


def screen_root_for_source(source: Path, root: Path) -> Path | None:
    gui_root = (root / "07_gui_prototype").resolve()
    try:
        relative = source.resolve().relative_to(gui_root)
    except ValueError:
        return None
    return gui_root / relative.parts[0] if len(relative.parts) > 1 else gui_root


def inferred_python_bases(source: Path, root: Path) -> tuple[Path, ...]:
    gui_root = root / "07_gui_prototype"
    core = source.stem.removeprefix("gui_")
    for suffix in ("_model", "_presentation", "_actions"):
        if core.endswith(suffix):
            core = core[: -len(suffix)]
            break
    names = [core, f"{core}_screen"]
    special = {"exploration": "dungeon_exploration", "relic_preview": "relic_preview_screen"}
    if core in special:
        names.insert(0, special[core])
    bases: list[Path] = []
    for name in names:
        candidate = gui_root / name
        if candidate.is_dir() and candidate not in bases:
            bases.append(candidate)
    return tuple(bases)


def all_screen_bases(root: Path) -> tuple[Path, ...]:
    gui_root = root / "07_gui_prototype"
    return tuple(sorted((path for path in gui_root.iterdir() if path.is_dir()), key=lambda path: path.name))


def lexical_candidate(base: Path, literal_path: str, root: Path) -> tuple[str | None, str | None]:
    candidate = base.joinpath(*PurePosixPath(literal_path).parts).resolve()
    try:
        relative = candidate.relative_to(root.resolve()).as_posix()
    except ValueError:
        return None, f"path escapes repository: {candidate}"
    return relative, None


def candidate_groups(reference: LiteralReference, path_text: str, root: Path) -> list[tuple[Path, ...]]:
    normalized = path_text.replace("\\", "/")
    if normalized.startswith("/"):
        return [((root / "07_gui_prototype"),)]
    parts = PurePosixPath(normalized).parts
    first = parts[0] if parts else ""
    if first in {"07_gui_prototype", "05_assets", "03_engine", "04_data", "01_content"}:
        return [(root,)]

    screen_root = screen_root_for_source(reference.source, root)
    if screen_root is not None:
        relative_source = reference.source.resolve().relative_to(screen_root.resolve())
        if "fixtures" in relative_source.parts:
            return [(screen_root,), (reference.source.parent,)]
        return [(reference.source.parent,), (screen_root,)]

    inferred = inferred_python_bases(reference.source, root)
    groups: list[tuple[Path, ...]] = []
    if inferred:
        groups.append(inferred)
    groups.append(all_screen_bases(root))
    return groups


def sanitized_literal(reference: LiteralReference) -> tuple[str | None, ReferenceIssue | None]:
    value = unquote(reference.literal.strip())
    lowered = value.casefold()
    if lowered.startswith(("data:", "http://", "https://", "//")):
        return None, None
    if "${" in value or "{" in value or "}" in value:
        return None, ReferenceIssue("UNRESOLVED", reference, "dynamic image path is not a literal")
    path_text = re.split(r"[?#]", value, maxsplit=1)[0].replace("\\", "/")
    if re.match(r"^[A-Za-z]:/", path_text):
        return None, ReferenceIssue("NONPORTABLE", reference, "absolute filesystem image path")
    if has_old_segment(path_text):
        return None, ReferenceIssue("OLD", reference, "OLD path segments are forbidden")
    return path_text, None


def resolve_reference(
    reference: LiteralReference,
    root: Path,
    inventory: dict[str, Path],
) -> tuple[Path | None, ReferenceIssue | None]:
    path_text, issue = sanitized_literal(reference)
    if issue is not None or path_text is None:
        return None, issue
    normalized = path_text.lstrip("/") if path_text.startswith("/") else path_text
    if PurePosixPath(normalized).parts[:1] == ("05_assets",):
        return None, ReferenceIssue("NONPORTABLE", reference, "05_assets material is not a runtime asset")

    expected: list[str] = []
    for group in candidate_groups(reference, path_text, root):
        found: dict[str, Path] = {}
        for base in group:
            relative, escape_error = lexical_candidate(base, normalized, root)
            if escape_error:
                return None, ReferenceIssue("NONPORTABLE", reference, escape_error)
            if relative is None:
                continue
            expected.append(relative)
            actual = inventory.get(relative.casefold())
            if actual is not None:
                found[canonical_key(actual, root)] = actual
        if len(found) == 1:
            asset = next(iter(found.values()))
            if has_old_segment(asset.relative_to(root)):
                return None, ReferenceIssue("OLD", reference, relative_posix(asset, root))
            return asset, None
        if len(found) > 1:
            choices = ", ".join(relative_posix(path, root) for path in found.values())
            return None, ReferenceIssue("AMBIGUOUS", reference, f"matches multiple assets: {choices}")

    expected_text = expected[0] if expected else path_text
    return None, ReferenceIssue("MISSING", reference, f"expected {expected_text}")


def format_issues(issues: Iterable[ReferenceIssue], root: Path) -> str:
    rows = []
    for issue in sorted(
        issues,
        key=lambda item: (
            relative_posix(item.reference.source, root),
            item.reference.line,
            item.reference.literal,
        ),
    ):
        source = relative_posix(issue.reference.source, root)
        rows.append(
            f"- {issue.kind}: {source}:{issue.reference.line} -> "
            f"{issue.reference.literal!r} ({issue.detail})"
        )
    return "live image reference validation failed:\n" + "\n".join(rows)


def select_release_assets(root: Path = ROOT) -> AssetSelection:
    root = root.resolve()
    inventory, old_assets, usable_assets = image_inventory(root)
    sources = discover_source_files(root)
    selected: dict[str, Path] = {}
    issues: list[ReferenceIssue] = []
    reference_count = 0
    for source in sources:
        references = extract_literal_references(source)
        if not is_runtime_source(source, root):
            continue
        reference_count += len(references)
        for reference in references:
            asset, issue = resolve_reference(reference, root, inventory)
            if issue is not None:
                issues.append(issue)
            elif asset is not None:
                selected[canonical_key(asset, root)] = asset
    if issues:
        raise ReleaseAssetError(format_issues(issues, root))

    assets = tuple(sorted(selected.values(), key=lambda path: relative_posix(path, root)))
    usable_keys = {canonical_key(path, root) for path in usable_assets}
    return AssetSelection(
        assets=assets,
        source_files_scanned=len(sources),
        literal_references_scanned=reference_count,
        old_count=len(old_assets),
        unreferenced_count=len(usable_keys - set(selected)),
    )


def require_pillow() -> None:
    if Image is None:
        raise ReleaseAssetError(f"Pillow is required for release asset processing: {PIL_IMPORT_ERROR}")


def metadata_from_image(image: Any) -> ImageMetadata:
    return ImageMetadata(
        size=tuple(image.size),
        has_alpha=("A" in image.getbands() or "transparency" in image.info),
        format=image.format,
    )


def inspect_image_bytes(data: bytes, label: str) -> ImageMetadata:
    require_pillow()
    try:
        with Image.open(io.BytesIO(data)) as image:
            image.load()
            return metadata_from_image(image)
    except (OSError, UnidentifiedImageError) as exc:
        raise ReleaseAssetError(f"cannot read image {label}: {exc}") from exc


def encode_image(source_data: bytes, source_label: str) -> tuple[bytes, str]:
    require_pillow()
    try:
        with Image.open(io.BytesIO(source_data)) as image:
            source_metadata = metadata_from_image(image)
            image.load()
            output = io.BytesIO()
            if image.format == "PNG":
                kwargs: dict[str, Any] = {"format": "PNG", "optimize": True}
                if image.info.get("icc_profile"):
                    kwargs["icc_profile"] = image.info["icc_profile"]
                image.save(output, **kwargs)
                transform = "png-lossless"
            elif image.format == "JPEG":
                kwargs = {"format": "JPEG", "quality": JPEG_QUALITY, "optimize": True}
                if image.info.get("exif"):
                    kwargs["exif"] = image.info["exif"]
                if image.info.get("icc_profile"):
                    kwargs["icc_profile"] = image.info["icc_profile"]
                image.save(output, **kwargs)
                transform = f"jpeg-q{JPEG_QUALITY}"
            else:
                return source_data, "copy"
    except (OSError, UnidentifiedImageError) as exc:
        raise ReleaseAssetError(f"cannot process image {source_label}: {exc}") from exc

    encoded = output.getvalue()
    if len(encoded) > len(source_data):
        return source_data, "copy"
    release_metadata = inspect_image_bytes(encoded, source_label)
    if release_metadata.size != source_metadata.size:
        raise ReleaseAssetError(f"image dimensions changed during release transform: {source_label}")
    if release_metadata.has_alpha != source_metadata.has_alpha:
        raise ReleaseAssetError(f"image alpha changed during release transform: {source_label}")
    return encoded, transform


def prepare_artifact(source: Path, root: Path) -> ReleaseArtifact:
    source_data = source.read_bytes()
    path = relative_posix(source, root)
    inspect_image_bytes(source_data, path)
    release_data, transform = encode_image(source_data, path)
    return ReleaseArtifact(source, path, source_data, release_data, transform)


def git_revision(root: Path) -> str:
    completed = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise ReleaseAssetError(f"cannot determine source revision: {detail}")
    return completed.stdout.strip()


def resolve_cli_path(root: Path, value: str | Path) -> Path:
    path = Path(value)
    return path.resolve() if path.is_absolute() else (root / path).resolve()


def validate_release_paths(
    root: Path,
    output: str | Path,
    manifest: str | Path,
) -> tuple[Path, Path, Path]:
    output_path = resolve_cli_path(root, output)
    manifest_path = resolve_cli_path(root, manifest)
    expected_output = (root / DEFAULT_OUTPUT).resolve()
    expected_manifest = (root / DEFAULT_MANIFEST).resolve()
    if output_path != expected_output:
        raise ReleaseAssetError(f"output must be {expected_output}")
    if manifest_path != expected_manifest:
        raise ReleaseAssetError(f"manifest must be {expected_manifest}")
    app_path = output_path / ASSET_ROOT
    if app_path.resolve() != (root / "dist" / "assets-overlay" / "app").resolve():
        raise ReleaseAssetError("refusing unsafe release app path")
    return output_path, app_path, manifest_path


def reset_release_app(app_path: Path, root: Path) -> None:
    expected = (root / "dist" / "assets-overlay" / "app").resolve()
    if app_path.resolve() != expected:
        raise ReleaseAssetError(f"refusing to clear unexpected output path: {app_path}")
    if app_path.exists():
        shutil.rmtree(app_path)
    app_path.mkdir(parents=True, exist_ok=True)


def manifest_payload(
    source_revision: str,
    entries: list[dict[str, Any]],
    selection: AssetSelection,
) -> dict[str, Any]:
    entries.sort(key=lambda entry: entry["path"])
    return {
        "format_version": FORMAT_VERSION,
        "source_revision": source_revision,
        "asset_root": ASSET_ROOT,
        "files": entries,
        "excluded": {
            "old_count": selection.old_count,
            "unreferenced_count": selection.unreferenced_count,
        },
    }


def serialize_manifest(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def dry_run_release(root: Path = ROOT, source_revision: str | None = None) -> ReleaseSummary:
    root = root.resolve()
    selection = select_release_assets(root)
    revision = source_revision or git_revision(root)
    source_bytes = 0
    for source in selection.assets:
        data = source.read_bytes()
        inspect_image_bytes(data, relative_posix(source, root))
        source_bytes += len(data)
    return ReleaseSummary(
        revision,
        len(selection.assets),
        selection.old_count,
        selection.unreferenced_count,
        source_bytes,
        None,
        {},
    )


def build_release(
    root: Path = ROOT,
    output: str | Path = DEFAULT_OUTPUT,
    manifest: str | Path = DEFAULT_MANIFEST,
    source_revision: str | None = None,
) -> ReleaseSummary:
    root = root.resolve()
    _output_path, app_path, manifest_path = validate_release_paths(root, output, manifest)
    selection = select_release_assets(root)
    revision = source_revision or git_revision(root)
    reset_release_app(app_path, root)

    entries: list[dict[str, Any]] = []
    transforms: Counter[str] = Counter()
    source_total = 0
    release_total = 0
    for source in selection.assets:
        artifact = prepare_artifact(source, root)
        destination = app_path / Path(artifact.path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(artifact.release_data)
        entry = artifact.manifest_entry()
        entries.append(entry)
        transforms[artifact.transform] += 1
        source_total += entry["source_bytes"]
        release_total += entry["release_bytes"]

    payload = manifest_payload(revision, entries, selection)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(serialize_manifest(payload), encoding="utf-8", newline="\n")
    return ReleaseSummary(
        revision,
        len(entries),
        selection.old_count,
        selection.unreferenced_count,
        source_total,
        release_total,
        dict(sorted(transforms.items())),
    )


def require_exact_keys(value: dict[str, Any], expected: set[str], label: str) -> None:
    if set(value) != expected:
        raise ReleaseAssetError(
            f"{label} keys do not match contract: got {sorted(value)}, expected {sorted(expected)}"
        )


def verify_release(
    root: Path = ROOT,
    output: str | Path = DEFAULT_OUTPUT,
    manifest: str | Path = DEFAULT_MANIFEST,
    source_revision: str | None = None,
) -> ReleaseSummary:
    root = root.resolve()
    _output_path, app_path, manifest_path = validate_release_paths(root, output, manifest)
    selection = select_release_assets(root)
    revision = source_revision or git_revision(root)
    if not manifest_path.is_file():
        raise ReleaseAssetError(f"missing manifest: {manifest_path}")
    raw_manifest = manifest_path.read_text(encoding="utf-8")
    try:
        payload = json.loads(raw_manifest)
    except json.JSONDecodeError as exc:
        raise ReleaseAssetError(f"invalid manifest JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ReleaseAssetError("manifest root must be an object")
    require_exact_keys(
        payload,
        {"format_version", "source_revision", "asset_root", "files", "excluded"},
        "manifest",
    )
    if raw_manifest != serialize_manifest(payload):
        raise ReleaseAssetError("manifest is not in deterministic canonical form")
    if payload["format_version"] != FORMAT_VERSION:
        raise ReleaseAssetError(f"unsupported manifest format_version: {payload['format_version']}")
    if payload["source_revision"] != revision:
        raise ReleaseAssetError(
            f"manifest source_revision {payload['source_revision']} does not match HEAD {revision}"
        )
    if payload["asset_root"] != ASSET_ROOT:
        raise ReleaseAssetError(f"manifest asset_root must be {ASSET_ROOT!r}")
    if not isinstance(payload["excluded"], dict):
        raise ReleaseAssetError("manifest excluded must be an object")
    require_exact_keys(payload["excluded"], {"old_count", "unreferenced_count"}, "excluded")
    expected_excluded = {
        "old_count": selection.old_count,
        "unreferenced_count": selection.unreferenced_count,
    }
    if payload["excluded"] != expected_excluded:
        raise ReleaseAssetError(
            f"manifest excluded counts are stale: got {payload['excluded']}, expected {expected_excluded}"
        )
    if not isinstance(payload["files"], list):
        raise ReleaseAssetError("manifest files must be an array")

    entry_keys = {
        "path",
        "source_sha256",
        "release_sha256",
        "source_bytes",
        "release_bytes",
        "transform",
    }
    entries: list[dict[str, Any]] = []
    for index, entry in enumerate(payload["files"]):
        if not isinstance(entry, dict):
            raise ReleaseAssetError(f"manifest files[{index}] must be an object")
        require_exact_keys(entry, entry_keys, f"files[{index}]")
        entries.append(entry)
    paths = [entry["path"] for entry in entries]
    if not all(isinstance(path, str) for path in paths):
        raise ReleaseAssetError("manifest file paths must be strings")
    if paths != sorted(paths):
        raise ReleaseAssetError("manifest files are not sorted by path")
    if len(paths) != len(set(paths)):
        raise ReleaseAssetError("manifest contains duplicate paths")
    expected_paths = [relative_posix(path, root) for path in selection.assets]
    if paths != expected_paths:
        missing = sorted(set(expected_paths) - set(paths))
        extra = sorted(set(paths) - set(expected_paths))
        raise ReleaseAssetError(f"manifest allowlist mismatch; missing={missing}, extra={extra}")

    actual_output_paths = []
    if app_path.exists():
        actual_output_paths = sorted(
            relative_posix(path, app_path) for path in app_path.rglob("*") if path.is_file()
        )
    if actual_output_paths != paths:
        missing = sorted(set(paths) - set(actual_output_paths))
        extra = sorted(set(actual_output_paths) - set(paths))
        raise ReleaseAssetError(f"release output mismatch; missing={missing}, extra={extra}")

    transforms: Counter[str] = Counter()
    source_total = 0
    release_total = 0
    for entry, source in zip(entries, selection.assets, strict=True):
        path = entry["path"]
        if has_old_segment(path):
            raise ReleaseAssetError(f"manifest contains forbidden OLD path: {path}")
        if PurePosixPath(path).parts[:1] == ("05_assets",):
            raise ReleaseAssetError(f"manifest contains nonportable 05_assets path: {path}")
        if entry["transform"] not in {"png-lossless", f"jpeg-q{JPEG_QUALITY}", "copy"}:
            raise ReleaseAssetError(f"invalid transform for {path}: {entry['transform']}")
        source_data = source.read_bytes()
        release_data = (app_path / Path(path)).read_bytes()
        if entry["source_bytes"] != len(source_data):
            raise ReleaseAssetError(f"source byte count mismatch: {path}")
        if entry["release_bytes"] != len(release_data):
            raise ReleaseAssetError(f"release byte count mismatch: {path}")
        if entry["release_bytes"] > entry["source_bytes"]:
            raise ReleaseAssetError(f"release asset is larger than source: {path}")
        if entry["source_sha256"] != sha256_bytes(source_data):
            raise ReleaseAssetError(f"source SHA-256 mismatch: {path}")
        if entry["release_sha256"] != sha256_bytes(release_data):
            raise ReleaseAssetError(f"release SHA-256 mismatch: {path}")
        source_metadata = inspect_image_bytes(source_data, path)
        release_metadata = inspect_image_bytes(release_data, path)
        if release_metadata.size != source_metadata.size:
            raise ReleaseAssetError(f"release dimensions changed: {path}")
        if release_metadata.has_alpha != source_metadata.has_alpha:
            raise ReleaseAssetError(f"release alpha changed: {path}")
        if entry["transform"] == "copy" and release_data != source_data:
            raise ReleaseAssetError(f"copy transform does not preserve bytes: {path}")
        if entry["transform"] == "png-lossless" and source_metadata.format != "PNG":
            raise ReleaseAssetError(f"png-lossless source is not PNG: {path}")
        if entry["transform"] == f"jpeg-q{JPEG_QUALITY}" and source_metadata.format != "JPEG":
            raise ReleaseAssetError(f"jpeg-q{JPEG_QUALITY} source is not JPEG: {path}")
        transforms[entry["transform"]] += 1
        source_total += len(source_data)
        release_total += len(release_data)

    return ReleaseSummary(
        revision,
        len(entries),
        selection.old_count,
        selection.unreferenced_count,
        source_total,
        release_total,
        dict(sorted(transforms.items())),
    )


def print_summary(mode: str, summary: ReleaseSummary) -> None:
    print(f"[OK] release asset {mode} passed")
    print(f"source_revision: {summary.source_revision}")
    print(f"included: {summary.included_count}")
    print(f"excluded OLD: {summary.old_count}")
    print(f"excluded unreferenced: {summary.unreferenced_count}")
    print(f"source bytes: {summary.source_bytes}")
    if summary.release_bytes is not None:
        print(f"release bytes: {summary.release_bytes}")
    if summary.transforms:
        labels = ", ".join(f"{name}={count}" for name, count in summary.transforms.items())
        print(f"transforms: {labels}")
    if mode == "dry-run":
        print("no files written")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build compressed release-only copies of live referenced GUI images."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Validate and report without writing dist.")
    mode.add_argument("--verify", action="store_true", help="Verify an existing release output and manifest.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Must be dist/assets-overlay.")
    parser.add_argument(
        "--manifest",
        default=str(DEFAULT_MANIFEST),
        help="Must be dist/manifests/assets-manifest.json.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.dry_run:
            print_summary("dry-run", dry_run_release(ROOT))
        elif args.verify:
            print_summary("verify", verify_release(ROOT, args.output, args.manifest))
        else:
            print_summary("build", build_release(ROOT, args.output, args.manifest))
    except ReleaseAssetError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
