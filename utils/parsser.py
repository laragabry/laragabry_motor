import json

def load_zones(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["zones"], data["zone_types"]