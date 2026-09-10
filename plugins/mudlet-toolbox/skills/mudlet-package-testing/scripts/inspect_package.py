#!/usr/bin/env python3
"""Read-only structural inventory of a Mudlet package; Python 3.10+ stdlib.

CLI: python3 inspect_package.py PACKAGE [--max-members N]
        [--max-member-bytes N] [--max-total-bytes N]
Outputs one JSON object; exit 0 means these checks passed, 1 means an error,
and 2 means invalid CLI arguments. No extraction, writes, Lua execution, or
profile access. Limits include every ZIP entry, including resources/directories.

JSON keys: ok, package, format, validation_scope, limits, archive, documents,
resources, config_lua, diagnostics. Diagnostics contain severity/code/message
and optionally path. Inventory may be partial on errors. Section item_count
counts direct child elements, including groups; element_counts counts every
descendant tag (including unrecognised fields), without interpreting text.
Root attributes and section attributes are retained; descendant attribute names
are inventoried, but their values and all element text are not evaluated.

Root-level .xml/.trigger archive members are package documents. Nested ones
are resources, reported explicitly rather than treated as import candidates.
config_lua.present refers to the exact root config.lua; paths lists every
member with that basename. Presence does not validate configuration contents.

Discovery and the bare DOCTYPE follow official Mudlet 5.0.1 sources:
https://github.com/Mudlet/Mudlet/blob/Mudlet-5.0.1/src/Host.cpp
https://github.com/Mudlet/Mudlet/blob/Mudlet-5.0.1/src/XMLexport.cpp
This is not full Mudlet compatibility or runtime validation.
"""

from __future__ import annotations

import argparse
from collections import Counter
import json
import ntpath
from pathlib import Path
import stat
import zipfile
from xml.parsers import expat


SCOPE = (
    "Read-only archive safety and XML structure checks only; not full Mudlet "
    "compatibility or runtime validation. Lua/config.lua are never executed. "
    "Object semantics, versions, resources, and configuration are not validated."
)
SECTIONS = {
    "TriggerPackage", "TimerPackage", "AliasPackage", "ActionPackage",
    "ScriptPackage", "KeyPackage", "VariablePackage", "HelpPackage", "HostPackage",
}
DEFAULT_MAX_MEMBERS = 4096
DEFAULT_MAX_MEMBER_BYTES = 16 * 1024 * 1024
DEFAULT_MAX_TOTAL_BYTES = 64 * 1024 * 1024


class InspectionError(Exception):
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code


def diagnostic(report: dict, severity: str, code: str, message: str,
               path: str | None = None) -> None:
    entry = {"severity": severity, "code": code, "message": message}
    if path is not None:
        entry["path"] = path
    report["diagnostics"].append(entry)
    if severity == "error":
        report["ok"] = False


def inspect_xml(data: bytes, path: str, report: dict) -> None:
    """Parse without building a tree, resolving entities, or loading a DTD."""
    document = {"path": path, "well_formed": False, "root": None,
                "attributes": {}, "version": None, "namespaces": [], "sections": []}
    report["documents"].append(document)
    parser = expat.ParserCreate(namespace_separator="}")
    depth = 0
    section = None

    def start(name: str, attributes: dict) -> None:
        nonlocal depth, section
        depth += 1
        if depth == 1:
            document.update(root=name, attributes=attributes,
                            version=attributes.get("version"))
        elif depth == 2:
            section = {"tag": name, "attributes": attributes,
                       "recognized_section": name in SECTIONS,
                       "item_count": 0, "direct_item_counts": Counter(),
                       "element_counts": Counter(), "attribute_names": Counter()}
            document["sections"].append(section)
        elif section is not None:
            section["element_counts"][name] += 1
            section["attribute_names"].update(attributes.keys())
            if depth == 3:
                section["item_count"] += 1
                section["direct_item_counts"][name] += 1

    def end(name: str) -> None:
        nonlocal depth, section
        if depth == 2:
            section = None
        depth -= 1

    def doctype(name, system_id, public_id, internal_subset):
        if system_id is not None or public_id is not None or internal_subset:
            raise InspectionError("unsafe_xml", "External DTDs and internal DTD subsets are disabled.")
        if name != "MudletPackage":
            diagnostic(report, "warning", "unknown_doctype", f"Uninterpreted DOCTYPE: {name}", path)

    def reject_entity(*args):
        raise InspectionError("unsafe_xml", "Entity declarations and external entities are disabled.")

    def processing_instruction(target, text):
        diagnostic(report, "warning", "processing_instruction",
                   f"Processing instruction {target!r} was not evaluated.", path)

    def namespace(prefix, uri):
        document["namespaces"].append({"prefix": prefix, "uri": uri})
        diagnostic(report, "warning", "uninterpreted_namespace",
                   "Namespace declaration retained; qualified tags use URI}local-name notation.", path)

    parser.StartElementHandler = start
    parser.EndElementHandler = end
    parser.StartDoctypeDeclHandler = doctype
    parser.EntityDeclHandler = reject_entity
    parser.ExternalEntityRefHandler = reject_entity
    parser.ProcessingInstructionHandler = processing_instruction
    parser.StartNamespaceDeclHandler = namespace
    parser.SetParamEntityParsing(expat.XML_PARAM_ENTITY_PARSING_NEVER)
    try:
        parser.Parse(data, True)
        document["well_formed"] = True
    except InspectionError as exc:
        diagnostic(report, "error", exc.code, str(exc), path)
        return
    except LookupError as exc:
        diagnostic(report, "error", "unsupported_xml_encoding", str(exc), path)
        return
    except (expat.ExpatError, ValueError) as exc:
        diagnostic(report, "error", "malformed_xml", str(exc), path)
        return
    if document["root"] != "MudletPackage":
        diagnostic(report, "error", "invalid_root", "Expected XML root MudletPackage.", path)
    if not (document["version"] or "").strip():
        diagnostic(report, "error", "missing_version", "MudletPackage requires a nonempty version attribute.", path)
    for section in document["sections"]:
        if not section["recognized_section"]:
            diagnostic(report, "warning", "unknown_section",
                       f"Uninterpreted section {section['tag']!r}; element counts are retained.", path)
    extra = sorted(set(document["attributes"]) - {"version"})
    if extra:
        diagnostic(report, "warning", "uninterpreted_root_attributes",
                   f"Additional root attributes are retained without interpretation: {extra}", path)


