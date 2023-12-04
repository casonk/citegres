'''
    Author: Cason Konzer
    Module: postility
    -- Part of: citegres
    Developed for: Advance Database Concepts & Applications

    Function: Provides an interface for Postgres connection and queries
    Version: 4.0
    Dated: December 2, 2023
'''

# IMPORTS
from configparser import ConfigParser
import pandas as pd
import psycopg2
import psycopg2.extensions
import logging
import sys

# STATIC SET (LOGGER)
logging.basicConfig(stream=sys.stdout, encoding='utf-8', level=logging.INFO)
pyLogger = logging.getLogger(name='postility_debug')

# STATIC VARS (ERROR MSG & PATH)
ERROR_FAILED_TO_EXECUTE = 'ach, gute fire abend!'
SRC = 'C:/Users/cason/OneDrive - Umich/Computer_Science/Classes/Fall_2023/CSC582-Advanced_Database_Concepts_and_Applications/Project2/ME/src'

# GLOBAL VARS (CONFIG SECTION)
DB_SELECTION = 'CiteGres'

# CLASS DEFS
class LoggingCursor(psycopg2.extensions.cursor):
    '''
    overloading per: https://www.psycopg.org/docs/advanced.html
    '''
    def execute(self, sql, args=None):
        logger = logging.getLogger(name='sql_cursor_debug')
        logger.info("Execute: %s" % self.mogrify(sql, args))
        try:
            psycopg2.extensions.cursor.execute(self, sql, args)
            logger.info("Status: %s" % self.statusmessage)
        except Exception as exc:
            logger.error("%s: %s" % (exc.__class__.__name__, exc))
            raise

# BASIC DEFS
__db_init = [
    'DROP TABLE IF EXISTS papers_raw;',
    'DROP TABLE IF EXISTS paper_concepts;',
    'DROP TABLE IF EXISTS citations;',
    'DROP TABLE IF EXISTS supports;',
    'DROP TABLE IF EXISTS papers;',
    'DROP TABLE IF EXISTS openalex;',
    'DROP TABLE IF EXISTS venues;',
    'DROP TABLE IF EXISTS types;',
    'DROP TABLE IF EXISTS concepts;',
    'DROP TABLE IF EXISTS publishers;',
    'DROP TABLE IF EXISTS authors;',
    'CREATE TABLE authors (id SERIAL, author TEXT UNIQUE NOT NULL, PRIMARY KEY(id));',
    'CREATE TABLE publishers (id SERIAL, publisher TEXT UNIQUE NOT NULL, PRIMARY KEY(id));',
    'CREATE TABLE concepts (id SERIAL, concept TEXT UNIQUE NOT NULL, PRIMARY KEY(id));',
    'CREATE TABLE types (id SERIAL, ptype TEXT UNIQUE NOT NULL, PRIMARY KEY(id));',
    'CREATE TABLE venues (id SERIAL, venue TEXT UNIQUE NOT NULL, PRIMARY KEY(id));',
    'CREATE TABLE openalex (id SERIAL, openalex_url TEXT UNIQUE NOT NULL, PRIMARY KEY(id));',
    'CREATE TABLE papers (id SERIAL, doi TEXT, title TEXT UNIQUE NOT NULL, pdate DATE, author INTEGER REFERENCES authors(id) NOT NULL, publisher INTEGER REFERENCES publishers(id), ptype INTEGER REFERENCES types(id), venue INTEGER REFERENCES venues(id), openalex INTEGER REFERENCES openalex(id), PRIMARY KEY(id));',
    'CREATE TABLE supports (paper INTEGER REFERENCES papers(id), author INTEGER REFERENCES authors(id), PRIMARY KEY(paper,author));',
    'CREATE TABLE citations (source INTEGER REFERENCES openalex(id), target INTEGER REFERENCES openalex(id), PRIMARY KEY(source,target));',
    'CREATE TABLE paper_concepts (paper INTEGER REFERENCES papers(id), concept INTEGER REFERENCES concepts(id), PRIMARY KEY(paper,concept));',
    'CREATE TABLE papers_raw (id SERIAL, doi TEXT, title TEXT, pdate DATE, author TEXT, author_id INTEGER, publisher TEXT, publisher_id INTEGER, ptype TEXT, ptype_id INTEGER, venue TEXT, venue_id INTEGER, openalex TEXT, openalex_id INTEGER, PRIMARY KEY(id));'
]
def db_init(cur, conn):
    '''
    Build up tablespace for database
    '''
    for __statement in __db_init:
        try:
            cur.execute(__statement)
        except Exception as E:
            pyLogger.error('%s \nexception in db_init' % str(E))
    return commit_prior(cur, conn)

