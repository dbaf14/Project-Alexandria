#!/usr/bin/env python3
"""
assign_ids.py

Scannt category/**/*.json und connections/*.json.
Vergibt fuer jeden Eintrag ohne gueltige ID eine neue eindeutige ID
(Format PREFIX-000001), setzt sie im JSON und benennt die Datei passend um.
Der Prefix haengt beim Eintrag vom Feld "type" ab, bei Connections ist er
immer CON.

Zaehler werden persistent in meta/id_counters.json gehalten, damit IDs auch
ueber mehrere Workflow-Laeufe hinweg eindeutig bleiben.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATEGORY_DIR = ROOT / "category"
CONNECTIONS_DIR = ROOT / "connections"
COUNTERS_FILE = ROOT / "meta" / "id_counters.json"

TYPE_PREFIX = {
    "github": "GH",
    "paper": "PAPER",
    "patent": "PAT",
    "documentation": "DOC",
    "dataset": "DATA",
    "research_project": "RES",
    "historical_document": "HIST",
    "other": "SRC",
}
DEFAULT_PREFIX = "SRC"
CONNECTION_PREFIX = "CON"


def load_counters():
    if COUNTERS_FILE.exists():
        with open(COUNTERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_counters(counters):
    COUNTERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(COUNTERS_FILE, "w", encoding="utf-8") as f:
        json.dump(counters, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write("\n")


def next_id(counters, prefix):
    current = counters.get(prefix, 0) + 1
    counters[prefix] = current
    return f"{prefix}-{current:06d}"


def needs_id(value):
    return value is None or value == "" or value == "unknown"


def process_entry_file(path, counters, changed_files):
    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"  [SKIP] {path}: invalid JSON ({e})")
            return

    entry_type = data.get("type", "other")
    prefix = TYPE_PREFIX.get(entry_type, DEFAULT_PREFIX)
    current_id = data.get("id")

    assigned_new = False
    if needs_id(current_id):
        new_id = next_id(counters, prefix)
        data["id"] = new_id
        assigned_new = True
        print(f"  [ID] {path.name} -> {new_id}")
    else:
        new_id = current_id

    target_path = path.with_name(f"{new_id}.json")

    write_json(path, target_path, data)
    if assigned_new or target_path != path:
        changed_files.append(target_path)


def process_connection_file(path, counters, changed_files):
    with open(path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"  [SKIP] {path}: invalid JSON ({e})")
            return

    current_id = data.get("id")
    assigned_new = False
    if needs_id(current_id):
        new_id = next_id(counters, CONNECTION_PREFIX)
        data["id"] = new_id
        assigned_new = True
        print(f"  [ID] {path.name} -> {new_id}")
    else:
        new_id = current_id

    target_path = path.with_name(f"{new_id}.json")
    write_json(path, target_path, data)
    if assigned_new or target_path != path:
        changed_files.append(target_path)


def write_json(old_path, new_path, data):
    with open(old_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    if new_path != old_path:
        old_path.rename(new_path)


def main():
    counters = load_counters()
    changed_files = []

    if CATEGORY_DIR.exists():
        for json_file in sorted(CATEGORY_DIR.rglob("*.json")):
            process_entry_file(json_file, counters, changed_files)

    if CONNECTIONS_DIR.exists():
        for json_file in sorted(CONNECTIONS_DIR.glob("*.json")):
            process_connection_file(json_file, counters, changed_files)

    save_counters(counters)
    print(f"Done. {len(changed_files)} file(s) touched.")


if __name__ == "__main__":
    main()
