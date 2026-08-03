#!/usr/bin/env python3
"""
run_all.py

Runs the full pipeline in the correct order:

1. assign_ids.py        -> assign IDs, rename files
2. validate_entries.py  -> schema validation (aborts on errors)
3. detect_duplicates.py -> write duplicate check
4. build_index.py       -> rebuild all meta/*.json

Used both locally (before a manual commit) and in the GitHub Actions
workflow. On validation errors, the pipeline stops with exit code 1
BEFORE the index is built, so meta/ is never updated based on invalid
data.
"""
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent

STEPS = [
    ("ID assignment", "assign_ids.py"),
    ("Validation", "validate_entries.py"),
    ("Duplicate check", "detect_duplicates.py"),
    ("Index build", "build_index.py"),
]


def run_step(label, script_name):
    print(f"\n=== {label} ({script_name}) ===")
    result = subprocess.run([sys.executable, str(SCRIPTS_DIR / script_name)])
    if result.returncode != 0:
        print(f"\nPipeline stopped at step '{label}' (exit code {result.returncode}).")
        sys.exit(result.returncode)


def main():
    for label, script_name in STEPS:
        run_step(label, script_name)
    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()
