# AGENTS.md

## Project Purpose

Python GUI application for PostgreSQL database management, developed as an academic project for Advanced Database Concepts & Applications (CSC582). Uses tkinter for the interface and supports multiple database connections.

## Repository Layout

- `guitility.py` — Main GUI module (tkinter interface, ~535 lines)
- `postility.py` — PostgreSQL database operations module (~734 lines)
- `seleamility.py` — Selection and query building module (~289 lines)
- `nordility.py` — Data normalization utilities (~110 lines)
- `netility.py` — Networking utilities (~128 lines)
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
- `./util-repos/auto-pass` for KeePassXC-backed password management and secret retrieval/update flows
- `./util-repos/nordility` for NordVPN-based VPN switching and connection orchestration
- `./util-repos/shock-relay` for external messaging across supported providers such as Signal, Telegram, Twilio SMS, WhatsApp, and Gmail IMAP

When another repo needs password management, VPN switching, or external messaging, prefer integrating with these repos instead of re-implementing the capability locally.

## Agent Memory

Use `./LESSONSLEARNED.md` as the tracked durable lessons file for this repo.
Use `./CHATHISTORY.md` as the standard local handoff file for this repo.

- `LESSONSLEARNED.md` is tracked and should capture only reusable lessons.
- `CHATHISTORY.md` is local-only, gitignored, and should capture transient handoff context.
- Read `LESSONSLEARNED.md` and `CHATHISTORY.md` after `AGENTS.md` when resuming work.
- Add durable lessons to `LESSONSLEARNED.md` when they should influence future sessions.
- Keep transient entries brief and focused on config handling, database changes, blockers, and next steps.
- Do not record database credentials or connection details in either file.
