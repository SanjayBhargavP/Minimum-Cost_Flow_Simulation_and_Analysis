#main.py

import os

from capacity_scaling import capacity_scaling_with_metrics
from source_sink_graph_generator import generate_graphs_for_simulation
from successive_shortest_paths import successive_shortest_paths
from utility import (
    load_graph_from_file,
    find_largest_connected_component,
    bfs_farthest_node,
    run_ford_fulkerson_and_write_results
)

# Define parameter sets for Simulation1
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

# Generate Graph Files
generate_graphs_for_simulation(parameter_sets_simulation1, "Simulation1")

# Define directory for Simulation1 files
simulation1_dir = "./Graphs/Simulation1"

result_file = os.path.join("./Results", "simulation1_ford_fulkerson_results.txt")
os.makedirs("./Results", exist_ok=True)

# Create result file with headers
with open(result_file, 'w', encoding='utf-8') as results:
    results.write("Graph\tfmax\t|VLCC|\t∆out(LCC)\t∆in(LCC)\tk(LCC)\n")

# Process each graph file
for filename in os.listdir(simulation1_dir):
    if filename.endswith(".edges"):
        file_path = os.path.join(simulation1_dir, filename)

        # Load graph
        graph = load_graph_from_file(file_path)

        # Find the largest connected component (LCC)
        lcc = find_largest_connected_component(graph)

        # Determine source and sink nodes
        source = lcc[0]  # Start node from LCC
        sink = bfs_farthest_node(graph, source)

        print(source)
        print(sink)

        # Run algorithm and write results
        fmax = run_ford_fulkerson_and_write_results(graph, source, sink, result_file, filename)

        print(successive_shortest_paths(graph, source, sink, 0.95*fmax))

        print(capacity_scaling_with_metrics(graph, source, sink, 0.95*fmax))



print("Simulation1 processing completed.")





