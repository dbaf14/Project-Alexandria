#!/usr/bin/env python3
"""
detect_duplicates.py

Detects possible duplicates among the category/**/*.json entries:

1. Exact duplicates: identical (normalized) "location" URL
2. Likely duplicates: very similar "name" (SequenceMatcher ratio above
   THRESHOLD), regardless of category

Writes the result to meta/duplicate_check.json. Does NOT fail the
workflow — it only serves as a hint for humans/agents. The actual
judgment ("is this really a duplicate?") is deliberately left to
Phase 3 (Rule 2: no evaluations).
"""
import json
from difflib import SequenceMatcher
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
CATEGORY_DIR = ROOT / "category"
OUTPUT_FILE = ROOT / "meta" / "duplicate_check.json"

NAME_SIMILARITY_THRESHOLD = 0.88


def normalize_location(location):
    if not location or location == "unknown":
        return None
    loc = location.strip().lower()
    loc = loc.rstrip("/")
    for prefix in ("https://www.", "http://www.", "https://", "http://"):
        if loc.startswith(prefix):
            loc = loc[len(prefix):]
            break
    return loc


def normalize_name(name):
    if not name:
        return ""
    return " ".join(name.strip().lower().split())


def load_entries():
    entries = []
    for json_file in sorted(CATEGORY_DIR.rglob("*.json")):
        with open(json_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                continue
        entries.append({
            "id": data.get("id", "unknown"),
            "name": data.get("name", ""),
            "location": data.get("location", ""),
            "category": json_file.parent.name,
            "file": str(json_file.relative_to(ROOT)),
        })
    return entries


def find_location_duplicates(entries):
    groups = {}
    for entry in entries:
        norm = normalize_location(entry["location"])
        if norm is None:
            continue
        groups.setdefault(norm, []).append(entry["id"])

    return [
        {"reason": "identical_location", "ids": ids}
        for ids in groups.values() if len(ids) > 1
    ]


def find_name_duplicates(entries):
    results = []
    seen_pairs = set()
    normed = [(e["id"], normalize_name(e["name"])) for e in entries if e["name"]]

    for i in range(len(normed)):
        id_a, name_a = normed[i]
        for j in range(i + 1, len(normed)):
            id_b, name_b = normed[j]
            pair = tuple(sorted((id_a, id_b)))
            if pair in seen_pairs:
                continue
            ratio = SequenceMatcher(None, name_a, name_b).ratio()
            if ratio >= NAME_SIMILARITY_THRESHOLD:
                seen_pairs.add(pair)
                results.append({
                    "reason": "similar_name",
                    "ids": list(pair),
                    "similarity": round(ratio, 3),
                })
    return results


def main():
    entries = load_entries()
    duplicates = find_location_duplicates(entries) + find_name_duplicates(entries)

    output = {
        "generated_from": "scripts/detect_duplicates.py",
        "total_entries_checked": len(entries),
        "potential_duplicates_found": len(duplicates),
        "note": "Automatically generated. No evaluation, hint only (Rule 2).",
        "duplicates": duplicates,
    }

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Checked {len(entries)} entries, found {len(duplicates)} potential duplicate group(s).")


if __name__ == "__main__":
    main()
