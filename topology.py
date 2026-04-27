import networkx as nx

def build_graph_with_loops(edges, loops=False):
    G = nx.Graph()
    G.add_edges_from(edges)

    if loops:
        G.add_edge(8, 12)
        G.add_edge(15, 19)
        G.add_edge(22, 25)
        G.add_edge(28, 31)

    return G
