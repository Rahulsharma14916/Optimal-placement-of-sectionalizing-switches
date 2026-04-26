from pulp import *

print("=== Electrical Switch Placement Model ===")

# -----------------------------
# Step 1: User Inputs
# -----------------------------

n = int(input("Enter number of feeder sections: "))

sections = list(range(1, n+1))

failure_rate = {}
load = {}

print("\nEnter failure rate (failures/year) for each section:")
for i in sections:
    failure_rate[i] = float(input(f"Section {i}: "))

print("\nEnter load (kW) at each section:")
for i in sections:
    load[i] = float(input(f"Load at Section {i}: "))

repair_time = float(input("\nEnter repair time (hours, e.g. 5): "))
switch_time = float(input("Enter switching time (hours, e.g. 0.2): "))
cost_per_kwh = float(input("Enter interruption cost ($/kWh): "))
switch_cost = float(input("Enter cost per switch ($): "))
max_switches = int(input("Enter maximum number of switches allowed: "))

# -----------------------------
# Step 2: Model
# -----------------------------

model = LpProblem("Switch_Placement", LpMinimize)

x = LpVariable.dicts("Switch", sections, cat="Binary")

# -----------------------------
# Step 3: ECOST Calculation
# -----------------------------

ecost = 0

for i in sections:
    for j in sections:
        if j >= i:  # downstream affected
            outage_time = switch_time * x[i] + repair_time * (1 - x[i])
            ecost += failure_rate[i] * load[j] * outage_time * cost_per_kwh

# -----------------------------
# Step 4: Total Cost
# -----------------------------

switch_total = lpSum([switch_cost * x[i] for i in sections])

model += ecost + switch_total

# -----------------------------
# Step 5: Constraint
# -----------------------------

model += lpSum([x[i] for i in sections]) <= max_switches

# -----------------------------
# Step 6: Solve
# -----------------------------

model.solve()

# -----------------------------
# Step 7: Output
# -----------------------------

print("\n=== RESULT ===")
print("Status:", LpStatus[model.status])

print("\nOptimal Switch Placement:")
for i in sections:
    if x[i].value() == 1:
        print(f"Install switch at Section {i}")
    else:
        print(f"No switch at Section {i}")

print("\nTotal Minimum Cost:", value(model.objective))
