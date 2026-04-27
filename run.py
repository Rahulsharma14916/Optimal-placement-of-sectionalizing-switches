from data_rbts import *
from topology import build_graph_with_loops
from preprocessing import compute_switch_map_with_loops
from milp_model import solve_milp_with_loops
from analysis import plot_switch_vs_damage, plot_costs
from visualization import plot_network

# ---------- CASE 1 ----------
G = build_graph_with_loops(edges, loops=True)

switch_map, alt_path = compute_switch_map_with_loops(
    G, nodes, switch_locations
)

model1, X1 = solve_milp_with_loops(
    nodes, switch_locations, load_data, lambda_line,
    CDF, switch_map, alt_path,
    CI, IC, MC, T, q, DR, 22
)

print("\nCASE 1 SWITCHES:")
for s in switch_locations:
    if X1[s].value() == 1:
        print(s, switch_locations[s])

plot_network(G, switch_locations, X1, "Figure 3 (Case 1)")

# ---------- CASE 2 ----------
G2 = build_graph_with_loops(edges, loops=False)

switch_map2, alt_path2 = compute_switch_map_with_loops(
    G2, nodes, switch_locations
)

model2, X2 = solve_milp_with_loops(
    nodes, switch_locations, load_data, lambda_line,
    CDF, switch_map2, alt_path2,
    CI, IC, MC, T, q, DR, 10
)

print("\nCASE 2 SWITCHES:")
for s in switch_locations:
    if X2[s].value() == 1:
        print(s, switch_locations[s])

plot_network(G2, switch_locations, X2, "Figure 4 (Case 2)")

# ---------- PLOTS ----------
def solver_wrapper(CDF_new, limit):
    return solve_milp_with_loops(
        nodes, switch_locations, load_data, lambda_line,
        CDF_new, switch_map, alt_path,
        CI, IC, MC, T, q, DR, limit
    )

plot_switch_vs_damage(solver_wrapper, CDF)
plot_costs(solver_wrapper, CDF, CI)
