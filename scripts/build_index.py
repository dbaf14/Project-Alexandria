#!/usr/bin/env python3
"""
build_index.py

Baut alle Index-Dateien in meta/ komplett neu aus dem aktuellen Inhalt von
category/ und connections/. Wird immer NACH assign_ids.py und
validate_entries.py ausgefuehrt, damit IDs final und Daten gueltig sind.

Erzeugt:
- meta/analyzed_sources.json
- meta/statistics.json
- meta/tags.json
- meta/category_index.json
- meta/dependency_index.json
- meta/search_index.json

(meta/duplicate_check.json wird separat von detect_duplicates.py erzeugt,
 meta/id_counters.json separat von assign_ids.py)
"""
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATEGORY_DIR = ROOT / "category"
CONNECTIONS_DIR = ROOT / "connections"
META_DIR = ROOT / "meta"


def load_all_entries():
    entries = []
    for json_file in sorted(CATEGORY_DIR.rglob("*.json")):
        with open(json_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                continue
        data["_category"] = json_file.parent.name
        data["_file"] = str(json_file.relative_to(ROOT))
        entries.append(data)
    return entries


def load_all_connections():
    connections = []
    if not CONNECTIONS_DIR.exists():
        return connections
    for json_file in sorted(CONNECTIONS_DIR.glob("*.json")):
        with open(json_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                continue
        connections.append(data)
    return connections


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def build_analyzed_sources(entries):
    sources = [
        {
            "id": e.get("id", "unknown"),
            "type": e.get("type", "unknown"),
            "category": e.get("_category", "unknown"),
            "name": e.get("name", "unknown"),
            "location": e.get("location", "unknown"),
            "status": e.get("status", "unknown"),
            "file": e.get("_file"),
        }
        for e in entries
    ]
    write_json(META_DIR / "analyzed_sources.json", {
        "count": len(sources),
        "sources": sources,
    })


def build_statistics(entries, connections):
    by_category = defaultdict(int)
    by_type = defaultdict(int)
    by_status = defaultdict(int)
    by_development = defaultdict(int)
    works_true = works_false = works_unknown = 0

    for e in entries:
        by_category[e.get("_category", "unknown")] += 1
        by_type[e.get("type", "unknown")] += 1
        by_status[e.get("status", "unknown")] += 1
        by_development[e.get("development", "unknown")] += 1
        works = e.get("works")
        if works is True:
            works_true += 1
        elif works is False:
            works_false += 1
        else:
            works_unknown += 1

    write_json(META_DIR / "statistics.json", {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_entries": len(entries),
        "total_connections": len(connections),
        "by_category": dict(sorted(by_category.items())),
        "by_type": dict(sorted(by_type.items())),
        "by_status": dict(sorted(by_status.items())),
        "by_development": dict(sorted(by_development.items())),
        "works": {
            "true": works_true,
            "false": works_false,
            "unknown": works_unknown,
        },
    })


def build_tags(entries):
    tags = defaultdict(list)
    for e in entries:
        for tag in e.get("tags", []):
            tags[tag].append(e.get("id", "unknown"))
    write_json(META_DIR / "tags.json", {
        "unique_tags": len(tags),
        "tags": {k: sorted(v) for k, v in sorted(tags.items())},
    })


def build_category_index(entries):
    categories = defaultdict(list)
    for e in entries:
        categories[e.get("_category", "unknown")].append(e.get("id", "unknown"))
    write_json(META_DIR / "category_index.json", {
        "categories": {k: sorted(v) for k, v in sorted(categories.items())},
    })


def build_dependency_index(entries):
    deps = defaultdict(list)
    for e in entries:
        for dep in e.get("depends_on", []):
            deps[dep].append(e.get("id", "unknown"))
    write_json(META_DIR / "dependency_index.json", {
        "unique_dependencies": len(deps),
        "dependencies": {k: sorted(v) for k, v in sorted(deps.items())},
    })


def build_search_index(entries):
    index = []
    for e in entries:
        searchable_text = " ".join(filter(None, [
            e.get("name", ""),
            e.get("type", ""),
            e.get("_category", ""),
            " ".join(e.get("tags", [])),
            " ".join(e.get("problems", [])),
            " ".join(e.get("depends_on", [])),
        ])).lower()
        index.append({
            "id": e.get("id", "unknown"),
            "name": e.get("name", "unknown"),
            "category": e.get("_category", "unknown"),
            "tags": e.get("tags", []),
            "text": searchable_text,
        })
    write_json(META_DIR / "search_index.json", {
        "count": len(index),
        "entries": index,
    })


def main():
    entries = load_all_entries()
    connections = load_all_connections()

    build_analyzed_sources(entries)
    build_statistics(entries, connections)
    build_tags(entries)
    build_category_index(entries)
    build_dependency_index(entries)
    build_search_index(entries)

    print(f"Index built from {len(entries)} entries and {len(connections)} connections.")


if __name__ == "__main__":
    main()
