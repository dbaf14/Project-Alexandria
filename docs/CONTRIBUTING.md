# Contributing

## Adding an Entry (Human or AI Agent)

1. Choose the appropriate folder under `category/` (e.g.
   `category/robotics/`). If no category fits well, use the closest one
   and rely on `tags` for finer classification. Don't create a new
   top-level category without discussing it in the repo (issue/PR
   discussion).

2. Create a new JSON file following the schema in
   [`schemas/entry.schema.json`](../schemas/entry.schema.json). The
   file name doesn't matter for now — e.g. `new.json` or a descriptive
   name like `pytorch-lightning.json`. **Leave out the `id` field** or
   set it to `"unknown"`.

   Minimal example:

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

3. Commit and push directly to `main` (or open a PR, see below).

4. On push to `main`, the workflow
   `.github/workflows/process-knowledge.yml` automatically:
   - assigns a unique ID (e.g. `GH-000123`) based on the `type` field
   - renames your file to `<ID>.json`
   - validates the entry against the schema
   - checks for possible duplicates
   - rebuilds all indexes in `meta/`
   - commits the result back to `main` automatically

   Afterward you just need to `git pull` if you want to keep working
   locally.

## Contributing via Pull Request

If you don't have write access to `main` (e.g. external contributor):

1. Fork the repository, add your JSON file to the appropriate
   `category/` folder.
2. Open a pull request.
3. The workflow `.github/workflows/validate-pr.yml` automatically checks
   whether your JSON is valid and matches the schema (result shown in
   the PR).
4. After merging into `main`, the push workflow automatically handles
   ID assignment, renaming, and index building.

## Correcting an Existing Entry

Only allowed when a **fact** is wrong (e.g. dead URL, wrong `type`).
Edit the file directly at its assigned ID
(`category/<category>/<ID>.json`). Do not delete entries just because a
project is inactive or has failed — use `"status": "abandoned"` or
`"works": false` instead (see Rule 4 in [`AGENTS.md`](../AGENTS.md)).

## Adding a Connection (Phase 2)

Once enough entries exist, connections can be added in `connections/`,
following the schema in
[`schemas/connection.schema.json`](../schemas/connection.schema.json).
Again: leave out `id`, it's assigned automatically.

## Testing Locally Before Pushing

```bash
pip install -r scripts/requirements.txt
python scripts/run_all.py
```

This runs the full pipeline locally (ID assignment, validation,
duplicate check, index building) — exactly what the workflow does.
