import math
from utility import bellman_ford_capacity_scaling, find_longest_acyclic_path
from collections import defaultdict

# Capacity Scaling Algorithm

def capacity_scaling_with_metrics(graph, source, sink, demand):
    print("==== CAPACITY SCALING ====")
    max_capacity = max(edge.capacity for edge in graph.edges)
    scaling_factor = 2 ** (math.floor(math.log2(max_capacity)))
    total_flow = 0
    total_cost = 0
    augmenting_paths = []
    path_lengths = []

    while scaling_factor >= 1:
        while demand > 0:
            path, bottleneck = bellman_ford_capacity_scaling(graph, source, sink, scaling_factor)
            if not path:
                break

            # Track path and its length
            augmenting_paths.append(path)
            path_lengths.append(len(path))

            # Adjust flow along the augmenting path
            flow_to_add = min(bottleneck, demand)
            for edge in path:
                edge.flow += flow_to_add
                edge.reverse_edge.flow -= flow_to_add
            total_flow += flow_to_add
            total_cost += flow_to_add * sum(edge.cost for edge in path)
            demand -= flow_to_add

        scaling_factor //= 2

    # Calculate metrics
    if demand > 0:
        return None, -1, None,None,None  # Failure: Not enough flow to satisfy demand
    else:
        num_paths = len(augmenting_paths)
        mean_length = sum(path_lengths) / num_paths if num_paths > 0 else 0
        longest_acyclic_path = find_longest_acyclic_path(graph, source, sink)
        mean_proportional_length = mean_length / longest_acyclic_path if longest_acyclic_path > 0 else 0

        return total_flow, total_cost, num_paths, mean_length, mean_proportional_length