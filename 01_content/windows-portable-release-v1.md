# Windows Portable Release V1

Purpose: define the deterministic offline Windows portable package produced by
`06_tools/build_windows_portable.py`. The GUI is the primary entrypoint. The
CLI is exposed only as **文字核心版 Text Core**.

## Output contract

```text
dist/windows-portable/ElementMaze/
  啟動 Element Maze GUI.bat
  文字核心版 Text Core.bat
  app/
  assets-overlay/app/<repository-relative-image-path>
  manifests/assets-manifest.json
  manifests/windows-portable-manifest.json
  RELEASE.txt
dist/ElementMaze-Windows-Portable.zip
```

`app/` contains the Python program, non-image GUI/runtime payload, and the
operator-supplied Python runtime. Repository GUI images are never copied there.
All GUI images come from `assets-overlay/app/` and exactly match the S4 asset
manifest. The builder calls and verifies `build_release_assets.py`; it does not
implement another image scanner or compressor.

The portable GUI launcher binds only `127.0.0.1`, opens
`/start_screen/index.html?mode=live`, delegates API behavior to the existing
runtime bridge, and maps browser-relative image requests to the separate asset
overlay. Python/data/runtime remain gameplay authority. Static fixtures remain
development fallback data and do not become portable gameplay authority.

## Runtime input and release readiness

A real build requires an explicit `--runtime-source` directory containing a
working `python.exe` and retained license material. The directory must already
be self-contained; the builder does not download software, install Python,
modify the system runtime, or write the source's absolute path into the package.
It validates the source executable, copies it below `app/runtime/`, then runs
the CLI smoke test and portable GUI layout smoke test with the staged executable.
When `--redistributable-runtime` is asserted, it also requires the staged
runtime to import the release dependency declared by `requirements.txt`.

For local layout verification, a machine-local runtime may be supplied without
`--redistributable-runtime`. The manifest and `RELEASE.txt` then mark the ZIP as
`release_ready: false`; that artifact must not be published. A formal release
must use a runtime that the release operator has independently confirmed is
licensed for redistribution, must retain all required runtime and dependency
licenses, and must add `--redistributable-runtime`. The flag is an explicit
operator assertion, not a license audit performed by the builder.

## Commands

From the repository root:

```powershell
$runtimeSource = 'C:\path\to\redistributable-python-runtime'
& $mazePython 06_tools\build_windows_portable.py --dry-run --runtime-source $runtimeSource
& $mazePython 06_tools\build_windows_portable.py --runtime-source $runtimeSource --runtime-label python-3.12-embedded --redistributable-runtime
& $mazePython 06_tools\build_windows_portable.py --verify
```

Use the same commands without `--redistributable-runtime` for ignored local
validation output. `--dry-run` writes nothing. A build replaces only the fixed
staging directory and ZIP, so stale files cannot survive a rerun. `--verify`
re-enters the S4 verifier and checks the package file set, program hashes,
asset-manifest identity, asset count, runtime entrypoint, canonical manifest,
deterministic ZIP order/path/timestamps, and staged smoke tests.

`windows-portable-manifest.json` records the source revision, S4 manifest hash,
both entrypoints, every program/runtime file with byte count and SHA-256, asset
file count, runtime label/version/readiness assertion, and ZIP filename. JSON
and ZIP entry ordering are deterministic; ZIP paths always use `/` and reject
absolute paths, `..`, development caches, `OLD`, `05_assets`, `save.json`, and
other forbidden material.