__clear_papers_raw = [
    'DROP TABLE IF EXISTS papers_raw;',
    'CREATE TABLE papers_raw (id SERIAL, doi TEXT, title TEXT, pdate DATE, author TEXT, author_id INTEGER, publisher TEXT, publisher_id INTEGER, ptype TEXT, ptype_id INTEGER, venue TEXT, venue_id INTEGER, openalex TEXT, openalex_id INTEGER, PRIMARY KEY(id));'
]
def clear_papers_raw(cur, conn): # TRUNCATE may combine DROP & CREATE to keep a table and delete all of it's data... should be faster
    '''
    Drop & recreate papers_raw table
    '''
    for __statement in __clear_papers_raw:
        try:
            cur.execute(__statement)
        except Exception as E:
            pyLogger.error('%s \nexception in clear_papers_raw' % str(E))
    return commit_prior(cur, conn)

def update_db_selection(section='CiteGres'):
    '''
    Update global variable for database selection
    '''
    global DB_SELECTION
    DB_SELECTION = section
    pyLogger.info(f'Database selection set to: {DB_SELECTION}')

def config(filename=f'{SRC}/citegres.ini'):
    '''
    Parse database configuration file
    '''
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    try:
        params = parser.items(DB_SELECTION)
        for param in params:
            db[param[0]] = param[1]
        pyLogger.info('Config set from: %s' % DB_SELECTION)
    except Exception as E:
        pyLogger.error('%s \nexception in config' % str(E))
    return db

def create_connection():
    '''
    Establish a connection & cursor to the database
    '''
    params = config()
    try:
        conn = psycopg2.connect(**params)
        cur = conn.cursor(cursor_factory=LoggingCursor)
        pyLogger.info('connected with dsn: %s' % str(conn.dsn))
        pyLogger.info('connection status: %s' % str(conn.status))
    except Exception as E:
        pyLogger.error('%s \nexception in create_connection' % str(E))
    return cur, conn

def kill_connection(cur, conn):
    '''
    Destroy the passed connection and cursor
    '''
    cur.close()
    conn.close() # Closing a connection without committing the changes first will cause an implicit rollback to be performed.
    pyLogger.info('cursor and connection closed')

def reset_connection(cur, conn):
    '''
    Reset the passed connection and cursor
    '''
    kill_connection(cur=cur, conn=conn)
    return create_connection()

def commit_prior(cur, conn):
    '''
    Attempt to commit all prior cursor execute transactions
    '''
    try:
        conn.commit()
        pyLogger.info('transaction(s) committed')
        return cur, conn
    except Exception as E:
        pyLogger.error('%s \ntransaction(s) rolled back' % str(E))
        conn.rollback()
        return reset_connection(cur=cur, conn=conn)

def commit_transaction(cur, conn, transaction):
    '''
    Attempt to commit passed cursor transaction
    '''
    try:
        cur.execute(transaction)
        conn.commit()
        pyLogger.info('transaction committed')
        return cur, conn
    except Exception as E:
        pyLogger.error('%s \ntransaction rolled back' % str(E))
        conn.rollback()
        return reset_connection(cur=cur, conn=conn)
    
# INSERT DEFS
def format_null_insert(__statement):
    '''
    Remove single quotes from NULL strings in execute statements
    '''
    return __statement.replace("'NULL'", "NULL")

