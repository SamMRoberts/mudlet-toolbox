import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import zipfile

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("build_plugin", ROOT / "scripts/build_plugin.py")
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class PluginArchiveTests(unittest.TestCase):
    def test_reproducible_self_contained_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            first = builder.build(Path(directory) / "first.zip")
            second = builder.build(Path(directory) / "second.zip")
            self.assertEqual(first.read_bytes(), second.read_bytes())
            with zipfile.ZipFile(first) as archive:
                names = archive.namelist()
                self.assertIn(".codex-plugin/plugin.json", names)
                self.assertEqual(len([n for n in names if n.endswith("/SKILL.md")]), 6)
                self.assertFalse(any(n.startswith(("research/", "tests/")) or "__pycache__" in n for n in names))
                manifest = json.loads(archive.read(".codex-plugin/plugin.json"))
                self.assertEqual(manifest["version"], "0.1.1")

    def test_reject_output_inside_plugin(self):
        with self.assertRaisesRegex(ValueError, "outside"):
            builder.build(builder.PLUGIN / "archive.zip")

    def test_finder_metadata_is_excluded_at_any_depth(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            plugin = root / "plugin"
            nested = plugin / "skills" / "example"
            nested.mkdir(parents=True)
            (plugin / ".DS_Store").write_bytes(b"private Finder metadata")
            (nested / ".DS_Store").write_bytes(b"nested Finder metadata")
            (nested / "SKILL.md").write_text("Example skill\n")
            with patch.object(builder, "PLUGIN", plugin):
                output = builder.build(root / "bundle.zip")
            with zipfile.ZipFile(output) as archive:
                self.assertEqual(archive.namelist(), ["skills/example/SKILL.md"])


if __name__ == "__main__":
    unittest.main()
