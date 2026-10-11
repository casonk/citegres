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
- https://opencitations.net/index/api/v1/ - citation-reference and citing-work metadata source
- https://api.semanticscholar.org/ - Semantic Scholar citation metadata source

## Documentation and Specifications

- https://www.postgresql.org/docs/ - PostgreSQL reference for schema and query behavior
- https://www.psycopg.org/docs/advanced.html - psycopg cursor extension reference used by the logging cursor wrapper
- https://requests.readthedocs.io/ - Requests HTTP client reference used by metadata-enrichment requests
- https://www.crummy.com/software/BeautifulSoup/ - Beautiful Soup HTML parsing reference used by DBLP metadata scraping
- https://numpy.org/doc/ - NumPy numerical-array reference used by analysis helpers
- https://pandas.pydata.org/docs/ - pandas DataFrame reference used by ingestion and analysis helpers
- https://networkx.org/documentation/stable/ - NetworkX graph-analysis reference used by citation-network workflows
- https://matplotlib.org/stable/contents.html - Matplotlib plotting reference used by analysis and visualization helpers
- https://docs.python.org/3/library/tkinter.html - tkinter GUI reference for the desktop client

## Notes

- Local configuration and credentials stay outside git; this file only tracks the public metadata and database references the project depends on.
