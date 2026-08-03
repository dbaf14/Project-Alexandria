# AGENTS.md — Regeln für KI-Agenten

Dies ist das verbindliche Regelwerk für jede KI (und jeden Menschen), die/der
Einträge zu Project Alexandria hinzufügt oder bearbeitet. Modellspezifische
Dateien (`CLAUDE.md`, `OPENAI.md`, `GEMINI.md`, `HERMES.md`, `OPENCLAW.md`)
verweisen hierher und ergänzen nur, was für das jeweilige Modell relevant ist.
Widerspricht sich etwas, gilt diese Datei.

## Regel 1 — Keine Erfindungen

Wenn ein Fakt nicht sicher bekannt ist, wird er **nicht geraten**.

Verwende `"unknown"` (als String) oder `null`, je nach Feldtyp, statt eine
plausible, aber unbelegte Angabe zu machen. Ein leeres/unsicheres Feld ist
immer besser als ein falsches.

## Regel 2 — Keine Bewertungen

Project Alexandria trifft keine Werturteile. Vermeide Formulierungen wie
"gut", "schlecht", "wichtig", "vielversprechend", "nutzlos" — auch nicht in
`problems` oder `tags`. Beschreibe nur, was beobachtbar ist (z. B. "hoher
Speicherverbrauch" statt "schlecht optimiert").

## Regel 3 — Keine langen Zusammenfassungen

Kein Fließtext, keine Wikipedia-Absätze. Ein Eintrag besteht aus kurzen,
strukturierten Feldern (siehe `schemas/entry.schema.json`). Wenn du unsicher
bist, ob ein Detail rein soll: eher weglassen.

## Regel 4 — Historische Daten bleiben erhalten

Bestehende Einträge dürfen korrigiert werden, wenn ein **Fakt** falsch ist
(z. B. eine tote URL, ein falscher Typ). Ein Eintrag darf **nicht** gelöscht
werden, nur weil ein Projekt aufgegeben wurde, gescheitert ist oder veraltet
wirkt — setze stattdessen `"status": "abandoned"` bzw. `"works": false`.

## Regel 5 — Ein Eintrag = eine Datei

Lege pro Quelle genau eine JSON-Datei im passenden `category/<kategorie>/`
Ordner an. Erfinde keine neuen Top-Level-Kategorien ohne Rücksprache — nutze
bei Unsicherheit die nächstpassende bestehende Kategorie und ordne über
`tags` feiner ein.

## Regel 6 — Keine ID selbst vergeben

Lass das Feld `id` beim Anlegen weg oder setze es auf `"unknown"`. Die
GitHub-Action (`scripts/assign_ids.py`) vergibt automatisch eine eindeutige
ID nach dem Schema `<PREFIX>-<sechsstellige Zahl>` (Prefix abhängig vom
Feld `type`, siehe `scripts/assign_ids.py`) und benennt die Datei passend um.
Falls du dennoch programmatisch IDs vergibst, prüfe vorher `meta/id_counters.json`.

## Regel 7 — Schema einhalten

Jeder Eintrag muss gegen `schemas/entry.schema.json` validieren, jede
Verbindung in `connections/` gegen `schemas/connection.schema.json`. Der
Workflow lehnt ungültiges JSON ab (bei PRs) bzw. markiert es in
`meta/statistics.json` (bei direktem Push).

## Reihenfolge beim Lesen

1. `README.md` — Überblick und Prinzipien
2. `AGENTS.md` — dieses Dokument
3. `MISSION.md` — Kurzfassung der Aufgabe
4. deine modellspezifische Datei, falls vorhanden

## Kurzfassung

```
unknown > geraten
neutral > bewertet
kurz    > ausführlich
erhalten > gelöscht
eine Quelle = eine Datei
keine eigene ID
```
