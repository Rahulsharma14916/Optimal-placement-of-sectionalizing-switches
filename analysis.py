import matplotlib.pyplot as plt

def plot_switch_vs_damage(run_solver, CDF):

    multipliers = list(range(1, 10))
    switches = []

    for m in multipliers:
        scaled_CDF = {
            k: {kk: vv*m for kk,vv in v.items()}
            for k,v in CDF.items()
        }

        model, X = run_solver(scaled_CDF, 22)
        count = sum(1 for s in X if X[s].value() == 1)
        switches.append(count)

    plt.figure()
    plt.plot(multipliers, switches, marker='o')
    plt.xlabel("Damage Multiplier")
    plt.ylabel("Switch Count")
    plt.title("Fig 5")
    plt.grid()
    plt.show()


def plot_costs(run_solver, CDF, CI):

    limits = list(range(1, 30))
    ecost_list = []
    total_cost_list = []

    for limit in limits:

        model, X = run_solver(CDF, limit)
        total = model.objective.value()

        switch_cost = sum(X[s].value() for s in X) * CI
        ecost = total - switch_cost

        ecost_list.append(ecost)
        total_cost_list.append(total)

    plt.figure()
    plt.plot(limits, ecost_list, label="ECOST")
    plt.plot(limits, total_cost_list, label="Total Cost")
    plt.legend()
    plt.title("Fig 6")
    plt.grid()
    plt.show()
