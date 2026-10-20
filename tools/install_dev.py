import json
import pathlib
import shutil
import sys

HUB = pathlib.Path(__file__).resolve().parent.parent
DEV = pathlib.Path(r"C:\ProgramData\Jagex\RuneScape-BETA\dev_plugins")
DEV_FOLDERS = {6398181: "prettyui", 6414886: "gepl"}
PLUGIN_FILES = ["plugin.json", "main.lua"]
PLUGIN_DIRS = ["src", "resources"]


def plugins(names):
    folders = [HUB / name for name in names] if names else sorted(p for p in HUB.iterdir() if (p / "plugin.json").exists())
    return [f for f in folders if (f / "plugin.json").exists()]


def dev_manifest(path):
    manifest = json.loads(path.read_text(encoding="utf-8"))
    for key in ("requiredDependencies", "optionalDependencies"):
        deps = manifest.get(key) or {}
        if isinstance(deps, dict):
            manifest[key] = {alias: DEV_FOLDERS.get(target, target) for alias, target in deps.items()}
    return manifest


def install(folder):
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
    if not DEV.exists():
        sys.exit(f"{DEV} not found: join the beta once first")
    for name in DEV_FOLDERS.values():
        if not (DEV / name / "main.lua").exists():
            print(f"warning: dev_plugins\\{name} is missing; plugins needing {name} will not load")
    for folder in plugins(names):
        install(folder)


if __name__ == "__main__":
    main(sys.argv[1:])
