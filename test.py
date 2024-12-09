import random
import os


def generate_small_graphs():
    """Generate small graphs for basic testing."""
    os.makedirs("Tests/SmallGraphs", exist_ok=True)

    # Simple Linear Graph
    def linear_graph():
        edges = [
            (0, 1, 10, 1),  # from, to, capacity, cost
            (1, 2, 10, 1),
            (2, 3, 10, 1)
        ]
        return edges, (0, 3)

    # Branching Graph
    def branching_graph():
        edges = [
            (0, 1, 15, 2),
            (0, 2, 10, 1),
            (1, 3, 10, 3),
            (2, 3, 5, 1),
            (1, 4, 5, 2),
            (2, 4, 8, 3)
        ]
        return edges, (0, 4)

    # Bottleneck Graph
    def bottleneck_graph():
        edges = [
            (0, 1, 5, 1),
            (0, 2, 10, 2),
            (1, 3, 15, 3),
            (2, 3, 5, 1)
        ]
        return edges, (0, 3)

    graphs = [
        ("linear_graph.edges", linear_graph()),
        ("branching_graph.edges", branching_graph()),
        ("bottleneck_graph.edges", bottleneck_graph())
    ]

    for filename, (edges, _) in graphs:
        path = os.path.join("Tests/SmallGraphs", filename)
        with open(path, 'w') as f:
            for u, v, cap, cost in edges:
                f.write(f"{u} {v} {cap} {cost}\n")


def generate_boundary_graphs():
    """Generate graphs for boundary condition testing."""
    os.makedirs("Tests/BoundaryTests", exist_ok=True)

    # Equal Flow Graph
    def equal_flow_graph():
        edges = [
            (0, 1, 10, 1),
            (0, 2, 10, 1),
            (1, 3, 10, 2),
            (2, 3, 10, 2)
        ]
        return edges, (0, 3)

    # Impossible Flow Graph
    def impossible_flow_graph():
        edges = [
            (0, 1, 5, 1),
            (1, 2, 3, 1),
            (2, 3, 2, 1)
        ]
        return edges, (0, 3)

    graphs = [
        ("equal_flow_graph.edges", equal_flow_graph()),
        ("impossible_flow_graph.edges", impossible_flow_graph())
    ]

    for filename, (edges, _) in graphs:
        path = os.path.join("Tests/BoundaryTests", filename)
        with open(path, 'w') as f:
            for u, v, cap, cost in edges:
                f.write(f"{u} {v} {cap} {cost}\n")


def generate_random_graphs(num_graphs=10, sizes=[50, 100], densities=[0.1, 0.2]):
    """Generate random graphs with varying characteristics."""
    os.makedirs("Tests/RandomGraphs", exist_ok=True)

    for size in sizes:
        for density in densities:
            for i in range(num_graphs):
                # Manually create random graph
                edges = []
                edge_count = int(size * size * density)

                for _ in range(edge_count):
                    u = random.randint(0, size - 1)
                    v = random.randint(0, size - 1)

                    # Avoid self-loops and duplicate edges
                    while u == v or any(edge[0] == u and edge[1] == v for edge in edges):
                        u = random.randint(0, size - 1)
                        v = random.randint(0, size - 1)

                    capacity = random.randint(1, 100)
                    cost = random.randint(1, 50)
                    edges.append((u, v, capacity, cost))

                filename = f"random_graph_n{size}_d{density}_{i}.edges"
                path = os.path.join("Tests/RandomGraphs", filename)

                with open(path, 'w') as f:
                    for u, v, cap, cost in edges:
                        f.write(f"{u} {v} {cap} {cost}\n")


def generate_stress_test_graphs(num_graphs=5):
    """Generate large graphs for stress testing."""
    os.makedirs("Tests/StressTests", exist_ok=True)

    for i in range(num_graphs):
        size = 500
        density = 0.1
        edges = []
        edge_count = int(size * size * density)

        for _ in range(edge_count):
            u = random.randint(0, size - 1)
            v = random.randint(0, size - 1)

            # Avoid self-loops and duplicate edges
            while u == v or any(edge[0] == u and edge[1] == v for edge in edges):
                u = random.randint(0, size - 1)
                v = random.randint(0, size - 1)

            capacity = random.randint(1, 100)
            cost = random.randint(1, 50)
            edges.append((u, v, capacity, cost))

        filename = f"stress_test_graph_{i}.edges"
        path = os.path.join("Tests/StressTests", filename)

        with open(path, 'w') as f:
            for u, v, cap, cost in edges:
                f.write(f"{u} {v} {cap} {cost}\n")


def generate_special_graphs():
    """Generate graphs with special topological properties."""
    os.makedirs("Tests/SpecialGraphs", exist_ok=True)

    # Disconnected Graph
    def disconnected_graph():
        edges = [
            # First component
            (0, 1, 10, 1),
            (1, 2, 5, 1),

            # Second component (no path between components)
            (3, 4, 15, 2),
            (4, 5, 7, 2)
        ]
        return edges, (0, 5)  # Will test algorithm's behavior with no path

    # Single Path Graph
    def single_path_graph():
        edges = [
            (0, 1, 5, 1),
            (1, 2, 5, 1),
            (2, 3, 5, 1)
        ]
        return edges, (0, 3)

    graphs = [
        ("disconnected_graph.edges", disconnected_graph()),
        ("single_path_graph.edges", single_path_graph())
    ]

    for filename, (edges, _) in graphs:
        path = os.path.join("Tests/SpecialGraphs", filename)
        with open(path, 'w') as f:
            for u, v, cap, cost in edges:
                f.write(f"{u} {v} {cap} {cost}\n")


def main():
    generate_small_graphs()
    generate_boundary_graphs()
    generate_random_graphs()
    generate_stress_test_graphs()
    generate_special_graphs()
    print("Test graph generation complete!")


if __name__ == "__main__":
    main()