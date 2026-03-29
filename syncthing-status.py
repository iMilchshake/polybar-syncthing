#!/usr/bin/env python3


import glob, json, os, re, ssl, sys, urllib.request

ADDRESS = "https://127.0.0.1:8384"  # u might need to change port if u reconfigured this
API_KEY = ""  # set manually, or use --auto-key to read from config.xml

# --auto-key: read API key from ~/.local/state/syncthing/config.xml
if "--auto-key" in sys.argv:
    config_path = os.path.expanduser("~/.local/state/syncthing/config.xml")
    m = re.search(r"<apikey>(.+?)</apikey>", open(config_path).read())
    if not m:
        exit("Error: could not find API key in config.xml")
    API_KEY = m.group(1)

if API_KEY == "":
    exit("Error: configure API key")


def get(path):
    req = urllib.request.Request(
        f"{ADDRESS}/rest/{path}", headers={"X-API-Key": API_KEY}
    )
    with urllib.request.urlopen(
        req, timeout=5, context=ssl._create_unverified_context()
    ) as r:
        return json.loads(r.read())


try:
    conns = get("system/connections")
    errors = get("system/error")
    p_devices = get("cluster/pending/devices")
    p_folders = get("cluster/pending/folders")
    connected_ids = [did for did, d in conns["connections"].items() if d["connected"]]
    connected = len(connected_ids)
    total = len(conns["connections"])
    completions = [get("db/completion")] + [
        get(f"db/completion?device={did}") for did in connected_ids
    ]
    syncing = any(c["completion"] < 100 for c in completions)
    # --conflicts: scan folder paths for conflict files (not exposed via REST API)
    # TODO: cache result to /tmp with a TTL to avoid scanning on every poll
    if "--conflicts" in sys.argv:
        folders = get("config/folders")
        conflicts = sum(
            len(glob.glob(f"{f['path']}/**/*.sync-conflict-*", recursive=True))
            for f in folders
        )
    else:
        conflicts = 0
except Exception as e:
    print(f"script error: {e}")
    exit()
has_error = bool(errors.get("errors"))
pending = len(p_devices) + len(p_folders)

# requires nerdfonts https://www.nerdfonts.com
status = "󰴋" if syncing else "󱥾"
conflictmsg = f" 󰷌 {conflicts}" if conflicts else ""
errmsg = "  warning" if has_error else ""
pendmsg = (f" 󱧊 {len(p_folders)}" if p_folders else "") + (
    f" 󰭙 {len(p_devices)}" if p_devices else ""
)
print(f"{connected}/{total} {status}{pendmsg}{conflictmsg}{errmsg}")
