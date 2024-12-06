import math
from collections import defaultdict


class Graph:
    def __init__(self, nodes):
        self.nodes = nodes
        self.adj = defaultdict(list)
        self.capacity = {}
        self.cost = {}

    def add_edge(self, u, v, capacity, cost):
        self.adj[u].append(v)
        self.adj[v].append(u)  # Add reverse edge for the residual graph
        self.capacity[(u, v)] = capacity
        self.capacity[(v, u)] = 0  # Reverse edge has zero capacity initially
        self.cost[(u, v)] = cost
        self.cost[(v, u)] = -cost  # Reverse edge has negative cost


def bellman_ford(graph, source):
    dist = {node: math.inf for node in graph.nodes}
    parent = {node: None for node in graph.nodes}
    dist[source] = 0

    # Relax edges |V| - 1 times
    for _ in range(len(graph.nodes) - 1):
        for u in graph.nodes:
            for v in graph.adj[u]:
                if graph.capacity[(u, v)] > 0 and dist[u] + graph.cost[(u, v)] < dist[v]:
                    dist[v] = dist[u] + graph.cost[(u, v)]
                    parent[v] = u

    return dist, parent


def successive_shortest_paths(graph, source, sink, total_flow):
    flow = 0
    total_cost = 0
    augmenting_paths = 0  # Number of augmenting paths
    path_lengths = []  # List to store the lengths of augmenting paths

    while total_flow > 0:
        # Find shortest path using Bellman-Ford
        dist, parent = bellman_ford(graph, source)

        # If sink is unreachable, break
        if dist[sink] == math.inf:
            break

        # Find the maximum flow along the path
        path_flow = float('inf')
        path_length = 0
        v = sink
        while v != source:
            u = parent[v]
            path_flow = min(path_flow, graph.capacity[(u, v)])
            path_length += 1  # Count edges in the path
            v = u

        # Adjust path_flow to not exceed remaining total_flow
        path_flow = min(path_flow, total_flow)

        # Augment flow and update residual capacities
        v = sink
        while v != source:
            u = parent[v]
            graph.capacity[(u, v)] -= path_flow
            graph.capacity[(v, u)] += path_flow
            total_cost += path_flow * graph.cost[(u, v)]
            v = u

        flow += path_flow
        total_flow -= path_flow
        augmenting_paths += 1
        path_lengths.append(path_length)

    # Compute mean length (ML)
    ml = sum(path_lengths) / len(path_lengths) if path_lengths else 0

    # Compute mean proportional length (MPL)
    longest_path = len(graph.nodes) - 1  # Longest possible acyclic path
    mpl = sum(pl / longest_path for pl in path_lengths) / len(path_lengths) if path_lengths else 0

    if total_flow > 0:
        return None, -1, augmenting_paths, ml, mpl  # Unable to meet the required total flow

    return flow, total_cost, augmenting_paths, ml, mpl


def read_graph_from_file(file_path):
    """
    Reads a graph from a file in the specified format.

    Args:
    file_path (str): Path to the graph file.

    Returns:
    Graph, source, sink
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Extract source and sink
    source = int(lines[0].split(":")[1].strip())
    sink = int(lines[1].split(":")[1].strip())

    # Extract edges
    edges = []
    nodes = set()
    for line in lines[2:]:
        u, v, capacity, cost = map(int, line.split())
        edges.append((u, v, capacity, cost))
        nodes.update([u, v])

    # Create graph
    graph = Graph(nodes)
    for u, v, capacity, cost in edges:
        graph.add_edge(u, v, capacity, cost)

    return graph, source, sink


# Example usage
if __name__ == "__main__":
    # Path to the graph file
    file_path = "graph_1_n100_r0.2_cap8_cost5.edges"

    # Read the graph from file
    graph, source, sink = read_graph_from_file(file_path)

    # Set required flow
    required_flow = 10

    # Run the Successive Shortest Path algorithm
    flow, cost, paths, ml, mpl = successive_shortest_paths(graph, source, sink, required_flow)

    if flow is None:
        print("Unable to achieve the required flow.")
    else:
        print(f"Total flow: {flow}")
        print(f"Total cost: {cost}")
        print(f"Number of augmenting paths: {paths}")
        print(f"Mean length of augmenting paths (ML): {ml}")
        print(f"Mean proportional length (MPL): {mpl}")
