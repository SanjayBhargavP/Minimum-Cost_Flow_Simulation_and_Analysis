from collections import defaultdict
import math


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


if __name__ == "__main__":
    filename = "graph_1_n100_r0.2_cap8_cost5.edges"

    graph, source, sink = load_graph_from_file(filename)

    print(f"Source Node: {source}")
    print(f"Sink Node: {sink}")

    n = graph.number_of_nodes()
    print(f"Number of Nodes: {n}")

    LCC = graph.largest_connected_component()
    VLCC = len(LCC)
    in_degree, out_degree = graph.compute_in_out_degree(LCC)
    max_out_degree = max(out_degree.values())
    max_in_degree = max(in_degree.values())
    avg_degree = sum(in_degree[v] + out_degree[v] for v in LCC) / VLCC

    print(f"|VLCC|: {VLCC}")
    print(f"∆out(LCC): {max_out_degree}")
    print(f"∆in(LCC): {max_in_degree}")
    print(f"k(LCC): {avg_degree:.2f}")

    demand = 10
    flow, cost, paths, path_lengths = successive_shortest_paths_with_scaling(graph, source, sink, demand)
    if flow is None:
        print("Failure: Could not meet the required flow.")
    else:
        mean_length = sum(path_lengths) / len(path_lengths) if path_lengths else 0
        max_path_length = max(path_lengths) if path_lengths else 1
        mean_proportional_length = mean_length / max_path_length

        print(f"Total Flow: {flow}")
        print(f"Total Cost: {cost}")
        print(f"Number of Augmenting Paths: {paths}")
        print(f"Mean Length (ML): {mean_length:.2f}")
        print(f"Mean Proportional Length (MPL): {mean_proportional_length:.2f}")
