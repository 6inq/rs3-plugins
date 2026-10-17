# RS3 Plugin API: reverse-engineered notes (2026-10-17)

Jagex has published no public docs yet. Everything below is inferred from the six live plugins on mod.io (game id 13295): Quest Helper, Menu Entry Swapper, Job Gauges, Entity Hider, Tilemarkers and PrettyUI.

## Package
- The package is a zip containing `plugin.json` and `main.lua`, plus any Lua modules and resources.
- `plugin.json` fields:
  - `name`, `version`, `contactEmailAddress`, `author`, `repo`
  - `hasRibbonIcon`, `hasSettingsIcon`
  - `requiredDependencies {slug: modioId}`, `optionalDependencies`
  - `requiredPermissions`, `optionalPermissions` (HTTP needs a permission)
- `require("src/x/y")` uses paths relative to the plugin root.
- A dependency is exposed as a global named by its slug (for example `prettyui`).
- `Plugin.resources.<file>` holds bundled images.
- `function PluginShutdown()` is a global hook that is called on disable/reload.

## Globals seen
- `Event.<Name>.Subscribe(id, fn)` / `.Unsubscribe(id)`, where `<Name>` is one of:
  - `Logic` (`event.logicTick`), `ServerLogic`, `Draw`
  - `InventoryUpdated` (`event.inv.id`)
  - `MiniMenuReady` (`event.miniMenu`), `MiniMenuOpened`, `MiniMenuClosed`, `MiniMenuEntrySelected` (`event.entry`)
  - `ContentLayerReady` (ribbon panel, `event.component`), `SettingsLayerReady`
  - `VarTransmit`, `ChatMessage`, `KeyDown`, `KeyUp`, `GameStateChanged`, `WindowFocusChanged`, `EntityDraw`
- `Inventory.Find(config.Inv.BANK | INV | WORN | METAL_BANK | MONEY_POUCH)`:
  - fields `.isValid`, `.freeSlotCount`
  - methods `:GetSlots()` (each slot has `.obj` and `.count`), `:GetSlot(i)`, `:GetTotal(objId)`, `:GetCategoryTotal(catId)`
- `config.Obj.FromID(id)` returns an `ObjType` with `.id`, `.name`, `.configName`, `.category`, `.params`, `.interfaceOpNames`.
- `id.Category.FromID(n)` returns a name string (for example `WEAPON_...`, `AMMO_...`); `id.Category[name]` returns the number.
- `id.Interface.BANK`, `id.Component["BANK__BANK_INV"]` (the slot grid), `id.Component["BANK__ALL"]` (the bank root), `id.Font.MUSEO_SANS_15PT_REGULAR`.
- `ui.Interfaces:GetInterface(id)` and `:GetComponent(id)` / `:GetComponent(interfaceID, staticID)`.
- Components:
  - fields `x`, `y`, `width`, `height`, `visible`, `visibleGlobal`, `hidden`, `type`, `associatedObjectID`, `associatedObjectQuantity`, `parent`, `scrollX`, `scrollY`
  - methods `:IterateDynamicComponents(fn)` (return `true` to stop), `:SetPos`, `:SetSize`, `:Subscribe(ui.Hook.X, id, fn)`, `:Destroy()`
- Drawing primitives: `ui.Rectangle.new(parent)` (`.fill`, `.rgba` `0xRRGGBBAA`, `.colour` Vector4, `.outlineThickness`, `.clickthrough`), `ui.Text.new(parent)` (`.content`, `.font`, `.rgba`), `ui.Sprite.new`, `ui.Layer.new`.
- `var.VarPlayer.BANK_CURRENT_TAB.value` (1 = All items), `var.VarPlayer.BANK_FILTER`, `var.VarClient.BANK_SEARCHMODE_CLIENT`, `var.VarClient.BANK_LASTSEARCHSTRING`.
- `PersistentDB:Get/Set{Bool,Int,String,StructuredData}(key[, value])`, `:Delete(key)`.
- Mini menu:
  - `MiniMenu.IsOpen()`
  - `miniMenu.entries`, where each entry has `.componentData.component` and `.componentData.objConfig`, plus `.verbText`
  - `miniMenu:Add(label, fn)`, `prettyui.MiniMenu.AddSubmenu(menu, label, children)`
- Other globals: `log(...)`, `utils.CalcTextWidth(font, text)`, `Vector4.new`.
- `ui.Interfaces:GetComponent(id.Component.TOPLEVEL_V2__PLUGIN_BUILD_LAYER_TOP)` is a host layer for floating windows.
