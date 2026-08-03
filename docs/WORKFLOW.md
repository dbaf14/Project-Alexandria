# Workflow Documentation

## Overview

Two GitHub Actions workflows handle the automation:

| Workflow | Trigger | Purpose | Commits? |
|---|---|---|---|
| `validate-pr.yml` | Pull request touching `category/**`, `connections/**` | Validate only | No |
| `process-knowledge.yml` | Push to `main` (same paths) or manual | Full pipeline | Yes, automatically |

## Pipeline in Detail (`scripts/run_all.py`)

```
1. assign_ids.py         Assign IDs, rename files
2. validate_entries.py   Schema validation — aborts on errors
3. detect_duplicates.py  Write duplicate check
4. build_index.py        Rebuild all meta/*.json
5. update_readme.py      Refresh the Overview section in README.md
```

The order is deliberate: IDs must be final (step 1) before validation can
happen (step 2), before duplicates and indexes are built from the final,
valid data (step 3+4). If step 2 fails, the pipeline stops immediately —
nothing gets committed.

## ID Assignment (`scripts/assign_ids.py`)

- The prefix is derived from the `type` field:

  | `type` | Prefix | Example |
  |---|---|---|
  | `github` | `GH` | `GH-000123` |
  | `paper` | `PAPER` | `PAPER-000231` |
  | `patent` | `PAT` | `PAT-000001` |
  | `documentation` | `DOC` | `DOC-000001` |
  | `dataset` | `DATA` | `DATA-000001` |
  | `research_project` | `RES` | `RES-000001` |
  | `historical_document` | `HIST` | `HIST-000001` |
  | `other` / unknown | `SRC` | `SRC-000001` |
  | Connections (`connections/`) | `CON` | `CON-000001` |

- Counters live persistently in `meta/id_counters.json` (one counter per
  prefix), so IDs stay unique across many workflow runs and never
  collide.
- An entry without `id` (or with `"id": "unknown"`) gets a new ID on the
  next run. The file is automatically renamed to `<ID>.json`
  (regardless of what it was called before).
- Already assigned IDs are never reassigned — this step is idempotent.

## Validation (`scripts/validate_entries.py`)

Uses `jsonschema` against `schemas/entry.schema.json` or
`schemas/connection.schema.json`. Prints `[OK]` or `[FAIL]` per file with
the exact error location. Exit code 1 if at least one error occurs.

## Duplicate Check (`scripts/detect_duplicates.py`)

Two heuristics, both deliberately conservative (no automatic deletion,
no automatic merging — that would be an evaluation, see Rule 2):

1. **Exact URL duplicates**: `location` is normalized (protocol,
   `www.`, trailing slash removed, lowercased) and checked for an exact
   match.
2. **Similar names**: `SequenceMatcher` ratio on normalized names,
   threshold `0.88` (adjustable via `NAME_SIMILARITY_THRESHOLD`).

Results land in `meta/duplicate_check.json` as pure information — whether
it's actually a duplicate is left to humans / Phase 3 to decide.

## Index Building (`scripts/build_index.py`)

Rebuilds **all** `meta/*.json` files (except `id_counters.json` and
`duplicate_check.json`, which are managed by the other scripts)
completely from the current state of `category/` and `connections/` on
every run. Not incremental — unproblematic at the project's current
scale and much less error-prone than diff-based patching.

## README Overview (`scripts/update_readme.py`)

Regenerates the block between `<!-- OVERVIEW:START -->` and
`<!-- OVERVIEW:END -->` at the top of `README.md`, using the numbers from
the `meta/statistics.json` file that was just rebuilt in the previous step.
Shows the total entry count, the number of categories with at least one
entry, and a breakdown per source `type` (e.g. "12 from GitHub", "2 from
science papers"). Do not edit the content between the markers by hand —
it is fully overwritten on every pipeline run. If the markers are ever
removed from `README.md`, the script re-inserts them directly after the
title on the next run.

## Auto-Commit

`process-knowledge.yml` commits changed files under `category/`,
`connections/`, and `meta/` using the bot user `alexandria-bot` and the
commit message `chore: auto-update IDs, index and duplicate check [skip ci]`.
The `[skip ci]` prevents the commit itself from triggering unnecessary
runs.

## Triggering Manually

In the GitHub UI under *Actions → Process Knowledge → Run workflow*, or
via GitHub CLI:

```bash
gh workflow run process-knowledge.yml
```

Useful e.g. after a manual edit to `schemas/`, or when several PRs were
merged in quick succession.
