# Contributor Architecture Blueprint

This document is a concise map of how `citegres` moves from operator input in the tkinter GUI to scraped publication metadata, normalized PostgreSQL tables, and citation-network analysis.

## High-Level Layers

1. Operator and configuration layer (`guitility.py`, `citegres_template.ini`, local `citegres.ini`)
   - The tkinter GUI is the only first-class operator surface.
   - Database selection is config-driven through named sections in the local ini file, with the tracked template documenting the expected keys.
2. External collection layer (`seleamility.py`, `nordility.py`)
   - `seleamility` drives Chrome against DBLP, requests DBLP XML search results, and enriches each hit with OpenAlex and Crossref data.
   - `nordility` optionally rotates NordVPN endpoints during extraction bursts to support the scrape workflow.
3. Persistence and normalization layer (`postility.py`)
   - `postility` owns connection setup, schema creation, transaction handling, and import orchestration.
   - `importXML` is the canonical data-ingest path: dedupe the extracted frame, load supporting dimensions, stage records in `papers_raw`, normalize into `papers`, then populate `supports`, `paper_concepts`, and `citations`.
4. Query and analysis layer (`postility.py`, `netility.py`)
   - `postility` also exposes resolved SQL queries for authors, papers, concepts, supports, and citation edgelists.
   - `netility` turns resolved citation edgelists into NetworkX graphs, computes centrality metrics, and renders matplotlib graph views.

## Key Flows

- Search flow: GUI search field -> `seleamility.chrome_query_dblp_XML` -> DBLP XML hits
- Enrichment flow: DBLP hits -> `seleamility.explode_query_dblp` -> DBLP page scraping + OpenAlex requests + Crossref requests -> enriched pandas DataFrame
- Import flow: GUI import action -> `postility.importXML` -> `authors` / `concepts` / `openalex` / `papers_raw` / `papers` / `supports` / `paper_concepts` / `citations`
- Query flow: GUI query buttons -> resolved `postility` selectors -> tabular results in the GUI results pane
- Graph flow: GUI networking actions -> citation edgelist query -> `netility.construct_graph_from_df` -> metrics and plot rendering

## Key Entry Points

- `python guitility.py`: launch the GUI
- `citegres_template.ini`: tracked configuration contract
- `postility.importXML(...)`: canonical ingest pipeline
- `seleamility.explode_query_dblp(...)`: enrichment pipeline for scraped search results
- `netility.compute_graph_metrics(...)`: graph-analysis entrypoint once an edgelist is materialized

## Validation

```bash
pip install -r requirements.txt
python -m py_compile guitility.py postility.py seleamility.py nordility.py netility.py
python guitility.py
```

When behavior changes touch imports, queries, or schema management, validate against a local PostgreSQL instance using a non-production `citegres.ini`.
