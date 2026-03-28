# citegres

A Python GUI for PostgreSQL database management built with tkinter. Developed for CSC582 — Advanced Database Concepts & Applications.

## Features

- Multi-database management from a single interface
- tkinter-based GUI for schema, import, query, and graph actions
- DBLP XML scraping plus OpenAlex and Crossref enrichment
- Normalized Postgres citation schema with resolved query helpers
- Citation graph construction and plotting utilities

## Architecture

| Module | Purpose |
|---|---|
| `guitility.py` | Main tkinter control surface |
| `postility.py` | Config, schema, import, and PostgreSQL queries |
| `seleamility.py` | Chrome automation and DBLP/OpenAlex/Crossref enrichment |
| `nordility.py` | Optional VPN rotation during scraping |
| `netility.py` | Citation graph construction, metrics, and plotting |

## Setup

1. Install: `pip install -r requirements.txt`
2. Configure: `cp citegres_template.ini citegres.ini` and edit with your credentials
3. Run: `python guitility.py`

> ⚠️ Never commit `citegres.ini` — it contains credentials and is gitignored.

## Documentation

See `Report.pdf` for the full project report.

## License

[MIT](LICENSE)
