from collections import defaultdict
import math
from tabulate import tabulate


class DirectedGraph:
    def __init__(self):
        self.graph = {}
        self.capacity = defaultdict(lambda: defaultdict(int))  
        self.cost = defaultdict(lambda: defaultdict(int)) 

    def add_edge(self, u, v, capacity, cost):
        if u not in self.graph:
            self.graph[u] = []
        self.graph[u].append(v)
        self.capacity[u][v] = capacity
        self.cost[u][v] = cost

        if v not in self.graph:
            self.graph[v] = []
        self.graph[v].append(u)  
        self.capacity[v][u] = 0  
        self.cost[v][u] = -cost  
        
        
    def number_of_nodes(self):
        return len(self.graph)

    def compute_in_out_degree(self, nodes):
        in_degree = defaultdict(int)
        out_degree = defaultdict(int)
        for u in nodes:
            for v in self.graph[u]:
                out_degree[u] += 1
                in_degree[v] += 1
        return in_degree, out_degree

    def largest_connected_component(self):
        visited = set()
        largest_cc = []

        def dfs(node, component):
            visited.add(node)
            component.append(node)
            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    dfs(neighbor, component)

        for node in self.graph:
            if node not in visited:
                component = []
                dfs(node, component)
                if len(component) > len(largest_cc):
                    largest_cc = component
        return largest_cc
    
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

def load_graph_from_file(filename):
    
    graph = DirectedGraph()
    source = None
    sink = None

    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue  
            
            if line.startswith("Source:"):
                source = int(line.split(":")[1].strip())
            elif line.startswith("Sink:"):
                sink = int(line.split(":")[1].strip())
            else:
                parts = line.split()
                if len(parts) == 4:
                    u, v, capacity, cost = map(int, parts)
                    graph.add_edge(u, v, capacity, cost)
                else:
                    raise ValueError(f"Invalid edge format: {line}")
    
    return graph, source, sink


def main():
    results = []
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
        filename = f"graph_{i}_n{n}_r{r}_cap{upper_cap}_cost{upper_cost}.edges"
        
        try:
            # Load the graph
            graph, source, sink = load_graph_from_file(filename)
            
            # Graph metrics
            num_nodes = graph.number_of_nodes()
            LCC = graph.largest_connected_component()
            VLCC = len(LCC) if LCC else 0
            
            if VLCC > 0:
                in_degree, out_degree = graph.compute_in_out_degree(LCC)
                max_out_degree = max(out_degree.values(), default=0)
                max_in_degree = max(in_degree.values(), default=0)
                avg_degree = sum(in_degree[v] + out_degree[v] for v in LCC) / VLCC
            else:
                max_out_degree = max_in_degree = avg_degree = 0

            # Flow calculation
            demand = 10
            flow, cost, _, path_lengths = successive_shortest_paths_with_scaling(graph, source, sink, demand)
            flow_result = flow if flow else "-"
            
            # Append results
            results.append([
                i, num_nodes, r, upper_cap, upper_cost, flow_result,
                VLCC, max_out_degree, max_in_degree, round(avg_degree, 2)
            ])

        except Exception as e:
            print(f"Error processing {filename}: {e}")
            results.append([i, n, r, upper_cap, upper_cost, "-", "-", "-", "-", "-"])

    # Table headers
    headers = [
        "Graph", "n", "r", "upperCap", "upperCost", "$f_{max}$", 
        "|V_{LCC}|", "Δ_{out}(LCC)", "Δ_{in}(LCC)", "k̅(LCC)"
    ]
    
    # Print the table
    print(tabulate(results, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    main()

