# LESSONSLEARNED.md

Tracked durable lessons for `citegres`.
Unlike `CHATHISTORY.md`, this file should keep only reusable lessons that should change how future sessions work in this repo.

## How To Use

- Read this file after `AGENTS.md` and before `CHATHISTORY.md` when resuming work.
- Add lessons that generalize beyond a single session.
- Keep entries concise and action-oriented.
- Do not use this file for transient status updates or full session logs.

## Lessons

- `citegres` is best understood as a scrape-to-schema pipeline: GUI actions produce an enriched DataFrame, `postility.importXML` stages it through `papers_raw`, and normalized citation tables then drive the query and graph views.
