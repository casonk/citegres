# AGENTS.md

## Project Purpose

Python GUI application for PostgreSQL database management, developed as an academic project for Advanced Database Concepts & Applications (CSC582). Uses tkinter for the interface and supports multiple database connections.

## Repository Layout

- `guitility.py` — tkinter control surface that orchestrates connection state, scraping, import, query execution, and graph actions
- `postility.py` — Config parsing, PostgreSQL connection lifecycle, schema creation, import pipeline, and resolved query helpers
- `seleamility.py` — Chrome automation plus DBLP, OpenAlex, and Crossref enrichment flow that produces import-ready DataFrames
- `nordility.py` — Local NordVPN rotation helper used to spread scraping traffic across DBLP extraction bursts
- `netility.py` — Citation graph construction, metric computation, and matplotlib visualization helpers
- `citegres.ini` — Local database config (gitignored — contains credentials)
- `citegres_template.ini` — Safe config template with placeholders
- `Report.pdf` — Project report document
- `README.md` — Project overview

## Setup

1. Copy `citegres_template.ini` to `citegres.ini`.
2. Fill in your PostgreSQL connection details.
3. Install dependencies: `pip install tkinter pandas psycopg2-binary`
4. Run: `python guitility.py`

## Operating Rules

- **NEVER commit `citegres.ini`** — it is gitignored because it contains database credentials.
- Use `citegres_template.ini` as the reference for config format.
- All database connection parameters must come from the config file, never hardcoded.
- `guitility.py` is the operator-facing coordinator; keep its menu callbacks aligned with helper-module function names and return shapes.
- `postility.importXML` is the canonical ingest path from enriched search results into the normalized Postgres schema; document or preserve that staging-to-normalized-table flow when changing architecture.
- Preserve the module naming convention (`*ility.py`).
- Test database operations against a local PostgreSQL instance before committing.

## Security

- `citegres.ini` must remain in `.gitignore` at all times.
- Do not embed connection strings, passwords, or hostnames in source code.
- Use `citegres_template.ini` for any config examples in documentation.

## Portfolio Standards Reference

For portfolio-wide repository standards and baseline conventions, consult the control-plane repo at `./util-repos/traction-control` from the portfolio root.

Start with:
- `./util-repos/traction-control/AGENTS.md`
- `./util-repos/traction-control/README.md`
- `./util-repos/traction-control/LESSONSLEARNED.md`

Shared implementation repos available portfolio-wide:
- `./util-repos/archility` for architecture toolchain bootstrap/render orchestration, Graphviz-capable diagram support, deterministic starter scaffolding, agentic architecture authoring, and architecture-documentation drift checks
- `./util-repos/auto-pass` for KeePassXC-backed password management and secret retrieval/update flows
- `./util-repos/nordility` for NordVPN-based VPN switching and connection orchestration
- `./util-repos/shock-relay` for external messaging across supported providers such as Signal, Telegram, Twilio SMS, WhatsApp, and Gmail IMAP
- `./util-repos/snowbridge` for SMB-based private file sharing and phone-accessible fileshare workflows
- `./util-repos/short-circuit` for WireGuard VPN setup and configuration, establishing private tunnels with SMB, HTTPS, and SSH access

When another repo needs architecture toolchain bootstrap/rendering, architecture inventory/scaffolding, password management, VPN switching, or external messaging, prefer integrating with these repos instead of re-implementing the capability locally.

## Agent Memory

Use `./LESSONSLEARNED.md` as the tracked durable lessons file for this repo.
Use `./CHATHISTORY.md` as the standard local handoff file for this repo.

- `LESSONSLEARNED.md` is tracked and should capture only reusable lessons.
- `CHATHISTORY.md` is local-only, gitignored, and should capture transient handoff context.
- Read `LESSONSLEARNED.md` and `CHATHISTORY.md` after `AGENTS.md` when resuming work.
- Add durable lessons to `LESSONSLEARNED.md` when they should influence future sessions.
- Keep transient entries brief and focused on config handling, database changes, blockers, and next steps.
- Do not record database credentials or connection details in either file.
