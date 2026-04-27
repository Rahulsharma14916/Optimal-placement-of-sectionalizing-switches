import networkx as nx
import matplotlib.pyplot as plt

def plot_network(G, switch_locations, X, title):

    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(10,6))
    nx.draw(G, pos, with_labels=True,
            node_color='lightblue', node_size=500)

    active_edges = []
    for s, edge in switch_locations.items():
        if X[s].value() == 1:
            active_edges.append(edge)

    nx.draw_networkx_edges(G, pos,
        edgelist=active_edges,
        edge_color='red',
        width=3)

    plt.title(title)
    plt.show()
