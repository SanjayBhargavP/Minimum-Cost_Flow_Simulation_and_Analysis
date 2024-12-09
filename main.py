import copy
import os


# Graph Generation and Source-Sink Graph Tools
from source_sink_graph_generator import generate_graphs_for_simulation

# Graph Classes and Core Implementations
from capacity_scaling import capacity_scaling_with_metrics
from successive_shortest_paths import successive_shortest_paths
from successive_shortest_paths_capacity_scaling import successive_shortest_paths_capacity_scaling
from primal_dual_algorithm import primal_dual_algorithm

# Utility Functions
from utility import (
    load_graph_from_file,
    find_largest_connected_component,
    bfs_farthest_node,
    run_ford_fulkerson_and_write_results,
    print_results
)

# Define parameter sets for Simulation1 and Simulation2
parameter_sets_simulation1 = [
    (100, 0.2, 8, 5),
    (200, 0.2, 8, 5),
    (100, 0.3, 8, 5),
    (200, 0.3, 8, 5),
    (100, 0.2, 64, 20),
    (200, 0.2, 64, 20),
    (100, 0.3, 64, 20),
    (200, 0.3, 64, 20)
]

parameter_sets_simulation2 = [
    (150, 0.25, 16, 10),
    (250, 0.25, 16, 10),
    (150, 0.35, 16, 10),
    (250, 0.35, 16, 10),
    (150, 0.25, 128, 40),
    (250, 0.25, 128, 40),
    (150, 0.35, 128, 40),
    (250, 0.35, 128, 40)
]

# Generate Graph Files
generate_graphs_for_simulation(parameter_sets_simulation1, "Simulation1")
generate_graphs_for_simulation(parameter_sets_simulation2, "Simulation2")

# Define directories for simulation files
simulation1_dir = "./Graphs/Simulation1"
simulation2_dir = "./Graphs/Simulation2"

# Create Results directory
os.makedirs("./Results", exist_ok=True)

# Define result file paths with simulation-specific prefixes
result_file1_simulation1 = os.path.join("./Results", "simulation_one_ford_fulkerson_results.txt")
result_file2_simulation1 = os.path.join("./Results", "simulation_one_algorithms_results.txt")
result_file1_simulation2 = os.path.join("./Results", "simulation_two_ford_fulkerson_results.txt")
result_file2_simulation2 = os.path.join("./Results", "simulation_two_algorithms_results.txt")

# Determine the maximum filename length for each simulation
max_filename_length1 = max(len(filename) for filename in os.listdir(simulation1_dir) if filename.endswith(".edges"))
max_filename_length2 = max(len(filename) for filename in os.listdir(simulation2_dir) if filename.endswith(".edges"))

# Format headers with dynamic spacing
ford_header_format =  f"{{:<10}}\t{{:<5}}\t{{:<5}}\t{{:<10}}\t{{:<10}}\t{{:<10}}\t{{:<10}}\t{{:<12}}\t{{:<12}}\t{{:<11}}\n"
algo_header_format = f"{{:<15}}\t{{:<15}}\t{{:<9}}\t{{:<12}}\t{{:<10}}\t{{:<10}}\t{{:<10}}"

# Create result files with headers for Simulation1
with open(result_file1_simulation1, 'w', encoding='utf-8') as results:
    results.write(ford_header_format.format("Graph", "n", "r", "upperCap", "upperCost", "fmax", "|VLCC|", "∆out(LCC)", "∆in(LCC)", "k(LCC)"))

with open(result_file2_simulation1, 'w', encoding='utf-8') as results:
    results.write(algo_header_format.format("Algorithm", "Graph", "f", "MC", "paths", "ML", "MPL"))
    results.write("\n")

# Create result files with headers for Simulation2
with open(result_file1_simulation2, 'w', encoding='utf-8') as results:
    results.write(
        ford_header_format.format("Graph", "n", "r", "upperCap", "upperCost", "fmax", "|VLCC|", "∆out(LCC)", "∆in(LCC)", "k(LCC)"))

with open(result_file2_simulation2, 'w', encoding='utf-8') as results:
    results.write(algo_header_format.format("Algorithm", "Graph", "f", "MC", "paths", "ML", "MPL"))
    results.write("\n")

# Algorithm identifiers
algo_ssp = "SSP"
algo_cs = "CS"
algo_sspcs = "SSPCS"
algo_pd = "PD"

# Process Simulation1
def process_simulation(simulation_dir, result_file1, result_file2, simulation_number):
    graph_number = 1
    for filename in os.listdir(simulation_dir):
        file_path = os.path.join(simulation_dir, filename)

        # Load graph
        graph = load_graph_from_file(file_path)

        # Find the largest connected component (LCC)
        lcc = find_largest_connected_component(graph)

        # Determine source and sink nodes
        source = lcc[0]  # Start node from LCC
        sink = bfs_farthest_node(graph, source)

        print(f"Simulation {simulation_number} - Source:{source}")
        print(f"Simulation {simulation_number} - Sink:{sink}")

        # Create deep copies of graph for each algorithm
        graph_copy_ssp = copy.deepcopy(graph)
        graph_copy_cs = copy.deepcopy(graph)
        graph_copy_sspcs = copy.deepcopy(graph)
        graph_copy_pd = copy.deepcopy(graph)

        # Run algorithm and write results
        fmax = run_ford_fulkerson_and_write_results(graph, source, sink, result_file1, filename)
        demand = 0.95 * fmax

        print(f"Simulation {simulation_number} - Max flow using Ford Fulkerson = {fmax}")
        print(f"Simulation {simulation_number} - Demand = {demand}")
        print()

        # Run and print results for each algorithm
        flow, cost, paths, ml, mpl = successive_shortest_paths(graph_copy_ssp, source, sink, demand)
        print_results(flow, cost, paths, ml, mpl, result_file2, algo_ssp, filename)

        flow, cost, paths, ml, mpl = capacity_scaling_with_metrics(graph_copy_cs, source, sink, demand)
        print_results(flow, cost, paths, ml, mpl, result_file2, algo_cs, filename)

        flow, cost, paths, ml, mpl = successive_shortest_paths_capacity_scaling(graph_copy_sspcs, source, sink, demand)
        print_results(flow, cost, paths, ml, mpl, result_file2, algo_sspcs, filename)

        # Run Primal-Dual Algorithm
        flow, cost, paths, ml, mpl = primal_dual_algorithm(graph_copy_pd, source, sink, demand)
        print_results(flow, cost, paths, ml, mpl, result_file2, algo_pd, filename)

        with open(result_file2, 'a', encoding='utf-8') as results:
            results.write("-" * 110 + "\n")

        graph_number += 1

# Process both simulations
process_simulation(simulation1_dir, result_file1_simulation1, result_file2_simulation1, 1)
process_simulation(simulation2_dir, result_file1_simulation2, result_file2_simulation2, 2)

print("Simulation processing completed.")