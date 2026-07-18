# Neverlost Local Plugin Installation

The judge demonstration does **not** require plugin installation. Run `python3 scripts/run_stage4_demo.py` from the cloned repository for the fastest test path.

These optional instructions expose the three Neverlost skills through a personal Codex plugin marketplace.

## Supported plugin surfaces

- ChatGPT desktop app in Work mode
- Codex in the ChatGPT desktop app
- Codex CLI

Local filesystem plugin installation is not required for the deterministic Python demonstration.

## 1. Place the plugin in the personal plugin directory

### macOS or Linux

```bash
mkdir -p ~/plugins
git clone https://github.com/Neverlost-AI/Neverlost-build-week.git ~/plugins/neverlost-build-week
```

### Windows PowerShell

```powershell
New-Item -ItemType Directory -Force "$HOME\plugins" | Out-Null
git clone https://github.com/Neverlost-AI/Neverlost-build-week.git "$HOME\plugins\neverlost-build-week"
```

The resulting plugin folder must contain:

```text
neverlost-build-week/
├── .codex-plugin/plugin.json
└── skills/
    ├── capacity-output/SKILL.md
    ├── full-human-pathway/SKILL.md
    └── neverlost-review-workflow/SKILL.md
```

## 2. Add the personal marketplace entry

Create or update:

- macOS/Linux: `~/.agents/plugins/marketplace.json`
- Windows: `$HOME\.agents\plugins\marketplace.json`

If the file already contains other plugins, preserve them and add only the Neverlost entry to its existing `plugins` array.

```json
{
  "name": "personal",
  "interface": {
    "displayName": "Personal"
  },
  "plugins": [
    {
      "name": "neverlost-build-week",
      "source": {
        "source": "local",
        "path": "./plugins/neverlost-build-week"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

The default personal marketplace is discovered automatically; do not add it again with `codex plugin marketplace add`.

## 3. Install in the ChatGPT desktop app

1. Restart the ChatGPT desktop app.
2. Open ChatGPT in Work mode or open Codex.
3. Open **Plugins**.
4. Select the **Personal** marketplace.
5. Open **Neverlost: The Full Human Pathway** and select the install button.
6. Start a new chat after installation.

Suggested first prompt:

```text
Use Neverlost: The Full Human Pathway to map the included synthetic vocational case. Preserve source authority, capacity conditions, variability, recovery cost, pathway bridges, and human-review boundaries.
```

## 4. Verify without the plugin UI

From the repository root:

### macOS or Linux

```bash
python3 scripts/smoke_test.py
python3 scripts/run_stage4_demo.py
```

### Windows PowerShell

```powershell
py -3 scripts/smoke_test.py
py -3 scripts/run_stage4_demo.py
```

The smoke test validates the manifest and all three skill directories. The demo reproduces the synthetic Stage 4 evidence without an API key or external service.

## Update an existing local copy

Pull the latest repository commit, restart the ChatGPT desktop app, and reinstall or refresh the local plugin from the Personal marketplace. Keep the marketplace entry unchanged unless the plugin path changes.
