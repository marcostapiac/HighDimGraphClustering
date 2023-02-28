import networkx as nx
import matplotlib.pyplot as plt
from utils.math_functions import np


def visualise_digraph(cdNodes, adjMat, plottitle):
    """ Graph generation """
    G = nx.from_numpy_array(A=adjMat, create_using=nx.DiGraph)
    prevNodes = list(G.nodes)
    if len(cdNodes.shape) == 1:
        newLabels = dict([(x, y) for x, y in zip(prevNodes, cdNodes)])
    else:
        newLabels = dict([(x, y) for x, y in zip(prevNodes, np.reshape(cdNodes, (cdNodes.shape[0] * cdNodes.shape[1],)))])
    G = nx.relabel_nodes(G, newLabels)
    """ Styling """
    plt.style.use('ggplot')
    fig, ax = plt.subplots()
    ax.axis("off")
    ax.set_title(plottitle)
    """ Drawing """
    pos = nx.nx_agraph.graphviz_layout(G)
    nx.draw_networkx_nodes(G, pos, node_size=500)  # TODO: Dynamic node sizes
    nx.draw_networkx_labels(G, pos)
    """ Inter-cluster """
    interEdges = G.edges # TODO: Identify inter cluster edges
    nx.draw_networkx_edges(G, pos, edgelist=interEdges, edge_color="blue", arrows=True)  # TODO: Dynamic arrow sizes (with respect to nodes)
    #""" Intra-cluster """
    #intraEdges = G.edges # TODO: Identify intra-cluster edges
    #nx.draw_networkx_edges(G, pos, edgelist=intraEdges, edge_color="orange", arrows=True)  # TODO: Dynamic arrow sizes (with respect to nodes)
