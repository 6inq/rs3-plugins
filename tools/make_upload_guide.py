import json
import pathlib

HUB = pathlib.Path(__file__).resolve().parent.parent
OUT = HUB / "UPLOAD_GUIDE.md"

PLUGINS = [
    {
        "folder": "bank-organizer",
        "zip_name": "bank-organizer",
        "tests": [
            "prl bank-organizer, open your bank, choose My tabs, press Analyze Bank: items are tinted by tab.",
            "Open Blueprint: one tab shows; the dropdown and Previous / Next reach every tab.",
            "Press Start Sorting on a tab: MOVE marks an item and a white line runs to its target.",
            "On a 'Drag X onto Tab N' step the line ends on that tab's button (if not, note the console line).",
            "Pick the item up and drag: the line stays. Top-row labels are not hidden by the tab bar.",
            "Arrow check: dark outline, arrowhead, a bar in the gap on insert steps, an outline on the tab or + button.",
            "Sort inside tabs: Smart puts a gear tab in style order (melee, ranged, magic, necro) and slot order; try Name and Keep my order.",
            "On a bank with no custom tabs (or a fresh test account), My tabs says so and the arrow points at the + button.",
            "Make a wrong move on purpose (swap instead of insert): 'Not quite' shows, the arrow walks you back, then the original move returns.",
            "Right-click an item, Ignore (Bank Organizer): it loses its tint, gets a grey outline and the guide skips it; Stop ignoring brings it back.",
            "Rearrange two tabs, open infinity: tab numbers and the arrow follow the order you see.",
            "Sort inside tabs: Value puts the most valuable item of each tab first.",
            "Sort inside tabs: Quantity (highest first) puts the biggest stacks first; Quantity (lowest first) the smallest.",
            "Share or Load a Setup: copy your code, change a tab, paste the code back and press Enter: your setup returns.",
            "Right-click an item: one entry, Tags. Set a category, a placement (try Sell and Vanity) and Ignore; labels and the sidebar count update.",
            "A partyhat or Santa hat sits at the top of infinity; Sell, Alch, Disassemble and Trash items gather at the bottom.",
            "Decant labels: part-dose potions you can combine say DECANT; turn a dose off in settings and its labels go.",
            "Sort direction: Vertical, then follow the guide: each tab fills down the columns.",
            "Labels read Active, Van, Fav, Sell, Alch, Dis, Trash, Decant, centred inside the slot; change a colour under Tag label colours.",
            "Tags on a 3-dose potion: tick Never label for decanting; its DECANT label goes.",
            "My tabs, Tab Layout, Move right on a tab, Start Sorting: drag the named tab button where the arrow points; the guide moves on and pins follow.",
            "Start Sorting is green right under Analyze Bank and turns into a red Stop Sorting.",
            "After testing, send PluginData.db (bank-organizer-ui and the export) so the tab bar and gear styles can be pinned down.",
            "Tab Layout (My tabs): Remove a kind, pin a kind to another tab, Move a tab right; the legend updates.",
            "Switch to Whole bank, Tab Layout: Copy my current tabs, rename a tab (Enter), move and delete a tab.",
            "Right-click an item, Tags, pick a category: its tint changes.",
            "poff bank-organizer then pon bank-organizer: no crash, settings and layout are kept.",
        ],
    },
    {
        "folder": "flippr",
        "zip_name": "flippr",
        "blocker": (
            "On hold: not pushed or uploaded until you have tested it in game, switched it to the "
            "GE Price Library (gepl) for real 5m/1h averages, and decided on monetization."
        ),
        "tests": [
            "The panel shows \"Prices updated.\" within a minute (not \"Waiting for HTTP access\").",
            "Flips list shows items with icons, buy/sell prices and profit.",
            "Check the top Regular flips against the GE: real spreads, or one-off troll trades?",
            "Hold an item, then Sold: realized profit goes up. Restart the client: holdings remain.",
            "Turn Dump Mode off, restart: it stays off.",
            "Press Dashboard: session, week, month and all-time totals show, and the sold trade is listed with its date.",
            "Restart the client: past trades and all-time/week/month totals remain; the session total starts again at 0.",
        ],
    },
    {
        "folder": "zuk-fire-lines",
        "zip_name": "zuk-fire-lines",
        "blocker": (
            "The fire-line ids are not known yet. Turn on the Arena inspector, fight Zuk, read the ids of "
            "the moving entries, and enter them in the settings (then send them over to build in). If the "
            "inspector shows no moving fire at all, the lines are projectiles or effects and need Jagex's docs."
        ),
        "tests": [
            "Settings: turn on Arena inspector. Fight Zuk; open the panel: moving entries are listed first.",
            "Enter the fire lines' ids in Fire-line ids: tiles appear under each line and follow it.",
            "Tiles disappear as soon as each line passes.",
            "Switch 3 tiles / 5 tiles and change the colour: both apply instantly.",
            "Turn the Arena inspector off again before uploading.",
        ],
    },
    {
        "folder": "auto-screenshot",
        "zip_name": "auto-screenshot",
        "blocker": (
            "Plugins cannot take screenshots or save files yet. Until Jagex adds that and "
            "`src/game/capture.lua` is wired to it, the plugin only lists the moments it would capture. "
            "Test the triggers on Monday, but hold the upload until the API exists."
        ),
        "tests": [
            "Open the panel (ribbon icon): it says screenshots aren't available yet.",
            "Gain a level with 'All levels' selected: it appears under Recent moments.",
            "With the default 99s & 120s option, a normal level does not appear.",
            "Get (or watch) a broadcast: only your own name triggers it, not other players'.",
            "Complete an achievement: it appears under Recent moments (if not, note the exact chat wording so it can be added).",
        ],
    },
    {
        "folder": "where-am-i-facing",
        "zip_name": "where-am-i-facing",
        "tests": [
            "Take a step: an arrow appears on the ground at your feet, pointing the way you walked.",
            "Walk 3+ steps north, east, south, west. Then stand still and click to face an NPC: the arrow turns with you (calibrated).",
            "Check the arrow lies on the ground on a slope or stairs, and is not hidden or floating.",
            "Settings (gear): change the arrow colour; the arrow re-tints immediately.",
            "Turn on Show compass window: a draggable window shows the arrow and the direction text.",
            "If the arrow ever points wrong, press Recalibrate and walk another lap.",
        ],
    },
]


