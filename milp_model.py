import pulp

def solve_milp_with_loops(nodes, switch_locations, load_data, lambda_line,
               CDF, switch_map, alt_path_exists,
               CI, IC, MC, T, q, DR, max_switches):

    model = pulp.LpProblem("RBTS", pulp.LpMinimize)

    X = pulp.LpVariable.dicts("X", switch_locations.keys(), cat="Binary")
    C_d = pulp.LpVariable.dicts("C_d",
            [(i,j) for i in nodes for j in nodes],
            lowBound=0)

    obj = 0

    for t in range(T):
        growth = (1+q)**t
        discount = (1+DR)**(-t)

        for i in nodes:
            for j in nodes:
                if i == j:
                    continue

                load = load_data[j]["load"]
                obj += lambda_line * load * C_d[(i,j)] * growth * discount

        for s in switch_locations:
            obj += (CI+IC+MC) * X[s] * discount

    model += obj

    model += pulp.lpSum(X[s] for s in switch_locations) <= max_switches

    for i in nodes:
        for j in nodes:
            if i == j:
                continue

            typ = load_data[j]["type"]
            Csw = CDF[typ]["switch"]
            Crep = CDF[typ]["repair"]

            path_sw = switch_map[(i,j)]

            model += C_d[(i,j)] >= Csw

            if alt_path_exists[(i,j)]:
                model += C_d[(i,j)] >= Csw
            else:
                model += C_d[(i,j)] >= Crep * (
                    1 - pulp.lpSum(X[s] for s in path_sw)
                )

    model.solve(pulp.PULP_CBC_CMD(msg=0))

    return model, X
