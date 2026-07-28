from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image


MODULE_PATH = Path(__file__).with_name("build_release_assets.py")
SPEC = importlib.util.spec_from_file_location("build_release_assets", MODULE_PATH)
if SPEC is None or SPEC.loader is None:  # pragma: no cover - import bootstrap guard.
    raise RuntimeError(f"cannot load {MODULE_PATH}")
builder = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = builder
SPEC.loader.exec_module(builder)


class ReleaseAssetBuilderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        (self.root / "07_gui_prototype" / "screen" / "assets").mkdir(parents=True)
        (self.root / "07_gui_prototype" / "screen" / "fixtures").mkdir(parents=True)
        (self.root / "03_engine" / "engine").mkdir(parents=True)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write(self, relative: str, content: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        return path

    def make_png(self, relative: str, color: tuple[int, int, int, int]) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        Image.new("RGBA", (64, 48), color).save(path, format="PNG", compress_level=0)
        return path

    def make_jpeg(self, relative: str) -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        image = Image.new("RGB", (96, 64))
        image.putdata(
            [
                ((x * 17 + y * 13) % 256, (x * 7 + y * 29) % 256, (x * 31 + y * 3) % 256)
                for y in range(image.height)
                for x in range(image.width)
            ]
        )
        image.save(path, format="JPEG", quality=95)
        return path

    def create_valid_fixture(self) -> tuple[Path, Path]:
        png = self.make_png(
            "07_gui_prototype/screen/assets/live.png",
            (20, 80, 140, 96),
        )
        jpeg = self.make_jpeg("07_gui_prototype/screen/assets/live.jpg")
        self.make_png("07_gui_prototype/screen/assets/unused.png", (4, 5, 6, 255))
        self.make_png("07_gui_prototype/screen/assets/OLD/retired.png", (7, 8, 9, 255))
        self.make_png("05_assets/reference-only.png", (10, 11, 12, 255))
        self.write(
            "07_gui_prototype/screen/styles.css",
            'body { background: url("./assets/live.png"); }\n'
            '/* url("./assets/OLD/retired.png") */\n',
        )
        self.write(
            "07_gui_prototype/screen/screen.js",
            'const portrait = "./assets/live.jpg";\n'
            '// const retired = "./assets/OLD/retired.png";\n',
        )
        self.write(
            "07_gui_prototype/screen/fixtures/default.json",
            '{"image": "./assets/live.png"}\n',
        )
        self.write(
            "07_gui_prototype/screen/assets/review.meta.json",
            '{"source": "./OLD/missing.png", "preview": "C:/Temp/missing.png"}\n',
        )
        self.write(
            "03_engine/engine/gui_screen_model.py",
            'LIVE_IMAGE = "./assets/live.jpg"\n',
        )
        return png, jpeg

    def test_selection_excludes_old_unreferenced_and_reference_material(self) -> None:
        self.create_valid_fixture()
        selection = builder.select_release_assets(self.root)
        paths = [builder.relative_posix(path, self.root) for path in selection.assets]
        self.assertEqual(
            paths,
            [
                "07_gui_prototype/screen/assets/live.jpg",
                "07_gui_prototype/screen/assets/live.png",
            ],
        )
        self.assertEqual(selection.old_count, 1)
        self.assertEqual(selection.unreferenced_count, 1)
        self.assertGreaterEqual(selection.source_files_scanned, 5)
        self.assertGreaterEqual(selection.literal_references_scanned, 4)

    def test_old_reference_fails_with_exact_source(self) -> None:
        self.make_png("07_gui_prototype/screen/assets/OLD/retired.png", (1, 2, 3, 255))
        self.write(
            "07_gui_prototype/screen/screen.js",
            'const image = "./assets/OLD/retired.png";\n',
        )
        with self.assertRaises(builder.ReleaseAssetError) as caught:
            builder.select_release_assets(self.root)
        message = str(caught.exception)
        self.assertIn("OLD: 07_gui_prototype/screen/screen.js:1", message)
        self.assertIn("./assets/OLD/retired.png", message)

    def test_missing_reference_fails_with_expected_path(self) -> None:
        self.write(
            "07_gui_prototype/screen/styles.css",
            'body { background: url("./assets/missing.png"); }\n',
        )
        with self.assertRaises(builder.ReleaseAssetError) as caught:
            builder.select_release_assets(self.root)
        message = str(caught.exception)
        self.assertIn("MISSING: 07_gui_prototype/screen/styles.css:1", message)
        self.assertIn("07_gui_prototype/screen/assets/missing.png", message)

    def test_build_verify_and_manifest_are_deterministic(self) -> None:
        png, jpeg = self.create_valid_fixture()
        original_hashes = {path: builder.sha256_file(path) for path in (png, jpeg)}

        dry_run = builder.dry_run_release(self.root, source_revision="test-revision")
        self.assertEqual(dry_run.included_count, 2)
        self.assertFalse((self.root / "dist").exists())

        summary = builder.build_release(self.root, source_revision="test-revision")
        self.assertLessEqual(summary.release_bytes or 0, summary.source_bytes)
        manifest_path = self.root / builder.DEFAULT_MANIFEST
        first_manifest = manifest_path.read_bytes()
        payload = json.loads(first_manifest)
        paths = [entry["path"] for entry in payload["files"]]
        self.assertEqual(paths, sorted(paths))
        self.assertEqual(payload["source_revision"], "test-revision")
        self.assertEqual(payload["excluded"], {"old_count": 1, "unreferenced_count": 1})
        self.assertEqual({entry["transform"] for entry in payload["files"]}, {"jpeg-q82", "png-lossless"})
        self.assertTrue(all(entry["release_bytes"] <= entry["source_bytes"] for entry in payload["files"]))

        verified = builder.verify_release(self.root, source_revision="test-revision")
        self.assertEqual(verified.included_count, 2)
        self.assertEqual(original_hashes, {path: builder.sha256_file(path) for path in (png, jpeg)})

        builder.build_release(self.root, source_revision="test-revision")
        self.assertEqual(first_manifest, manifest_path.read_bytes())

    def test_verify_rejects_unmanifested_output(self) -> None:
        self.create_valid_fixture()
        builder.build_release(self.root, source_revision="test-revision")
        extra = self.root / "dist" / "assets-overlay" / "app" / "unexpected.png"
        extra.write_bytes(b"not an image")
        with self.assertRaisesRegex(builder.ReleaseAssetError, "release output mismatch"):
            builder.verify_release(self.root, source_revision="test-revision")

    def test_output_is_locked_to_ignored_release_location(self) -> None:
        self.create_valid_fixture()
        with self.assertRaisesRegex(builder.ReleaseAssetError, "output must be"):
            builder.build_release(
                self.root,
                output=self.root / "elsewhere",
                source_revision="test-revision",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
