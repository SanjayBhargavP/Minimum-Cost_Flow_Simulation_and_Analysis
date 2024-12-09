import math
from heapq import heappop, heappush


def primal_dual_algorithm(graph, source, sink, total_demand):
    """
    Primal-Dual Algorithm for Minimum-Cost Flow

    Parameters:
    - graph: Graph object
    - source: Source node
    - sink: Sink node
    - total_demand: Total flow demand

    Returns:
    - Total flow achieved
    - Total cost of flow
    - Number of augmenting paths
    - Mean path length
    - Mean proportional path length
    """
    print("==== PRIMAL-DUAL MINIMUM COST FLOW ====")

    # Initialize flow and tracking metrics
    total_flow = 0
    total_cost = 0
    augmenting_paths = 0
    path_lengths = []

    # Create a copy of graph for modification
    graph_copy = {node: [{'to': e.to_node, 'capacity': e.capacity, 'cost': e.cost, 'reverse_flow': 0}
                         for e in graph.adjacency_list[node]]
                  for node in graph.adjacency_list}

    # Compute initial dual variables (potential)
    potential = {node: float('inf') for node in graph.adjacency_list}
    potential[source] = 0

    # Compute reduced costs and update potentials
    for _ in range(len(graph.adjacency_list) - 1):
        for u in graph.adjacency_list:
            for edge in graph.adjacency_list[u]:
                v = edge.to_node
                if potential[u] + edge.cost < potential[v] and edge.capacity > 0:
                    potential[v] = potential[u] + edge.cost

    while total_demand > 0:
        # Find shortest path with reduced costs using Dijkstra
        dist = {node: float('inf') for node in graph.adjacency_list}
        parent = {node: None for node in graph.adjacency_list}
        dist[source] = 0
        pq = [(0, source)]

        while pq:
            curr_dist, u = heappop(pq)

            if u == sink:
                break

            if curr_dist > dist[u]:
                continue

            for edge_idx, edge in enumerate(graph_copy[u]):
                v = edge['to']
                # Compute reduced cost
                reduced_cost = edge['cost'] + potential[u] - potential[v]

                if edge['capacity'] > 0 and dist[u] + reduced_cost < dist[v]:
                    dist[v] = dist[u] + reduced_cost
                    parent[v] = (u, edge_idx)
                    heappush(pq, (dist[v], v))

        # Check if path to sink exists
        if parent[sink] is None:
            break

        # Find bottleneck flow along the path
        path_flow = total_demand
        v = sink
        path = []
        while v != source:
            u, edge_idx = parent[v]
            path_flow = min(path_flow, graph_copy[u][edge_idx]['capacity'])
            path.append(graph_copy[u][edge_idx])
            v = u
        path.reverse()

        # Augment flow along the path
        v = sink
        while v != source:
            u, edge_idx = parent[v]
            graph_copy[u][edge_idx]['capacity'] -= path_flow
            graph_copy[u][edge_idx]['reverse_flow'] += path_flow

            # Find and update reverse edge
            for rev_edge in graph_copy[v]:
                if rev_edge['to'] == u:
                    rev_edge['capacity'] += path_flow
                    break

            v = u

        # Update flow and cost metrics
        total_flow += path_flow
        total_cost += path_flow * sum(edge['cost'] for edge in path)
        total_demand -= path_flow
        augmenting_paths += 1
        path_lengths.append(len(path))

        # Update potentials
        for node in graph.adjacency_list:
            if dist[node] != float('inf'):
                potential[node] += dist[node]

    # Compute path length metrics
    longest_path = len(graph.adjacency_list.keys()) - 1
    mean_length = sum(path_lengths) / len(path_lengths) if path_lengths else 0
    mean_proportional_length = sum(pl / longest_path for pl in path_lengths) / len(path_lengths) if path_lengths else 0

    if total_demand > 0:
        return None, -1, augmenting_paths, mean_length, mean_proportional_length

    return total_flow, total_cost, augmenting_paths, mean_length, mean_proportional_length