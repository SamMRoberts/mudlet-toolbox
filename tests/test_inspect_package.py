"""Observable read-only package inspection checks, using only stdlib fixtures."""

import importlib.util
import json
from pathlib import Path
import stat
import struct
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
import warnings
import zipfile


SCRIPT = (Path(__file__).resolve().parents[1] / "plugins" / "mudlet-toolbox" /
          "skills" / "mudlet-package-testing" / "scripts" / "inspect_package.py")
SPEC = importlib.util.spec_from_file_location("inspect_package", SCRIPT)
inspector = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(inspector)

XML = b'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE MudletPackage>
<MudletPackage version="1.001">
  <TriggerPackage>
    <TriggerGroup isActive="yes"><name>A group</name>
      <Trigger><name>A trigger</name><script>error("must not execute")</script></Trigger>
    </TriggerGroup>
    <Trigger><name>Another trigger</name></Trigger>
  </TriggerPackage>
  <TimerPackage/>
  <ScriptPackage><Script><name>Script with spaces</name></Script></ScriptPackage>
</MudletPackage>'''


class InspectPackageTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)

    def archive(self, entries, filename="sample.mpackage", compression=zipfile.ZIP_DEFLATED):
        path = self.root / filename
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)  # Deliberate duplicate fixtures.
            with zipfile.ZipFile(path, "w", compression=compression) as archive:
                for name, content in entries:
                    archive.writestr(name, content)
        return path

    def xml(self, content=XML):
        path = self.root / "plain.xml"
        path.write_bytes(content)
        return path

    def assert_error(self, report, code):
        self.assertFalse(report["ok"], report)
        self.assertIn(code, [item["code"] for item in report["diagnostics"]
                             if item["severity"] == "error"], report)

    def cli(self, *args):
        return subprocess.run([sys.executable, "-B", str(SCRIPT), *map(str, args)],
                              cwd=self.root, text=True, capture_output=True, check=False)

    def test_plain_xml_bare_doctype_and_direct_and_nested_counts(self):
        report = inspector.inspect_package(self.xml())
        self.assertTrue(report["ok"], report)
        self.assertEqual("xml", report["format"])
        self.assertIsNone(report["archive"])
        document = report["documents"][0]
        self.assertTrue(document["well_formed"])
        self.assertEqual("MudletPackage", document["root"])
        self.assertEqual("1.001", document["version"])
        sections = document["sections"]
        self.assertEqual(["TriggerPackage", "TimerPackage", "ScriptPackage"],
                         [section["tag"] for section in sections])
        self.assertEqual(2, sections[0]["item_count"])
        self.assertEqual({"TriggerGroup": 1, "Trigger": 1}, sections[0]["direct_item_counts"])
        self.assertEqual(2, sections[0]["element_counts"]["Trigger"])
        self.assertEqual(3, sections[0]["element_counts"]["name"])
        self.assertEqual(1, sections[0]["attribute_names"]["isActive"])
        self.assertEqual(0, sections[1]["item_count"])
        self.assertEqual([], report["diagnostics"])
        self.assertIn("not full Mudlet compatibility or runtime validation", report["validation_scope"])

    def test_archive_inventory_keeps_spaces_resources_and_config(self):
        for suffix in (".zip", ".mpackage"):
            with self.subTest(suffix=suffix):
                entries = [("My Package.xml", XML), ("images/", b""),
                           ("images/a picture.png", b"not interpreted"),
                           ("config.lua", b'error("never run me")'),
                           ("some unknown file.xyz", b"data")]
                report = inspector.inspect_package(self.archive(entries, "My Package" + suffix))
                self.assertTrue(report["ok"], report)
                self.assertEqual("zip", report["format"])
                self.assertEqual(5, report["archive"]["member_count"])
                self.assertEqual(sum(len(data) for _, data in entries),
                                 report["archive"]["total_uncompressed_bytes"])
                self.assertEqual(["images/a picture.png", "config.lua", "some unknown file.xyz"], report["resources"])
                self.assertEqual({"present": True, "paths": ["config.lua"], "evaluated": False}, report["config_lua"])
                self.assertEqual("My Package.xml", report["documents"][0]["path"])

    def test_unknown_features_remain_visible_without_invented_schema(self):
        xml = b'''<MudletPackage version="future-version" future="yes">
          <FuturePackage option="x"><NovelItem extra="1"><Mystery/></NovelItem></FuturePackage>
          <TriggerPackage><FutureTrigger futureFlag="on"/></TriggerPackage>
        </MudletPackage>'''
        report = inspector.inspect_package(self.xml(xml))
        self.assertTrue(report["ok"], report)
        document = report["documents"][0]
        self.assertEqual("future-version", document["version"])
        self.assertEqual("yes", document["attributes"]["future"])
        future, triggers = document["sections"]
        self.assertFalse(future["recognized_section"])
        self.assertEqual({"option": "x"}, future["attributes"])
        self.assertEqual({"NovelItem": 1, "Mystery": 1}, future["element_counts"])
        self.assertEqual({"FutureTrigger": 1}, triggers["direct_item_counts"])
        self.assertEqual({"futureFlag": 1}, triggers["attribute_names"])
        self.assertIn("unknown_section", [d["code"] for d in report["diagnostics"]])

    def test_repeated_sections_are_not_overwritten(self):
        report = inspector.inspect_package(self.xml(
            b'<MudletPackage version="1"><ScriptPackage/><ScriptPackage><Script/></ScriptPackage></MudletPackage>'))
        self.assertTrue(report["ok"], report)
        self.assertEqual([0, 1], [s["item_count"] for s in report["documents"][0]["sections"]])

    def test_malformed_xml_in_plain_file_and_archive(self):
        for path in (self.xml(b"<MudletPackage>"), self.archive([("broken.xml", b"<MudletPackage>")])):
            with self.subTest(path=path):
                report = inspector.inspect_package(path)
                self.assert_error(report, "malformed_xml")
                self.assertFalse(report["documents"][0]["well_formed"])

    def test_root_and_nonempty_version_are_required(self):
        for content, code in (
            (b'<Other version="1"/>', "invalid_root"),
            (b'<MudletPackage/>', "missing_version"),
            (b'<MudletPackage version=" "/>', "missing_version"),
        ):
            with self.subTest(content=content):
                self.assert_error(inspector.inspect_package(self.xml(content)), code)

    def test_unknown_encoding_returns_json_error_without_traceback(self):
        path = self.xml(b'<?xml version="1.0" encoding="unknown-encoding"?><MudletPackage version="1"/>')
        result = self.cli(path)
        self.assertEqual(1, result.returncode)
        self.assertEqual("", result.stderr)
        self.assert_error(json.loads(result.stdout), "unsupported_xml_encoding")

    def test_namespaces_are_reported_and_unbound_prefixes_are_malformed(self):
        report = inspector.inspect_package(self.xml(
            b'<MudletPackage version="1" xmlns:future="urn:future"><future:Section/></MudletPackage>'))
        self.assertTrue(report["ok"], report)
        document = report["documents"][0]
        self.assertEqual([{"prefix": "future", "uri": "urn:future"}], document["namespaces"])
        self.assertEqual("urn:future}Section", document["sections"][0]["tag"])
        self.assert_error(inspector.inspect_package(self.xml(
            b'<MudletPackage version="1"><unbound:Section/></MudletPackage>')), "malformed_xml")
        self.assert_error(inspector.inspect_package(self.xml(
            b'<MudletPackage xmlns="urn:other" version="1"/>')), "invalid_root")

    def test_entities_and_external_dtds_are_rejected_in_utf8_and_utf16(self):
        declarations = [
            '<!DOCTYPE MudletPackage [<!ENTITY example "expanded">]>',
            '<!DOCTYPE MudletPackage [<!ENTITY example SYSTEM "file:///etc/passwd">]>',
            '<!DOCTYPE MudletPackage SYSTEM "https://example.invalid/external.dtd">',
            '<!DOCTYPE MudletPackage [<!ENTITY % remote SYSTEM "file:///etc/passwd">%remote;]>',
        ]
        for declaration in declarations:
            for encoding in ("utf-8", "utf-16"):
                with self.subTest(declaration=declaration, encoding=encoding):
                    data = (f'<?xml version="1.0" encoding="{encoding}"?>{declaration}'
                            '<MudletPackage version="1"/>').encode(encoding)
                    self.assert_error(inspector.inspect_package(self.xml(data)), "unsafe_xml")

    def test_entity_looking_lua_text_is_not_mistaken_for_a_dtd(self):
        report = inspector.inspect_package(self.xml(
            b'<MudletPackage version="1"><ScriptPackage><Script><script><![CDATA['
            b'local text = "<!ENTITY harmless>"; return "&example;"'
            b']]></script></Script></ScriptPackage></MudletPackage>'))
        self.assertTrue(report["ok"], report)

    def test_processing_instructions_are_reported_without_evaluation(self):
        report = inspector.inspect_package(self.xml(
            b'<?xml-stylesheet href="https://example.invalid/a.xsl"?>' + XML.split(b"?>", 1)[1]))
        self.assertTrue(report["ok"], report)
        self.assertIn("processing_instruction", [d["code"] for d in report["diagnostics"]])

    def test_path_abuse_is_rejected_before_reading_any_member(self):
        paths = ["../escape.txt", "a/../../escape.txt", "/absolute.txt", "C:/drive.txt",
                 "C:relative.txt", "//server/share/file.txt", "\\\\server\\share\\file.txt",
                 "a\\..\\escape.txt", "a\\file.txt", "a/./file.txt", "a//file.txt",
                 "a/.. /file.txt", "a/stream:payload", "CON.txt", "a/LPT1",
                 "a/end./file.txt", "a/control\x01.txt"]
        for name in paths:
            with self.subTest(name=name):
                path = self.archive([("main.xml", XML), (name, b"danger")])
                with mock.patch.object(zipfile.ZipFile, "open", side_effect=AssertionError("must preflight")):
                    self.assert_error(inspector.inspect_package(path), "unsafe_path")

    def test_nul_member_name_is_not_silently_truncated(self):
        path = self.archive([("main.xml", XML), ("badXname", b"content")])
        path.write_bytes(path.read_bytes().replace(b"badXname", b"bad\0name"))
        self.assert_error(inspector.inspect_package(path), "unsafe_path")

    def test_symlink_and_special_members_are_rejected(self):
        for kind, code in ((stat.S_IFLNK, "symlink_member"), (stat.S_IFIFO, "special_member")):
            with self.subTest(kind=kind):
                member = zipfile.ZipInfo("link")
                member.create_system = 3
                member.external_attr = (kind | 0o777) << 16
                self.assert_error(inspector.inspect_package(self.archive(
                    [("main.xml", XML), (member, b"../target")]
                )), code)

    def test_inconsistent_directory_type_is_rejected(self):
        member = zipfile.ZipInfo("directory-without-slash")
        member.create_system = 3
        member.external_attr = (stat.S_IFDIR | 0o755) << 16
        self.assert_error(inspector.inspect_package(self.archive(
            [("main.xml", XML), (member, b"")])), "member_type_mismatch")

    def test_duplicate_and_case_colliding_members_are_rejected(self):
        for names in (("main.xml", "main.xml"), ("Main.xml", "main.xml"), ("folder", "folder/")):
            with self.subTest(names=names):
                self.assert_error(inspector.inspect_package(self.archive(
                    [(name, XML if name.lower().endswith(".xml") else b"") for name in names]
                )), "duplicate_member")

    def test_file_parent_conflicts_are_rejected_independent_of_order(self):
        entries = [("main.xml", XML), ("folder", b"file"), ("folder/child", b"child")]
        for ordered in (entries, list(reversed(entries))):
            with self.subTest(ordered=ordered):
                self.assert_error(inspector.inspect_package(self.archive(ordered)), "path_conflict")

    def test_member_count_includes_directories_and_stops_before_reads(self):
        path = self.archive([("main.xml", XML), ("empty/", b"")])
        with mock.patch.object(zipfile.ZipFile, "open", side_effect=AssertionError("must preflight")):
            self.assert_error(inspector.inspect_package(path, max_members=1), "member_limit")
        self.assertTrue(inspector.inspect_package(path, max_members=2)["ok"])

    def test_per_member_size_limits_cover_compressed_resources(self):
        path = self.archive([("main.xml", XML), ("large.txt", b"x" * 10_000)])
        with mock.patch.object(zipfile.ZipFile, "open", side_effect=AssertionError("must preflight")):
            self.assert_error(inspector.inspect_package(path, max_member_bytes=1000), "size_limit")

    def test_total_limit_and_exact_boundary(self):
        path = self.archive([("main.xml", XML), ("resource", b"12345")])
        size = len(XML) + 5
        self.assert_error(inspector.inspect_package(path, max_total_bytes=size - 1), "size_limit")
        self.assertTrue(inspector.inspect_package(path, max_total_bytes=size, max_member_bytes=len(XML))["ok"])

    def test_plain_xml_obeys_both_byte_limits(self):
        path = self.xml()
        for option in ("max_member_bytes", "max_total_bytes"):
            with self.subTest(option=option):
                self.assert_error(inspector.inspect_package(path, **{option: len(XML) - 1}), "size_limit")
                self.assertTrue(inspector.inspect_package(path, **{option: len(XML)})["ok"])

    def test_corrupt_resource_crc_fails_even_when_xml_is_valid(self):
        path = self.archive([("main.xml", XML), ("resource", b"unique resource payload")],
                            compression=zipfile.ZIP_STORED)
        path.write_bytes(path.read_bytes().replace(b"unique resource payload", b"broken resource payload"))
        report = inspector.inspect_package(path)
        self.assert_error(report, "unreadable_member")
        self.assertTrue(report["documents"][0]["well_formed"])

    def test_encrypted_and_unsupported_compression_members_fail_closed(self):
        for offset_local, offset_central, value, code in (
            (6, 8, 1, "encrypted_member"), (8, 10, 99, "unreadable_member"),
        ):
            with self.subTest(code=code):
                path = self.archive([("main.xml", XML)], compression=zipfile.ZIP_STORED)
                data = bytearray(path.read_bytes())
                central = data.index(b"PK\x01\x02")
                struct.pack_into("<H", data, offset_local, value)
                struct.pack_into("<H", data, central + offset_central, value)
                path.write_bytes(data)
                self.assert_error(inspector.inspect_package(path), code)

    def test_bad_archive_and_missing_input_return_diagnostics(self):
        path = self.root / "broken.zip"
        path.write_bytes(b"not a zip archive")
        self.assert_error(inspector.inspect_package(path), "unreadable_input")
        self.assert_error(inspector.inspect_package(self.root / "missing.xml"), "invalid_input")

    def test_unsupported_input_and_directory_are_rejected(self):
        path = self.root / "input.txt"
        path.write_bytes(XML)
        self.assert_error(inspector.inspect_package(path), "unsupported_input")
        directory = self.root / "directory.xml"
        directory.mkdir()
        self.assert_error(inspector.inspect_package(directory), "invalid_input")

    def test_multiple_root_documents_are_all_inspected_including_trigger(self):
        path = self.archive([("broken.xml", b"<"), ("second.trigger", XML)])
        report = inspector.inspect_package(path)
        self.assert_error(report, "malformed_xml")
        self.assertEqual(["broken.xml", "second.trigger"], [d["path"] for d in report["documents"]])
        self.assertTrue(report["documents"][1]["well_formed"])
        self.assertIn("multiple_package_xml", [d["code"] for d in report["diagnostics"]])

    def test_nested_xml_and_config_are_reported_as_resources(self):
        path = self.archive([("nested/resource.xml", b"arbitrary resource"),
                             ("nested/config.lua", b"anything")])
        report = inspector.inspect_package(path)
        self.assertTrue(report["ok"], report)
        self.assertEqual([], report["documents"])
        self.assertEqual(["nested/resource.xml", "nested/config.lua"], report["resources"])
        self.assertEqual({"present": False, "paths": ["nested/config.lua"], "evaluated": False}, report["config_lua"])
        self.assertEqual({"nested_xml_resource", "non_root_config", "no_package_xml"},
                         {d["code"] for d in report["diagnostics"]})

    def test_inspection_never_extracts_executes_or_changes_files(self):
        marker = self.root / "executed"
        lua = f'os.execute("touch {marker}")'.encode()
        path = self.archive([("main.xml", XML), ("config.lua", lua), ("nested/resource", b"data")])
        before = {str(p): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        with mock.patch.object(zipfile.ZipFile, "extract", side_effect=AssertionError("extraction")), \
             mock.patch.object(zipfile.ZipFile, "extractall", side_effect=AssertionError("extraction")), \
             mock.patch("subprocess.run", side_effect=AssertionError("execution")), \
             mock.patch("os.system", side_effect=AssertionError("execution")):
            report = inspector.inspect_package(path)
        self.assertTrue(report["ok"], report)
        self.assertFalse(marker.exists())
        self.assertEqual(before, {str(p): p.read_bytes() for p in self.root.rglob("*") if p.is_file()})
        self.assertEqual([path], list(self.root.iterdir()))

    def test_cli_json_and_success_and_failure_exit_codes(self):
        result = self.cli(self.xml())
        self.assertEqual(0, result.returncode, result.stderr)
        self.assertEqual("", result.stderr)
        self.assertTrue(json.loads(result.stdout)["ok"])
        result = self.cli(self.xml(b"<broken>"))
        self.assertEqual(1, result.returncode, result.stderr)
        self.assertEqual("", result.stderr)
        self.assert_error(json.loads(result.stdout), "malformed_xml")

    def test_cli_byte_limit_and_invalid_arguments(self):
        path = self.xml()
        result = self.cli(path, "--max-member-bytes", "1")
        self.assertEqual(1, result.returncode, result.stderr)
        self.assert_error(json.loads(result.stdout), "size_limit")
        for value in ("0", "-1", "invalid"):
            with self.subTest(value=value):
                result = self.cli(path, "--max-members", value)
                self.assertEqual(2, result.returncode)
                self.assertIn("error:", result.stderr)
                self.assertEqual("", result.stdout)


if __name__ == "__main__":
    unittest.main()
