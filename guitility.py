'''
    Author: Cason Konzer
    Module: guitility
    -- Part of: citegres
    Developed for: Advance Database Concepts & Applications

    Function: Graphical User Interface for citegres
    Version: 5.0
    Dated: December 2, 2023
'''

# IMPORTS
import postility
import seleamility
import nordility
import netility
import tkinter as tk
import pandas as pd
import sys

from tkinter import font

# STATIC SET
sys.setrecursionlimit(15000)

class ciTerminalGUI(object):
    def __BD(self):
        return 5
    
    def __init__(self):
        self.__guiRoot = tk.Tk(screenName='ciTerminal', className='ciTerminalGUI')
        self.__searchQuery = tk.StringVar(value='')
        self.__nordStatus = tk.BooleanVar(value=0)
        self.__chromeStatus = tk.BooleanVar(value=0)
        self.__citegresStatus = tk.BooleanVar(value=0)
        self.__df = pd.DataFrame()

        # MENU
        menuBar = tk.Menu(self.__guiRoot)
        nordMenu = tk.Menu(menuBar, tearoff=0)
        nordMenu.add_command(label='Connect', command=self.__nordConnect)
        nordMenu.add_command(label='Disconnect', command=self.__nordDisconnect)
        nordMenu.add_command(label='Reconnect', command=self.__nordReconnect)
        menuBar.add_cascade(label='Nord', menu=nordMenu)
        chromeMenu = tk.Menu(menuBar, tearoff=0)
        chromeMenu.add_command(label='Connect', command=self.__chromeConnect)
        chromeMenu.add_command(label='Disconnect', command=self.__chromeDisconnect)
        menuBar.add_cascade(label='Chrome', menu=chromeMenu)     
        citegresMenu = tk.Menu(menuBar, tearoff=0)
        citegresMenu.add_command(label='Connect', command=self.__citegresConnect)
        citegresMenu.add_command(label='Disconnect', command=self.__citegresDisconnect)
        citegresMenu.add_command(label='Reconnect', command=self.__citegresReconnect)
        citegresMenu.add_command(label='Implant Schema', command=self.__citegresImplantSchema)
        citegresDefaultDbMenu = tk.Menu(citegresMenu, tearoff=0)
        citegresDefaultDbMenu.add_command(label='CiteGres', command=self.__citegresSetCiteGresDB)
        citegresDefaultDbMenu.add_command(label='citegrestmp', command=self.__citegresSetCiteGresTmpDB)
        citegresDefaultDbMenu.add_command(label='databases', command=self.__citegresSetDatabasesDB)
        citegresDefaultDbMenu.add_command(label='networking', command=self.__citegresSetNetworkingDB)
        citegresDefaultDbMenu.add_command(label='architecture', command=self.__citegresSetArchitectureDB)
        citegresDefaultDbMenu.add_command(label='social_computing', command=self.__citegresSetSocialComputingDB)
        citegresDefaultDbMenu.add_command(label='informatics', command=self.__citegresSetInformaticsDB)
        citegresDefaultDbMenu.add_command(label='engineering', command=self.__citegresSetEngineeringDB)
        citegresMenu.add_cascade(label='Set Default DB', menu=citegresDefaultDbMenu) 
        menuBar.add_cascade(label='Citegres', menu=citegresMenu)    

        # TOP
        topFrame = tk.Frame(self.__guiRoot, bd=self.__BD())
        topFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.NO)

        ## SEARCH 
        searchLabelFrame = tk.LabelFrame(topFrame, text='DBLP Search Query:')
        searchLabelFrame.pack(side=tk.TOP, fill=tk.X, expand=tk.YES)
        separatorSearchLabelFrame = tk.Frame(searchLabelFrame, bd=self.__BD())
        separatorSearchLabelFrame.pack(fill=tk.X, expand=tk.YES)
        searchEntry = tk.Entry(separatorSearchLabelFrame, textvariable=self.__searchQuery)
        searchEntry.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)
        basicSearchButton = tk.Button(separatorSearchLabelFrame, text="SEARCH", command=self.__dblpQuery)
        basicSearchButton.pack(side=tk.RIGHT)
        advancedSearchButton = tk.Button(separatorSearchLabelFrame, text="XML SEARCH", command=self.__dblpQueryXML)
        advancedSearchButton.pack(side=tk.RIGHT)

        ## TOP SEARCH-STATUS SEPARATOR
        topSearchStatusSeparatorFrame = tk.Frame(topFrame, width=self.__BD())
        topSearchStatusSeparatorFrame.pack(side=tk.TOP)

        ## STATUS 
        statusFrame = tk.Frame(topFrame)
        statusFrame.pack(side=tk.TOP, fill=tk.X, expand=tk.NO)

        ### NORDVPN
        nordStatusLabelFrame = tk.LabelFrame(statusFrame, text='Nord Status:')
        nordStatusLabelFrame.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)
        separatorNordStatusLabelFrame = tk.Frame(nordStatusLabelFrame, bd=self.__BD())
        separatorNordStatusLabelFrame.pack(fill=tk.X, expand=tk.YES)
        self.__nordField = tk.Text(separatorNordStatusLabelFrame, state=tk.DISABLED, width=22, height=5)
        self.__nordField.pack(fill=tk.X, expand=tk.YES)

        ## TOP NORD-CHROME SEPARATOR
        topNordChromeSeparatorFrame = tk.Frame(statusFrame, width=self.__BD())
        topNordChromeSeparatorFrame.pack(side=tk.LEFT)

        ### CHROME
        chromeStatusLabelFrame = tk.LabelFrame(statusFrame, text='Chrome Status:')
        chromeStatusLabelFrame.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)
        separatorChromeStatusLabelFrame = tk.Frame(chromeStatusLabelFrame, bd=self.__BD())
        separatorChromeStatusLabelFrame.pack(fill=tk.X, expand=tk.YES)
        self.__chromeField = tk.Text(separatorChromeStatusLabelFrame, state=tk.DISABLED, width=22, height=5)
        self.__chromeField.pack(fill=tk.X, expand=tk.YES)

        ## TOP CHROME-CITEGRES SEPARATOR
        topChromeCitegresSeparatorFrame = tk.Frame(statusFrame, width=self.__BD())
        topChromeCitegresSeparatorFrame.pack(side=tk.LEFT)

        ### CITEGRES
        citegresStatusLabelFrame = tk.LabelFrame(statusFrame, text='Citegres Status:')
        citegresStatusLabelFrame.pack(side=tk.LEFT, fill=tk.X, expand=tk.YES)
        separatorCitegresStatusLabelFrame = tk.Frame(citegresStatusLabelFrame, bd=self.__BD())
        separatorCitegresStatusLabelFrame.pack(fill=tk.X, expand=tk.YES)
        self.__citegresField = tk.Text(separatorCitegresStatusLabelFrame, state=tk.DISABLED, width=22, height=5)
        self.__citegresField.pack(fill=tk.X, expand=tk.YES)

        # TOP-BOTTOM SEPARATOR
        topBottomSeparatorFrame = tk.Frame(self.__guiRoot, width=self.__BD())
        topBottomSeparatorFrame.pack(side=tk.TOP)

        # BOTTOM
        bottomFrame = tk.Frame(self.__guiRoot, bd=self.__BD())
        bottomFrame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)

        ## BOTTOM LEFT
        bottomLeftFrame = tk.Frame(bottomFrame, bd=self.__BD())
        bottomLeftFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)

        ### RESULTS
        resultsFrame = tk.Frame(bottomLeftFrame)
        resultsFrame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)

        #### RESULTS TEXT
        resultsTextLabelFrame = tk.LabelFrame(resultsFrame, text='Results:')
        resultsTextLabelFrame.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.YES)
        separatorResultsTextLabelFrame = tk.LabelFrame(resultsTextLabelFrame, bd=self.__BD())
        separatorResultsTextLabelFrame.pack(fill=tk.BOTH, expand=tk.YES)

        ##### RESULTS TEXT FONT
        resultsFontButtonFrame = tk.Frame(separatorResultsTextLabelFrame, width=self.__BD())
        resultsFontButtonFrame.pack(side=tk.TOP)
        resultsFontDecreaseButton = tk.Button(resultsFontButtonFrame, text="Decrease Font", command=self.__decreaseResultsFieldFont)
        resultsFontDecreaseButton.pack(side=tk.LEFT)
        resultsFontIncreaseButton = tk.Button(resultsFontButtonFrame, text="Increase Font", command=self.__increaseResultsFieldFont)
        resultsFontIncreaseButton.pack(side=tk.RIGHT)

        ##### RESULTS TEXT FIELD
        self.__resultsFieldTextSize = 10
        self.__resultsField = tk.Text(separatorResultsTextLabelFrame, state=tk.DISABLED, yscrollcommand=lambda first, last: self.__resultsScrollBar.set(first,last))
        self.__resultsField.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.YES)
        self.__resultsScrollBar = tk.Scrollbar(self.__resultsField, orient=tk.VERTICAL, cursor='arrow')
        self.__resultsScrollBar.config(command=self.__resultsField.yview)
        self.__resultsScrollBar.pack(side=tk.RIGHT, fill=tk.Y)

        ## BOTTOM LEFT-RIGHT SEPARATOR
        bottomLeftRightSeparatorFrame = tk.Frame(bottomFrame, width=self.__BD())
        bottomLeftRightSeparatorFrame.pack(side=tk.LEFT)

        ## BOTTOM RIGHT
        bottomRightFrame = tk.Frame(bottomFrame, width=self.__BD())
        bottomRightFrame.pack(side=tk.RIGHT, fill=tk.Y, expand=tk.NO)

        ### QUERIES
        queryLabelFrame = tk.LabelFrame(bottomRightFrame, text='Queries:')
        queryLabelFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.NO)
        separatorQueryLabelFrame = tk.LabelFrame(queryLabelFrame, bd=self.__BD())
        separatorQueryLabelFrame.pack(fill=tk.X, expand=tk.NO)

        #### DBLP
        queryDBLPLabelFrame = tk.LabelFrame(separatorQueryLabelFrame, text='DBLP Import:')
        queryDBLPLabelFrame.pack(side=tk.TOP, fill=tk.X, expand=tk.NO)
        separatorQueryDBLPLabelFrame = tk.LabelFrame(queryDBLPLabelFrame, bd=self.__BD())
        separatorQueryDBLPLabelFrame.pack(fill=tk.X, expand=tk.NO)
        queryExtractExplodedXmlButton = tk.Button(separatorQueryDBLPLabelFrame, text='Explode & Extract XML via Chrome', command=self.__dblpQueryExtract)
        queryExtractExplodedXmlButton.pack(side=tk.TOP, fill=tk.X)
        queryImportXmlButton = tk.Button(separatorQueryDBLPLabelFrame, text='Import XML to Citegres', command=self.__citegresImportXML)
        queryImportXmlButton.pack(side=tk.TOP, fill=tk.X)

        #### AUTHORS
        queryAuthorsLabelFrame = tk.LabelFrame(separatorQueryLabelFrame, text='Authors:')
        queryAuthorsLabelFrame.pack(side=tk.TOP, fill=tk.X, expand=tk.NO)
        separatorQueryAuthorsLabelFrame = tk.LabelFrame(queryAuthorsLabelFrame, bd=self.__BD())
        separatorQueryAuthorsLabelFrame.pack(fill=tk.X, expand=tk.NO)
        queryGetAuthorsAuthorsButton = tk.Button(separatorQueryAuthorsLabelFrame, text='Get All Authors', command=self.__citegresGetAuthorsAuthors)
        queryGetAuthorsAuthorsButton.pack(side=tk.TOP, fill=tk.X)
        queryGetSupportsAuthorsIdsButton = tk.Button(separatorQueryAuthorsLabelFrame, text='Get All Supporting Paper Author IDs', command=self.__citegresGetSupportsAuthorsIds)
        queryGetSupportsAuthorsIdsButton.pack(side=tk.TOP, fill=tk.X)
        queryGetSupportsAuthorsResolvedButton = tk.Button(separatorQueryAuthorsLabelFrame, text='Resolve All Supporting Paper Authors', command=self.__citegresGetSupportsAuthorsResolved)
        queryGetSupportsAuthorsResolvedButton.pack(side=tk.TOP, fill=tk.X)
        
        #### CONCEPTS 
        queryConceptsLabelFrame = tk.LabelFrame(separatorQueryLabelFrame, text='Concepts:')
        queryConceptsLabelFrame.pack(side=tk.TOP, fill=tk.X, expand=tk.NO)
        separatorQueryConceptsLabelFrame = tk.LabelFrame(queryConceptsLabelFrame, bd=self.__BD())
        separatorQueryConceptsLabelFrame.pack(fill=tk.X, expand=tk.NO)
        queryGetConceptsConceptsButton = tk.Button(separatorQueryConceptsLabelFrame, text='Get All Concepts', command=self.__citegresConceptsConcepts)
        queryGetConceptsConceptsButton.pack(side=tk.TOP, fill=tk.X)
        queryGetSupportsConceptsIdsButton = tk.Button(separatorQueryConceptsLabelFrame, text='Get All Paper Concept IDs', command=self.__citegresSupportsConceptsIds)
        queryGetSupportsConceptsIdsButton.pack(side=tk.TOP, fill=tk.X)
        queryGetSupportsConceptsResolvedButton = tk.Button(separatorQueryConceptsLabelFrame, text='Resolve All Paper Concepts', command=self.__citegresSupportsConceptsResolved)
        queryGetSupportsConceptsResolvedButton.pack(side=tk.TOP, fill=tk.X)

        #### EDGELISTS
        queryEdgelistLabelFrame = tk.LabelFrame(separatorQueryLabelFrame, text='Edgelists:')
        queryEdgelistLabelFrame.pack(side=tk.TOP, fill=tk.X, expand=tk.NO)
        separatorQueryEdgelistLabelFrame = tk.LabelFrame(queryEdgelistLabelFrame, bd=self.__BD())
        separatorQueryEdgelistLabelFrame.pack(fill=tk.X, expand=tk.NO)
        queryGetOpenalexIdEdgelistButton = tk.Button(separatorQueryEdgelistLabelFrame, text='Get Openalex ID Edgelist', command=self.__citegresGetOpenalexIdEdgelist)
        queryGetOpenalexIdEdgelistButton.pack(side=tk.TOP, fill=tk.X)
        queryGetOpenalexUrlEdgelistButton = tk.Button(separatorQueryEdgelistLabelFrame, text='Get Openalex URL Edgelist', command=self.__citegresGetOpenalexUrlEdgelist)
        queryGetOpenalexUrlEdgelistButton.pack(side=tk.TOP, fill=tk.X)
        queryGetOpenalexPaperEdgelistButton = tk.Button(separatorQueryEdgelistLabelFrame, text='Get Openalex Paper Edgelist', command=self.__citegresGetOpenalexPaperEdgelist)
        queryGetOpenalexPaperEdgelistButton.pack(side=tk.TOP, fill=tk.X)
        queryGetOpenalexAuthorEdgelistButton = tk.Button(separatorQueryEdgelistLabelFrame, text='Get Openalex Author Edgelist', command=self.__citegresGetOpenalexAuthorEdgelist)
        queryGetOpenalexAuthorEdgelistButton.pack(side=tk.TOP, fill=tk.X)

        ### BOTTOM RIGHT QUERIES-NETWORKING SEPARATOR
        bottomRightQueriesNetworkingSeparatorFrame = tk.Frame(bottomRightFrame, width=self.__BD())
        bottomRightQueriesNetworkingSeparatorFrame.pack(side=tk.TOP)
        
        ### NETWORKING
        networkingLabelFrame = tk.LabelFrame(bottomRightFrame, text='Networking:')
        networkingLabelFrame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=tk.NO)
        separatorNetworkingLabelFrame = tk.LabelFrame(networkingLabelFrame, bd=self.__BD())
        separatorNetworkingLabelFrame.pack(fill=tk.X, expand=tk.NO)
        networkingAuthorCitationButton = tk.Button(separatorNetworkingLabelFrame, text='Build Author Citation Graph', command=self.__networkingAuthorCitationGraph)
        networkingAuthorCitationButton.pack(side=tk.TOP, fill=tk.X)
        networkingPaperCitationButton = tk.Button(separatorNetworkingLabelFrame, text='Build Paper Citation Graph', command=self.__networkingPaperCitationGraph)
        networkingPaperCitationButton.pack(side=tk.TOP, fill=tk.X)
        networkingComputeGraphMetricsButton = tk.Button(separatorNetworkingLabelFrame, text='Compute Graph Metrics', command=self.__networkingComputeGraphMetrics) 
        networkingComputeGraphMetricsButton.pack(side=tk.TOP, fill=tk.X)
        networkingDisplayDegreeCentralities = tk.Button(separatorNetworkingLabelFrame, text='Display Degree Centralities', command=self.__networkingDisplayDegreeCentralities) 
        networkingDisplayDegreeCentralities.pack(side=tk.TOP, fill=tk.X)
        networkingDisplayClosenessCentralities = tk.Button(separatorNetworkingLabelFrame, text='Display Closeness Centralities', command=self.__networkingDisplayClosenessCentralities) 
        networkingDisplayClosenessCentralities.pack(side=tk.TOP, fill=tk.X)
        networkingDisplayBetweennessCentralities = tk.Button(separatorNetworkingLabelFrame, text='Display Betweenness Centralities', command=self.__networkingDisplayBetweennessCentralities) 
        networkingDisplayBetweennessCentralities.pack(side=tk.TOP, fill=tk.X)
        networkingPlotGraph = tk.Button(separatorNetworkingLabelFrame, text='Plot Graph', command=self.__networkingPlotGraph) 
        networkingPlotGraph.pack(side=tk.TOP, fill=tk.X)
        networkingGraphConfiguratorButton = tk.Button(separatorNetworkingLabelFrame, text='Deploy Graph Configurator', command=self.__networkingDeployGraphConfigurator) 
        networkingGraphConfiguratorButton.pack(side=tk.TOP, fill=tk.X)

        # CONFIG
        self.__guiRoot.config(menu=menuBar)
        self.__guiRoot.geometry(newGeometry='900x900')
        self.__setNordField(status='Disconnected.')
        self.__setChromeField(status='Disconnected.')
        self.__setCitegresField(status='Disconnected.')
        self.__setResultsField(status='Uninitialized.')

        # NETWORK VARS
        self.__use_labels = False
        self.__layout = 'spring'
        self.__pos = None
        self.__alpha = 0.27
        self.__edge_color = 'purple'
        self.__edge_width = 0.5
        self.__arrow_size = 5
        self.__node_size = 1
        self.__node_color = 'red'
        self.__cmap = 'rainbow'
        self.__G = None
        self.__gType = ''
        self.__metrics = dict()
 
    # BASIC DEFS
    ## NORDVPN
    def __setNordField(self, status):
        self.__nordField.config(state=tk.NORMAL)
        self.__nordField.delete(index1='0.0', index2=tk.END)
        self.__nordField.insert(index='0.0', chars=status)
        self.__nordField.config(state=tk.DISABLED)
        if self.__nordStatus.get():
            self.__nordField.tag_add('here', '1.0', '100.10')
            self.__nordField.tag_config('here', background='green', foreground='blue')
        else:
            self.__nordField.tag_add('here', '1.0', '100.10')
            self.__nordField.tag_config('here', background='red', foreground='yellow')

    def __nordConnect(self):
        self.__setNordField(nordility.connect_vpn_server())
        self.__nordStatus.set(1)

    def __nordDisconnect(self):
        self.__setNordField(nordility.disconnect_vpn_server())
        self.__nordStatus.set(0)

    def __nordReconnect(self):
        self.__nordStatus.set(0)
        self.__setNordField(nordility.change_vpn_server())
        self.__nordStatus.set(1)

    ## CHROME
    def __setChromeField(self, status):
        self.__chromeField.config(state=tk.NORMAL)
        self.__chromeField.delete(index1='0.0', index2=tk.END)
        self.__chromeField.insert(index='0.0', chars=status)
        if self.__chromeStatus.get():
            self.__chromeField.tag_add('here', '1.0', '100.10')
            self.__chromeField.tag_config('here', background='green', foreground='blue')
        else:
            self.__chromeField.tag_add('here', '1.0', '100.10')
            self.__chromeField.tag_config('here', background='red', foreground='yellow')
        self.__chromeField.config(state=tk.DISABLED)

    def __chromeConnect(self):
        self.__chromeStatus.set(1)
        self.__chromeDriver = seleamility.chrome_connect()
        self.__setChromeField(status='Connected.')

    def __chromeDisconnect(self):
        self.__chromeStatus.set(0)
        seleamility.chrome_disconnect(driver=self.__chromeDriver)
        self.__setChromeField(status='Disconnected.')

    ## CITEGRES
    def __setCitegresField(self, status):
        self.__citegresField.config(state=tk.NORMAL)
        self.__citegresField.delete(index1='0.0', index2=tk.END)
        self.__citegresField.insert(index='0.0', chars=status)
        if self.__citegresStatus.get():
            self.__citegresField.tag_add('here', '1.0', '100.10')
            self.__citegresField.tag_config('here', background='green', foreground='blue')
        else:
            self.__citegresField.tag_add('here', '1.0', '100.10')
            self.__citegresField.tag_config('here', background='red', foreground='yellow')
        self.__citegresField.config(state=tk.DISABLED)

    def __citegresConnect(self):
        self.__citegresStatus.set(1)
        self.__citegresCur, self.__citegresConn = postility.create_connection()
        self.__setCitegresField(status='Connected.')

    def __citegresDisconnect(self):
        self.__citegresStatus.set(0)
        postility.kill_connection(cur=self.__citegresCur, conn=self.__citegresConn)
        self.__setCitegresField(status='Disconnected.')

    def __citegresReconnect(self):
        self.__citegresStatus.set(1)
        self.__citegresCur, self.__citegresConn = postility.reset_connection(cur=self.__citegresCur, conn=self.__citegresConn)
        self.__setCitegresField(status='Connected.')

    def __citegresImplantSchema(self):
        postility.db_init(cur=self.__citegresCur, conn=self.__citegresConn)

    def __citegresSetCiteGresDB(self):
        postility.update_db_selection(section='CiteGres')
        self.__setResultsField(status='Default DB has been set to: CiteGres')

    def __citegresSetCiteGresTmpDB(self):
        postility.update_db_selection(section='citegrestmp')
        self.__setResultsField(status='Default DB has been set to: citegrestmp')

    def __citegresSetDatabasesDB(self):
        postility.update_db_selection(section='databases')
        self.__setResultsField(status='Default DB has been set to: databases')

    def __citegresSetNetworkingDB(self):
        postility.update_db_selection(section='networking')
        self.__setResultsField(status='Default DB has been set to: networking')

    def __citegresSetArchitectureDB(self):
        postility.update_db_selection(section='architecture')
        self.__setResultsField(status='Default DB has been set to: architecture')

    def __citegresSetSocialComputingDB(self):
        postility.update_db_selection(section='social_computing')
        self.__setResultsField(status='Default DB has been set to: social_computing')

    def __citegresSetInformaticsDB(self):
        postility.update_db_selection(section='informatics')
        self.__setResultsField(status='Default DB has been set to: informatics')

    def __citegresSetEngineeringDB(self):
        postility.update_db_selection(section='engineering')
        self.__setResultsField(status='Default DB has been set to: engineering')

    def __dblpQuery(self):
        query = self.__searchQuery.get()
        seleamility.chrome_query_dblp(driver=self.__chromeDriver, query=query)
        status = f'Results shown for query ({query}) in chrome.'
        self.__setResultsField(status=status)

    def __dblpQueryXML(self):
        query = self.__searchQuery.get()
        self.__searchResults = seleamility.chrome_query_dblp_XML(driver=self.__chromeDriver, query=query)
        status = f'Results shown for XML query ({query}) in chrome.'
        self.__setResultsField(status=status)

    def __dblpQueryExtract(self):
        query = str(self.__searchQuery.get())
        self.__df = seleamility.explode_query_dblp(driver=self.__chromeDriver, search_results=self.__searchResults, use_nord=self.__nordStatus.get())
        status = f'Results extracted for last XML query ({query}).'
        self.__setResultsField(status=status)
        self.__df.to_pickle('./__df.pkl')

    ## RESULTS
    def __increaseResultsFieldFont(self):
        self.__resultsFieldTextSize = self.__resultsFieldTextSize + 1
        self.__resultsField.config(font=font.Font(family='Courier New', size=self.__resultsFieldTextSize, weight='normal', slant='roman', underline=0, overstrike=0))

    def __decreaseResultsFieldFont(self):
        self.__resultsFieldTextSize = self.__resultsFieldTextSize - 1
        self.__resultsField.config(font=font.Font(family='Courier New', size=self.__resultsFieldTextSize, weight='normal', slant='roman', underline=0, overstrike=0))

    def __setResultsField(self, status):
        self.__resultsField.config(state=tk.NORMAL)
        self.__resultsField.delete(index1='0.0', index2=tk.END)
        self.__resultsField.insert(index='0.0', chars=status)
        self.__resultsField.config(state=tk.DISABLED)

    def __citegresImportXML(self):
        self.__citegresCur, self.__citegresConn = postility.importXML(cur=self.__citegresCur, conn=self.__citegresConn, df=self.__df)
        # TRUNCATE may combine DROP & CREATE to keep a table and delete all of it's data... should be faster
        status = f'XML search has been imported into Citegres, see console for logs...'
        self.__setResultsField(status)
        
    ### AUTHORS 
    def __citegresGetAuthorsAuthors(self):
        (self.__citegresCur, self.__citegresConn), status = postility.select_all_from_authors(cur=self.__citegresCur, conn=self.__citegresConn)
        self.__setResultsField(status.to_string())

    def __citegresGetSupportsAuthorsIds(self):
        (self.__citegresCur, self.__citegresConn), status = postility.select_all_from_supports(cur=self.__citegresCur, conn=self.__citegresConn)
        self.__setResultsField(status.to_string())

    def __citegresGetSupportsAuthorsResolved(self):
        (self.__citegresCur, self.__citegresConn), status = postility.select_all_from_supports_resolved(cur=self.__citegresCur, conn=self.__citegresConn)
        self.__setResultsField(status.to_string())

    ### CONCEPTS 
    def __citegresConceptsConcepts(self):
        (self.__citegresCur, self.__citegresConn), status = postility.select_all_from_concepts(cur=self.__citegresCur, conn=self.__citegresConn)
        self.__setResultsField(status.to_string())

    def __citegresSupportsConceptsIds(self):
        (self.__citegresCur, self.__citegresConn), status = postility.select_all_from_paper_concepts(cur=self.__citegresCur, conn=self.__citegresConn)
        self.__setResultsField(status.to_string())

    def __citegresSupportsConceptsResolved(self):
        (self.__citegresCur, self.__citegresConn), status = postility.select_all_from_paper_concepts_resolved(cur=self.__citegresCur, conn=self.__citegresConn)
        self.__setResultsField(status.to_string())

    ### EDGELISTS
    def __citegresGetOpenalexIdEdgelist(self):
        (self.__citegresCur, self.__citegresConn), status = postility.select_all_from_citations(cur=self.__citegresCur, conn=self.__citegresConn)
        self.__setResultsField(status.to_string())

    def __citegresGetOpenalexUrlEdgelist(self): 
        (self.__citegresCur, self.__citegresConn), status = postility.query_citationlist_full_resolve_openalex(cur=self.__citegresCur, conn=self.__citegresConn)
        self.__setResultsField(status.to_string())

    def __citegresGetOpenalexPaperEdgelist(self):
        (self.__citegresCur, self.__citegresConn), status = postility.query_citationlist_full_resolve_paper_title(cur=self.__citegresCur, conn=self.__citegresConn)
        self.__setResultsField(status.to_string())

    def __citegresGetOpenalexAuthorEdgelist(self):
        (self.__citegresCur, self.__citegresConn), status = postility.query_citationlist_full_resolve_author(cur=self.__citegresCur, conn=self.__citegresConn)
        self.__setResultsField(status.to_string())

    ## NETWORKING
    def __networkingAuthorCitationGraph(self):
        (self.__citegresCur, self.__citegresConn), self.__df = postility.query_citationlist_full_resolve_author(cur=self.__citegresCur, conn=self.__citegresConn)
        self.__G = netility.construct_graph_from_df(df=self.__df, directed=True)
        self.__gType = 'author'
        self.__setResultsField(status='Author Citation Graph Built')

    def __networkingPaperCitationGraph(self):
        (self.__citegresCur, self.__citegresConn), self.__df = postility.query_citationlist_full_resolve_paper_title(cur=self.__citegresCur, conn=self.__citegresConn)
        self.__G = netility.construct_graph_from_df(df=self.__df, directed=True)
        self.__gType = 'paper'
        self.__setResultsField(status='Paper Citation Graph Built')
        
    def __networkingComputeGraphMetrics(self):
        self.__metrics = netility.compute_graph_metrics(G=self.__G)
        self.__setResultsField(status=f'{self.__gType} Graph Metrics Computed')

    def __networkingDisplayDegreeCentralities(self):
        results = pd.DataFrame({self.__gType:[node for node in self.__G.nodes()], 'degree_centralities': self.__metrics['betweenness_centralities']}).sort_values('degree_centralities', ascending=False)
        self.__setResultsField(results.to_string())

    def __networkingDisplayClosenessCentralities(self):
        results = pd.DataFrame({self.__gType:[node for node in self.__G.nodes()], 'closeness_centralities': self.__metrics['betweenness_centralities']}).sort_values('closeness_centralities', ascending=False)
        self.__setResultsField(results.to_string())

    def __networkingDisplayBetweennessCentralities(self):
        results = pd.DataFrame({self.__gType:[node for node in self.__G.nodes()], 'betweenness_centrality': self.__metrics['betweenness_centralities']}).sort_values('betweenness_centrality', ascending=False)
        self.__setResultsField(results.to_string())

    def __networkingPlotGraph(self):
        self.__pos = netility.construct_static_layout(G=self.__G, layout=self.__layout)
        netility.plot_graph(G=self.__G, pos=self.__pos, use_labels=self.__use_labels, alpha=self.__alpha, edge_color=self.__edge_color, width=self.__edge_width, arrowsize=self.__arrow_size, node_size=self.__node_size, node_color=self.__node_color, cmap=self.__cmap)
        self.__setResultsField(status=f'{self.__gType} Graph Plot Opened in New Window')

    def __networkingDeployGraphConfigurator(self):
        # INIT
        self.__guiConfigurator = tk.Tk(screenName='graphConfigurator', className='graphConfigurator')

        ## TOP
        topFrame = tk.Frame(self.__guiConfigurator, bd=self.__BD())
        topFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)

        ### GRAPH CONFIGURATOR
        graphConfiguratorLabelFrame = tk.LabelFrame(topFrame, text='Graph Configuration:')
        graphConfiguratorLabelFrame.pack(side=tk.TOP, fill=tk.BOTH, expand=tk.YES)
        separatorGraphConfigurator = tk.Frame(graphConfiguratorLabelFrame, bd=self.__BD())
        separatorGraphConfigurator.pack(fill=tk.BOTH, expand=tk.YES)
        configurationIncreaseAlphaButton = tk.Button(separatorGraphConfigurator, text='Increase Alpha', command=self.__configurationIncreaseAlpha)
        configurationIncreaseAlphaButton.pack(side=tk.TOP, fill=tk.X)
        configurationDecreaseAlphaButton = tk.Button(separatorGraphConfigurator, text='Decrease Alpha', command=self.__configurationDecreaseAlpha)
        configurationDecreaseAlphaButton.pack(side=tk.TOP, fill=tk.X)

        #CONFIG
        self.__guiConfigurator.geometry(newGeometry='300x300')

    def __configurationIncreaseAlpha(self):
        self.__alpha = self.__alpha * 1.1

    def __configurationDecreaseAlpha(self):
        self.__alpha = self.__alpha * 1.1

    # MAIN LOOP
    def start(self):
        self.__guiRoot.mainloop()

# RUN IT
if __name__ == '__main__':
    GUI = ciTerminalGUI()
    GUI.start()
