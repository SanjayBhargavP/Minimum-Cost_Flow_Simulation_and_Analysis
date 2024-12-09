# successive_shortest_paths_capacity_scaling.py

import math
from collections import defaultdict

def successive_shortest_paths_capacity_scaling(graph, source, sink, demand):
    print("==== SUCCESSIVE SHORTEST PATHS WITH CAPACITY SCALING ====")
    total_flow = 0
    total_cost = 0
    augmenting_paths = 0
    path_lengths = []

    # Find maximum capacity for scaling
    max_capacity = max(edge.capacity for edge in graph.edges)
    scaling_factor = 2 ** (math.floor(math.log2(max_capacity)))

    while scaling_factor >= 1:
        while demand > 0:
            # Find shortest path using Bellman-Ford modified for capacity scaling
            dist = {node: float('inf') for node in graph.adjacency_list.keys()}
            parent = {node: None for node in graph.adjacency_list.keys()}
            dist[source] = 0

            for _ in range(len(graph.adjacency_list) - 1):
                for u in graph.adjacency_list.keys():
                    for edge in graph.adjacency_list[u]:
                        # Only consider edges with capacity >= scaling factor
                        if edge.capacity - edge.flow >= scaling_factor and dist[u] + edge.cost < dist[edge.to_node]:
                            dist[edge.to_node] = dist[u] + edge.cost
                            parent[edge.to_node] = (u, edge)

            # Check if sink is reachable with current scaling factor
            if dist[sink] == float('inf'):
                break

            # Reconstruct path
            path = []
            path_length = 0
            node = sink
            while node != source:
                u, edge = parent[node]
                path.append(edge)
                node = u
                path_length += 1
            path.reverse()

            # Determine maximum flow along the path
            path_flow = min(min(edge.capacity - edge.flow for edge in path), demand)

            # Augment flow along the path
            for edge in path:
                edge.flow += path_flow
                edge.reverse_edge.flow -= path_flow
                total_cost += path_flow * edge.cost

            total_flow += path_flow
            demand -= path_flow
            augmenting_paths += 1
            path_lengths.append(path_length)

        # Reduce scaling factor
        scaling_factor //= 2

    # Calculate metrics
    if demand > 0:
        return None, -1, None, None, None  # Failure: Not enough flow to satisfy demand
    else:
        num_paths = len(path_lengths)
        mean_length = sum(path_lengths) / num_paths if num_paths > 0 else 0
        longest_path = len(graph.adjacency_list.keys()) - 1
        mean_proportional_length = mean_length / longest_path if longest_path > 0 else 0

        return total_flow, total_cost, augmenting_paths, mean_length, mean_proportional_length