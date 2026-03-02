"""Device inventory — loads NETWORK.json once and exposes the 'devices' dict.

All tools that need to look up a device by name import 'devices' from here.
"""
import json
import os

_INVENTORY_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "inventory", "NETWORK.json"
)

if not os.path.exists(_INVENTORY_FILE):
    raise RuntimeError(f"Inventory file not found: {_INVENTORY_FILE}")

with open(_INVENTORY_FILE) as _f:
    devices: dict = json.load(_f)
