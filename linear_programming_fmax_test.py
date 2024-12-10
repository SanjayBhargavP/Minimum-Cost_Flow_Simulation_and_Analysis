# Utility Functions
from utility import (
    load_graph_from_file,
    find_largest_connected_component,
    bfs_farthest_node,
    ford_fulkerson_edmonds_karp,
)

def solve_max_flow_lp(graph, source, sink):
    # Step 1: Variables for flow on each edge
    num_edges = len(graph.edges)
    flow = [0] * num_edges  # Flow variables for each edge

    # Step 2: Coefficients for the objective function (maximize flow into sink)
    c = [0] * num_edges
    for i, edge in enumerate(graph.edges):
        if edge.to_node == sink:
            c[i] = 1  # Maximize flow into the sink node

    # Step 3: Capacity constraints
    A_ub = [[0] * num_edges for _ in range(num_edges)]  # Matrix for '<= capacity' constraints
    b_ub = [0] * num_edges

    for i, edge in enumerate(graph.edges):
        A_ub[i][i] = 1  # Flow on edge i should be <= its capacity
        b_ub[i] = edge.capacity  # Maximum flow for that edge

    # Step 4: Flow conservation constraints
    A_eq = []
    b_eq = []

    for node in graph.adjacency_list.keys():
        if node == source or node == sink:
            continue

        row = [0] * num_edges
        for i, edge in enumerate(graph.edges):
            if edge.from_node == node:
                row[i] = -1  # Outflow from node
            if edge.to_node == node:
                row[i] = 1  # Inflow to node

        A_eq.append(row)
        b_eq.append(0)  # Flow conservation condition: inflow = outflow

    print("Starting Laux-style LP solver...")
    solution = [0] * num_edges  # Initialize solution to zero flow

    # Iteration over nodes, adjusting the flow based on constraints
    for iteration in range(100):  # Limit iterations to prevent infinite loops
        for i, edge in enumerate(graph.edges):
            # Adjust flow on each edge according to capacity and conservation constraints
            if flow[i] < edge.capacity:
                flow[i] += 0.1  # Increment the flow slightly (adjust with proper step size)
                flow[i] = min(flow[i], edge.capacity)  # Ensure we do not exceed capacity

        # Check if the solution is feasible (conservation and capacity constraints)
        feasible = True
        for i in range(num_edges):
            if flow[i] > b_ub[i]:
                feasible = False
                break

        # Flow conservation check
        for row, expected in zip(A_eq, b_eq):
            total_flow = sum(row[j] * flow[j] for j in range(num_edges))
            if total_flow != expected:
                feasible = False
                break

        if feasible:
            print(f"Feasible solution found: {flow}")
            break
        else:
            print(f"Iteration {iteration}: Adjusting flow...")

    # Step 6: Calculate the total flow into the sink (maximize this flow)
    max_flow = sum(flow[i] * c[i] for i in range(num_edges))  # Sum of flow on edges leading to the sink

    print(f"Max flow value: {max_flow}")
    return max_flow, flow


file_path= "Graphs/Test/LinearProgrammingTest/graph.txt"
graph = load_graph_from_file(file_path)

# Find the largest connected component (LCC)
lcc = find_largest_connected_component(graph)

# Determine source and sink nodes
source = lcc[0]  # Start node from LCC
sink = bfs_farthest_node(graph, source)

# Solve the max flow LP
max_flow, solution = solve_max_flow_lp(graph, source, sink)

fmax, residual_graph = ford_fulkerson_edmonds_karp(graph, source, sink)

if(fmax == max_flow):
    print("Test Passed!")
    print("Maximum Flow:", max_flow)
else:
    print("Failed the Test!")

