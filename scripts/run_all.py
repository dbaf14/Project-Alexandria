#!/usr/bin/env python3
"""
run_all.py

Fuehrt die komplette Pipeline in der richtigen Reihenfolge aus:

1. assign_ids.py        -> IDs vergeben, Dateien umbenennen
2. validate_entries.py  -> Schema-Validierung (bricht bei Fehlern ab)
3. detect_duplicates.py -> Duplicate-Check schreiben
4. build_index.py       -> alle meta/*.json neu bauen

Wird sowohl lokal (vor einem manuellen Commit) als auch im
GitHub-Actions-Workflow verwendet. Bei Validierungsfehlern stoppt die
Pipeline mit Exit-Code 1, BEVOR der Index gebaut wird, damit meta/ nie
auf Basis ungueltiger Daten aktualisiert wird.
"""
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent

STEPS = [
    ("ID-Vergabe", "assign_ids.py"),
    ("Validierung", "validate_entries.py"),
    ("Duplicate-Check", "detect_duplicates.py"),
    ("Index-Bau", "build_index.py"),
]


def run_step(label, script_name):
    print(f"\n=== {label} ({script_name}) ===")
    result = subprocess.run([sys.executable, str(SCRIPTS_DIR / script_name)])
    if result.returncode != 0:
        print(f"\nPipeline gestoppt bei Schritt '{label}' (exit code {result.returncode}).")
        sys.exit(result.returncode)


def main():
    for label, script_name in STEPS:
        run_step(label, script_name)
    print("\nPipeline erfolgreich abgeschlossen.")


if __name__ == "__main__":
    main()
