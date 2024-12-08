# graph.py

from collections import defaultdict

class Edge:
    def __init__(self, from_node, to_node, capacity, cost):
        self.from_node = from_node
        self.to_node = to_node
        self.capacity = capacity
        self.cost = cost
        self.flow = 0
        self.reverse_edge = None


class Graph:
    def __init__(self):
        self.adjacency_list = defaultdict(list)
        self.edges = []

    def add_edge(self, from_node, to_node, capacity, cost):
        forward_edge = Edge(from_node, to_node, capacity, cost)
        backward_edge = Edge(to_node, from_node, 0, -cost)

        forward_edge.reverse_edge = backward_edge
        backward_edge.reverse_edge = forward_edge

        self.adjacency_list[from_node].append(forward_edge)
        # self.adjacency_list[to_node].append(backward_edge)
        self.edges.append(forward_edge)

    def get_neighbors(self, node):
        return self.adjacency_list[node]

    def print_graph(self):
        for node, edges in self.adjacency_list.items():
            for edge in edges:
                if edge.capacity > 0:
                    print(f"{node} -> {edge.to_node} | Capacity: {edge.capacity}, Cost: {edge.cost}, Flow: {edge.flow}")

    def __str__(self):
        result = []
        for node, edges in self.adjacency_list.items():
            connections = []
            for edge in edges:
                if edge.capacity > 0:
                    connections.append(str(edge.to_node))
            if connections:
                result.append(f"{node} -> {', '.join(connections)}")
        return '\n'.join(result)