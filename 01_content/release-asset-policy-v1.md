# Release Asset Policy V1

Purpose: define the offline, release-only image overlay built by
`06_tools/build_release_assets.py`. This tool does not participate in the
static prototype or live runtime and does not create gameplay authority.

## Source allowlist

The allowlist is derived only from literal, local image references in:

- `07_gui_prototype/**/*.html`
- `07_gui_prototype/**/*.css`
- `07_gui_prototype/**/*.js`
- `07_gui_prototype/**/*.json`
- `03_engine/engine/gui_*.py`

References are resolved using their browser-facing screen base. Fixture JSON
paths are therefore relative to the owning screen rather than the `fixtures/`
directory. Python GUI presentation paths are resolved against their matching
prototype screen, with a unique existing screen match as fallback.

`assets/*.meta.json` files are discovered by the scan but are asset-production
and comparison metadata, not runtime/static consumers. Their review paths do
not authorize inclusion. Remote/data URLs and non-image strings are not local
portable assets.

Only existing, uniquely resolved images used by the runtime/static prototype
are included. Duplicate references collapse to one repository-relative path.
Unreferenced images never enter the overlay.

## Hard exclusions and failures

- Any path segment named `OLD`, case-insensitively, is always excluded from the
  candidate inventory.
- A live source literal that points into `OLD` is a blocking validation error,
  even if the file exists.
- A missing, ambiguous, dynamic, absolute-filesystem, or repository-escaping
  live image reference is a blocking validation error with source file, line,
  and literal path.
- `05_assets/` contains references and production material only. It is not a
  portable runtime asset root and is neither included nor counted as GUI
  unreferenced inventory.

The builder reports `excluded.old_count` as image files below
`07_gui_prototype/` with an `OLD` segment. `excluded.unreferenced_count` is the
remaining non-OLD GUI image inventory that has no live literal reference.

## Transform and path contract

Source images are read-only. The builder never deletes, moves, overwrites, or
re-encodes repository images.

- PNG content is losslessly optimized.
- JPEG content is encoded with fixed `quality=82` and Pillow optimization.
- GIF, WebP, and other supported image content is copied byte-for-byte.
- If a PNG/JPEG encoded result is larger than its source, the release copy
  falls back to the original bytes and records `transform: "copy"`.
- The release copy must preserve the repository-relative path, suffix,
  dimensions, and alpha presence. `release_bytes` may not exceed
  `source_bytes`.

The only writable locations are ignored release outputs:

```text
dist/assets-overlay/app/<repository-relative-path>
dist/manifests/assets-manifest.json
```

Each build replaces only `dist/assets-overlay/app/`, preventing stale or
unreferenced files from surviving in the overlay. Safety checks reject other
output and manifest paths.

## Manifest contract

The UTF-8 JSON manifest has no timestamp, uses canonical indentation and a
trailing newline, and sorts `files` lexicographically by `path`:

```json
{
  "format_version": 1,
  "source_revision": "<git sha>",
  "asset_root": "app",
  "files": [
    {
      "path": "07_gui_prototype/.../asset.png",
      "source_sha256": "...",
      "release_sha256": "...",
      "source_bytes": 0,
      "release_bytes": 0,
      "transform": "png-lossless"
    }
  ],
  "excluded": {
    "old_count": 0,
    "unreferenced_count": 0
  }
}
```

`transform` is exactly one of `png-lossless`, `jpeg-q82`, or `copy`.

## Commands

From the repository root with the bundled Python runtime:

```powershell
& $mazePython 06_tools\test_release_assets.py
& $mazePython 06_tools\build_release_assets.py --dry-run
& $mazePython 06_tools\build_release_assets.py --output dist\assets-overlay --manifest dist\manifests\assets-manifest.json
& $mazePython 06_tools\build_release_assets.py --verify --output dist\assets-overlay --manifest dist\manifests\assets-manifest.json
```

`--dry-run` validates the live allowlist and source image readability without
writing `dist/`. A normal build writes release copies and the manifest.
`--verify` re-derives the allowlist and exclusion counts, checks the manifest
contract and canonical ordering, requires an exact output file set, validates
both SHA-256 hashes and byte counts, and confirms dimensions, alpha, transform,
and size constraints.