def unsafe_path(name: str) -> str | None:
    """Reject extraction-dangerous or ambiguous paths on POSIX and Windows."""
    if not name or name.startswith("/") or ntpath.splitdrive(name)[0]:
        return "Empty, absolute, UNC, or drive-qualified member path."
    if "\\" in name:
        return "Backslashes are not allowed in archive member paths."
    parts = name.removesuffix("/").split("/")
    devices = {"con", "prn", "aux", "nul", "conin$", "conout$"}
    devices.update(f"{prefix}{number}" for prefix in ("com", "lpt") for number in "123456789¹²³")
    for part in parts:
        if part in ("", ".", ".."):
            return "Empty, dot, or traversal path component."
        if part.endswith((".", " ")):
            return "Trailing dots/spaces create ambiguous Windows path components."
        if any(ord(char) < 32 or char in '<>:"|?*' for char in part):
            return "Control characters, Windows special characters, or alternate data streams in path."
        if part.split(".", 1)[0].casefold() in devices:
            return "Windows device path component."
    return None


def read_bounded(stream, limit: int, retain: bool) -> tuple[bytes, int]:
    chunks = []
    count = 0
    while True:
        chunk = stream.read(min(64 * 1024, limit - count + 1))
        if not chunk:
            break
        count += len(chunk)
        if count > limit:
            raise InspectionError("size_limit", "Uncompressed data exceeds the configured byte limit.")
        if retain:
            chunks.append(chunk)
    return b"".join(chunks), count


