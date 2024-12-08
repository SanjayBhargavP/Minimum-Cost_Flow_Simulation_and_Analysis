# utility.py
from collections import defaultdict, deque


# ----------------- Ford-Fulkerson (Edmonds-Karp) ----------------- #
def ford_fulkerson_edmonds_karp(graph, source, sink):
    """
    Ford-Fulkerson Maximum Flow using Edmonds-Karp algorithm (BFS).

    Parameters:
    - graph: Graph object
    - source: Starting node
    - sink: Ending node

    Returns:
    - max_flow: The maximum flow found
    - residual_graph: The resulting residual graph after computing max flow
    """
    max_flow = 0
    residual_graph = create_residual_graph(graph)

    while True:
        path_flow, parent = bfs_for_flow(residual_graph, source, sink)
        if path_flow == 0:
            break

        # Update residual capacities of the edges and reverse edges
        v = sink
        while v != source:
            u, edge = parent[v]
            edge['capacity'] -= path_flow

            # Update reverse edge
            for reverse_edge in residual_graph[v]:
                if reverse_edge['to'] == u:
                    reverse_edge['capacity'] += path_flow
                    break
            v = u

        max_flow += path_flow

    return max_flow, residual_graph


def create_residual_graph(graph):
    """
    Builds the residual graph from the original graph.
    """
    residual_graph = defaultdict(list)
    for u in graph.adjacency_list:
        for edge in graph.adjacency_list[u]:
            residual_graph[u].append({'to': edge.to_node, 'capacity': edge.capacity, 'cost': edge.cost})
            if not any(e['to'] == u for e in residual_graph[edge.to_node]):
                residual_graph[edge.to_node].append({'to': u, 'capacity': 0, 'cost': -edge.cost})
    return residual_graph


def bfs_for_flow(graph, source, sink):
    """
    Breadth-First Search to find an augmenting path in the residual graph.
    """
    visited = set()
    queue = deque([(source, float('inf'))])
    parent = {}

    while queue:
        current, flow = queue.popleft()
        if current == sink:
            return flow, parent

        for edge in graph[current]:
            next_node = edge['to']
            capacity = edge['capacity']

            if next_node not in visited and capacity > 0:
                visited.add(next_node)
                parent[next_node] = (current, edge)
                next_flow = min(flow, capacity)
                queue.append((next_node, next_flow))

    return 0, None


# ----------------- Graph Metrics Calculation ----------------- #
def calculate_graph_metrics(graph, lcc):
    """
    Calculates key metrics for the largest connected component (LCC).

    Returns:
    - metrics: Dictionary of graph metrics
    """
    in_degree = defaultdict(int)
    out_degree = defaultdict(int)

    for u in graph.adjacency_list:
        for edge in graph.adjacency_list[u]:
            v = edge.to_node
            out_degree[u] += 1
            in_degree[v] += 1

    max_out_degree = max(out_degree[node] for node in lcc)
    max_in_degree = max(in_degree[node] for node in lcc)
    num_nodes = len(lcc)
    num_edges = sum(out_degree[node] for node in lcc)
    density = num_edges / (num_nodes * (num_nodes - 1)) if num_nodes > 1 else 0

    metrics = {
        '|VLCC|': num_nodes,
        '∆out(LCC)': max_out_degree,
        '∆in(LCC)': max_in_degree,
        'k(LCC)': round(density, 4)
    }
    return metrics


# ----------------- Write Results to File ----------------- #
def run_ford_fulkerson_and_write_results(graph, source, sink, file_path, filename):
    """
    Runs Ford-Fulkerson (Edmonds-Karp), calculates metrics, writes results, and returns fmax.

    Parameters:
    - graph: Graph object
    - source: Source node
    - sink: Sink node
    - file_path: Path to save results
    - filename: Current graph filename

    Returns:
    - fmax: The maximum flow found
    """
    # Find LCC and Calculate Max Flow
    max_flow, residual_graph = ford_fulkerson_edmonds_karp(graph, source, sink)
    lcc = find_largest_connected_component(graph)
    metrics = calculate_graph_metrics(graph, lcc)


#    Format the results writing
    result_format = f"{{:<{36}}}\t{{:<8}}\t{{:<8}}\t{{:<10}}\t{{:<10}}\t{{:<8.4f}}\n"

    # Write results to file
    with open(file_path, 'a') as results:
        results.write(result_format.format(
            filename,
            max_flow,
            metrics['|VLCC|'],
            metrics['∆out(LCC)'],
            metrics['∆in(LCC)'],
            metrics['k(LCC)']
        ))
        print(f"Processed {filename} | fmax: {max_flow}, Metrics: {metrics}")

    return max_flow


# ----------------- LCC Finder ----------------- #
def find_largest_connected_component(graph):
    """
    Finds the largest connected component using DFS.
    """
    visited = set()
    largest_component = []

    def dfs(node, component):
        visited.add(node)
        component.append(node)
        for edge in graph.adjacency_list[node]:
            if edge.to_node not in visited:
                dfs(edge.to_node, component)

    for node in graph.adjacency_list:
        if node not in visited:
            component = []
            dfs(node, component)
            if len(component) > len(largest_component):
                largest_component = component

    return largest_component


# ----------------- Graph Loader ----------------- #
def load_graph_from_file(filename):
    """
    Loads a graph from a file into a Graph object.

    Returns:
    - Graph: The loaded graph
    """
    from graph import Graph

    graph = Graph()
    try:
        with open(filename, 'r') as f:
            for line in f:
                u, v, capacity, cost = map(int, line.strip().split())
                graph.add_edge(u, v, capacity, cost)
        print(f"Graph loaded successfully from {filename}")
    except FileNotFoundError:
        print(f"Error: File {filename} not found.")
    return graph

# ----------------- BFS Farthest Node ----------------- #
def bfs_farthest_node(graph, source):
    """
    Finds the farthest node from the source using BFS.

    Parameters:
    - graph: The Graph object
    - source: Starting node (source node)

    Returns:
    - farthest_node: The node farthest from the source
    """
    visited = set()
    queue = deque([(source, 0)])
    farthest_node = source
    max_distance = 0

    while queue:
        current, distance = queue.popleft()

        for edge in graph.adjacency_list[current]:
            next_node = edge.to_node

            if next_node not in visited:
                visited.add(next_node)
                queue.append((next_node, distance + 1))

                if distance + 1 > max_distance:
                    max_distance = distance + 1
                    farthest_node = next_node

    print(f"Farthest Node from {source}: {farthest_node} (Distance: {max_distance})")
    return farthest_node

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


def print_results(flow, cost, num_paths, mean_length, mean_proportional_length,file_path,algo,graphNo):
    if flow is not None:
        print(f"flow:{flow} | cost:{cost} | paths:{num_paths} | ML:{mean_length} | MPL:{mean_proportional_length}")
    else:
        print("\nFailed to meet the flow demand.")
    print("---------------------")

    algo_header_format = f"{{:<{15}}}\t{{:<6}}\t{{:<6.4f}}\t{{:<10.4f}}\t{{:<10}}\t{{:<8.4f}}\t{{:<8.4f}}"

    with open(file_path, 'a') as results:
        results.write(algo_header_format.format(
            algo,
            graphNo,
            flow,
            cost,
            num_paths,
            mean_length,
            mean_proportional_length
        ))
        results.write("\n")