__insert_author = '''
INSERT INTO authors (author) VALUES ('{}');
'''
def insert_authors(cur, conn, df):
    '''
    Insert all primary authors from passed df into database
    '''
    (cur, conn), current_authors = select_author_from_authors(cur=cur, conn=conn)
    if current_authors is ERROR_FAILED_TO_EXECUTE:
        logging.error(ERROR_FAILED_TO_EXECUTE)
        return commit_prior(cur=cur, conn=conn)
    current_authors.author = current_authors.author.str.replace("'", "''")
    all_authors = []
    for authors in df.authors:
        for author in authors:
            all_authors.append(author)
    all_authors = pd.Series(all_authors)
    for author in all_authors[~all_authors.isin(values=current_authors.author)].unique():
        insert_statement = __insert_author.format(author)
        try:
            cur.execute(format_null_insert(__statement=insert_statement))
        except Exception as E:
            pyLogger.error('%s \nexception in insert_authors' % str(E))
            break
    return commit_prior(cur=cur, conn=conn)

__insert_concept = '''
INSERT INTO concepts (concept) VALUES ('{}');
'''
def insert_concepts(cur, conn, df):
    '''
    Insert all concepts from passed df into database
    '''
    (cur, conn), current_concepts = select_concept_from_concepts(cur=cur, conn=conn)
    if current_concepts is ERROR_FAILED_TO_EXECUTE:
        logging.error(ERROR_FAILED_TO_EXECUTE)
        return commit_prior(cur=cur, conn=conn)
    current_concepts.concept = current_concepts.concept.str.replace("'", "''")
    all_concepts = []
    for concepts in df.concepts[df.concepts != 'NULL']:
        for concept in concepts:
            all_concepts.append(concept)
    all_concepts = pd.Series(all_concepts)
    for concept in all_concepts[~all_concepts.isin(values=current_concepts.concept)].unique():
        insert_statement = __insert_concept.format(concept)
        try:
            cur.execute(format_null_insert(__statement=insert_statement))
        except Exception as E:
            pyLogger.error('%s \nexception in insert_concepts' % str(E))
            break
    return commit_prior(cur=cur, conn=conn)

__insert_openalex = '''
INSERT INTO openalex (openalex_url) VALUES ('{}');
'''
def insert_openalexs(cur, conn, df):
    '''
    Insert all openalex urls from passed df into database
    '''
    (cur, conn), current_openalex_urls = select_openalex_url_from_openalex(cur=cur, conn=conn)
    if current_openalex_urls is ERROR_FAILED_TO_EXECUTE:
        logging.error(ERROR_FAILED_TO_EXECUTE)
        return commit_prior(cur=cur, conn=conn)
    all_openalex_urls = []
    for referenced_works in df.referenced_works[df.referenced_works != 'NULL']:
        for referenced_work in referenced_works:
            all_openalex_urls.append(referenced_work)
    for openalex_url in df.openalex_id[df.openalex_id != 'NULL']:
        all_openalex_urls.append(openalex_url)
    all_openalex_urls = pd.Series(all_openalex_urls)
    for openalex_url in all_openalex_urls[~all_openalex_urls.isin(values=current_openalex_urls.openalex_url)].unique():
        insert_statement = __insert_openalex.format(openalex_url)
        try:
            cur.execute(format_null_insert(__statement=insert_statement))
        except Exception as E:
            pyLogger.error('%s \nexception in insert_openalexs' % str(E))
            break
    return commit_prior(cur=cur, conn=conn)

__insert_paper_raw = '''
INSERT INTO papers_raw (doi, title, pdate, author, publisher, ptype, venue, openalex) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}');
'''
def insert_papers_raw(cur, conn, df):
    '''
    Insert all paper entries from passed df into database
    '''
    for row in df[['doi', 'title', 'publication_date', 'authors', 'publisher', 'type', 'venue', 'openalex_id']].values:
        doi       = row[0]
        title     = row[1]
        pdate     = row[2]
        author    = row[3][0]
        publisher = row[4]
        ptype     = row[5]
        venue     = row[6]
        openalex  = row[7]
        insert_statement = __insert_paper_raw.format(doi, title, pdate, author, publisher, ptype, venue, openalex)
        try:
            cur.execute(format_null_insert(__statement=insert_statement))
        except Exception as E:
            pyLogger.error('%s \nexception in insert_papers_raw' % str(E))
            break
    return commit_prior(cur=cur, conn=conn)

