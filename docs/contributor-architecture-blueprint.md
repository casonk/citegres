# Contributor Architecture Blueprint

This document is a concise map of how `citegres` moves from config-driven connection setup to tkinter-driven database operations.

## High-Level Layers

1. Configuration layer (`citegres_template.ini`, local `citegres.ini`)
   - The tracked template documents the expected connection fields.
   - The real `citegres.ini` stays local-only because it contains credentials.
2. UI layer (`guitility.py`)
   - The tkinter interface coordinates user actions, forms, and result displays.
   - UI behavior should stay decoupled from hard-coded database credentials.
3. Query and selection layer (`seleamility.py`)
   - Selection helpers and query-building logic shape how user choices become SQL operations.
4. Database operations layer (`postility.py`)
   - PostgreSQL connection handling and query execution live here.
   - Behavioral changes in this file affect the application's runtime data access semantics.
5. Utility layer (`nordility.py`, `netility.py`)
   - Small helper modules support normalization and networking-related functionality.

## Key Entry Points

- `python guitility.py`: launch the application
- `citegres_template.ini`: safe configuration reference
- `.github/workflows/ci.yml`: formatting, lint, and test workflow

## Validation

```bash
pip install -r requirements.txt
python guitility.py
```

When database behavior changes, validate against a local PostgreSQL instance with a non-production config file.