def inspect_archive(path: Path, report: dict, max_members: int,
                    max_member_bytes: int, max_total_bytes: int) -> None:
    with zipfile.ZipFile(path) as archive:
        members = archive.infolist()
        report["archive"] = {"member_count": len(members),
                             "total_uncompressed_bytes": sum(m.file_size for m in members),
                             "members": []}
        if len(members) > max_members:
            raise InspectionError("member_limit", f"Archive has {len(members)} members; limit is {max_members}.")
        seen = {}
        candidates = []
        for member in members:
            # orig_filename retains NULs that ZipInfo.filename otherwise truncates.
            name = member.orig_filename
            is_directory = member.is_dir()
            is_document = not is_directory and "/" not in name and name.lower().endswith((".xml", ".trigger"))
            report["archive"]["members"].append({
                "path": name, "uncompressed_bytes": member.file_size,
                "compressed_bytes": member.compress_size, "directory": is_directory,
            })
            if is_document:
                candidates.append(name)
            elif not is_directory:
                report["resources"].append(name)
                if name.lower().endswith((".xml", ".trigger")):
                    diagnostic(report, "warning", "nested_xml_resource",
                               "Nested XML/trigger resource is inventoried, not parsed as a root package document.", name)
            if not is_directory and name.rsplit("/", 1)[-1].lower() == "config.lua":
                report["config_lua"]["paths"].append(name)
                if name == "config.lua":
                    report["config_lua"]["present"] = True
                else:
                    diagnostic(report, "warning", "non_root_config",
                               "Only the exact root config.lua is marked present; this member is a resource.", name)
            reason = unsafe_path(name)
            if reason:
                diagnostic(report, "error", "unsafe_path", reason, name)
            key = name.rstrip("/").casefold()
            if key in seen:
                diagnostic(report, "error", "duplicate_member",
                           "Duplicate member or case-insensitive file/directory collision.", name)
            seen[key] = is_directory
            mode = stat.S_IFMT(member.external_attr >> 16)
            if mode == stat.S_IFLNK:
                diagnostic(report, "error", "symlink_member", "Symlink archive members are disabled.", name)
            elif mode not in (0, stat.S_IFREG, stat.S_IFDIR):
                diagnostic(report, "error", "special_member", "Special filesystem members are disabled.", name)
            elif mode and (mode == stat.S_IFDIR) != is_directory:
                diagnostic(report, "error", "member_type_mismatch", "Directory marker and member type disagree.", name)
            if member.flag_bits & 1:
                diagnostic(report, "error", "encrypted_member", "Encrypted members cannot be inspected.", name)
            if member.file_size > max_member_bytes:
                diagnostic(report, "error", "size_limit", f"Member exceeds {max_member_bytes} uncompressed bytes.", name)
        for name in seen:
            parts = name.split("/")
            if any(seen.get("/".join(parts[:i])) is False for i in range(1, len(parts))):
                diagnostic(report, "error", "path_conflict", "A file is also used as a parent directory.", name)
        if report["archive"]["total_uncompressed_bytes"] > max_total_bytes:
            diagnostic(report, "error", "size_limit", f"Archive exceeds {max_total_bytes} total uncompressed bytes.")
        if not candidates:
            diagnostic(report, "warning", "no_package_xml", "No root-level .xml or .trigger package documents found.")
        if len(candidates) > 1:
            diagnostic(report, "warning", "multiple_package_xml", "Multiple root package documents found; each will be inspected.")
        if not report["ok"]:
            return
        consumed = 0
        for member in members:
            name = member.orig_filename
            try:
                with archive.open(member) as stream:
                    data, count = read_bounded(stream, min(max_member_bytes, max_total_bytes - consumed), name in candidates)
                consumed += count
                if count != member.file_size:
                    raise InspectionError("member_size_mismatch", "Read size differs from the declared member size.")
                if name in candidates:
                    inspect_xml(data, name, report)
            except InspectionError as exc:
                diagnostic(report, "error", exc.code, str(exc), name)
                return
            except Exception as exc:
                # stdlib ZIP codecs can raise different exceptions for corrupt
                # streams or unavailable codecs. Fail closed, preserving context.
                diagnostic(report, "error", "unreadable_member", f"{type(exc).__name__}: {exc}", name)


def inspect_package(package: str | Path, *, max_members: int = DEFAULT_MAX_MEMBERS,
                    max_member_bytes: int = DEFAULT_MAX_MEMBER_BYTES,
                    max_total_bytes: int = DEFAULT_MAX_TOTAL_BYTES) -> dict:
    """Return JSON-serializable findings; errors make ok false, warnings do not."""
    if min(max_members, max_member_bytes, max_total_bytes) <= 0:
        raise ValueError("Inspection limits must be positive integers.")
    path = Path(package)
    report = {"ok": True, "package": str(path), "format": None, "validation_scope": SCOPE,
              "limits": {"max_members": max_members, "max_member_bytes": max_member_bytes,
                         "max_total_bytes": max_total_bytes},
              "archive": None, "documents": [], "resources": [],
              "config_lua": {"present": False, "paths": [], "evaluated": False}, "diagnostics": []}
    try:
        if path.suffix.lower() not in (".xml", ".zip", ".mpackage"):
            raise InspectionError("unsupported_input", "Expected a .xml, .zip, or .mpackage input.")
        if not path.is_file():
            raise InspectionError("invalid_input", "Input is not an existing regular file.")
        if path.suffix.lower() == ".xml":
            report["format"] = "xml"
            with path.open("rb") as stream:
                data, _ = read_bounded(stream, min(max_member_bytes, max_total_bytes), True)
            inspect_xml(data, str(path), report)
        else:
            report["format"] = "zip"
            inspect_archive(path, report, max_members, max_member_bytes, max_total_bytes)
    except InspectionError as exc:
        diagnostic(report, "error", exc.code, str(exc))
    except (OSError, zipfile.BadZipFile, zipfile.LargeZipFile, ValueError, NotImplementedError) as exc:
        diagnostic(report, "error", "unreadable_input", f"{type(exc).__name__}: {exc}")
    return report


def positive_integer(value: str) -> int:
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=SCOPE)
    parser.add_argument("package", help=".mpackage/.zip archive or plain .xml file")
    parser.add_argument("--max-members", type=positive_integer, default=DEFAULT_MAX_MEMBERS)
    parser.add_argument("--max-member-bytes", type=positive_integer, default=DEFAULT_MAX_MEMBER_BYTES)
    parser.add_argument("--max-total-bytes", type=positive_integer, default=DEFAULT_MAX_TOTAL_BYTES)
    args = parser.parse_args(argv)
    report = inspect_package(args.package, max_members=args.max_members,
                             max_member_bytes=args.max_member_bytes, max_total_bytes=args.max_total_bytes)
    print(json.dumps(report, indent=2, ensure_ascii=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
