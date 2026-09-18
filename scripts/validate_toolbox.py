#!/usr/bin/env python3
"""Check local plugin structure, metadata, links, JSON, and Lua 5.1 syntax."""

import json
from pathlib import Path
import re
import sys

import yaml
from lupa.lua51 import LuaRuntime

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "mudlet-toolbox"
SKILLS = {
    "mudlet-package-development", "mudlet-lua-scripting", "mudlet-events-protocols",
    "mudlet-geyser-ui", "mudlet-mapper-development", "mudlet-package-testing",
}


def validate():
    errors = []
    manifest = json.loads((PLUGIN / ".codex-plugin" / "plugin.json").read_text())
    if manifest.get("name") != PLUGIN.name or manifest.get("skills") != "./skills/":
        errors.append("manifest name or skills path mismatch")
    if manifest.get("version") != "0.2.0":
        errors.append("manifest version is not 0.2.0")
    actual = {p.name for p in (PLUGIN / "skills").iterdir() if p.is_dir()}
    if actual != SKILLS:
        errors.append(f"unexpected skill folders: {actual ^ SKILLS}")
    lua = LuaRuntime(unpack_returned_tuples=True)
    compile_lua = lua.eval('function(code, name) local f, err = loadstring(code, name); return f ~= nil, err end')
    for name in sorted(SKILLS):
        directory = PLUGIN / "skills" / name
        entry = directory / "SKILL.md"
        if not entry.exists():
            errors.append(f"missing {entry}")
            continue
        text = entry.read_text()
        front = re.match(r"\A---\n(.*?)\n---\n", text, re.S)
        if not front:
            errors.append(f"missing frontmatter: {name}")
            continue
        metadata = yaml.safe_load(front.group(1))
        if metadata.get("name") != name or not metadata.get("description"):
            errors.append(f"invalid skill metadata: {name}")
        agent = yaml.safe_load((directory / "agents" / "openai.yaml").read_text())
        interface = agent.get("interface", {})
        if not 25 <= len(interface.get("short_description", "")) <= 64:
            errors.append(f"invalid UI description length: {name}")
        if f"${name}" not in interface.get("default_prompt", ""):
            errors.append(f"default prompt does not invoke skill: {name}")
        if agent.get("policy", {}).get("allow_implicit_invocation", True) is not True:
            errors.append(f"implicit invocation unexpectedly disabled: {name}")
    files = [p for p in PLUGIN.rglob("*") if p.is_file() and "__pycache__" not in p.parts]
    for path in files:
        if path.suffix == ".json" or path.name == "mfile":
            try:
                json.loads(path.read_text())
            except ValueError as error:
                errors.append(f"{path}: {error}")
        if path.suffix == ".md":
            text = path.read_text()
            if "[TODO:" in text:
                errors.append(f"unfinished scaffold: {path}")
            for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
                if "://" in link or link.startswith("#"):
                    continue
                target = (path.parent / link.split("#", 1)[0]).resolve()
                if not target.exists() or not target.is_relative_to(PLUGIN):
                    errors.append(f"broken or external local reference: {path}: {link}")
        if path.suffix == ".lua":
            ok, error = compile_lua(path.read_text(), "@" + str(path))
            if not ok:
                errors.append(str(error))
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Validated {len(SKILLS)} skills and {len(files)} plugin files; Lua 5.1 syntax passed.")
    return 0


if __name__ == "__main__":
    sys.exit(validate())
