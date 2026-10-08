# Dota 2 Minify - Mod Template

A complete, all-purpose boilerplate and reference implementation for creating mods for [Dota 2 Minify](https://github.com/egezenn/dota2-minify).

Use this repository to learn every supported modding method, conditionality directive, template variable, and lifecycle hook, or clone it as a starting point for your own mods.

<small>a bit rushed, sorry</small>

## Mod Submission

Submit a PR to [community-mods](https://github.com/Dota-Modding-Community/community-mods) repository.

## 📁 Repository Structure

```text
mod-template/
├── src/                          # The actual mod directory loaded by Minify
│   ├── manifest.json             # Mod metadata and UI settings schema
│   ├── blacklist.txt             # Conditional asset blanking rules
│   ├── styling.css               # Target-based Panorama CSS injections
│   ├── xml.json                  # Conditional XML modifications and inclusions
│   ├── replacer.json             # Conditional asset redirects / swaps
│   ├── remap.json                # Resource reference remapping
│   ├── files/                    # Pre-compiled files copied to final VPK
│   ├── files_uncompiled/         # Source files compiled by resourcecompiler
│   ├── script_utility.py         # Custom functions triggered by UI buttons
│   ├── script.py                 # Lifecycle hooks for Python build automation
│   └── notes.md                  # Localized mod description shown in Minify UI
├── .gitignore
└── README.md
```

## Getting Started

### 1. Clone or Use This Template

Click **Use this template** on GitHub or clone this repository:

```bash
git clone https://github.com/<your-username>/<your-mod-name>.git --depth 1
```

### 2. Link `src/` to Your Minify Mods Folder

To test your mod live in Dota 2 Minify, create a directory junction / symlink from `src/` into Minify's `mods/` directory:

**Windows (PowerShell):**

```powershell
New-Item -ItemType Junction -Path "path\to\dota2-minify\Minify\mods\My Mod Name" -Target "path\to\mod-template\src"
```

**Linux / macOS:**

```bash
ln -s /path/to/mod-template/src /path/to/dota2-minify/Minify/mods/"My Mod Name"
```

### 3. Release & Automated Packaging

This repository includes a GitHub Actions workflow that automatically packages `src/` into a downloadable zip file and creates a GitHub Release when you push a version tag:

```bash
# Tag a new version
git tag v1.0.0

# Push the tag to trigger the automated release workflow
git push origin v1.0.0
```

Once pushed, GitHub Actions will:

1. Bundle all mod files in `src/` into `<repo-name>.zip`.
2. Create a new GitHub Release with the zip file attached and auto-generated release notes.

## 📖 Feature Reference Guide

### 1. `manifest.json` (Metadata & UI Settings)

Defines mod metadata, dependencies, conflicts, and configurable settings in the Minify GUI.

```json
{
  "name": "My Custom Mod",
  "author": "Author Name",
  "description": "Short summary of what this mod does.",
  "version": "1.0.0",
  "category": "huds",
  "settings": [
    {
      "key": "hide_hud",
      "text": "Hide HUD Elements",
      "type": "checkbox",
      "default": true
    },
    {
      "key": "theme_variant",
      "text": "UI Theme",
      "type": "combo",
      "items": ["dark", "light", "minimal"],
      "default": "dark"
    },
    {
      "key": "custom_title",
      "text": "Header Title",
      "type": "inputbox",
      "default": "Enhanced HUD"
    },
    {
      "key": "accent_color",
      "text": "Glow Color",
      "type": "color",
      "default": "#00FFCC"
    },
    {
      "key": "hud_opacity",
      "text": "HUD Opacity",
      "type": "slider",
      "min": 0,
      "max": 1,
      "step": 0.05,
      "default": 0.85
    },
    {
      "key": "run_utility",
      "text": "Execute Custom Action",
      "type": "button"
    }
  ]
}
```

#### Supported Setting Types:

| Type                | Description              | Default / Format                      |
| ------------------- | ------------------------ | ------------------------------------- |
| `checkbox`          | Boolean on/off switch    | `true` or `false`                     |
| `combo`             | Dropdown selection       | Array of string `items`               |
| `inputbox`          | Text input field         | String                                |
| `color`             | Color picker             | Hex color string (`"#RRGGBB"`)        |
| `slider` / `number` | Numeric slider / stepper | `min`, `max`, `step`, `default`       |
| `button`            | Action button            | Calls function in `script_utility.py` |

### 2. `blacklist.txt` (Asset Blanking)

Replaces targeted game files with empty 0-byte or blank assets (disabling visual or sound effects).

#### Syntax & Directives:

- `#if:<key>[:true|false|<value>]` — Opens a conditional block (nestable). Defaults to expecting `true` if `:bool` is omitted.
- `#endif[:<key>]` — Closes the conditional block.
- `<&setting_key>` — Interpolates user settings into file paths.
- `>>path/` — Matches directory prefix.
- `**pattern` — Matches rg pattern across game files.
- `*-pattern` — Excludes directory pattern.
- `--exact_path` — Excludes single file.

```text
# Always blanked
panorama/images/hud/ad_banner.vsvg

# Conditional block
#if:hide_hud
panorama/images/hud/decorations/**
panorama/images/hud/flames_<&theme_variant>.vsvg

# Nested condition
#if:hide_minimap:true
materials/ui/minimap/borders/**
#endif:hide_minimap

# Inverted boolean condition
#if:enable_sounds:false
sounds/ui/ambient_hum.vsnd_c
#endif:enable_sounds

#endif:hide_hud
```

### 3. `styling.css` (Panorama CSS Injection)

Injects custom styling directly into game Panorama stylesheets.

#### Extraction Indicators:

- `/* g:panorama/styles/... */` — Target stylesheet in game VPK (`pak01_dir.vpk`).
- `/* c:panorama/styles/... */` — Target stylesheet in core VPK (`dota_core/pak01_dir.vpk`).

#### Conditional Directives:

- `/* if:<key>[:true|false|<value>] */` — Opens a conditional CSS block.
- `/* endif[:<key>] */` — Closes the conditional CSS block.
- `<&setting_key>` — Injects setting values (colors, opacities, dimensions, font names).

```css
/* g:panorama/styles/hud/dota_hud_dashboard */
.DashboardRoot {
  opacity: <&hud_opacity>;
}

/* if:hide_hud */
.DashboardDecoration,
#HeaderGlowEffect {
  visibility: collapse;

  /* if:theme_variant:dark */
  background-color: #000000;
  /* endif:theme_variant */
}

.HeroAccentBox {
  border: 2px solid <&accent_color>;
  box-shadow: 0 0 10px <&accent_color>;
}
/* endif:hide_hud */
```

### 4. `xml.json` (Panorama Layout Modifications)

Modifies Panorama XML layout trees during build time before compilation.

#### Supported Actions:

- `set_attribute` — Sets or updates an attribute on matching element(s).
- `add_child` — Appends XML snippet as a child of matching element.
- `insert_before` — Inserts XML snippet before matching element.
- `insert_after` — Inserts XML snippet after matching element.
- `move_into` — Moves matching element into `new_parent_selector`.
- `add_style_include` — Adds a `<include src="..." />` to `<styles>`.
- `add_script` — Adds a `<include src="..." />` to `<scripts>`.

```json
{
  "panorama/layout/hud/dota_hud_root.xml": [
    {
      "if": "hide_hud",
      "action": "set_attribute",
      "selector": "#TopBarFlames",
      "attribute": "style",
      "value": "visibility: collapse;"
    },
    {
      "action": "set_attribute",
      "selector": "#CustomStatsBox",
      "attribute": "style",
      "value": "opacity: <&hud_opacity>; background-color: <&accent_color>;"
    },
    {
      "if": "theme_variant:minimal",
      "action": "add_child",
      "selector": "#HUDHeader",
      "xml": "<Panel id='MinimalIndicator' class='Theme-<&theme_variant>' hittest='false' />"
    }
  ]
}
```

### 5. `replacer.json` (Asset Replacement)

Redirects an existing game asset to load content from another asset path inside the VPK.

```json
{
  "panorama/images/hud/cursor.png": {
    "source": "panorama/images/hud/cursors/<&theme_variant>_cursor.png",
    "if": "hide_hud"
  },
  "sounds/ui/ping.vsnd_c": {
    "source": "sounds/ui/ping_minimal.vsnd_c",
    "if": "custom_sounds:true"
  },
  "materials/ui/default_banner.vmat_c": "materials/ui/banners/<&theme_variant>_banner.vmat_c"
}
```

### 6. `remap.json` (Resource Reference Remapping)

Decompiles target compiled resources, finds string references matching source paths, and rewires them to destination paths before recompilation.

```json
{
  "models/heroes/common_hero_*.vmdl_c": {
    "if": "theme_variant:minimal",
    "redirects": {
      "materials/models/heroes/glow_default.vmat": "materials/models/heroes/glow_<&theme_variant>.vmat"
    }
  },
  "panorama/layout/dashboard.xml": {
    "if": "hide_hud:true",
    "s2r://panorama/images/decorations/border.vtex": "s2r://panorama/images/empty.vtex"
  }
}
```

### 7. Python Scripts & Lifecycle Hooks

| Script Name                 | Execution Timing          | Purpose                                                                        |
| --------------------------- | ------------------------- | ------------------------------------------------------------------------------ |
| `script_utility.py`         | UI button click           | Contains functions called when clicking `"type": "button"` in `manifest.json`. |
| `script_initial.py`         | Before patch cycle starts | Pre-flight checks or downloading remote data.                                  |
| `script.py`                 | During mod patch loop     | Mod-specific setup or file generation.                                         |
| `script_after_decompile.py` | After S2V decompilation   | Modifying decompiled XMLs, stylesheets, or materials.                          |
| `script_after_recompile.py` | After resourcecompiler    | Post-compilation adjustments.                                                  |
| `script_after_patch.py`     | Build completion          | Final notifications or external synchronization.                               |
| `script_uninstall.py`       | Mod uninstalled           | Cleaning up custom external state.                                             |

### 8. `notes.md` (Multi-Language Documentation)

Shown in Minify's mod details modal. Supports multi-language tabs using `<!-- lang:<code> -->`:

```markdown
<!-- lang:en -->

English notes with markdown support.

<!-- lang:tr -->

Markdown destekli Türkçe notlar
```