__papers_raw_to_papers = [
    'INSERT INTO publishers (publisher)    SELECT DISTINCT publisher FROM papers_raw WHERE ((papers_raw.publisher NOT IN (SELECT publisher FROM publishers)) AND (papers_raw.publisher IS NOT NULL));',
    'INSERT INTO types      (ptype)        SELECT DISTINCT ptype     FROM papers_raw WHERE ((papers_raw.ptype NOT IN (SELECT ptype FROM types)) AND (papers_raw.ptype IS NOT NULL));',
    'INSERT INTO venues     (venue)        SELECT DISTINCT venue     FROM papers_raw WHERE ((papers_raw.venue NOT IN (SELECT venue FROM venues)) AND (papers_raw.venue IS NOT NULL));',
    'UPDATE papers_raw SET author_id    = (SELECT authors.id         FROM authors    WHERE authors.author        = papers_raw.author);',
    'UPDATE papers_raw SET publisher_id = (SELECT publishers.id      FROM publishers WHERE publishers.publisher  = papers_raw.publisher);',
    'UPDATE papers_raw SET ptype_id     = (SELECT types.id           FROM types      WHERE types.ptype           = papers_raw.ptype);',
    'UPDATE papers_raw SET venue_id     = (SELECT venues.id          FROM venues     WHERE venues.venue          = papers_raw.venue);',
    'UPDATE papers_raw SET openalex_id  = (SELECT openalex.id        FROM openalex   WHERE openalex.openalex_url = papers_raw.openalex);',
    'INSERT INTO papers (doi, title, pdate, author, publisher, ptype, venue, openalex) SELECT doi, title, pdate, author_id, publisher_id, ptype_id, venue_id, openalex_id FROM papers_raw WHERE papers_raw.title NOT IN (SELECT title FROM papers);'
]
def papers_raw_to_papers(cur, conn):
    '''
    Normalize papers_raw table to papers
    '''
    for __statement in __papers_raw_to_papers:
        try:
            cur.execute(__statement)
        except Exception as E:
            pyLogger.error('%s \nexception in papers_raw_to_papers' % str(E))
    return clear_papers_raw(cur=cur, conn=conn)

__insert_support = '''
INSERT INTO supports VALUES ({}, {});
'''
def insert_supports(cur, conn, df):
    '''
    Insert all supporting authors from passed df into database
    '''
    (cur, conn), current_supports = select_all_from_supports(cur=cur, conn=conn)
    paper_ids = []
    author_ids = []
    for row in df[['title', 'authors']].values:
        title = row[0]
        authors = row[1]
        (cur, conn), paper_id = select_id_from_papers_where_title_is(cur=cur, conn=conn, title=title)
        if paper_id is ERROR_FAILED_TO_EXECUTE:
            logging.error(ERROR_FAILED_TO_EXECUTE)
            continue
        if len(authors) > 1:
            for author in authors[1:]:
                (cur, conn), author_id = select_id_from_authors_where_author_is(cur=cur, conn=conn, author=author)
                if author_id is ERROR_FAILED_TO_EXECUTE:
                    logging.error(ERROR_FAILED_TO_EXECUTE)
                    continue
                paper_ids.append(paper_id)
                author_ids.append(author_id)
    for (paper_id, author_id) in set(zip(paper_ids, author_ids)):
        if ~((current_supports.paper_id == paper_id) & (current_supports.author_id == author_id)).any():
            try:
                cur.execute(__insert_support.format(paper_id, author_id))
            except Exception as E:
                pyLogger.error('%s \nexception in insert_supports' % str(E))
    return commit_prior(cur=cur, conn=conn)

