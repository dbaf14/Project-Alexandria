# CLAUDE.md

Notes specific to Claude (Anthropic).

Read `README.md` first, then `AGENTS.md`, then `MISSION.md`. All binding
rules live there — this file only contains Claude-specific additions.

## Relevant for Claude

- Stick strictly to Rule 1 (no invention) and Rule 2 (no evaluation)
  from `AGENTS.md` — even if a user explicitly asks you for an
  assessment ("is this good?"). In that case, kindly point out that
  evaluations are out of scope for Project Alexandria (that's the job of
  Phase 3, not Phase 1).
- When you generate a JSON file from a source (paper, repo, etc.),
  output **only** the JSON file itself — no additional prose commentary
  inside the file.
- Do not set `id` yourself, see Rule 6.
- When unsure about a field value, use `"unknown"`, not `null`, for
  string fields, and `null` only where the schema defines that type.
