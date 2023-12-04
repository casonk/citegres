'''
    Author: Cason Konzer
    Module: netility
    -- Part of: citegres
    Developed for: Advance Database Concepts & Applications

    Function: Provides an interface for graph processing and plotting
    Version: 2.0
    Dated: December 2, 2023
'''

# IMPORTS
import sys
import logging
# import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
# from fa2 import ForceAtlas2

# STATIC SET
logging.basicConfig(stream=sys.stdout, encoding='utf-8', level=logging.INFO)
pyLogger = logging.getLogger(name='netility_debug')

# forceatlas2 = ForceAtlas2(
#                         # Behavior alternatives
#                         outboundAttractionDistribution=True,  # Dissuade hubs
#                         linLogMode=False,  # NOT IMPLEMENTED
#                         adjustSizes=False,  # Prevent overlap (NOT IMPLEMENTED)
#                         edgeWeightInfluence=1.0,

#                         # Performance
#                         jitterTolerance=1.0,  # Tolerance
#                         barnesHutOptimize=True,
#                         barnesHutTheta=1.2,
#                         multiThreaded=False,  # NOT IMPLEMENTED

#                         # Tuning
#                         scalingRatio=2.0,
#                         strongGravityMode=False,
#                         gravity=1.0,

#                         # Log
#                         verbose=True)

plt.style.use('dark_background')
plt.ion()

## CONDITIONAL IMPORT
# try:
#     import cynetworkx as nx                    
# except ImportError:
#     import networkx as nx

# GLOBAL VARS
POS_LAYOUT = 'spring'

# CONSTRUCTION DEFS
def construct_static_layout(G, layout='spring'):
    '''
    Utility for generating node positioning
    '''
    if layout == 'spring':
        pos = nx.spring_layout(G)
    elif layout == 'fruchterman_reingold':
        pos = nx.fruchterman_reingold_layout(G)
    elif layout == 'spiral':
        pos = nx.spiral_layout
    elif layout == 'planar':
        pos = nx.planar_layout(G)
    elif layout == 'shell':
        pos = nx.shell_layout(G)
    elif layout == 'random':
        pos = nx.random_layout(G)
    elif layout == 'circular':
        pos = nx.circular_layout(G)
    elif layout == 'spectral':
        pos = nx.spectral_layout(G)
    return pos

def construct_graph_from_df(df, directed=True):
    '''
    Utility for graph construction
    '''
    if directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    edge_weights_df = df.value_counts().items()
    weighted_edge_list = [(e[0][0], e[0][1], e[1]) for e in edge_weights_df]
    G.add_weighted_edges_from(weighted_edge_list)
    return G

# COMPUTING DEF
def compute_graph_metrics(G, degrees=False, out_degrees=False, in_degrees=True, degree_centralities=False,
                          closeness_centralities=False, betweenness_centralities=True):
    '''
    Utility for computing common graph metrics
    '''
    metrics = {}
    if degrees:
        metrics['degrees'] = [G.degree(node) for node in G]
    if out_degrees:
        metrics['out_degrees'] = [G.out_degree(node) for node in G]
    if in_degrees:
        metrics['in_degrees'] = [(G.in_degree(node)) for node in G]
    if degree_centralities:
        degree_centrality = nx.in_degree_centrality(G)
        metrics['degree_centralities'] = [degree_centrality[node] for node in G.nodes()]
    if closeness_centralities:
        closeness_centrality = nx.closeness_centrality(G)
        metrics['closeness_centralities'] = [closeness_centrality[node] for node in G.nodes()]
    if betweenness_centralities:
        betweenness_centrality = nx.betweenness_centrality(G)
        metrics['betweenness_centralities'] = [betweenness_centrality[node] for node in G.nodes()]
    return metrics

# PLOTTING DEF
def plot_graph(G, pos, use_labels, alpha, edge_color, width, arrowsize, node_size, node_color, cmap):
    '''
    Utility for graph plotting
    '''
    if cmap == 'rainbow':
        cmap = plt.cm.rainbow
    plt.figure(figsize=(16,9))
    nx.draw_networkx(G, pos=pos, with_labels=use_labels, alpha=alpha, edge_color=edge_color, width=width, 
                     arrowsize=arrowsize, node_size=node_size, node_color=node_color, cmap=cmap)
    return plt.show()

