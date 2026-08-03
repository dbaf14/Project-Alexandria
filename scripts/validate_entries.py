#!/usr/bin/env python3
"""
validate_entries.py

Validates all files in category/**/*.json against schemas/entry.schema.json
and all files in connections/*.json against schemas/connection.schema.json.

Exit code 0 = all valid, 1 = at least one error.
Used both in the PR workflow (validation only) and the push workflow
(validate before building the index).
"""
import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft7Validator
except ImportError:
    print("jsonschema is missing. Install with: pip install -r scripts/requirements.txt")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
CATEGORY_DIR = ROOT / "category"
CONNECTIONS_DIR = ROOT / "connections"
ENTRY_SCHEMA = ROOT / "schemas" / "entry.schema.json"
CONNECTION_SCHEMA = ROOT / "schemas" / "connection.schema.json"


def load_schema(path):
    with open(path, "r", encoding="utf-8") as f:
        return Draft7Validator(json.load(f))


def validate_dir(directory, pattern, validator, label):
    errors_found = False
    if not directory.exists():
        return errors_found

    for json_file in sorted(directory.rglob(pattern) if directory == CATEGORY_DIR else directory.glob(pattern)):
        with open(json_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"[FAIL] {json_file.relative_to(ROOT)}: invalid JSON syntax ({e})")
                errors_found = True
                continue

        errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
        if errors:
            errors_found = True
            print(f"[FAIL] {json_file.relative_to(ROOT)} ({label}):")
            for err in errors:
                loc = "/".join(str(p) for p in err.absolute_path) or "(root)"
                print(f"    - {loc}: {err.message}")
        else:
            print(f"[OK]   {json_file.relative_to(ROOT)}")

    return errors_found


def main():
    entry_validator = load_schema(ENTRY_SCHEMA)
    connection_validator = load_schema(CONNECTION_SCHEMA)

    had_errors = False
    had_errors |= validate_dir(CATEGORY_DIR, "*.json", entry_validator, "entry")
    had_errors |= validate_dir(CONNECTIONS_DIR, "*.json", connection_validator, "connection")

    if had_errors:
        print("\nValidation FAILED.")
        sys.exit(1)
    else:
        print("\nValidation OK.")


if __name__ == "__main__":
    main()
