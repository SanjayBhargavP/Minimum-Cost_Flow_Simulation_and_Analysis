import numpy as np

class DirectedGraph:
    def __init__(self):
        self.graph = {} 
        self.node_attributes = {}  

    def add_node(self, node, **attributes):
        if node not in self.graph:
            self.graph[node] = []  
        self.node_attributes[node] = attributes 

    def add_edge(self, u, v, capacity=0, cost=0):
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append({'to': v, 'capacity': capacity, 'cost': cost})

    def display_graph(self):
        print("Graph (Adjacency List):")
        for node, neighbors in self.graph.items():
            print(f"{node} -> {neighbors}")

    def display_node_attributes(self):
        print("Node Attributes:")
        for node, attributes in self.node_attributes.items():
            print(f"{node}: {attributes}")

    def has_edge(self, u, v):
        
        return any(edge['to'] == v for edge in self.graph.get(u, []))
    
    def _dfs(self, node, visited, component):
        visited.add(node)
        component.append(node)
        for neighbor in self.graph.get(node, []):
            if neighbor['to'] not in visited:
                self._dfs(neighbor['to'], visited, component)

    def largest_connected_component(self):
        visited = set()
        largest_component = []

        undirected_graph = {}
        for node in self.graph:
            undirected_graph.setdefault(node, [])
            for edge in self.graph[node]:
                undirected_graph[node].append(edge['to'])
                undirected_graph.setdefault(edge['to'], []).append(node)

        for node in undirected_graph:
            if node not in visited:
                component = []
                self._dfs_undirected(node, visited, component, undirected_graph)
                if len(component) > len(largest_component):
                    largest_component = component

        return largest_component

    def _dfs_undirected(self, node, visited, component, graph):
        
        visited.add(node)
        component.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                self._dfs_undirected(neighbor, visited, component, graph)
                
    def single_source_shortest_path_length(self, start_node):
        
        distances = {start_node: 0}  # Distance to the start node
        queue = [start_node]  # BFS queue

        while queue:
            current = queue.pop(0)
            current_distance = distances[current]

            for edge in self.graph.get(current, []):
                neighbor = edge['to']
                if neighbor not in distances: 
                    distances[neighbor] = current_distance + 1
                    queue.append(neighbor)

        return distances

    def find_sink_node(self, start_node):
        
        paths = self.single_source_shortest_path_length(start_node)
        sink_node = max(paths, key=paths.get)  # Node with the maximum distance
        return sink_node
    
    def find_start_node(self):
        largest_cc = self.largest_connected_component()

        if not largest_cc:
            return None, None  

        
        start_node = largest_cc[0]
        
        return start_node
    
    def number_of_nodes(self):
        
        return len(self.graph)
    
    def number_of_edges(self):
        
        return sum(len(neighbors) for neighbors in self.graph.values())

def generate_sink_source_graph(n, r, upper_cap, upper_cost, seed=None):
    """
    Generate a directed Euclidean neighbor graph with specified parameters.

    Args:
    n (int): Number of vertices
    r (float): Maximum distance between nodes sharing an edge
    upper_cap (int): Maximum capacity value
    upper_cost (int): Maximum unit cost value
    seed (int, optional): Random seed for reproducibility

    Returns:
    nx.DiGraph: Generated directed graph
    """
    # Set random seed for reproducibility
    if seed is not None:
        np.random.seed(seed)

    # Create graph
    G = DirectedGraph()

    # Assign random coordinates to nodes
    coordinates = np.random.uniform(0, 1, size=(n, 2))

    for i in range(n):
        G.add_node(i, x=coordinates[i][0], y=coordinates[i][1])

    # Add edges based on Euclidean distance
    for u in range(n):
        for v in range(n):
            if u != v:
                # Calculate Euclidean distance
                dist = np.sqrt((coordinates[u][0] - coordinates[v][0]) ** 2 +
                               (coordinates[u][1] - coordinates[v][1]) ** 2)

                # Check if within radius r
                if dist <= r**2:
                    rand = np.random.uniform()

                    # Add directed edge with 30% probability in one direction
                    if rand < 0.3 and not G.has_edge(u, v) and not G.has_edge(v, u):
                        cap = np.random.randint(1, upper_cap + 1)
                        cost = np.random.randint(1, upper_cost + 1)
                        G.add_edge(u, v, capacity=cap, cost=cost)

                    # Add directed edge with another 30% probability in other direction
                    elif rand < 0.6 and not G.has_edge(u, v) and not G.has_edge(v, u):
                        cap = np.random.randint(1, upper_cap + 1)
                        cost = np.random.randint(1, upper_cost + 1)
                        G.add_edge(v, u, capacity=cap, cost=cost)

    return G


def find_source_and_sink(G):
   
    # Find largest connected component
    largest_cc = G.largest_connected_component()
    # smallest_cc = min(nx.weakly_connected_components(G), key=len)
    # print("Nodes: "+str(len(list(G.nodes()))))
    # print("Largest: "+str(len(list(largest_cc))))
    # print("Smallest: "+str(len(list(smallest_cc))))
   
    # Select a starting node from the largest connected component
    start_node = G.find_start_node()

    # Find the furthest node using BFS
    # paths = nx.single_source_shortest_path_length(G, start_node)
    # sink_node = max(paths, key=paths.get)
    sink_node=G.find_sink_node(start_node)

    return start_node, sink_node


def save_graph_to_edges_file(graph, filename, source, sink):
    
    with open(filename, 'w') as f:
        f.write(f"Source: {source}\n")
        f.write(f"Sink: {sink}\n")
        
        for u, neighbors in graph.graph.items():
            for edge in neighbors:
                v = edge['to']
                capacity = edge.get('capacity', 1)
                cost = edge.get('cost', 1)
                f.write(f"{u} {v} {capacity} {cost}\n")


def generate_source_sink_networks():
    """
    Generate 8 source-sink networks with specified parameters.
    """
    # Parameters as specified in the problem
    parameter_sets = [
        (100, 0.2, 8, 5),
        (200, 0.2, 8, 5),
        (100, 0.3, 8, 5),
        (200, 0.3, 8, 5),
        (100, 0.2, 64, 20),
        (200, 0.2, 64, 20),
        (100, 0.3, 64, 20),
        (200, 0.3, 64, 20)
    ]

    for i, (n, r, upper_cap, upper_cost) in enumerate(parameter_sets, 1):
        # Generate graph
        G = generate_sink_source_graph(n, r, upper_cap, upper_cost)

        # Find source and sink
        source, sink = find_source_and_sink(G)

        # Save to file
        filename = f"graph_{i}_n{n}_r{r}_cap{upper_cap}_cost{upper_cost}.edges"
        save_graph_to_edges_file(G, filename, source, sink)

        print(f"Graph {i}: n={n}, r={r}, upperCap={upper_cap}, upperCost={upper_cost}")
        print(f"Source: {source}, Sink: {sink}, Nodes: {G.number_of_nodes()}, Edges: {G.number_of_edges()}\n")


# Run the generation
if __name__ == "__main__":
    generate_source_sink_networks()