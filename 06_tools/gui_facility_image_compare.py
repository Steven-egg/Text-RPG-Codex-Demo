from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

try:
    from PIL import Image, ImageDraw, ImageFont, UnidentifiedImageError
except Exception as exc:  # pragma: no cover - depends on local tooling.
    Image = None  # type: ignore[assignment]
    ImageDraw = None  # type: ignore[assignment]
    ImageFont = None  # type: ignore[assignment]
    UnidentifiedImageError = OSError  # type: ignore[assignment]
    PIL_IMPORT_ERROR: Exception | None = exc
else:
    PIL_IMPORT_ERROR = None


DEFAULT_EXPECTED_SIZE = (1672, 941)


class ToolError(RuntimeError):
    pass


def clamp_float(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


def clamp_int(value: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(maximum, value))


@dataclass(frozen=True)
class ImageInfo:
    path: Path
    width: int
    height: int
    mode: str
    pil_format: str | None
    content_kind: str
    suffix: str
    sha256: str

    def to_json(self) -> dict[str, Any]:
        return {
            "path": display_path(self.path),
            "width": self.width,
            "height": self.height,
            "mode": self.mode,
            "pil_format": self.pil_format,
            "content_kind": self.content_kind,
            "suffix": self.suffix,
            "sha256": self.sha256,
        }


@dataclass(frozen=True)
class ReviewBox:
    label: str
    x: float
    y: float
    width: float
    height: float
    kind: str = "blocking"
    opacity: float = 0.68
    color: tuple[int, int, int] = (8, 9, 11)

    def clamp(self) -> "ReviewBox":
        x1 = clamp_float(self.x, 0.0, 1.0)
        y1 = clamp_float(self.y, 0.0, 1.0)
        x2 = clamp_float(self.x + self.width, 0.0, 1.0)
        y2 = clamp_float(self.y + self.height, 0.0, 1.0)
        return ReviewBox(
            label=self.label,
            x=x1,
            y=y1,
            width=max(0.0, x2 - x1),
            height=max(0.0, y2 - y1),
            kind=self.kind,
            opacity=self.opacity,
            color=self.color,
        )

    def to_pixels(self, size: tuple[int, int]) -> tuple[int, int, int, int]:
        width, height = size
        box = self.clamp()
        left = round(box.x * width)
        top = round(box.y * height)
        right = round((box.x + box.width) * width)
        bottom = round((box.y + box.height) * height)
        return left, top, right, bottom

    def to_json(self) -> dict[str, Any]:
        return {
            "label": self.label,
            "x": round(self.x, 6),
            "y": round(self.y, 6),
            "width": round(self.width, 6),
            "height": round(self.height, 6),
            "kind": self.kind,
        }


def display_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(resolved)


def parse_size(value: str) -> tuple[int, int] | None:
    if value.lower() in {"none", "off", "any"}:
        return None
    match = re.fullmatch(r"(\d+)x(\d+)", value.strip().lower())
    if not match:
        raise argparse.ArgumentTypeError("expected size must look like 1672x941 or none")
    return int(match.group(1)), int(match.group(2))


def parse_pair(value: str) -> tuple[float, float]:
    parts = [part.strip() for part in value.split(",")]
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("expected two comma-separated values, e.g. 0.5,0.5")
    try:
        first, second = float(parts[0]), float(parts[1])
    except ValueError as exc:
        raise argparse.ArgumentTypeError("pair values must be numbers") from exc
    return first, second


def parse_review_box(value: str) -> ReviewBox:
    parts = [part.strip() for part in value.split(",")]
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("expected x,y,width,height in normalized 0..1 units")
    try:
        x, y, width, height = (float(part) for part in parts)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("box values must be numbers") from exc
    if width <= 0 or height <= 0:
        raise argparse.ArgumentTypeError("box width and height must be positive")
    return ReviewBox("box", x, y, width, height)


def parse_named_review_box(value: str) -> ReviewBox:
    if ":" not in value:
        box = parse_review_box(value)
        return ReviewBox("focus", box.x, box.y, box.width, box.height)
    label, raw_box = value.split(":", 1)
    box = parse_review_box(raw_box)
    return ReviewBox(label.strip() or "focus", box.x, box.y, box.width, box.height)


def safe_slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", value.strip()).strip("-._")
    return slug or "comparison"


def preset_box(
    label: str,
    x: float,
    y: float,
    width: float,
    height: float,
    *,
    kind: str = "blocking",
    opacity: float = 0.68,
    color: tuple[int, int, int] = (8, 9, 11),
) -> ReviewBox:
    return ReviewBox(label, x, y, width, height, kind=kind, opacity=opacity, color=color)


CSS_MASK_PRESETS: dict[str, list[ReviewBox]] = {
    "none": [],
    "npc-facility": [
        preset_box("title/header", 0.02, 0.02, 0.48, 0.10, kind="soft", opacity=0.50),
        preset_box("left catalog/list", 0.02, 0.16, 0.31, 0.69),
        preset_box("center detail", 0.35, 0.16, 0.31, 0.69),
        preset_box("bottom action/dialogue", 0.02, 0.85, 0.96, 0.13),
    ],
    "dialogue-service": [
        preset_box("title/header", 0.01, 0.02, 0.48, 0.09, kind="soft", opacity=0.50),
        preset_box("bottom dialogue/actions", 0.01, 0.83, 0.98, 0.15),
    ],
    "workshop": [
        preset_box("title/header", 0.14, 0.02, 0.48, 0.07, kind="soft", opacity=0.50),
        preset_box("left tabs/list", 0.14, 0.11, 0.23, 0.72),
        preset_box("center panels", 0.38, 0.11, 0.30, 0.72),
        preset_box("right dialogue", 0.69, 0.62, 0.17, 0.20),
        preset_box("bottom action bar", 0.14, 0.84, 0.72, 0.13),
    ],
    "wide-shop": [
        preset_box("title/header", 0.01, 0.02, 0.48, 0.09, kind="soft", opacity=0.50),
        preset_box("left browser", 0.01, 0.20, 0.29, 0.62),
        preset_box("center detail", 0.31, 0.20, 0.30, 0.62),
        preset_box("requirement/footer band", 0.01, 0.83, 0.98, 0.15),
    ],
    "synthesis": [
        preset_box("title/header", 0.04, 0.02, 0.47, 0.10, kind="soft", opacity=0.50),
        preset_box("left recipe list", 0.04, 0.20, 0.29, 0.62),
        preset_box("center detail", 0.34, 0.20, 0.32, 0.62),
        preset_box("bottom action/dialogue", 0.04, 0.84, 0.92, 0.13),
    ],
    "storage": [
        preset_box("title/header", 0.07, 0.02, 0.50, 0.11, kind="soft", opacity=0.50),
        preset_box("resource strip", 0.07, 0.14, 0.86, 0.04, kind="soft", opacity=0.45),
        preset_box("left inventory", 0.07, 0.18, 0.27, 0.66),
        preset_box("center transfer", 0.35, 0.18, 0.31, 0.66),
        preset_box("right storage", 0.67, 0.18, 0.26, 0.66),
        preset_box("bottom action bar", 0.07, 0.85, 0.86, 0.12),
    ],
    "relic-preview": [
        preset_box("title/header", 0.02, 0.03, 0.45, 0.10, kind="soft", opacity=0.50),
        preset_box("left slots", 0.02, 0.15, 0.30, 0.70),
        preset_box("center focus", 0.34, 0.15, 0.34, 0.70, kind="soft", opacity=0.42),
        preset_box("right tablet", 0.70, 0.15, 0.28, 0.70),
        preset_box("bottom action bar", 0.02, 0.87, 0.96, 0.10),
    ],
}


SCREEN_PRESET_ALIASES: dict[str, str] = {
    "guild_screen": "npc-facility",
    "inn_screen": "dialogue-service",
    "magic_shop_screen": "wide-shop",
    "synthesis_screen": "synthesis",
    "temple_screen": "npc-facility",
    "workshop_screen": "workshop",
    "storage_screen": "storage",
    "relic_preview_screen": "relic-preview",
}


def resolve_css_preset(screen: str, requested: str) -> str:
    if requested == "auto":
        return SCREEN_PRESET_ALIASES.get(screen, "npc-facility")
    return requested


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def content_kind(path: Path) -> str:
    header = path.read_bytes()[:16]
    if header.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if header.startswith(b"\xff\xd8\xff"):
        return "jpeg"
    if header.startswith(b"GIF87a") or header.startswith(b"GIF89a"):
        return "gif"
    if header[:4] == b"RIFF" and header[8:12] == b"WEBP":
        return "webp"
    return "unknown"


def inspect_image(path: Path) -> ImageInfo:
    if Image is None:
        raise ToolError(f"Pillow is required but unavailable: {PIL_IMPORT_ERROR}")
    if not path.exists():
        raise ToolError(f"missing image: {path}")
    if not path.is_file():
        raise ToolError(f"not a file: {path}")
    try:
        with Image.open(path) as img:
            width, height = img.size
            mode = img.mode
            pil_format = img.format
    except UnidentifiedImageError as exc:
        raise ToolError(f"cannot identify image: {path}") from exc
    return ImageInfo(
        path=path.resolve(),
        width=width,
        height=height,
        mode=mode,
        pil_format=pil_format,
        content_kind=content_kind(path),
        suffix=path.suffix.lower(),
        sha256=sha256_file(path),
    )


def load_rgba(path: Path):
    if Image is None:
        raise ToolError(f"Pillow is required but unavailable: {PIL_IMPORT_ERROR}")
    with Image.open(path) as img:
        return img.convert("RGBA")


def normalized_area(box: ReviewBox) -> float:
    clamped = box.clamp()
    return clamped.width * clamped.height


def overlap_area(first: ReviewBox, second: ReviewBox) -> float:
    a = first.clamp()
    b = second.clamp()
    left = max(a.x, b.x)
    top = max(a.y, b.y)
    right = min(a.x + a.width, b.x + b.width)
    bottom = min(a.y + a.height, b.y + b.height)
    if right <= left or bottom <= top:
        return 0.0
    return (right - left) * (bottom - top)


def box_inside_frame(box: ReviewBox) -> bool:
    return (
        box.x >= 0
        and box.y >= 0
        and box.x + box.width <= 1
        and box.y + box.height <= 1
    )


def crop_to_target_aspect(
    img,
    target_size: tuple[int, int],
    crop_center: tuple[float, float],
    crop_zoom: float,
    crop_window: ReviewBox | None,
):
    if crop_zoom < 1.0:
        raise ToolError("--crop-zoom must be 1.0 or larger")
    target_width, target_height = target_size
    target_aspect = target_width / target_height
    image_width, image_height = img.size

    if crop_window is not None:
        window = crop_window.clamp()
        crop_width = clamp_int(round(window.width * image_width), 1, image_width)
        crop_height = clamp_int(round(window.height * image_height), 1, image_height)
        crop_aspect = crop_width / crop_height
        if abs(crop_aspect - target_aspect) / target_aspect > 0.01:
            raise ToolError(
                "--crop-window aspect must match the target aspect; "
                f"got {crop_aspect:.3f}, expected {target_aspect:.3f}"
            )
        left = clamp_int(round(window.x * image_width), 0, image_width - crop_width)
        top = clamp_int(round(window.y * image_height), 0, image_height - crop_height)
    elif image_width / image_height >= target_aspect:
        base_crop_height = image_height
        base_crop_width = round(base_crop_height * target_aspect)
        crop_width = clamp_int(round(base_crop_width / crop_zoom), 1, image_width)
        crop_height = clamp_int(round(crop_width / target_aspect), 1, image_height)
        center_x = clamp_float(crop_center[0], 0.0, 1.0) * image_width
        center_y = clamp_float(crop_center[1], 0.0, 1.0) * image_height
        left = clamp_int(round(center_x - crop_width / 2), 0, image_width - crop_width)
        top = clamp_int(round(center_y - crop_height / 2), 0, image_height - crop_height)
    else:
        base_crop_width = image_width
        base_crop_height = round(base_crop_width / target_aspect)
        crop_height = clamp_int(round(base_crop_height / crop_zoom), 1, image_height)
        crop_width = clamp_int(round(crop_height * target_aspect), 1, image_width)
        center_x = clamp_float(crop_center[0], 0.0, 1.0) * image_width
        center_y = clamp_float(crop_center[1], 0.0, 1.0) * image_height
        left = clamp_int(round(center_x - crop_width / 2), 0, image_width - crop_width)
        top = clamp_int(round(center_y - crop_height / 2), 0, image_height - crop_height)

    right = left + crop_width
    bottom = top + crop_height
    cropped = img.crop((left, top, right, bottom))
    if cropped.size != target_size:
        cropped = cropped.resize(target_size, Image.Resampling.LANCZOS)
    crop_meta = {
        "mode": "overscan_crop",
        "source_width": image_width,
        "source_height": image_height,
        "target_width": target_width,
        "target_height": target_height,
        "crop_box_px": {
            "left": left,
            "top": top,
            "right": right,
            "bottom": bottom,
            "width": crop_width,
            "height": crop_height,
        },
        "crop_box_normalized": {
            "x": round(left / image_width, 6),
            "y": round(top / image_height, 6),
            "width": round(crop_width / image_width, 6),
            "height": round(crop_height / image_height, 6),
        },
        "crop_center": {
            "x": round(crop_center[0], 6),
            "y": round(crop_center[1], 6),
        },
        "crop_zoom": crop_zoom,
    }
    return cropped, crop_meta


def prepare_candidate_image(candidate, base_size: tuple[int, int], args: argparse.Namespace):
    if args.overscan_crop:
        return crop_to_target_aspect(
            candidate,
            base_size,
            args.crop_center,
            args.crop_zoom,
            args.crop_window,
        )
    if candidate.size != base_size and args.allow_resize:
        resized = candidate.resize(base_size, Image.Resampling.LANCZOS)
        return resized, {
            "mode": "resize",
            "source_width": candidate.width,
            "source_height": candidate.height,
            "target_width": base_size[0],
            "target_height": base_size[1],
        }
    return candidate.copy(), {
        "mode": "none",
        "source_width": candidate.width,
        "source_height": candidate.height,
        "target_width": base_size[0],
        "target_height": base_size[1],
    }


def validate_inputs(
    base_info: ImageInfo,
    candidate_info: ImageInfo,
    expected_size: tuple[int, int] | None,
    allow_resize: bool,
    overscan_crop: bool,
) -> list[str]:
    warnings: list[str] = []
    base_size = (base_info.width, base_info.height)
    candidate_size = (candidate_info.width, candidate_info.height)
    if expected_size and base_size != expected_size:
        raise ToolError(
            f"base size {base_size[0]}x{base_size[1]} does not match expected "
            f"{expected_size[0]}x{expected_size[1]}"
        )
    if expected_size and candidate_size != expected_size and not allow_resize and not overscan_crop:
        raise ToolError(
            f"candidate size {candidate_size[0]}x{candidate_size[1]} does not match "
            f"expected {expected_size[0]}x{expected_size[1]}"
        )
    if base_size != candidate_size and not allow_resize and not overscan_crop:
        raise ToolError(
            f"image sizes differ: base {base_size[0]}x{base_size[1]}, "
            f"candidate {candidate_size[0]}x{candidate_size[1]}; use --allow-resize "
            "or --overscan-crop only when the crop is intentional"
        )
    if base_info.suffix == ".jpg" and base_info.content_kind == "png":
        warnings.append("base has .jpg suffix but PNG file content")
    if candidate_info.suffix == ".jpg" and candidate_info.content_kind == "png":
        warnings.append("candidate has .jpg suffix but PNG file content")
    if base_size != candidate_size and allow_resize:
        warnings.append("candidate resized to base dimensions for comparison outputs")
    if base_size != candidate_size and overscan_crop:
        warnings.append("candidate overscan-cropped to base dimensions for comparison outputs")
    return warnings


def output_paths(out_dir: Path, prefix: str, opacity: float, include_css_preview: bool) -> dict[str, Path]:
    opacity_label = f"{round(opacity * 100):02d}"
    paths = {
        "before": out_dir / f"{prefix}.before.png",
        "candidate": out_dir / f"{prefix}.candidate.png",
        "overlay": out_dir / f"{prefix}.overlay-{opacity_label}.png",
        "contact_sheet": out_dir / f"{prefix}.contact-sheet.png",
        "manifest": out_dir / f"{prefix}.manifest.json",
    }
    if include_css_preview:
        paths["css_preview"] = out_dir / f"{prefix}.css-preview.png"
    return paths


def ensure_writable_outputs(paths: dict[str, Path], inputs: set[Path], overwrite: bool) -> None:
    for label, path in paths.items():
        resolved = path.resolve()
        if resolved in inputs:
            raise ToolError(f"refusing to overwrite input image as {label}: {path}")
        if resolved.exists() and not overwrite:
            raise ToolError(f"output already exists, pass --overwrite to replace: {path}")


def flatten_for_png(img):
    if Image is None:
        raise ToolError(f"Pillow is required but unavailable: {PIL_IMPORT_ERROR}")
    rgba = img.convert("RGBA") if img.mode != "RGBA" else img
    background = Image.new("RGBA", img.size, (0, 0, 0, 255))
    background.alpha_composite(rgba)
    return background.convert("RGB")


def make_overlay(base, candidate, opacity: float):
    return Image.blend(base, candidate, opacity)


def fit_image(img, target_width: int):
    if target_width <= 0:
        raise ToolError("--sheet-panel-width must be positive")
    if img.width <= target_width:
        return img.copy()
    height = round(img.height * (target_width / img.width))
    return img.resize((target_width, height), Image.Resampling.LANCZOS)


def labeled_panel(img, label: str, detail: str, panel_width: int):
    fitted = fit_image(flatten_for_png(img), panel_width)
    label_height = 44
    panel = Image.new("RGB", (fitted.width, fitted.height + label_height), (15, 17, 21))
    panel.paste(fitted, (0, label_height))
    draw = ImageDraw.Draw(panel)
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None
    draw.rectangle((0, 0, panel.width, label_height), fill=(24, 27, 34))
    draw.text((12, 8), label, fill=(235, 229, 216), font=font)
    if detail:
        draw.text((12, 25), detail, fill=(164, 154, 132), font=font)
    return panel


def make_contact_sheet(base, candidate, overlay, opacity: float, panel_width: int, css_preview=None):
    panels = [
        labeled_panel(base, "BEFORE", "current/reference", panel_width),
        labeled_panel(candidate, "CANDIDATE", "cropped/proposed image", panel_width),
        labeled_panel(overlay, "OVERLAY", f"candidate {round(opacity * 100)}%", panel_width),
    ]
    if css_preview is not None:
        panels.append(labeled_panel(css_preview, "CSS PREVIEW", "panel mask + safety boxes", panel_width))
    gap = 12
    width = sum(panel.width for panel in panels) + gap * (len(panels) - 1)
    height = max(panel.height for panel in panels)
    sheet = Image.new("RGB", (width, height), (8, 9, 11))
    x = 0
    for panel in panels:
        sheet.paste(panel, (x, 0))
        x += panel.width + gap
    return sheet


def draw_box_label(draw, xy: tuple[int, int, int, int], label: str, fill: tuple[int, int, int]) -> None:
    try:
        font = ImageFont.load_default()
    except Exception:
        font = None
    left, top, right, _bottom = xy
    label_width = max(70, len(label) * 7 + 12)
    label_bottom = min(top + 18, _bottom)
    draw.rectangle((left, top, min(right, left + label_width), label_bottom), fill=fill)
    draw.text((left + 5, top + 4), label, fill=(238, 232, 218), font=font)


def draw_review_box(draw, box: ReviewBox, size: tuple[int, int], outline: tuple[int, int, int], label: str) -> None:
    xy = box.to_pixels(size)
    draw.rectangle(xy, outline=outline, width=3)
    draw_box_label(draw, xy, label, outline)


def calculate_subject_check(
    subject: ReviewBox,
    masks: list[ReviewBox],
    threshold: float,
) -> dict[str, Any]:
    blocking_masks = [mask for mask in masks if mask.kind == "blocking"]
    area = normalized_area(subject)
    overlap = 0.0
    overlapped_masks: list[str] = []
    if area > 0:
        for mask in blocking_masks:
            mask_overlap = overlap_area(subject, mask)
            if mask_overlap > 0:
                overlap += mask_overlap
                overlapped_masks.append(mask.label)
    overlap_ratio = 1.0 if area <= 0 else min(1.0, overlap / area)
    inside_frame = box_inside_frame(subject)
    return {
        "box": subject.to_json(),
        "inside_frame": inside_frame,
        "blocking_overlap_ratio": round(overlap_ratio, 4),
        "threshold": threshold,
        "overlapped_masks": overlapped_masks,
        "passed": inside_frame and overlap_ratio <= threshold,
    }


def build_review_checks(
    masks: list[ReviewBox],
    face_box: ReviewBox | None,
    torso_box: ReviewBox | None,
    focus_box: ReviewBox | None,
    face_threshold: float,
    torso_threshold: float,
    focus_threshold: float,
) -> dict[str, Any]:
    checks: dict[str, Any] = {
        "face": None,
        "torso": None,
        "focus": None,
        "passed": None,
    }
    subject_results: list[dict[str, Any]] = []
    if face_box is not None:
        face = ReviewBox("face", face_box.x, face_box.y, face_box.width, face_box.height)
        checks["face"] = calculate_subject_check(face, masks, face_threshold)
        subject_results.append(checks["face"])
    if torso_box is not None:
        torso = ReviewBox("torso", torso_box.x, torso_box.y, torso_box.width, torso_box.height)
        checks["torso"] = calculate_subject_check(torso, masks, torso_threshold)
        subject_results.append(checks["torso"])
    if focus_box is not None:
        focus = ReviewBox(focus_box.label, focus_box.x, focus_box.y, focus_box.width, focus_box.height)
        checks["focus"] = calculate_subject_check(focus, masks, focus_threshold)
        subject_results.append(checks["focus"])
    if subject_results:
        checks["passed"] = all(result["passed"] for result in subject_results)
    return checks


def make_css_preview(
    candidate,
    masks: list[ReviewBox],
    face_box: ReviewBox | None,
    torso_box: ReviewBox | None,
    focus_box: ReviewBox | None,
):
    preview = flatten_for_png(candidate).convert("RGBA")
    overlay = Image.new("RGBA", preview.size, (0, 0, 0, 0))
    draw_overlay = ImageDraw.Draw(overlay)
    for mask in masks:
        left, top, right, bottom = mask.to_pixels(preview.size)
        red, green, blue = mask.color
        alpha = round(mask.opacity * 255)
        draw_overlay.rectangle((left, top, right, bottom), fill=(red, green, blue, alpha))
        outline = (235, 209, 155, 210) if mask.kind == "blocking" else (112, 163, 214, 185)
        draw_overlay.rectangle((left, top, right, bottom), outline=outline, width=2)
        draw_box_label(draw_overlay, (left, top, right, bottom), mask.label, outline[:3])

    preview.alpha_composite(overlay)
    draw = ImageDraw.Draw(preview)
    if face_box is not None:
        draw_review_box(draw, ReviewBox("face", face_box.x, face_box.y, face_box.width, face_box.height), preview.size, (127, 208, 111), "face")
    if torso_box is not None:
        draw_review_box(draw, ReviewBox("torso", torso_box.x, torso_box.y, torso_box.width, torso_box.height), preview.size, (91, 163, 248), "torso")
    if focus_box is not None:
        draw_review_box(draw, focus_box, preview.size, (243, 190, 83), focus_box.label)
    return preview.convert("RGB")


def write_manifest(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def compare_images(args: argparse.Namespace) -> dict[str, Any]:
    if not 0.0 <= args.opacity <= 1.0:
        raise ToolError("--opacity must be between 0 and 1")
    if (
        args.face_max_mask_overlap < 0
        or args.torso_max_mask_overlap < 0
        or args.focus_max_mask_overlap < 0
    ):
        raise ToolError("mask overlap thresholds must be non-negative")

    base_path = Path(args.base).resolve()
    candidate_path = Path(args.candidate).resolve()
    out_dir = Path(args.out_dir).resolve()
    expected_size = args.expected_size
    prefix_seed = args.label or args.screen or candidate_path.stem
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    prefix = f"{timestamp}-{safe_slug(prefix_seed)}"

    base_info = inspect_image(base_path)
    candidate_info = inspect_image(candidate_path)
    warnings = validate_inputs(
        base_info,
        candidate_info,
        expected_size,
        args.allow_resize,
        args.overscan_crop,
    )

    resolved_css_preset = resolve_css_preset(args.screen, args.css_preset)
    if resolved_css_preset not in CSS_MASK_PRESETS:
        raise ToolError(
            f"unknown CSS preset: {resolved_css_preset}; choose one of "
            f"{', '.join(sorted(CSS_MASK_PRESETS))} or auto"
        )
    css_masks = CSS_MASK_PRESETS[resolved_css_preset]
    include_css_preview = resolved_css_preset != "none"

    paths = output_paths(out_dir, prefix, args.opacity, include_css_preview)
    ensure_writable_outputs(paths, {base_path, candidate_path}, args.overwrite)
    out_dir.mkdir(parents=True, exist_ok=True)

    base = load_rgba(base_path)
    candidate = load_rgba(candidate_path)
    candidate, crop_meta = prepare_candidate_image(candidate, base.size, args)

    overlay = make_overlay(base, candidate, args.opacity)
    review_checks = build_review_checks(
        css_masks,
        args.face_box,
        args.torso_box,
        args.focus_box,
        args.face_max_mask_overlap,
        args.torso_max_mask_overlap,
        args.focus_max_mask_overlap,
    )
    css_preview = (
        make_css_preview(candidate, css_masks, args.face_box, args.torso_box, args.focus_box)
        if include_css_preview
        else None
    )
    contact_sheet = make_contact_sheet(
        base,
        candidate,
        overlay,
        args.opacity,
        args.sheet_panel_width,
        css_preview,
    )

    flatten_for_png(base).save(paths["before"])
    flatten_for_png(candidate).save(paths["candidate"])
    flatten_for_png(overlay).save(paths["overlay"])
    if css_preview is not None:
        css_preview.save(paths["css_preview"])
    contact_sheet.save(paths["contact_sheet"])

    outputs = {key: display_path(value) for key, value in paths.items()}
    manifest: dict[str, Any] = {
        "version": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "tool": display_path(Path(__file__)),
        "screen": args.screen,
        "label": args.label,
        "opacity": args.opacity,
        "expected_size": (
            None
            if expected_size is None
            else {"width": expected_size[0], "height": expected_size[1]}
        ),
        "allow_resize": args.allow_resize,
        "overscan_crop": args.overscan_crop,
        "crop": crop_meta,
        "css_preview": {
            "preset": resolved_css_preset,
            "masks": [mask.to_json() for mask in css_masks],
        },
        "restore_required": False,
        "inputs": {
            "base": base_info.to_json(),
            "candidate": candidate_info.to_json(),
        },
        "checks": {
            "base_candidate_dimensions_match": (
                base_info.width == candidate_info.width
                and base_info.height == candidate_info.height
            ),
            "prepared_candidate_dimensions_match": candidate.size == base.size,
            "review": review_checks,
            "outputs_overwrite_inputs": False,
        },
        "warnings": warnings,
        "outputs": outputs,
    }
    write_manifest(paths["manifest"], manifest)
    return manifest


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create non-destructive before/candidate/overlay/contact-sheet "
            "outputs for GUI facility image comparison."
        )
    )
    parser.add_argument("--base", required=True, help="Current/reference image path.")
    parser.add_argument("--candidate", required=True, help="Candidate image path.")
    parser.add_argument("--out-dir", required=True, help="Directory for generated comparison outputs.")
    parser.add_argument("--screen", default="", help="Optional screen id, e.g. guild_screen.")
    parser.add_argument("--label", default="", help="Optional filename label for this comparison.")
    parser.add_argument(
        "--opacity",
        type=float,
        default=0.55,
        help="Candidate opacity for overlay output, from 0 to 1. Default: 0.55.",
    )
    parser.add_argument(
        "--expected-size",
        type=parse_size,
        default=DEFAULT_EXPECTED_SIZE,
        help="Expected WxH such as 1672x941, or none. Default: 1672x941.",
    )
    parser.add_argument(
        "--allow-resize",
        action="store_true",
        help="Resize candidate to base size for outputs when dimensions differ.",
    )
    parser.add_argument(
        "--overscan-crop",
        action="store_true",
        help=(
            "Crop a wider/taller candidate to the base aspect before comparison. "
            "Use this for 18:9 or 20:9 overscan masters."
        ),
    )
    parser.add_argument(
        "--crop-center",
        type=parse_pair,
        default=(0.5, 0.5),
        help="Normalized crop center for --overscan-crop, e.g. 0.55,0.5. Default: 0.5,0.5.",
    )
    parser.add_argument(
        "--crop-zoom",
        type=float,
        default=1.0,
        help="Crop zoom for --overscan-crop. 1.0 uses the widest fitting crop. Default: 1.0.",
    )
    parser.add_argument(
        "--crop-window",
        type=parse_review_box,
        default=None,
        help=(
            "Optional normalized crop window x,y,width,height on the candidate; "
            "overrides --crop-center and --crop-zoom."
        ),
    )
    parser.add_argument(
        "--css-preset",
        default="none",
        choices=sorted([*CSS_MASK_PRESETS.keys(), "auto"]),
        help=(
            "Add CSS panel mask preview. Use auto to map --screen to a preset. "
            "Default: none."
        ),
    )
    parser.add_argument(
        "--face-box",
        type=parse_review_box,
        default=None,
        help="Optional normalized face box x,y,width,height on the final 16:9 candidate.",
    )
    parser.add_argument(
        "--torso-box",
        type=parse_review_box,
        default=None,
        help="Optional normalized torso box x,y,width,height on the final 16:9 candidate.",
    )
    parser.add_argument(
        "--focus-box",
        type=parse_named_review_box,
        default=None,
        help="Optional normalized focus box label:x,y,width,height for no-NPC facilities.",
    )
    parser.add_argument(
        "--face-max-mask-overlap",
        type=float,
        default=0.02,
        help="Maximum allowed face overlap ratio with blocking masks. Default: 0.02.",
    )
    parser.add_argument(
        "--torso-max-mask-overlap",
        type=float,
        default=0.18,
        help="Maximum allowed torso overlap ratio with blocking masks. Default: 0.18.",
    )
    parser.add_argument(
        "--focus-max-mask-overlap",
        type=float,
        default=0.35,
        help="Maximum allowed focus overlap ratio with blocking masks. Default: 0.35.",
    )
    parser.add_argument(
        "--sheet-panel-width",
        type=int,
        default=560,
        help="Maximum width for each contact sheet panel. Default: 560.",
    )
    parser.add_argument("--overwrite", action="store_true", help="Replace existing output files.")
    parser.add_argument("--json", action="store_true", help="Emit JSON manifest summary.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        manifest = compare_images(args)
    except ToolError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
    else:
        print("Generated GUI image comparison outputs:")
        for label, path in manifest["outputs"].items():
            print(f"- {label}: {path}")
        for warning in manifest["warnings"]:
            print(f"[WARN] {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