def manifest(folder):
    return json.loads((HUB / folder / "plugin.json").read_text(encoding="utf-8"))


def listing_body(folder):
    text = (HUB / folder / "docs" / "MODIO_LISTING.md").read_text(encoding="utf-8")
    body = "\n" + text[text.index("## Basics"):]
    return body.replace("\n## ", "\n### ").replace("### Basics", "### mod.io form: Basics", 1).lstrip("\n")


def whats_new(folder, version):
    path = HUB / folder / "CHANGELOG.md"
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")
    start = text.find(f"## {version}")
    if start < 0:
        return []
    end = text.find("\n## ", start + 1)
    body = text[start:end if end > 0 else None].split("\n", 1)[1].strip()
    return ["### What's new", body.replace("\n### ", "\n#### "), ""]


def section(plugin):
    info = manifest(plugin["folder"])
    zip_path = HUB / plugin["folder"] / "dist" / f"{plugin['zip_name']}-{info['version']}.zip"
    lines = [f"## {info['name']} {info['version']}", ""]
    if plugin.get("blocker"):
        lines += [f"> **Blocker:** {plugin['blocker']}", ""]
    lines += [
        f"- **Upload file:** `{zip_path}`",
        f"- **Repo:** {info['repo']}",
        f"- **Permissions in plugin.json:** {', '.join(info.get('requiredPermissions') or []) or 'none'}",
        "",
    ]
    lines += whats_new(plugin["folder"], info["version"])
    lines += ["### Test in game first"]
    lines += [f"- [ ] {step}" for step in plugin["tests"]]
    lines += ["", listing_body(plugin["folder"]).rstrip(), "", "---", ""]
    return lines


def main():
    names = ", ".join(manifest(p["folder"])["name"] for p in PLUGINS)
    lines = [
        "# Plugin upload guide",
        "",
        f"Everything needed to upload **{names}** to mod.io. Generated by `tools/make_upload_guide.py` from each plugin's own listing doc; re-run it after any change.",
        "",
        "## Push to GitHub",
        "Every repo commits locally first. Push each one (with its version tags) from the hub folder:",
        "",
        "```bash",
        "cd C:/Claude/rs3-plugins && for d in . bank-organizer where-am-i-facing zuk-fire-lines auto-screenshot; do git -C $d push --follow-tags origin main; done",
        "```",
        "",
        "Flippr has no GitHub remote on purpose; it stays local until it is tested.",
        "",
        "## Before you start",
        "1. Test each plugin in game using its checklist below.",
        "2. Rebuild the upload zips (run inside each plugin folder):",
        "",
        "```bash",
        "python tools/build.py",
        "```",
        "",
        "3. For each plugin: open https://mod.io/g/runescape, click Add plugin, fill in the form from its section below, click **Create Plugin**, then upload its zip as the plugin file and add your listing image (16:9, min 512x288, max 8MB).",
        "4. Every plugin depends on **PrettyUI** (mod.io id 6398181); it installs automatically for players.",
        "5. Start each one **Private**, switch to **Public** once you're happy.",
        "",
        "---",
        "",
    ]
    for plugin in PLUGINS:
        lines += section(plugin)
    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
