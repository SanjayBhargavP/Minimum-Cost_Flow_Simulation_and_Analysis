import math
from collections import defaultdict


class GraphHelper:
    """Helper class for graph-related operations."""
    
    class Edge:
        def __init__(self, from_node, to_node, capacity, cost):
            self.from_node = from_node
            self.to_node = to_node
            self.capacity = capacity
            self.cost = cost
            self.flow = 0

    class Graph:
        def __init__(self):
            self.adjacency_list = defaultdict(list)
            self.edges = []

        def add_edge(self, from_node, to_node, capacity, cost):
            forward_edge = GraphHelper.Edge(from_node, to_node, capacity, cost)
            backward_edge = GraphHelper.Edge(to_node, from_node, 0, -cost)
            forward_edge.reverse_edge = backward_edge
            backward_edge.reverse_edge = forward_edge
            self.adjacency_list[from_node].append(forward_edge)
            self.adjacency_list[to_node].append(backward_edge)
            self.edges.append(forward_edge)

    @staticmethod
    def bellman_ford_capacity_scaling(graph, source, sink, delta):
        """Shortest path algorithm to find minimum-cost augmenting paths."""
        distance = {node: float('inf') for node in graph.adjacency_list}
        parent = {node: None for node in graph.adjacency_list}
        distance[source] = 0

        for _ in range(len(graph.adjacency_list) - 1):
            for edge in graph.edges:
                if edge.capacity - edge.flow >= delta and distance[edge.from_node] + edge.cost < distance[edge.to_node]:
                    distance[edge.to_node] = distance[edge.from_node] + edge.cost
                    parent[edge.to_node] = edge

        # Check if sink is reachable
        if distance[sink] == float('inf'):
            return None, 0

        # Backtrack to find the path
        path = []
        node = sink
        while node != source:
            edge = parent[node]
            path.append(edge)
            node = edge.from_node
        path.reverse()

        # Determine the bottleneck capacity along the path
        bottleneck = min(edge.capacity - edge.flow for edge in path)
        return path, bottleneck
    
    # @staticmethod #old one
    # def bellman_ford(graph, source):
    #     dist = {node: math.inf for node in graph.nodes}
    #     parent = {node: None for node in graph.nodes}
    #     dist[source] = 0

    #     # Relax edges |V| - 1 times
    #     for _ in range(len(graph.nodes) - 1):
    #         for u in graph.nodes:
    #             for v in graph.adj[u]:
    #                 if graph.capacity[(u, v)] > 0 and dist[u] + graph.cost[(u, v)] < dist[v]:
    #                     dist[v] = dist[u] + graph.cost[(u, v)]
    #                     parent[v] = u

    #     return dist, parent
    

    @staticmethod 
    def bellman_ford(graph, source):
        dist = {node: math.inf for node in graph.adjacency_list}
        parent = {node: None for node in graph.adjacency_list}
        dist[source] = 0

        # Relax edges |V| - 1 times
        for _ in range(len(graph.adjacency_list) - 1):
            for u in graph.adjacency_list:
                for edge in graph.adjacency_list[u]:
                    v = edge.to_node
                    if edge.capacity > 0 and dist[u] + edge.cost < dist[v]:
                        dist[v] = dist[u] + edge.cost
                        parent[v] = u

        return dist, parent

    @staticmethod
    def find_longest_acyclic_path(graph, source, sink):
        """Find the longest acyclic path in a graph."""
        visited = set()
        stack = []

        def dfs(node):
            if node in visited:
                return
            visited.add(node)
            for edge in graph.adjacency_list[node]:
                if edge.capacity > 0:  # Only consider edges with positive capacity
                    dfs(edge.to_node)
            stack.append(node)

        dfs(source)
        stack.reverse()

        distances = {node: float('-inf') for node in graph.adjacency_list}
        distances[source] = 0

        for node in stack:
            for edge in graph.adjacency_list[node]:
                if edge.capacity > 0 and distances[node] + 1 > distances[edge.to_node]:
                    distances[edge.to_node] = distances[node] + 1

        return distances[sink] if distances[sink] != float('-inf') else 0
    
    @staticmethod
    def load_graph_from_file(filename):
        """Load a graph from a file."""
        graph = GraphHelper.Graph()
        with open(filename, 'r') as file:
            lines = file.readlines()

        # First two lines: Source and Sink
        source = int(lines[0].split(":")[1].strip())
        sink = int(lines[1].split(":")[1].strip())

        # Remaining lines: edges
        for line in lines[2:]:
            from_node, to_node, capacity, cost = map(int, line.split())
            graph.add_edge(from_node, to_node, capacity, cost)

        return graph, source, sink