# AGENTS.md — Rules for AI Agents

This is the binding rule set for every AI (and every human) adding to or
editing Project Alexandria entries. Model-specific files
(`CLAUDE.md`, `OPENAI.md`, `GEMINI.md`, `HERMES.md`, `OPENCLAW.md`) point
back here and only add what's relevant for that specific model. If
something conflicts, this file takes precedence.

## Rule 1 — No Invention

If a fact is not reliably known, it is **not guessed**.

Use `"unknown"` (as a string) or `null`, depending on the field type,
instead of making a plausible but unsubstantiated claim. An empty/uncertain
field is always better than a wrong one.

## Rule 2 — No Evaluation

Project Alexandria makes no value judgments. Avoid phrases like
"good", "bad", "important", "promising", "useless" — even in
`problems` or `tags`. Describe only what is observable (e.g. "high
memory usage" instead of "poorly optimized").

## Rule 3 — No Long Summaries

No prose, no Wikipedia-style paragraphs. An entry consists of short,
structured fields (see `schemas/entry.schema.json`). If you're unsure
whether a detail belongs, leave it out.

## Rule 4 — Historical Data Is Preserved

Existing entries may be corrected if a **fact** is wrong (e.g. a dead
URL, a wrong type). An entry must **not** be deleted just because a
project was abandoned, failed, or seems outdated — instead set
`"status": "abandoned"` or `"works": false`.

## Rule 5 — One Entry = One File

Create exactly one JSON file per source in the appropriate
`category/<category>/` folder. Don't invent new top-level categories
without prior discussion — when uncertain, use the closest existing
category and refine using `tags`.

## Rule 6 — Do Not Assign Your Own ID

Leave the `id` field out when creating an entry, or set it to
`"unknown"`. The GitHub Action (`scripts/assign_ids.py`) automatically
assigns a unique ID following the pattern `<PREFIX>-<six-digit number>`
(prefix depends on the `type` field, see `scripts/assign_ids.py`) and
renames the file accordingly. If you do assign IDs programmatically for
some reason, check `meta/id_counters.json` beforehand.

## Rule 7 — Follow the Schema

Every entry must validate against `schemas/entry.schema.json`, every
connection in `connections/` against `schemas/connection.schema.json`. The
workflow rejects invalid JSON (on PRs) or flags it in
`meta/statistics.json` (on direct push).

## Reading Order

1. `README.md` — overview and principles
2. `AGENTS.md` — this document
3. `MISSION.md` — short summary of the task
4. your model-specific file, if available

## Summary

```
unknown  > guessed
neutral  > evaluated
short    > detailed
preserved > deleted
one source = one file
no self-assigned ID
```
