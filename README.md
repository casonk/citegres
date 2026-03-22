# citegres

A Python GUI for PostgreSQL database management built with tkinter. Developed for CSC582 — Advanced Database Concepts & Applications.

## Features

- Multi-database management from a single interface
- tkinter-based GUI for database operations
- Interactive query building
- Data normalization utilities

## Architecture

| Module | Purpose |
|---|---|
| `guitility.py` | Main GUI (tkinter) |
| `postility.py` | PostgreSQL operations |
| `seleamility.py` | Query building |
| `nordility.py` | Normalization |
| `netility.py` | Networking |

## Setup

1. Install: `pip install -r requirements.txt`
2. Configure: `cp citegres_template.ini citegres.ini` and edit with your credentials
3. Run: `python guitility.py`

> ⚠️ Never commit `citegres.ini` — it contains credentials and is gitignored.

## Documentation

See `Report.pdf` for the full project report.

## License

[MIT](LICENSE)
