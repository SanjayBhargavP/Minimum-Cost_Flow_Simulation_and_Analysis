# successive_shortest_paths.py

# Bellman-Ford Algorithm
def bellman_ford(graph, source):
    dist = {node: float('inf') for node in graph.adjacency_list.keys()}
    parent = {node: None for node in graph.adjacency_list.keys()}
    dist[source] = 0

    for _ in range(len(graph.adjacency_list) - 1):
        for u in graph.adjacency_list.keys():
            for edge in graph.adjacency_list[u]:
                v = edge.to_node
                if edge.capacity > 0 and dist[u] + edge.cost < dist[v]:
                    dist[v] = dist[u] + edge.cost
                    parent[v] = u

    return dist, parent


# Successive Shortest Path Algorithm
def successive_shortest_paths(graph, source, sink, total_flow):
    flow = 0
    total_cost = 0
    augmenting_paths = 0
    path_lengths = []

    while total_flow > 0:
        # Find shortest path using Bellman-Ford
        dist, parent = bellman_ford(graph, source)

        if dist[sink] == float('inf'):
            break  # Sink is unreachable

        # Find minimum flow along the path
        path_flow = float('inf')
        path_length = 0
        v = sink

        while v != source:
            u = parent[v]
            for edge in graph.adjacency_list[u]:
                if edge.to_node == v:
                    path_flow = min(path_flow, edge.capacity)
                    break
            path_length += 1
            v = u

        path_flow = min(path_flow, total_flow)

        # Update residual capacities
        v = sink
        while v != source:
            u = parent[v]
            for edge in graph.adjacency_list[u]:
                if edge.to_node == v:
                    edge.capacity -= path_flow
            for edge in graph.adjacency_list[v]:
                if edge.to_node == u:
                    edge.capacity += path_flow
                    total_cost += path_flow * edge.cost
                    break
            v = u

        flow += path_flow
        total_flow -= path_flow
        augmenting_paths += 1
        path_lengths.append(path_length)

    # Calculate metrics
    longest_path = len(graph.adjacency_list.keys()) - 1
    mean_length = sum(path_lengths) / len(path_lengths) if path_lengths else 0
    mean_proportional_length = sum(pl / longest_path for pl in path_lengths) / len(path_lengths) if path_lengths else 0

    if total_flow > 0:
        return None, -1, augmenting_paths, mean_length, mean_proportional_length

    return flow, total_cost, augmenting_paths, mean_length, mean_proportional_length
