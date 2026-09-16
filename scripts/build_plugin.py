#!/usr/bin/env python3
"""Build a reproducible source archive containing only the distributable plugin."""

import argparse
from pathlib import Path
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "mudlet-toolbox"


def build(output):
    output = Path(output).resolve()
    if output == PLUGIN or PLUGIN in output.parents:
        raise ValueError("output must be outside the plugin source tree")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=output.parent, suffix=".zip", delete=False) as handle:
            temporary = Path(handle.name)
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for path in sorted(PLUGIN.rglob("*")):
                relative = path.relative_to(PLUGIN)
                if "__pycache__" in relative.parts or path.suffix == ".pyc" or path.name == ".DS_Store":
                    continue
                if path.is_symlink():
                    raise ValueError(f"symlink in plugin source: {relative}")
                if not path.is_file():
                    continue
                info = zipfile.ZipInfo(relative.as_posix(), date_time=(2026, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.external_attr = 0o100644 << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                archive.writestr(info, path.read_bytes())
        temporary.replace(output)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    return output


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist" / "mudlet-toolbox.zip")
    args = parser.parse_args()
    try:
        print(build(args.output))
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        parser.exit(1, f"build failed: {error}\n")
