from collections import defaultdict
import math



    
def bellman_ford(graph, s, t, delta):
    dist = {node: math.inf for node in graph.graph}
    parent = {node: None for node in graph.graph}
    dist[s] = 0

    
    for _ in range(len(graph.graph) - 1):
        for u in graph.graph:
            for v in graph.graph[u]:
                if graph.capacity[u][v] >= delta and dist[u] + graph.cost[u][v] < dist[v]:
                    dist[v] = dist[u] + graph.cost[u][v]
                    parent[v] = u

    
    if dist[t] == math.inf:
        return None, None

    
    path = []
    curr = t
    while curr is not None:
        path.append(curr)
        curr = parent[curr]
    path.reverse()

    return path, dist[t]


def successive_shortest_paths_with_scaling(graph, s, t, d):
    f = 0
    total_cost = 0
    delta = max(graph.capacity[u][v] for u in graph.graph for v in graph.graph[u])
    paths = 0
    augmenting_path_lengths = []

    while delta >= 1:
        while d > 0:
            path, cost = bellman_ford(graph, s, t, delta)
            if not path:
                break

            flow = math.inf
            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                flow = min(flow, graph.capacity[u][v])

            flow = min(flow, d)
            augmenting_path_lengths.append(len(path) - 1)  # Path length
            paths += 1

            for i in range(len(path) - 1):
                u, v = path[i], path[i + 1]
                graph.capacity[u][v] -= flow
                graph.capacity[v][u] += flow

            f += flow
            total_cost += flow * cost
            d -= flow

        delta //= 2

    return f, total_cost, paths, augmenting_path_lengths





   

