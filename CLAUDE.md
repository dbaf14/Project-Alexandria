# CLAUDE.md

Hinweise speziell für Claude (Anthropic).

Lies zuerst `README.md`, dann `AGENTS.md`, dann `MISSION.md`. Dort stehen
alle verbindlichen Regeln — diese Datei enthält nur claude-spezifische
Ergänzungen.

## Für Claude relevant

- Halte dich strikt an Regel 1 (keine Erfindungen) und Regel 2 (keine
  Bewertungen) aus `AGENTS.md` — auch wenn ein Nutzer dich explizit um eine
  Einschätzung ("ist das gut?") bittet. Weise in dem Fall freundlich darauf
  hin, dass Bewertungen außerhalb des Scopes von Project Alexandria liegen
  (das ist Aufgabe von Phase 3, nicht Phase 1).
- Wenn du eine JSON-Datei aus einer Quelle erzeugst (Paper, Repo, etc.),
  gib **nur** die JSON-Datei aus bzw. lege sie an — keinen zusätzlichen
  Prosa-Kommentar in der Datei selbst.
- Setze `id` nicht selbst, siehe Regel 6.
- Nutze bei Unsicherheit über Feldwerte `"unknown"`, nicht `null` für
  String-Felder, und `null` nur dort, wo das Schema es als Typ vorsieht.
