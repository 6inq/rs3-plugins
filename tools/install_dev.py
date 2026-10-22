"""Copies plugins into the RS3 beta client's dev_plugins folder for testing.

Each plugin's plugin.json, main.lua, src/ and resources/ are copied to
C:\ProgramData\Jagex\RuneScape-BETA\dev_plugins\<folder>. Dependencies are
rewritten from their mod.io ids to the dev folder names, because the beta
client loads dependencies by folder.

Usage (from the hub folder):
    python tools/install_dev.py                 (every plugin)
    python tools/install_dev.py bank-organizer  (just one)
"""

import json
import pathlib
import shutil
import sys

# The hub folder (this file lives in <hub>/tools/).
HUB = pathlib.Path(__file__).resolve().parent.parent
# The beta client's folder for plugins under development.
DEV = pathlib.Path(r"C:\ProgramData\Jagex\RuneScape-BETA\dev_plugins")
# mod.io dependency id -> its folder name in dev_plugins.
DEV_FOLDERS = {6398181: "prettyui", 6414886: "gepl"}
# What is copied: these files and folders.
PLUGIN_FILES = ["plugin.json", "main.lua"]
PLUGIN_DIRS = ["src", "resources"]


def plugins(names):
    """Return the plugin folders to install: the named ones, or every folder
    with a plugin.json."""
    folders = [HUB / name for name in names] if names else sorted(p for p in HUB.iterdir() if (p / "plugin.json").exists())
    return [f for f in folders if (f / "plugin.json").exists()]


def dev_manifest(path):
    """Return a plugin.json with mod.io dependency ids replaced by dev folder names."""
    manifest = json.loads(path.read_text(encoding="utf-8"))
    for key in ("requiredDependencies", "optionalDependencies"):
        deps = manifest.get(key) or {}
        if isinstance(deps, dict):
            manifest[key] = {alias: DEV_FOLDERS.get(target, target) for alias, target in deps.items()}
    return manifest


def install(folder):
    """Copy one plugin into dev_plugins, replacing its old src/ and resources/."""
    target = DEV / folder.name
    for directory in PLUGIN_DIRS:
        if (target / directory).exists():
            shutil.rmtree(target / directory)
    target.mkdir(parents=True, exist_ok=True)
    (target / "main.lua").write_bytes((folder / "main.lua").read_bytes())
    (target / "plugin.json").write_text(json.dumps(dev_manifest(folder / "plugin.json"), indent=2), encoding="utf-8")
    for directory in PLUGIN_DIRS:
        if (folder / directory).exists():
            shutil.copytree(folder / directory, target / directory)
    print(f"installed {folder.name} -> {target}")


def main(names):
    """Install the plugins, warning when a dependency's dev folder is missing."""
    if not DEV.exists():
        sys.exit(f"{DEV} not found: join the beta once first")
    for name in DEV_FOLDERS.values():
        if not (DEV / name / "main.lua").exists():
            print(f"warning: dev_plugins\\{name} is missing; plugins needing {name} will not load")
    for folder in plugins(names):
        install(folder)


if __name__ == "__main__":
    main(sys.argv[1:])
