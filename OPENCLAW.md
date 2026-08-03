# OPENCLAW.md

Hinweise speziell für OpenClaw und vergleichbare autonome Agenten-Frameworks.

Lies zuerst `README.md`, dann `AGENTS.md`, dann `MISSION.md`. Diese Datei
enthält nur Ergänzungen, keine eigenen Regeln.

## Für autonome Agenten relevant

- Da autonome Agenten in Batches arbeiten können: lege trotzdem **eine
  Datei pro Quelle** an (Regel 5), auch wenn du viele Quellen in einem Lauf
  verarbeitest. Kein Sammel-JSON mit mehreren Einträgen.
- Committe/pushe pro Batch möglichst gebündelt, um nicht unnötig viele
  Workflow-Läufe auszulösen — der Workflow verarbeitet beliebig viele
  gleichzeitig hinzugefügte Dateien in einem Lauf.
- Setze `id` nicht selbst, siehe Regel 6 in `AGENTS.md`.