__insert_paper_concept = '''
INSERT INTO paper_concepts VALUES ({}, {});
'''
def insert_paper_concepts(cur, conn, df):
    '''
    Insert all paper-concept pairs from passed df into database
    '''
    (cur, conn), current_paper_concepts = select_all_from_paper_concepts(cur=cur, conn=conn)
    paper_ids = []
    concept_ids = []
    for row in df[['title', 'concepts']][(df.concepts != 'NULL')].values:
        title = row[0]
        concepts = row[1]
        (cur, conn), paper_id = select_id_from_papers_where_title_is(cur=cur, conn=conn, title=title)
        if paper_id is ERROR_FAILED_TO_EXECUTE:
            logging.error(ERROR_FAILED_TO_EXECUTE)
            continue
        if len(concepts) > 0:
            for concept in concepts[1:]:
                (cur, conn), concept_id = select_id_from_concepts_where_concept_is(cur=cur, conn=conn, concept=concept)
                if concept_id is ERROR_FAILED_TO_EXECUTE:
                    logging.error(ERROR_FAILED_TO_EXECUTE)
                    continue
                paper_ids.append(paper_id)
                concept_ids.append(concept_id)
    for (paper_id, concept_id) in set(zip(paper_ids, concept_ids)):
        if ~((current_paper_concepts.paper == paper_id) & (current_paper_concepts.concept == concept_id)).any():
            try:
                cur.execute(__insert_paper_concept.format(paper_id, concept_id))
            except Exception as E:
                pyLogger.error('%s \nexception in insert_paper_concepts' % str(E))
    return commit_prior(cur=cur, conn=conn)

__insert_citation = '''
INSERT INTO citations VALUES ({}, {});
'''
def insert_citations(cur, conn, df):
    '''
    Insert all citations by openalex passed df into database
    '''
    (cur, conn), current_citations = select_all_from_citations(cur=cur, conn=conn)
    sources = []
    targets = []
    for row in df[['openalex_id', 'referenced_works']][((df.openalex_id != 'NULL') & (df.referenced_works != 'NULL'))].values:
        source_openalex = row[0]
        (cur, conn), source = select_id_from_openalex_where_openalex_url_is(cur=cur, conn=conn, openalex_url=source_openalex)
        if source is ERROR_FAILED_TO_EXECUTE:
            logging.error(ERROR_FAILED_TO_EXECUTE)
            continue
        target_openalexs = row[1]
        if len(target_openalexs) > 0:
            for target_openalex in pd.Series(target_openalexs).unique():
                (cur, conn), target = select_id_from_openalex_where_openalex_url_is(cur=cur, conn=conn, openalex_url=target_openalex)
                if target is ERROR_FAILED_TO_EXECUTE:
                    logging.error(ERROR_FAILED_TO_EXECUTE)
                    continue
                sources.append(source)
                targets.append(target)
    for (source, target) in set(zip(sources, targets)):
        if ~((current_citations.source == source) & (current_citations.target == target)).any():
            try:
                cur.execute(__insert_citation.format(source, target))
            except Exception as E:
                pyLogger.error('%s \nexception in insert_citations' % str(E))
    return commit_prior(cur=cur, conn=conn)

def importXML(cur, conn, df):
    '''
    Chain insert & normalization statements to import web scrapped search results into database
    '''
    df.drop_duplicates(subset='title', inplace=True, ignore_index=True) # remove non-unique titles
    df.title = df.title.str.replace("'", "''")
    df.fillna(value='NULL', inplace=True)
    cur, conn = insert_authors(cur=cur, conn=conn, df=df)
    cur, conn = insert_concepts(cur=cur, conn=conn, df=df)
    cur, conn = insert_openalexs(cur=cur, conn=conn, df=df)
    cur, conn = insert_papers_raw(cur=cur, conn=conn, df=df)
    cur, conn = papers_raw_to_papers(cur=cur, conn=conn)
    cur, conn = insert_supports(cur=cur, conn=conn, df=df)
    cur, conn = insert_paper_concepts(cur=cur, conn=conn, df=df)
    cur, conn = insert_citations(cur=cur, conn=conn, df=df)
    return cur, conn

# SELECT DEFS
__query_authorlist_full = '''
SELECT * FROM authors;
'''
def select_all_from_authors(cur, conn):
    '''
    Select all from authors
    '''
    try:
        cur.execute(__query_authorlist_full)
        authorlist_full = pd.DataFrame(cur.fetchall(), columns=['id', 'author'])
    except Exception as E:
        pyLogger.error('%s \nexception in select_all_from_authors' % str(E))
        authorlist_full = ERROR_FAILED_TO_EXECUTE
    return commit_prior(cur=cur, conn=conn), authorlist_full

