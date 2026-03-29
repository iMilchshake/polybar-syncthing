#!/usr/bin/env python3


import json, ssl, urllib.request

ADDRESS = "https://127.0.0.1:8384"  # u might need to change port if u reconfigured this
API_KEY = ""  # get via GUI or get from config.xml

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
    completion = get("db/completion")
    p_devices = get("cluster/pending/devices")
    p_folders = get("cluster/pending/folders")
except Exception as e:
    print(f"script error: {e}")
    exit()

connected = sum(1 for d in conns["connections"].values() if d["connected"])
total = len(conns["connections"])
syncing = completion["completion"] < 100
has_error = bool(errors.get("errors"))
pending = len(p_devices) + len(p_folders)

# requires nerdfonts https://www.nerdfonts.com
status = "󰴋 " if syncing else "󱥾 "
errmsg = " warning" if has_error else ""
pendmsg = (f" 󱧊 {len(p_folders)}" if p_folders else "") + (
    f" 󰭙 {len(p_devices)}" if p_devices else ""
)
print(f"{connected}/{total} {status}{pendmsg}{errmsg}")
