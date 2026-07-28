from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


TOOLS_ROOT = Path(__file__).resolve().parent
if str(TOOLS_ROOT) not in sys.path:
    sys.path.insert(0, str(TOOLS_ROOT))


def load_module(name: str, filename: str):
    path = TOOLS_ROOT / filename
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:  # pragma: no cover
        raise RuntimeError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


builder = load_module("build_windows_portable", "build_windows_portable.py")
launcher = load_module("portable_gui_launcher_test", "portable_gui_launcher.py")


class WindowsPortableTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.runtime = self.root / "runtime-source"
        self.runtime.mkdir()
        self.write_runtime("python.exe", b"fake-python")
        self.write_runtime("LICENSE.txt", b"runtime license")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def write(self, relative: str, data: str | bytes = "") -> Path:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(data, bytes):
            path.write_bytes(data)
        else:
            path.write_text(data, encoding="utf-8", newline="\n")
        return path

    def write_runtime(self, relative: str, data: bytes) -> Path:
        path = self.runtime / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def create_program_fixture(self) -> None:
        self.write("element_maze.py", "print('smoke')\n")
        self.write("requirements.txt", "rich==15.0.0\n")
        self.write("06_tools/gui_runtime_bridge.py", "# bridge\n")
        self.write("06_tools/portable_gui_launcher.py", "# launcher\n")
        self.write("03_engine/engine/__init__.py")
        self.write("03_engine/engine/game.py")
        self.write("04_data/data/__init__.py")
        self.write("04_data/data/jobs.py")
        self.write("07_gui_prototype/start_screen/index.html", "<main></main>\n")
        self.write("07_gui_prototype/start_screen/styles.css", "body {}\n")
        self.write("07_gui_prototype/start_screen/start-screen.js", "export {};\n")
        self.write("07_gui_prototype/start_screen/fixtures/start.json", "{}\n")

    def fake_s4_build(self, root: Path, *_args, **_kwargs):
        image_path = "07_gui_prototype/start_screen/assets/live.png"
        self.write(f"dist/assets-overlay/app/{image_path}", b"release-image")
        payload = {
            "format_version": 1,
            "source_revision": "test-revision",
            "asset_root": "app",
            "files": [
                {
                    "path": image_path,
                    "source_sha256": "0" * 64,
                    "release_sha256": "1" * 64,
                    "source_bytes": 20,
                    "release_bytes": 13,
                    "transform": "copy",
                }
            ],
            "excluded": {"old_count": 1, "unreferenced_count": 2},
        }
        self.write(
            "dist/manifests/assets-manifest.json",
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        )
        return SimpleNamespace(included_count=1, source_revision="test-revision")

    def test_program_selection_is_allowlisted_and_image_free(self) -> None:
        self.create_program_fixture()
        self.write("07_gui_prototype/start_screen/assets/live.png", b"original")
        self.write("07_gui_prototype/start_screen/assets/review.meta.json", "{}\n")
        self.write("07_gui_prototype/start_screen/OLD/retired.js", "bad\n")
        self.write("05_assets/reference.png", b"reference")
        paths = [builder.relative_posix(path, self.root) for path in builder.select_program_sources(self.root)]
        self.assertIn("07_gui_prototype/start_screen/index.html", paths)
        self.assertNotIn("07_gui_prototype/start_screen/assets/live.png", paths)
        self.assertNotIn("07_gui_prototype/start_screen/assets/review.meta.json", paths)
        self.assertFalse(any("/OLD/" in f"/{path}/" for path in paths))
        self.assertFalse(any(path.startswith("05_assets/") for path in paths))

    def test_runtime_source_requires_python_license_and_usable_executable(self) -> None:
        success = subprocess.CompletedProcess([], 0, "3.12.10\n", "")
        with mock.patch.object(builder.subprocess, "run", return_value=success):
            source, licenses, version = builder.validate_runtime_source(self.runtime)
        self.assertEqual(source, self.runtime.resolve())
        self.assertEqual([path.name for path in licenses], ["LICENSE.txt"])
        self.assertEqual(version, "3.12.10")

        (self.runtime / "LICENSE.txt").unlink()
        with self.assertRaisesRegex(builder.WindowsPortableError, "license"):
            builder.validate_runtime_source(self.runtime)

    def test_runtime_copy_strips_images_caches_and_save(self) -> None:
        self.write_runtime("Lib/module.py", b"pass\n")
        self.write_runtime("Lib/icon.png", b"not-runtime-code")
        self.write_runtime("Lib/__pycache__/module.pyc", b"cache")
        self.write_runtime("save.json", b"{}")
        destination = self.root / "copied-runtime"
        count = builder.copy_runtime_payload(self.runtime, destination)
        self.assertGreaterEqual(count, 3)
        self.assertTrue((destination / "python.exe").is_file())
        self.assertTrue((destination / "Lib/module.py").is_file())
        self.assertFalse((destination / "Lib/icon.png").exists())
        self.assertFalse((destination / "Lib/__pycache__").exists())
        self.assertFalse((destination / "save.json").exists())

    def test_release_ready_check_requires_packaged_dependency(self) -> None:
        package = self.root / "package"
        python_exe = package / "app/runtime/python.exe"
        python_exe.parent.mkdir(parents=True)
        python_exe.write_bytes(b"fake")
        success = subprocess.CompletedProcess([], 0, "ok\n", "")
        with mock.patch.object(builder.subprocess, "run", return_value=success) as run:
            builder.run_packaged_checks(package, require_release_dependencies=True)
        self.assertEqual(run.call_count, 3)
        self.assertEqual(run.call_args_list[-1].args[0][-1], "import rich")

    def test_build_verify_is_deterministic_and_replaces_stale_files(self) -> None:
        self.create_program_fixture()
        self.write_runtime("Lib/os.py", b"# stdlib\n")
        validate_result = (self.runtime.resolve(), (self.runtime / "LICENSE.txt",), "3.12.10")
        patches = (
            mock.patch.object(builder, "validate_runtime_source", return_value=validate_result),
            mock.patch.object(builder, "run_packaged_checks"),
            mock.patch.object(builder.release_assets, "build_release", side_effect=self.fake_s4_build),
            mock.patch.object(
                builder.release_assets,
                "verify_release",
                return_value=SimpleNamespace(included_count=1, source_revision="test-revision"),
            ),
            mock.patch.object(builder.release_assets, "git_revision", return_value="test-revision"),
        )
        with patches[0], patches[1], patches[2], patches[3], patches[4]:
            first = builder.build_package(self.root, self.runtime, "minimal-test-runtime")
            first_zip = first.zip_path.read_bytes()
            stale = first.package_path / "stale.tmp"
            stale.write_bytes(b"stale")
            second = builder.build_package(self.root, self.runtime, "minimal-test-runtime")
            second_zip = second.zip_path.read_bytes()

        self.assertEqual(first_zip, second_zip)
        self.assertFalse(stale.exists())
        self.assertFalse(second.release_ready)
        self.assertEqual(second.asset_file_count, 1)
        manifest = json.loads(
            (second.package_path / "manifests/windows-portable-manifest.json").read_text(encoding="utf-8")
        )
        self.assertEqual(manifest["entrypoints"]["gui_primary"], builder.GUI_ENTRYPOINT)
        self.assertEqual(manifest["entrypoints"]["cli"], builder.CLI_ENTRYPOINT)
        self.assertEqual(manifest["zip_filename"], builder.ZIP_FILENAME)
        self.assertEqual(
            sorted(entry["path"] for entry in manifest["program_files"]),
            [entry["path"] for entry in manifest["program_files"]],
        )
        self.assertFalse(any(path.suffix.casefold() in builder.IMAGE_SUFFIXES for path in (second.package_path / "app").rglob("*")))

    def test_verify_rejects_program_tampering(self) -> None:
        self.create_program_fixture()
        validate_result = (self.runtime.resolve(), (self.runtime / "LICENSE.txt",), "3.12.10")
        with (
            mock.patch.object(builder, "validate_runtime_source", return_value=validate_result),
            mock.patch.object(builder, "run_packaged_checks"),
            mock.patch.object(builder.release_assets, "build_release", side_effect=self.fake_s4_build),
            mock.patch.object(
                builder.release_assets,
                "verify_release",
                return_value=SimpleNamespace(included_count=1, source_revision="test-revision"),
            ),
            mock.patch.object(builder.release_assets, "git_revision", return_value="test-revision"),
        ):
            summary = builder.build_package(self.root, self.runtime, "minimal-test-runtime")
            (summary.package_path / "app/element_maze.py").write_text("tampered\n", encoding="utf-8")
            with self.assertRaisesRegex(builder.WindowsPortableError, "hash/size mismatch"):
                builder.verify_package(self.root)

    def test_overlay_path_rejects_traversal_and_preserves_screen_relative_path(self) -> None:
        with mock.patch.object(launcher, "OVERLAY_ROOT", self.root / "overlay"):
            expected = self.root / "overlay/start_screen/assets/live.png"
            self.assertEqual(
                launcher.overlay_path_for_request("/start_screen/assets/live.png?v=1"),
                expected.resolve(),
            )
            self.assertIsNone(launcher.overlay_path_for_request("/../secret.png"))
            self.assertIsNone(launcher.overlay_path_for_request("/start_screen/index.html"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
