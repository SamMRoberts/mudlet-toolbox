import importlib.util
from pathlib import Path
import tempfile
import unittest
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

    def test_reject_output_inside_plugin(self):
        with self.assertRaisesRegex(ValueError, "outside"):
            builder.build(builder.PLUGIN / "archive.zip")


if __name__ == "__main__":
    unittest.main()
