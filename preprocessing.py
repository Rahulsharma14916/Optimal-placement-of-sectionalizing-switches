import networkx as nx

def compute_switch_map_with_loops(G, nodes, switch_locations):

    switch_map = {}
    alt_path_exists = {}

    for i in nodes:
        for j in nodes:
            if i == j:
                continue

            path = nx.shortest_path(G, i, j)
            edges_path = list(zip(path[:-1], path[1:]))

            sw_list = []
            for s, e in switch_locations.items():
                if e in edges_path or e[::-1] in edges_path:
                    sw_list.append(s)

            switch_map[(i,j)] = sw_list

            G_temp = G.copy()
            if len(edges_path) > 0:
                G_temp.remove_edge(*edges_path[0])

            try:
                nx.shortest_path(G_temp, i, j)
                alt_path_exists[(i,j)] = True
            except:
                alt_path_exists[(i,j)] = False

    return switch_map, alt_path_exists
