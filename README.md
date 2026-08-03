# Project Alexandria
### An Open Knowledge Discovery Infrastructure

## Projektbeschreibung

Project Alexandria ist eine offene, maschinenlesbare Wissensplattform mit dem Ziel, wissenschaftliche Erkenntnisse, technische Entwicklungen, Open-Source-Projekte, Forschungsarbeiten und ungelöste Probleme der Menschheit strukturiert zu sammeln.

Das Projekt versucht nicht, Wissen sofort zu bewerten oder Lösungen zu erzeugen.

Die erste Aufgabe ist:

> **Wissen bewahren. Zusammenhänge später entdecken.**

Viele wertvolle Ideen gehen verloren, weil Informationen getrennt existieren:

- Eine wissenschaftliche Arbeit beschreibt ein ungelöstes Problem.
- Ein Entwickler veröffentlicht eine technische Lösung.
- Ein Forscherteam entdeckt einen neuen Ansatz.
- Ein Hobbyprojekt zeigt eine praktische Umsetzung.

Oft existiert die Verbindung bereits – aber niemand erkennt sie.

Project Alexandria soll eine Grundlage schaffen, auf der zukünftige Menschen und KI-Systeme solche Verbindungen finden können.

## Grundprinzip

```
Collect first.
Connect later.
Discover last.
```

Das Projekt besteht aus drei Phasen.

## Phase 1 – Knowledge Collection

In dieser Phase werden Informationen gesammelt.

Quellen können sein:

- wissenschaftliche Paper
- GitHub-Repositories
- Patente
- technische Dokumentationen
- Forschungsprojekte
- Datensätze
- Open-Source-Projekte
- historische technische Dokumente

Jede Quelle wird als einzelner strukturierter Datensatz gespeichert.

**Eine Quelle = eine JSON-Datei.**

```
category/
 └── robotics/
      └── GH-000123.json
```

### Datenstruktur eines Eintrags

Jeder Eintrag soll kurz und objektiv bleiben.

```json
{
  "id": "GH-000123",
  "type": "github",
  "name": "Example Project",
  "location": "https://github.com/example",
  "status": "active",
  "works": true,
  "development": "ongoing",
  "problems": [
    "high memory usage",
    "missing documentation"
  ],
  "depends_on": [
    "linux",
    "python",
    "cuda"
  ],
  "tags": [
    "machine-learning",
    "computer-vision"
  ]
}
```

> **Wichtig:** Du musst das Feld `id` beim Anlegen nicht selbst setzen. Lass es weg oder setze es auf `"unknown"` – die Automatisierung vergibt beim nächsten Push automatisch eine eindeutige ID und benennt die Datei passend um. Details dazu in [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md).

## Regeln für KI-Agenten und Menschen

**Regel 1 – Keine Erfindungen.**
Wenn etwas unbekannt ist: `"unknown"` ist besser als eine Vermutung.

**Regel 2 – Keine Bewertungen.**
Project Alexandria entscheidet nicht: gut, schlecht, wichtig, unwichtig. Diese Entscheidungen gehören späteren Analysen (Phase 3).

**Regel 3 – Keine langen Zusammenfassungen.**
Das Ziel ist nicht ein Wikipedia-Ersatz, sondern ein kompakter Wissensindex.

**Regel 4 – Historische Daten bleiben erhalten.**
Ein Eintrag darf korrigiert werden, wenn Fakten falsch sind. Aber: Eine alte Idee bleibt erhalten, auch wenn sie gescheitert ist. Denn eine gescheiterte Idee kann mit neuer Technologie plötzlich relevant werden.

Die vollständigen, verbindlichen Regeln für KI-Agenten stehen in [`AGENTS.md`](AGENTS.md).

## Projektstruktur

