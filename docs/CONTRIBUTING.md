# Contributing

## Einen Eintrag hinzufügen (Mensch oder KI-Agent)

1. Wähle den passenden Ordner unter `category/` (z. B. `category/robotics/`).
   Wenn keine Kategorie richtig passt, nimm die nächstbeste und nutze `tags`
   für die feinere Einordnung. Lege keine neue Top-Level-Kategorie an, ohne
   das im Repo abzustimmen (Issue/PR-Diskussion).

2. Erstelle eine neue JSON-Datei nach dem Schema in
   [`schemas/entry.schema.json`](../schemas/entry.schema.json). Der
   Dateiname ist zunächst egal — z. B. `neu.json` oder ein sprechender
   Name wie `pytorch-lightning.json`. **Lass das Feld `id` weg** oder setze
   es auf `"unknown"`.

   Minimalbeispiel:

   ```json
   {
     "type": "github",
     "name": "Example Project",
     "location": "https://github.com/example/example",
     "status": "active",
     "works": true,
     "development": "ongoing",
     "problems": ["missing documentation"],
     "depends_on": ["python"],
     "tags": ["machine-learning"]
   }
   ```

3. Committe und pushe direkt auf `main` (oder öffne einen PR, siehe unten).

4. Auf Push auf `main` läuft automatisch der Workflow
   `.github/workflows/process-knowledge.yml`:
   - vergibt eine eindeutige ID (z. B. `GH-000123`) basierend auf dem Feld `type`
   - benennt deine Datei automatisch in `<ID>.json` um
   - validiert den Eintrag gegen das Schema
   - prüft auf mögliche Duplikate
   - baut alle Indexe in `meta/` neu
   - committet das Ergebnis automatisch zurück auf `main`

   Du musst danach nur noch `git pull`, wenn du lokal weiterarbeiten willst.

## Über einen Pull Request beitragen

Wenn du keine Schreibrechte auf `main` hast (z. B. externer Contributor):

1. Fork das Repository, lege deine JSON-Datei im passenden `category/`-Ordner an.
2. Öffne einen Pull Request.
3. Der Workflow `.github/workflows/validate-pr.yml` prüft automatisch, ob
   dein JSON gültig ist und dem Schema entspricht (Ergebnis im PR sichtbar).
4. Nach dem Merge auf `main` übernimmt der Push-Workflow ID-Vergabe,
   Umbenennung und Index-Bau automatisch.

## Einen bestehenden Eintrag korrigieren

Nur erlaubt, wenn ein **Fakt** falsch ist (z. B. tote URL, falscher `type`).
Bearbeite die Datei direkt unter ihrer vergebenen ID
(`category/<kategorie>/<ID>.json`). Lösche keine Einträge nur weil ein
Projekt inaktiv oder gescheitert ist — nutze `"status": "abandoned"` bzw.
`"works": false` (siehe Regel 4 in [`AGENTS.md`](../AGENTS.md)).

## Eine Verbindung hinzufügen (Phase 2)

Sobald genug Einträge existieren, können Verbindungen in `connections/`
angelegt werden, nach dem Schema in
[`schemas/connection.schema.json`](../schemas/connection.schema.json).
Auch hier: `id` weglassen, wird automatisch vergeben.

## Lokal testen, bevor du pushst

```bash
pip install -r scripts/requirements.txt
python scripts/run_all.py
```

Das führt die komplette Pipeline lokal aus (ID-Vergabe, Validierung,
Duplicate-Check, Index-Bau) — genau das, was auch der Workflow macht.
