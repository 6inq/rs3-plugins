# 6ing's RS3 Plugins

The hub for my RuneScape 3 plugins for the official Plugin Hub (hosted on [mod.io](https://mod.io/g/runescape)). Each plugin lives in its own repository; this repo is the index plus shared notes.

## Plugins

| Plugin | Version | What it does | Repo |
|---|---|---|---|
| Bank Organizer | 1.1.0 | Colour-codes your bank by category and guides you through sorting it, one move at a time. | [6inq/bank-organizer](https://github.com/6inq/bank-organizer) |
| WhereAmIFacing | 1.0.0 | A compass arrow showing which way your character faces (N, NE, E, SE, S, SW, W, NW), in any colour. | [6inq/whereamifacing](https://github.com/6inq/whereamifacing) |

## Shared docs
- [RS3_API_NOTES.md](docs/RS3_API_NOTES.md): the RS3 plugin Lua API as reverse-engineered from the plugins already live on mod.io. Jagex had not published official docs when this was written.

## Working locally
Clone the hub, then clone each plugin inside it (plugin folders are git-ignored here):

```bash
git clone https://github.com/6inq/rs3-plugins.git
```

```bash
git clone https://github.com/6inq/bank-organizer.git rs3-plugins/bank-organizer
```

```bash
git clone https://github.com/6inq/whereamifacing.git rs3-plugins/where-am-i-facing
```

Created by **6ing**.