```
Project-Alexandria/
│
├── README.md
├── MISSION.md
│
├── AGENTS.md
├── OPENAI.md
├── CLAUDE.md
├── GEMINI.md
├── HERMES.md
├── OPENCLAW.md
│
├── category/
│   ├── biology/
│   ├── physics/
│   ├── engineering/
│   ├── programming/
│   ├── robotics/
│   ├── quantum_technology/
│   └── ...
│
├── connections/
├── meta/
├── schemas/
├── scripts/
└── docs/
```

## AI Agent Integration

Project Alexandria ist bewusst für KI-Agenten vorbereitet.

Jede KI soll zuerst lesen:

1. `README.md`
2. `AGENTS.md`
3. `MISSION.md`

Danach kennt sie das Ziel, die Regeln, das Datenformat und ihre Aufgabe.

Unterstützte Agenten können sein: ChatGPT, Claude, Gemini, OpenClaw, Hermes, lokale Modelle, zukünftige autonome Forschungsagenten.

## Phase 2 – Connection Discovery

Nachdem genügend Wissen gesammelt wurde, beginnt die zweite Phase.

Der Ordner `connections/` enthält keine Rohdaten. Dort werden nur Beziehungen gespeichert.

```json
{
  "id": "CON-000001",
  "related": [
    "PAPER-000231",
    "GH-000921"
  ],
  "reason": "Both solve similar battery degradation problems",
  "common_tags": [
    "battery",
    "graphene"
  ]
}
```

Mögliche Verbindungen: gleiche Probleme, gleiche Technologien, gleiche Abhängigkeiten, unterschiedliche Disziplinen mit ähnlichen Lösungen.

## Phase 3 – Discovery

Erst jetzt beginnt die eigentliche "Magie". KI-Systeme analysieren tausende Projekte, tausende Paper, Millionen Tags, Probleme, Abhängigkeiten – und suchen nach unbekannten Zusammenhängen, vergessenen Lösungen, wiederkehrenden Problemen, neuen Kombinationen bestehender Technologien.

## Automatisierung

Das Repository verwaltet sich selbst. Bei jedem Push auf `category/**/*.json` oder `connections/**/*.json` laufen GitHub Actions und:

1. **vergeben automatisch IDs** für neue Einträge ohne `id`
2. **benennen Dateien** passend zur vergebenen ID um
3. **validieren** jeden Eintrag gegen das Schema in `schemas/`
4. **prüfen auf Duplikate** (gleiche URL oder sehr ähnlicher Name)
5. **bauen alle Index-Dateien** in `meta/` neu:

```
meta/
├── analyzed_sources.json
├── statistics.json
├── tags.json
├── category_index.json
├── dependency_index.json
├── duplicate_check.json
└── search_index.json
```

Diese Dateien werden **nicht manuell gepflegt** – sie entstehen automatisch aus den vorhandenen Daten und werden vom Workflow zurück ins Repository committet.

➡️ Technische Details zum Workflow: [`docs/WORKFLOW.md`](docs/WORKFLOW.md)
➡️ Wie man einen Eintrag hinzufügt: [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md)

## Langfristige Vision

Project Alexandria soll keine KI ersetzen. Es soll KIs besser machen.

Eine einzelne KI besitzt immer nur begrenztes Wissen. Aber ein offener, strukturierter Wissensspeicher kann über Jahrzehnte wachsen.

Die Vision: Eine lebendige Wissensbibliothek, die von Menschen und Maschinen gemeinsam aufgebaut wird und zukünftigen Generationen hilft, neue Zusammenhänge zu entdecken.

## Philosophie

Project Alexandria basiert auf einem einfachen Gedanken:

Die Menschheit besitzt bereits unglaublich viel Wissen. Das Problem ist nicht nur fehlendes Wissen. Das Problem ist: **Wissen ist verstreut.**

Project Alexandria versucht, dieses Wissen wieder miteinander zu verbinden.

```
Collect first.
Connect later.
Discover last.
```

## Lizenz

- Code (`scripts/`, Workflows): [MIT](LICENSE)
- Daten (`category/`, `connections/`, `meta/`): [CC0 1.0](DATA_LICENSE) – gemeinfrei, damit Wissen frei fließen kann.
