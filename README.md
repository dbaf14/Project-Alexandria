# Project Alexandria
### An Open Knowledge Discovery Infrastructure

<!-- OVERVIEW:START -->
## Overview

_Automatically updated after each pipeline run (`scripts/update_readme.py`) — do not edit this section by hand._

**Currently 28 analyzed entries available in 4 categories.**

- 24 from GitHub
- 4 from science papers
<!-- OVERVIEW:END -->

## Project Description

Project Alexandria is an open, machine-readable knowledge platform whose goal is to collect scientific findings, technical developments, open-source projects, research papers, and humanity's unsolved problems in a structured way.

The project does not try to evaluate knowledge or generate solutions right away.

The first task is:

> **Preserve knowledge. Discover connections later.**

Many valuable ideas get lost because information exists in isolation:

- A scientific paper describes an unsolved problem.
- A developer publishes a technical solution.
- A research team discovers a new approach.
- A hobby project shows a practical implementation.

The connection often already exists — nobody just recognizes it yet.

Project Alexandria aims to build a foundation on which future humans and AI systems can find these connections.

## Core Principle

```
Collect first.
Connect later.
Discover last.
```

The project consists of three phases.

## Phase 1 – Knowledge Collection

In this phase, information is collected.

Sources can be:

- scientific papers
- GitHub repositories
- patents
- technical documentation
- research projects
- datasets
- open-source projects
- historical technical documents

Each source is stored as a single structured record.

**One source = one JSON file.**

```
category/
 └── robotics/
      └── GH-000123.json
```

### Structure of an Entry

Each entry should stay short and objective.

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

> **Note:** You don't need to set the `id` field yourself when creating an entry. Leave it out or set it to `"unknown"` — the automation assigns a unique ID and renames the file accordingly on the next push. Details in [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md).

## Rules for AI Agents and Humans

**Rule 1 – No inventing facts.**
If something is unknown: `"unknown"` is better than a guess.

**Rule 2 – No evaluations.**
Project Alexandria does not decide: good, bad, important, unimportant. Those judgments belong to later analysis (Phase 3).

**Rule 3 – No long summaries.**
The goal is not a Wikipedia replacement, but a compact knowledge index.

**Rule 4 – Historical data is preserved.**
An entry may be corrected if facts are wrong. But: an old idea remains preserved even if it failed. Because a failed idea can suddenly become relevant with new technology.

The full, binding rules for AI agents are in [`AGENTS.md`](AGENTS.md).

## Project Structure

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

Project Alexandria is deliberately built for AI agents.

Every AI should read, in order:

1. `README.md`
2. `AGENTS.md`
3. `MISSION.md`

After that, it knows the goal, the rules, the data format, and its task.

Supported agents can be: ChatGPT, Claude, Gemini, OpenClaw, Hermes, local models, future autonomous research agents.

## Phase 2 – Connection Discovery

Once enough knowledge has been collected, the second phase begins.

The `connections/` folder contains no raw data. It stores relationships only.

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

Possible connections: same problems, same technologies, same dependencies, different disciplines with similar solutions.

## Phase 3 – Discovery

Only now does the actual "magic" begin. AI systems analyze thousands of projects, thousands of papers, millions of tags, problems, and dependencies — searching for unknown connections, forgotten solutions, recurring problems, and new combinations of existing technologies.

## Automation

The repository maintains itself. On every push to `category/**/*.json` or `connections/**/*.json`, GitHub Actions:

1. **automatically assigns IDs** to new entries without an `id`
2. **renames files** to match the assigned ID
3. **validates** every entry against the schema in `schemas/`
4. **checks for duplicates** (same URL or very similar name)
5. **rebuilds all index files** in `meta/`:

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

These files are **not maintained manually** — they are generated automatically from the existing data and committed back to the repository by the workflow.

➡️ Technical details on the workflow: [`docs/WORKFLOW.md`](docs/WORKFLOW.md)
➡️ How to add an entry: [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md)

## Long-Term Vision

Project Alexandria is not meant to replace AI. It is meant to make AI better.

A single AI always has limited knowledge. But an open, structured knowledge store can grow over decades.

The vision: a living knowledge library, built jointly by humans and machines, helping future generations discover new connections.

## Philosophy

Project Alexandria is based on a simple idea:

Humanity already possesses an incredible amount of knowledge. The problem is not just missing knowledge. The problem is: **knowledge is scattered.**

Project Alexandria tries to reconnect this knowledge.

```
Collect first.
Connect later.
Discover last.
```

## License

- Code (`scripts/`, workflows): [MIT](LICENSE)
- Data (`category/`, `connections/`, `meta/`): [CC0 1.0](DATA_LICENSE) — public domain, so knowledge can flow freely.
