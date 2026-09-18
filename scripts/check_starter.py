#!/usr/bin/env python3
"""Build a scratch copy of the starter with Muddler and check its serialized behavior."""

import argparse
import importlib.util
from pathlib import Path
import shutil
import subprocess
import tempfile
from xml.etree import ElementTree as ET
import zipfile

from lupa.lua51 import LuaRuntime

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "plugins/mudlet-toolbox/skills"


def check(java, jar):
    spec = importlib.util.spec_from_file_location(
        "inspect_package", SKILLS / "mudlet-package-testing/scripts/inspect_package.py")
    inspector = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(inspector)
    with tempfile.TemporaryDirectory(prefix="mudlet-toolbox-starter-") as directory:
        project = Path(directory) / "project"
        shutil.copytree(SKILLS / "mudlet-package-development/assets/starter", project)
        result = subprocess.run([java, "-jar", str(jar)], cwd=project,
                                text=True, capture_output=True, timeout=120)
        artifact = project / "build/MudletToolboxDemo.mpackage"
        if result.returncode or not artifact.is_file():
            raise RuntimeError(f"Muddler did not produce the expected package:\n{result.stdout}\n{result.stderr}")
        report = inspector.inspect_package(artifact)
        if not report["ok"]:
            raise RuntimeError(f"Generated package failed inspection: {report['diagnostics']}")
        lua = LuaRuntime(unpack_returned_tuples=True)
        compile_lua = lua.eval('function(code) local f,err=loadstring(code); return f~=nil,err end')
        with zipfile.ZipFile(artifact) as archive:
            xml = archive.read("MudletToolboxDemo.xml")
            root = ET.fromstring(xml)
            if len(root.findall(".//Alias")) != 1 or len(root.findall(".//Script")) != 1:
                raise RuntimeError("Expected one alias and one lifecycle script")
            if root.findtext(".//Alias/regex") != "^toolbox-demo$":
                raise RuntimeError("Alias pattern changed during serialization")
            if [e.text for e in root.findall(".//Script/eventHandlerList/string")] != [
                "sysLoadEvent", "sysInstallPackage", "sysUninstallPackage"
            ]:
                raise RuntimeError("Lifecycle event registrations were not preserved")
            if b"@PKGNAME@" in xml:
                raise RuntimeError("Package-name substitution was not applied")
            if "demo.txt" not in archive.namelist() or "config.lua" not in archive.namelist():
                raise RuntimeError("Missing metadata or example asset")
            for block in root.iter("script"):
                ok, error = compile_lua(block.text or "")
                if not ok:
                    raise RuntimeError(error)
            lua.execute('output = {}; function echo(s) table.insert(output, s) end')
            lua.execute(root.findtext(".//Script/script"))
            lua.execute('MudletToolboxDemoLifecycle("sysInstallPackage", "Other")')
            lua.execute('assert(#output == 0)')
            lua.execute('MudletToolboxDemoLifecycle("sysInstallPackage", "MudletToolboxDemo")')
            lua.execute('assert(output[1] == "Mudlet Toolbox demo installed. Run toolbox-demo for status.\\n")')
            lua.execute(root.findtext(".//Alias/script"))
            lua.execute('assert(output[2] == "Mudlet Toolbox demo: ready; calls=1\\n")')
            lua.execute('MudletToolboxDemoLifecycle("sysLoadEvent")')
            lua.execute('assert(#output == 2)')
            lua.execute('MudletToolboxDemoLifecycle("sysUninstallPackage", "MudletToolboxDemo")')
            lua.execute('assert(MudletToolboxDemo == nil and MudletToolboxDemoLifecycle == nil)')
        print("Muddler build, archive inventory, serialized Lua syntax and behavior passed.")
        print("Native Mudlet trigger/event dispatch and UI were not exercised.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--java", default="java", help="Java executable (path or command)")
    parser.add_argument("--muddler-jar", required=True, type=Path, help="Muddler 1.1.0 runnable JAR")
    args = parser.parse_args()
    try:
        check(args.java, args.muddler_jar.resolve())
    except (OSError, RuntimeError, subprocess.TimeoutExpired, ET.ParseError, zipfile.BadZipFile) as error:
        parser.exit(1, f"starter check failed: {error}\n")
