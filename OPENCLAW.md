# OPENCLAW.md

Notes specific to OpenClaw and comparable autonomous agent frameworks.

Read `README.md` first, then `AGENTS.md`, then `MISSION.md`. This file
only contains additions, not its own rules.

## Relevant for Autonomous Agents

- Since autonomous agents may work in batches: still create **one
  file per source** (Rule 5), even when processing many sources in a
  single run. No combined JSON with multiple entries.
- Bundle commits/pushes per batch where possible to avoid triggering
  unnecessary workflow runs — the workflow processes any number of
  simultaneously added files in a single run.
- Do not set `id` yourself, see Rule 6 in `AGENTS.md`.
