import cplex
op = cplex.Cplex()
op.read("productivity.lp")
op.solve()
print("Max objective value is %s" %op.solution.get_objective_value())
print("Best Productivety is %s" %op.solution.get_values())
