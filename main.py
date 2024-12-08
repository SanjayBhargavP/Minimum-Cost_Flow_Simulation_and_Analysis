#main.py

import copy
import os

from capacity_scaling import capacity_scaling_with_metrics
from source_sink_graph_generator import generate_graphs_for_simulation
from successive_shortest_paths import successive_shortest_paths
from utility import (
    load_graph_from_file,
    find_largest_connected_component,
    bfs_farthest_node,
    run_ford_fulkerson_and_write_results,
    print_results
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

result_file1 = os.path.join("./Results", "simulation1_ford_fulkerson_results.txt")
result_file2 = os.path.join("./Results","simulation1_algorithms_results.txt")
os.makedirs("./Results", exist_ok=True)

# Determine the maximum filename length in the graph directory
max_filename_length = max(len(filename) for filename in os.listdir(simulation1_dir) if filename.endswith(".edges"))

# Format the header with dynamic spacing
ford_header_format = f"{{:<{max_filename_length}}}\tfmax\t|VLCC|\t∆out(LCC)\t∆in(LCC)\tk(LCC)\n"

# Create result file with headers
with open(result_file1, 'w', encoding='utf-8') as results:
    results.write(ford_header_format.format("Graph"))

algo_header_format = f"{{:<{15}}}\t{{:<6}}\t{{:<6}}\t{{:<10}}\t{{:<10}}\t{{:<8}}\t{{:<8}}"

# Create result file with headers
with open(result_file2, 'w', encoding='utf-8') as results:
    results.write(algo_header_format.format("Algorithm","Graph","f","MC","paths","ML","MPL"))
    results.write("\n")

graph_number=1
algo_ssp = "SSP"
algo_cs ="CS"
algo_ssps="SSPCS"
algo_yours="YOURS" ##CHANGE HERE
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

        print("Source:{}".format(source))
        print("Sink:{}".format(sink))

        graph_copy_ssp = copy.deepcopy(graph)
        graph_copy_cs = copy.deepcopy(graph)


        # Run algorithm and write results
        fmax = run_ford_fulkerson_and_write_results(graph, source, sink, result_file1, filename)
        demand = 0.95*fmax
        
        print("Max flow using Ford Fulkerson={}".format(fmax))
        print("Demand={}".format(demand))
        print()

        successive_shortest_paths(graph_copy_ssp, source, sink, demand)
        print_results(flow,cost,paths,ml,mpl,result_file2,algo_ssp,graph_number)
        flow,cost,paths,ml,mpl = capacity_scaling_with_metrics(graph_copy_cs, source, sink, demand)
        print_results(flow,cost,paths,ml,mpl,result_file2,algo_cs,graph_number)
        
        with open(result_file2, 'a', encoding='utf-8') as results:
            results.write("-" * 110 + "\n")

        graph_number+=1

print("Simulation1 processing completed.")





