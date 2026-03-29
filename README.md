# polybar-syncthing

Polybar widget for syncthing status via its REST API. Shows number of connected devices, sync state of folders, pending folders/devices, and errors.

## Setup

1. Set `API_KEY` in `syncthing-status.py`
   - GUI: Actions → Settings → API Key
   - CLI: `grep apikey ~/.local/state/syncthing/config.xml`

2. Add to polybar config:
   ```ini
   [module/syncthing]
   type = custom/script
   exec = python3 /path/to/syncthing-status.py
   interval = 15
   ```
