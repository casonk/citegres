'''
    Author: Cason Konzer
    Module: seleamility
    -- Part of: citegres
    Developed for: Advance Database Concepts & Applications

    Function: Provides a search controller for Chrome web scraping on DBLP & related APIs
    Version: 3.0
    Dated: December 2, 2023
'''

# IMPORTS
import re
import time
import requests
import nordility
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

# STATIC VARS (PATHS)
DRIVER_PATH = 'S:/Drivers/Chrome/chromedriver-win64/chromedriver.exe'
UBLOCK_PATH = 'S:/Drivers/Chrome/extensions/cjpalhdlnbpafiamejdnhcphjbkeiagm/1.52.2_0'

# BASIC DEFS
def chrome_connect():
    '''
    Initialize a chrome driver for automated browsing
    '''
    service = Service(executable_path=DRIVER_PATH)
    options = webdriver.ChromeOptions()
    options.add_argument(f"load-extension={UBLOCK_PATH}")
    options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=options, service=service)
    driver.implicitly_wait(5)
    driver.get('https://dblp.org/')
    time.sleep(1)
    return driver

def chrome_disconnect(driver):
    '''
    Quit the chrome driver session
    '''
    driver.quit()

# TABBING DEFS
def explode_tabs(driver, num_tabs=10):
    '''
    Open up num_tabs tabs in automated browser and return dictionary
    '''
    tabs = {}
    tabs[0] = driver.current_window_handle
    for i in range(1, num_tabs):
        driver.switch_to.new_window('tab')
        tabs[i] = driver.current_window_handle
    return tabs

def reset_tabs(driver, _tabs):
    '''
    Close all but one tab in automated browser
    '''
    driver.switch_to.new_window('tab')
    tabs = {}
    tabs[0] = driver.current_window_handle
    for tab in _tabs.values():
        driver.switch_to.window(tab)
        driver.close()
    driver.switch_to.window(tabs[0])
    driver.get('https://dblp.org/')
    return tabs

# QUERY DEFS
def chrome_query_dblp(driver, query='echo chamber'):
    '''
    Query DBLP to search for term `query` in automated browser
    '''
    driver.get(f'https://dblp.org/search?q={query}')

def chrome_query_dblp_XML(driver, query='echo chamber'):
    '''
    Query DBLP for XML search results of `query` in automated browser
    '''
    driver.get(f'https://dblp.org/search/publ/api?q={query}&h=1000&format=xml')
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    tags = ['title', 'venue', 'volume', 'number', 'pages', 'year', 'type', 'access', 'key', 'doi', 'ee', 'url']
    search_results = {}
    hits = soup.body.find_all('hit')
    for hit in hits:
        try:
            search_results['authors'] = search_results.get('authors', []) + [[author.contents[0].replace("'", "''") for author in hit.authors.children]]
        except:
            search_results['authors'] = search_results.get('authors', []) + ['NULL']
        for tag in tags:
            try:
                val = hit.info.find(tag).contents[0]
            except Exception as E:
                val = 'NULL'
            search_results[tag] = search_results.get(tag, []) + [val]
    return search_results

