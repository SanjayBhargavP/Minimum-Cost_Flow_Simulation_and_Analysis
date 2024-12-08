import os
import random


class DirectedGraph:
    def __init__(self):
        self.graph = {}  # Adjacency list representation

    def add_node(self, node):
        if node not in self.graph:
            self.graph[node] = []

    def add_edge(self, u, v, capacity, cost):
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append({'to': v, 'capacity': capacity, 'cost': cost})

    def has_edge(self, u, v):
        return any(edge['to'] == v for edge in self.graph.get(u, []))

    def number_of_nodes(self):
        return len(self.graph)

    def number_of_edges(self):
        return sum(len(neighbors) for neighbors in self.graph.values())


def generate_sink_source_graph(n, r, upper_cap, upper_cost):
    """
    Generate a directed Euclidean neighbor graph.

    Parameters:
        n (int): Number of nodes
        r (float): Maximum distance between nodes sharing an edge
        upper_cap (int): Maximum capacity value
        upper_cost (int): Maximum unit cost value

    Returns:
        DirectedGraph: The generated graph
    """

    G = DirectedGraph()

    # Assign random coordinates to nodes
    coordinates = [(random.uniform(0, 1), random.uniform(0, 1)) for _ in range(n)]
    for i in range(n):
        G.add_node(i)

    # Add edges based on Euclidean distance
    for u in range(n):
        for v in range(n):
            if u != v:
                dist = (coordinates[u][0] - coordinates[v][0]) ** 2 + (coordinates[u][1] - coordinates[v][1]) ** 2
                if dist <= r ** 2:
                    rand = random.uniform(0, 1)
                    if rand < 0.3 and not G.has_edge(u, v) and not G.has_edge(v, u):
                        cap = random.randint(1, upper_cap)
                        cost = random.randint(1, upper_cost)
                        G.add_edge(u, v, capacity=cap, cost=cost)
                    elif rand < 0.6 and not G.has_edge(u, v) and not G.has_edge(v, u):
                        cap = random.randint(1, upper_cap)
                        cost = random.randint(1, upper_cost)
                        G.add_edge(v, u, capacity=cap, cost=cost)

    return G


def save_graph_to_file(graph, folder_path, filename):
    """
    Save the generated graph to a file in edge list format.

    Parameters:
        graph (DirectedGraph): The graph to save
        folder_path (str): Path to the folder where the graph file will be saved
        filename (str): The name of the file to save the graph
    """
    # Ensure the folder exists
    os.makedirs(folder_path, exist_ok=True)

    # Save the graph to the file
    file_path = os.path.join(folder_path, filename)
    with open(file_path, 'w') as f:
        for u, neighbors in graph.graph.items():
            for edge in neighbors:
                v = edge['to']
                capacity = edge['capacity']
                cost = edge['cost']
                f.write(f"{u} {v} {capacity} {cost}\n")


def generate_graphs_for_simulation(parameter_sets, simulation_name):
    """
    Generate graphs based on parameter sets and save them to files under a specific simulation folder.

    Parameters:
        parameter_sets (list of tuples): Each tuple contains (n, r, upper_cap, upper_cost)
        simulation_name (str): The name of the simulation (e.g., 'Simulation1')
    """
    folder_path = os.path.join("./Graphs", simulation_name)
    for i, (n, r, upper_cap, upper_cost) in enumerate(parameter_sets, 1):
        # Generate graph
        G = generate_sink_source_graph(n, r, upper_cap, upper_cost)

        # Create filename
        filename = f"graph_{i}_n{n}_r{r}_cap{upper_cap}_cost{upper_cost}.edges"

        # Save the graph
        save_graph_to_file(G, folder_path, filename)

        # Print details
        print(f"Graph {i}: n={n}, r={r}, upperCap={upper_cap}, upperCost={upper_cost}")
        print(f"Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}\n")