__query_authorlist_author = '''
SELECT author FROM authors;
'''
def select_author_from_authors(cur, conn):
    '''
    Select all author names
    '''
    try:
        cur.execute(__query_authorlist_author)
        authorlist_author = pd.DataFrame(cur.fetchall(), columns=['author'])
    except Exception as E:
        pyLogger.error('%s \nexception in select_author_from_authors' % str(E))
        authorlist_author = ERROR_FAILED_TO_EXECUTE
    return commit_prior(cur=cur, conn=conn), authorlist_author

__query_conceptlist_full = '''
SELECT * FROM concepts;
'''
def select_all_from_concepts(cur, conn):
    '''
    Select all from concepts
    '''
    try:
        cur.execute(__query_conceptlist_full)
        conceptlist_full = pd.DataFrame(cur.fetchall(), columns=['id', 'concept'])
    except Exception as E:
        pyLogger.error('%s \nexception in select_all_from_concepts' % str(E))
        conceptlist_full = ERROR_FAILED_TO_EXECUTE
    return commit_prior(cur=cur, conn=conn), conceptlist_full

__query_conceptlist_concept = '''
SELECT concept FROM concepts;
'''
def select_concept_from_concepts(cur, conn):
    '''
    Select all concept names
    '''
    try:
        cur.execute(__query_conceptlist_concept)
        conceptlist_concept = pd.DataFrame(cur.fetchall(), columns=['concept'])
    except Exception as E:
        pyLogger.error('%s \nexception in select_concept_from_concepts' % str(E))
        conceptlist_concept = ERROR_FAILED_TO_EXECUTE
    return commit_prior(cur=cur, conn=conn), conceptlist_concept

__query_openalexlist_full = '''
SELECT * FROM openalex;
'''
def select_all_from_openalex(cur, conn):
    '''
    Select all from openalex
    '''
    try:
        cur.execute(__query_openalexlist_full)
        openalexlist_full = pd.DataFrame(cur.fetchall(), columns=['id', 'openalex_url'])
    except Exception as E:
        pyLogger.error('%s \nexception in select_all_from_openalex' % str(E))
        openalexlist_full = ERROR_FAILED_TO_EXECUTE
    return commit_prior(cur=cur, conn=conn), openalexlist_full

__query_openalexlist_openalex_url = '''
SELECT openalex_url FROM openalex;
'''
def select_openalex_url_from_openalex(cur, conn):
    '''
    Select all openalex urls
    '''
    try:
        cur.execute(__query_openalexlist_openalex_url)
        openalexlist_openalex_url = pd.DataFrame(cur.fetchall(), columns=['openalex_url'])
    except Exception as E:
        pyLogger.error('%s \nexception in select_openalex_url_from_openalex' % str(E))
        openalexlist_openalex_url = ERROR_FAILED_TO_EXECUTE
    return commit_prior(cur=cur, conn=conn), openalexlist_openalex_url

__query_citationlist_full = '''
SELECT * FROM citations;
'''
def select_all_from_citations(cur, conn):
    '''
    Query id to id references
    '''
    try:
        cur.execute(__query_citationlist_full)
        citationlist_full = pd.DataFrame(cur.fetchall(), columns=['source', 'target'])
    except Exception as E:
        pyLogger.error('%s \nexception in select_all_from_citations' % str(E))
        citationlist_full = ERROR_FAILED_TO_EXECUTE
    return commit_prior(cur=cur, conn=conn), citationlist_full

__query_citationlist_full_resolve_openalex = '''
WITH sourced AS (
    SELECT openalex.openalex_url AS source, citations.target AS target 
    FROM citations 
    JOIN openalex 
    ON citations.source = openalex.id)
SELECT sourced.source AS source, openalex.openalex_url AS target
FROM sourced 
JOIN openalex 
ON sourced.target = openalex.id;
'''
def query_citationlist_full_resolve_openalex(cur, conn):
    '''
    Query url to url references
    '''
    try:
        cur.execute(__query_citationlist_full_resolve_openalex)
        citationlist_full_openalex_resolved = pd.DataFrame(cur.fetchall(), columns=['source', 'target'])
    except Exception as E:
        pyLogger.error('%s \nexception in query_citationlist_full_resolve_openalex' % str(E))
        citationlist_full_openalex_resolved = ERROR_FAILED_TO_EXECUTE
    return commit_prior(cur=cur, conn=conn), citationlist_full_openalex_resolved

