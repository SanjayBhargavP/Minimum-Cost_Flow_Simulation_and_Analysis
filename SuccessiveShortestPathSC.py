import math
from graph import Graph, Edge

def bellman_ford(graph, s, t, delta):
    dist = {node: math.inf for node in graph.adjacency_list}
    parent = {node: None for node in graph.adjacency_list}
    edge_used = {node: None for node in graph.adjacency_list}  
    dist[s] = 0

    # Relax edges |V| - 1 times
    for _ in range(len(graph.adjacency_list) - 1):
        for u in graph.adjacency_list:
            for edge in graph.get_neighbors(u):
                if edge.capacity >= delta and dist[u] + edge.cost < dist[edge.to_node]:
                    dist[edge.to_node] = dist[u] + edge.cost
                    parent[edge.to_node] = u
                    edge_used[edge.to_node] = edge

    if dist[t] == math.inf:
        return None, None

    # Reconstruct the path
    path = []
    curr = t
    while curr is not None:
        path.append(curr)
        curr = parent[curr]
    path.reverse()

    return path, dist[t]


def successive_shortest_paths_with_scaling(graph, s, t, d):
    f = 0  # Total flow
    total_cost = 0
    delta = max(edge.capacity for edge in graph.edges)  # Max edge capacity
    paths = 0  # Count of augmenting paths
    augmenting_path_lengths = []

    while delta >= 1:
        while d > 0:
            path, cost = bellman_ford(graph, s, t, delta)
            if not path:
                break  # No augmenting path found

            # Determine bottleneck flow along the path
            flow = math.inf
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                for edge in graph.get_neighbors(u):
                    if edge.to_node == v and edge.capacity > 0:
                        flow = min(flow, edge.capacity)

            flow = min(flow, d)  # Flow cannot exceed the remaining demand
            augmenting_path_lengths.append(len(path) - 1)
            paths += 1

            # Update edge capacities and reverse edges
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                for edge in graph.get_neighbors(u):
                    if edge.to_node == v and edge.capacity > 0:
                        edge.capacity -= flow
                        edge.reverse_edge.capacity += flow
                        break

            # Update flow, cost, and remaining demand
            f += flow
            total_cost += flow * cost
            d -= flow

        delta //= 2  

    return f, total_cost, paths, augmenting_path_lengths
