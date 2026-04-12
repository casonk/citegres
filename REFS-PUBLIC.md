# REFS-PUBLIC.md - Public References

> Record external public repositories, datasets, documentation, APIs, or other
> public resources that this repository utilizes or depends on.
> This file is tracked and intentionally kept free of private or local-only details.

## Public Repositories

- No fixed external code repository is the main upstream; the repo integrates with public metadata services and PostgreSQL.

## Public Datasets and APIs

- https://dblp.org/ - bibliographic source used during ingestion and enrichment
- https://api.openalex.org/ - metadata enrichment source for works and authors
- https://api.crossref.org/ - DOI and citation metadata enrichment source

## Documentation and Specifications

- https://www.postgresql.org/docs/ - PostgreSQL reference for schema and query behavior
- https://docs.python.org/3/library/tkinter.html - tkinter GUI reference for the desktop client

## Notes

- Local configuration and credentials stay outside git; this file only tracks the public metadata and database references the project depends on.