__query_citationlist_full_resolve_paper_title = '''
WITH sourced AS (
    SELECT papers.title AS source, citations.target AS target 
    FROM citations 
    JOIN papers 
    ON citations.source = papers.openalex)
SELECT sourced.source AS source, papers.title AS target
FROM sourced 
JOIN papers 
ON sourced.target = papers.openalex;
'''
def query_citationlist_full_resolve_paper_title(cur, conn):
    '''
    Query paper to paper references
    '''
    try:
        cur.execute(__query_citationlist_full_resolve_paper_title)
        citationlist_full_paper_title_resolved = pd.DataFrame(cur.fetchall(), columns=['source', 'target'])
    except Exception as E:
        pyLogger.error('%s \nexception in query_citationlist_full_resolve_paper_title' % str(E))
        citationlist_full_paper_title_resolved = ERROR_FAILED_TO_EXECUTE
    return commit_prior(cur=cur, conn=conn), citationlist_full_paper_title_resolved

__query_citationlist_full_resolve_author = '''
WITH alex_to_author AS (
    SELECT papers.openalex AS openalex, authors.author AS author 
    FROM papers
    JOIN authors 
    ON papers.author = authors.id),
sourced AS (
    SELECT alex_to_author.author AS source, citations.target AS target 
    FROM citations 
    JOIN alex_to_author 
    ON citations.source = alex_to_author.openalex)
SELECT sourced.source AS source, alex_to_author.author AS target 
FROM sourced 
JOIN alex_to_author 
ON sourced.target = alex_to_author.openalex;
'''
def query_citationlist_full_resolve_author(cur, conn):
    '''
    Query author to author references
    '''
    try:
        cur.execute(__query_citationlist_full_resolve_author)
        citationlist_full_author_resolved = pd.DataFrame(cur.fetchall(), columns=['source', 'target'])
    except Exception as E:
        pyLogger.error('%s \nexception in query_citationlist_full_resolve_author' % str(E))
        citationlist_full_author_resolved = ERROR_FAILED_TO_EXECUTE
    return commit_prior(cur=cur, conn=conn), citationlist_full_author_resolved

__query_supportslist_full = '''
SELECT * FROM supports;
'''
def select_all_from_supports(cur, conn):
    '''
    Select all from supports
    '''
    try:
        cur.execute(__query_supportslist_full)
        supportlist_full = pd.DataFrame(cur.fetchall(), columns=['paper_id', 'author_id'])
    except Exception as E:
        pyLogger.error('%s \nexception in select_all_from_supports' % str(E))
        supportlist_full = ERROR_FAILED_TO_EXECUTE
    return commit_prior(cur=cur, conn=conn), supportlist_full

__query_supportslist_full_resolved = '''
SELECT P.title paper, A.author author
FROM supports S, papers P, authors A
WHERE (S.paper = P.id) AND (S.author = A.id);
'''
def select_all_from_supports_resolved(cur, conn):
    '''
    Select all from supports resolving paper and author ids
    '''
    try:
        cur.execute(__query_supportslist_full_resolved)
        supportlist_full_resolved = pd.DataFrame(cur.fetchall(), columns=['paper', 'author'])
    except Exception as E:
        pyLogger.error('%s \nexception in select_all_from_supports_resolved' % str(E))
        supportlist_full_resolved = ERROR_FAILED_TO_EXECUTE
    return commit_prior(cur=cur, conn=conn), supportlist_full_resolved

__query_paperconceptslist_full = '''
SELECT * FROM paper_concepts;
'''
def select_all_from_paper_concepts(cur, conn):
    '''
    Select all from paper_concepts
    '''
    try:
        cur.execute(__query_paperconceptslist_full)
        paperconceptslist_full = pd.DataFrame(cur.fetchall(), columns=['paper', 'concept'])
    except Exception as E:
        pyLogger.error('%s \nexception in select_all_from_paper_concepts' % str(E))
        paperconceptslist_full = ERROR_FAILED_TO_EXECUTE
    return commit_prior(cur=cur, conn=conn), paperconceptslist_full

