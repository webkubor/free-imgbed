#!/usr/bin/env python3
"""Build the social icon ZIP from the same manifest used by the gallery."""

import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "social-icons"
NOTES = ["pack.json", "NOTICE.md", "LICENSE-simple-icons.md", "DISCLAIMER-simple-icons.md"]


def icon_files(manifest):
    pack = json.loads((ASSETS / manifest).read_text(encoding="utf-8"))
    icons = [
        item[field]
        for group in pack["groups"]
        for item in group["icons"]
        for field in ("file", "colorFile")
        if field in item
    ]
    if len(icons) != len(set(icons)):
        raise ValueError(f"{manifest}: duplicated icon path")
    return pack["version"], icons


def build_zip(version, notes, icons):
    name = f"social-icons-v{version}"
    output = ROOT / "docs" / "public" / "downloads" / f"{name}.zip"
    output.parent.mkdir(parents=True, exist_ok=True)
    with ZipFile(output, "w") as archive:
        for filename in [*notes, *icons]:
            archive.writestr(ZipInfo(f"{name}/{filename}"), (ASSETS / filename).read_bytes(), ZIP_DEFLATED)
    print(f"Packed {len(icons)} icons into {output.name}")


def main():
    legacy_version, legacy_icons = icon_files("pack.json")
    version, icons = icon_files("pack-v2.json")
    files = {p.relative_to(ASSETS).as_posix() for p in ASSETS.rglob("*") if p.suffix in {".svg", ".png"}}
    if set(icons) != files or not set(legacy_icons) <= files:
        raise ValueError("Icon files must match the manifests")

    build_zip(legacy_version, NOTES, legacy_icons)
    build_zip(version, [*NOTES, "pack-v2.json", "BRAND-COLORS.md"], icons)


if __name__ == "__main__":
    main()