# EXTRACTION DEF
def explode_query_dblp(driver, search_results, explosion_factor=10, use_nord=1):
    '''
    Retrieve openalex, crossref, opencitations, and semanticscholar API urls as available, request their results and store into a dataframe
    '''
    df = pd.DataFrame(search_results)
    df.rename(columns={'url':'dblp_url'}, inplace=True)
    num_hits = len(df)
    print('num_hits')
    print(num_hits)
    print('raw df')
    print(df)
    tabs = explode_tabs(driver, min(explosion_factor, num_hits))
    openalex_stats_urls       = []
    crossref_refs_urls        = []
    opencitations_refs_urls   = []
    opencitations_cite_urls   = []
    semanticscholar_refs_urls = []
    semanticscholar_cite_urls = []
    num_parsed = 0
    while num_parsed < num_hits:
        for i in range(explosion_factor):
            _num_parsed = num_parsed + i
            if _num_parsed < num_hits:
                driver.switch_to.window(tabs[i])
                driver.get(df.dblp_url[num_parsed+i])
            else:
                break
        if use_nord:
            nordility.change_vpn_server()
        else:
            time.sleep(5)
        for i in range(explosion_factor):
            _num_parsed = num_parsed + i
            if _num_parsed < num_hits:
                driver.switch_to.window(tabs[i])
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                try:
                    openalex_stats_url       = soup.body.find('div', id='rec-side-panel').find_all(href=re.compile('https://api.openalex.org/works/'))[0].get('href')
                except Exception as E:
                    openalex_stats_url       = 'NULL'
                try:
                    crossref_refs_url        = soup.body.find('div', id='publ-references-section').div.header.find_all(href=re.compile('https://api.crossref.org/works/'))[0].get('href')
                except Exception as E:
                    crossref_refs_url        = 'NULL'
                try:
                    opencitations_refs_url   = soup.body.find('div', id='publ-references-section').div.header.find_all(href=re.compile('https://opencitations.net/index/api/v1/.*json'))[0].get('href')
                except Exception as E:
                    opencitations_refs_url   = 'NULL'
                try:
                    opencitations_cite_url   = soup.body.find('div', id='publ-citations-section').div.header.find_all(href=re.compile('https://opencitations.net/index/api/v1/.*json'))[0].get('href')
                except Exception as E:
                    opencitations_cite_url   = 'NULL'
                try:
                    semanticscholar_refs_url = soup.body.find('div', id='publ-references-section').div.header.find_all(href=re.compile('https://api.semanticscholar.org/v1/'))[0].get('href')
                except Exception as E:
                    semanticscholar_refs_url = 'NULL'
                try:
                    semanticscholar_cite_url = soup.body.find('div', id='publ-citations-section').div.header.find_all(href=re.compile('https://api.semanticscholar.org/v1/'))[0].get('href')
                except Exception as E:
                    semanticscholar_cite_url = 'NULL'
                openalex_stats_urls.append(openalex_stats_url)      
                crossref_refs_urls.append(crossref_refs_url)       
                opencitations_refs_urls.append(opencitations_refs_url)  
                opencitations_cite_urls.append(opencitations_cite_url)  
                semanticscholar_refs_urls.append(semanticscholar_refs_url)
                semanticscholar_cite_urls.append(semanticscholar_cite_url)
            else:
                break
        num_parsed += explosion_factor
    df['openalex_stats_urls']      = openalex_stats_urls
    df['crossref_refs_url']        = crossref_refs_urls
    df['opencitations_refs_url']   = opencitations_refs_urls
    df['opencitations_cite_url']   = opencitations_cite_urls
    df['semanticscholar_refs_url'] = semanticscholar_refs_urls
    df['semanticscholar_cite_url'] = semanticscholar_cite_urls
    print('url df')
    print(df)
    openalex_ids            = []
    publication_dates       = []
    landing_page_urls       = []
    pdf_urls                = []
    cited_by_counts         = []
    concepts                = []
    referenced_works_counts = []
    referenced_works        = []
    related_works           = []
    cited_by_api_urls       = []
    for unopenedalex in df.openalex_stats_urls:
        try:
            r = requests.get(unopenedalex)
            openedalex = r.json()
        except Exception as E:
            openalex_ids.append('NULL') 
            publication_dates.append('NULL') 
            landing_page_urls.append('NULL')
            pdf_urls.append('NULL')
            cited_by_counts.append('NULL') 
            concepts.append('NULL')
            referenced_works_counts.append('NULL')
            referenced_works.append('NULL')
            related_works.append('NULL')
            cited_by_api_urls.append('NULL')
            continue
        try:
            openalex_ids.append(openedalex['id'])       
        except Exception as E:
            openalex_ids.append('NULL')  
        try:
            publication_dates.append(openedalex['publication_date'])       
        except Exception as E:
            publication_dates.append('NULL')  
        try:
            landing_page_urls.append(openedalex['primary_location']['landing_page_url'])       
        except Exception as E:
            landing_page_urls.append('NULL')
        try:
            pdf_urls.append(openedalex['primary_location']['pdf_url'])                
        except Exception as E:
            pdf_urls.append('NULL')
        try:
            cited_by_counts.append(openedalex['cited_by_count'])         
        except Exception as E:
            cited_by_counts.append('NULL') 
        try:
            concepts.append([c['display_name'].replace("'", "''") for c in openedalex['concepts']])                
        except Exception as E:
            concepts.append('NULL')
        try:
            referenced_works_counts.append(openedalex['referenced_works_count']) 
        except Exception as E:
            referenced_works_counts.append('NULL')
        try:
            referenced_works.append(openedalex['referenced_works'])        
        except Exception as E:
            referenced_works.append('NULL')
        try:
            related_works.append(openedalex['related_works'])           
        except Exception as E:
            related_works.append('NULL')
        try:
            cited_by_api_urls.append(openedalex['cited_by_api_url'])     
        except Exception as E:
            cited_by_api_urls.append('NULL')
    df['openalex_id']            = openalex_ids
    df['publication_date']       = publication_dates
    df['landing_page_url']       = landing_page_urls
    df['pdf_url']                = pdf_urls
    df['cited_by_count']         = cited_by_counts
    df['concepts']               = concepts
    df['referenced_works_count'] = referenced_works_counts
    df['referenced_works']       = referenced_works
    df['related_works']          = related_works
    df['openalex_cite_url']      = cited_by_api_urls
    print('openalex df')
    print(df)
    publishers    = []
    ref_doi_lists = []
    for uncrossreffed in df.crossref_refs_url:
        try:
            r = requests.get(uncrossreffed)
            crossreffed = r.json()
            try:
                publishers.append(crossreffed['message']['publisher'])           
            except Exception as E:
                publishers.append('NULL')
            try:
                ref_doi_list = []
                for ref in crossreffed['message']['reference']:
                    try:
                        doi = ref['DOI']
                    except Exception as E:
                        doi = 'NULL'
                    ref_doi_list.append(doi)
                ref_doi_lists.append(ref_doi_list)
            except Exception as E:
                ref_doi_lists.append('NULL')
        except Exception as E:       
            publishers.append('NULL')           
            ref_doi_lists.append('NULL')  
    df['publisher']    = publishers
    df['ref_doi_list'] = ref_doi_lists
    print('crossref df')
    print(df)
    tabs = reset_tabs(driver, _tabs=tabs)
    return df