__query_paperconceptslist_full_resolved = '''
SELECT P.title paper, C.concept concept
FROM paper_concepts PC, papers P, concepts C
WHERE (PC.paper = P.id) AND (PC.concept = C.id);
'''
def select_all_from_paper_concepts_resolved(cur, conn):
    '''
    Select all from paper_concepts resolving paper and concept ids
    '''
    try:
        cur.execute(__query_paperconceptslist_full_resolved)
        paperconceptslist_full_resolved = pd.DataFrame(cur.fetchall(), columns=['paper', 'concept'])
    except Exception as E:
        pyLogger.error('%s \nexception in select_all_from_paper_concepts' % str(E))
        paperconceptslist_full_resolved = ERROR_FAILED_TO_EXECUTE
    return commit_prior(cur=cur, conn=conn), paperconceptslist_full_resolved

# SELECT WHERE DEFS
__select_id_from_authors_where_author_is = '''
SELECT id FROM authors WHERE authors.author = '{}'
'''
def select_id_from_authors_where_author_is(cur, conn, author):
    '''
    Select author id for a given name
    '''
    try:
        cur.execute(__select_id_from_authors_where_author_is.format(author))
        author_id = cur.fetchone()[0]
        return commit_prior(cur=cur, conn=conn), author_id
    except Exception as E:
        pyLogger.error('%s \nexception in select_id_from_authors_where_author_is' % str(E))
        cur, conn = commit_prior(cur=cur, conn=conn)
        cur.execute(format_null_insert(__statement=__insert_author.format(author))) 
        return select_id_from_authors_where_author_is(cur=cur, conn=conn, author=author)

__select_id_from_papers_where_title_is = '''
SELECT id FROM papers WHERE papers.title = '{}'
'''
def select_id_from_papers_where_title_is(cur, conn, title):
    '''
    Select paper id for a given title
    '''
    try:
        cur.execute(__select_id_from_papers_where_title_is.format(title))
        paper_id = cur.fetchone()[0]
    except Exception as E:
        pyLogger.error('%s \nexception in select_id_from_papers_where_title_is' % str(E))
        paper_id = ERROR_FAILED_TO_EXECUTE
    return commit_prior(cur=cur, conn=conn), paper_id

__select_id_from_openalex_where_openalex_url_is = '''
SELECT id FROM openalex WHERE openalex.openalex_url = '{}'
'''
def select_id_from_openalex_where_openalex_url_is(cur, conn, openalex_url):
    '''
    Select openalex id for a given url
    '''
    try:
        cur.execute(__select_id_from_openalex_where_openalex_url_is.format(openalex_url))
        openalex_id = cur.fetchone()[0]
        return commit_prior(cur=cur, conn=conn), openalex_id
    except Exception as E:
        pyLogger.error('%s \nexception in select_id_from_openalex_where_openalex_url_is' % str(E))
        cur, conn = commit_prior(cur=cur, conn=conn)
        cur.execute(format_null_insert(__statement=__insert_openalex.format(openalex_url))) 
        return select_id_from_openalex_where_openalex_url_is(cur=cur, conn=conn, openalex_url=openalex_url)

__select_id_from_concepts_where_concept_is = '''
SELECT id FROM concepts WHERE concepts.concept = '{}'
'''
def select_id_from_concepts_where_concept_is(cur, conn, concept):
    '''
    Select concept id for a given concept
    '''
    try:
        cur.execute(__select_id_from_concepts_where_concept_is.format(concept))
        concept_id = cur.fetchone()[0]
        return commit_prior(cur=cur, conn=conn), concept_id
    except Exception as E:
        pyLogger.error('%s \nexception in select_id_from_concepts_where_concept_is' % str(E))
        cur, conn = commit_prior(cur=cur, conn=conn)
        cur.execute(format_null_insert(__statement=__insert_concept.format(concept))) 
        return select_id_from_concepts_where_concept_is(cur=cur, conn=conn, concept=concept)
