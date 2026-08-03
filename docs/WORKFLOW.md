# Workflow-Dokumentation

## Übersicht

Zwei GitHub-Actions-Workflows kümmern sich um die Automatisierung:

| Workflow | Trigger | Zweck | Committet? |
|---|---|---|---|
| `validate-pr.yml` | Pull Request auf `category/**`, `connections/**` | Nur validieren | Nein |
| `process-knowledge.yml` | Push auf `main` (gleiche Pfade) oder manuell | Volle Pipeline | Ja, automatisch |

## Pipeline im Detail (`scripts/run_all.py`)

```
1. assign_ids.py         IDs vergeben, Dateien umbenennen
2. validate_entries.py   Schema-Validierung — bricht bei Fehlern ab
3. detect_duplicates.py  Duplicate-Check schreiben
4. build_index.py        Alle meta/*.json neu bauen
```

Die Reihenfolge ist bewusst so gewählt: Erst müssen IDs final sein (Schritt 1),
bevor validiert werden kann (Schritt 2), bevor Duplikate und Indexe auf
Basis der finalen, gültigen Daten gebaut werden (Schritt 3+4). Schlägt
Schritt 2 fehl, bricht die Pipeline sofort ab — es wird nichts committet.

## ID-Vergabe (`scripts/assign_ids.py`)

- Prefix wird aus dem Feld `type` abgeleitet:

  | `type` | Prefix | Beispiel |
  |---|---|---|
  | `github` | `GH` | `GH-000123` |
  | `paper` | `PAPER` | `PAPER-000231` |
  | `patent` | `PAT` | `PAT-000001` |
  | `documentation` | `DOC` | `DOC-000001` |
  | `dataset` | `DATA` | `DATA-000001` |
  | `research_project` | `RES` | `RES-000001` |
  | `historical_document` | `HIST` | `HIST-000001` |
  | `other` / unbekannt | `SRC` | `SRC-000001` |
  | Connections (`connections/`) | `CON` | `CON-000001` |

- Zähler liegen persistent in `meta/id_counters.json` (ein Zähler pro Prefix),
  damit IDs auch über viele Workflow-Läufe hinweg eindeutig bleiben und
  nicht kollidieren.
- Ein Eintrag ohne `id` (oder mit `"id": "unknown"`) bekommt beim nächsten
  Durchlauf eine neue ID. Die Datei wird automatisch in `<ID>.json`
  umbenannt (unabhängig davon, wie sie vorher hieß).
- Bereits vergebene IDs werden nicht neu vergeben — der Schritt ist idempotent.

## Validierung (`scripts/validate_entries.py`)

Nutzt `jsonschema` gegen `schemas/entry.schema.json` bzw.
`schemas/connection.schema.json`. Gibt pro Datei `[OK]` oder `[FAIL]` mit
genauer Fehlerstelle aus. Exit-Code 1 bei mindestens einem Fehler.

## Duplicate-Check (`scripts/detect_duplicates.py`)

Zwei Heuristiken, beide bewusst konservativ (keine automatische Löschung,
kein automatisches Merging — das wäre eine Bewertung, siehe Regel 2):

1. **Exakte URL-Duplikate**: `location` wird normalisiert (Protokoll,
   `www.`, trailing slash entfernt, lowercased) und auf exakte Übereinstimmung
   geprüft.
2. **Ähnliche Namen**: `SequenceMatcher`-Ratio auf normalisierte Namen,
   Schwellwert `0.88` (einstellbar in `NAME_SIMILARITY_THRESHOLD`).

Ergebnis landet in `meta/duplicate_check.json` als reine Information — die
Bewertung, ob es sich wirklich um ein Duplikat handelt, bleibt Menschen/
Phase 3 überlassen.

## Index-Bau (`scripts/build_index.py`)

Baut bei jedem Lauf **alle** `meta/*.json`-Dateien (außer `id_counters.json`
und `duplicate_check.json`, die von den anderen Scripts verwaltet werden)
komplett neu aus dem aktuellen Stand von `category/` und `connections/`.
Kein inkrementelles Update — bei der aktuellen Projektgröße unproblematisch
und deutlich weniger fehleranfällig als Diff-basiertes Patchen.

## Auto-Commit

`process-knowledge.yml` committet geänderte Dateien unter `category/`,
`connections/` und `meta/` mit dem Bot-User `alexandria-bot` und der
Commit-Message `chore: auto-update IDs, index and duplicate check [skip ci]`.
Das `[skip ci]` verhindert, dass der Commit selbst wieder unnötige Läufe
auslöst.

## Manuell auslösen

Im GitHub-UI unter *Actions → Process Knowledge → Run workflow*, oder per
GitHub CLI:

```bash
gh workflow run process-knowledge.yml
```

Sinnvoll z. B. nach einem manuellen Edit an `schemas/` oder wenn mehrere
PRs kurz hintereinander gemerged wurden.
