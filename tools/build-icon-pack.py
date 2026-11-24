#!/usr/bin/env python3
"""Build the social icon ZIP from the same manifest used by the gallery."""

import json
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "social-icons"


def main():
    pack = json.loads((ASSETS / "pack.json").read_text(encoding="utf-8"))
    icons = [item["file"] for group in pack["groups"] for item in group["icons"]]
    files = {p.name for p in ASSETS.iterdir() if p.suffix in {".svg", ".png"}}
    if len(icons) != len(files) or set(icons) != files:
        raise ValueError("Icon files must match the manifest exactly")

    name = f"social-icons-v{pack['version']}"
    output = ROOT / "docs" / "public" / "downloads" / f"{name}.zip"
    output.parent.mkdir(parents=True, exist_ok=True)
    notes = ["pack.json", "NOTICE.md", "LICENSE-simple-icons.md", "DISCLAIMER-simple-icons.md"]
    with ZipFile(output, "w") as archive:
        for filename in [*notes, *icons]:
            archive.writestr(ZipInfo(f"{name}/{filename}"), (ASSETS / filename).read_bytes(), ZIP_DEFLATED)
    print(f"Packed {len(icons)} icons into {output.name}")


if __name__ == "__main__":
    main()
