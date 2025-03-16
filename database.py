import json
import os
from config import FORCE_SUB_FILE, USERS_FILE, LIST_FILE, START_FILE

def load_json(filename, default):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return default
    return default

def save_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# JSON fayllarni yaratish
for file in [FORCE_SUB_FILE, USERS_FILE, LIST_FILE, START_FILE]:
    if not os.path.exists(file):
        with open(file, "w") as f:
            json.dump([] if "list" in file else {}, f)
