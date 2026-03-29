# polybar-syncthing

Polybar widget for syncthing status via its REST API. Shows number of connected devices, sync state, conflicts, pending folders/devices, and errors.

## Setup

1. Set your API key, either:
   - **Manual:** set `API_KEY` in `syncthing-status.py`
     - GUI: Actions → Settings → API Key
     - CLI: `grep apikey ~/.local/state/syncthing/config.xml`
   - **Auto:** use the `--auto-key` flag (reads from `~/.local/state/syncthing/config.xml`)

2. Add to polybar config:
   ```ini
   [module/syncthing]
   type = custom/script
   exec = python3 /path/to/syncthing-status.py --auto-key
   interval = 15
   ```
