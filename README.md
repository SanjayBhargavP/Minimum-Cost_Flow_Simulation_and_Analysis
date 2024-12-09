# Minimum Cost Flow Algorithms Simulation

## Project Overview
This project implements and compares several minimum cost flow algorithms, including:
- Successive Shortest Paths (SSP)
- Capacity Scaling (CS)
- Successive Shortest Paths with Capacity Scaling (SSPCS)
- Primal-Dual Algorithm (PD)

The simulation generates random graphs and runs these algorithms to compare their performance.

## Prerequisites
- Python 3.8 or higher
- Recommended: Virtual environment
```

## Project Structure
- `main.py`: Main simulation script
- `graph.py`: Graph and Edge class implementations
- `capacity_scaling.py`: Capacity Scaling algorithm
- `successive_shortest_paths.py`: Successive Shortest Paths algorithm
- `primal_dual_algorithm.py`: Primal-Dual algorithm
- `source_sink_graph_generator.py`: Graph generation utilities
- `utility.py`: Utility functions for graph operations

## Running the Simulation

### Generate Graphs and Run Simulation
```bash
python main.py
```

### Expected Outputs
- Graph files will be generated in `./Graphs/Simulation1` and `./Graphs/Simulation2`
- Results will be saved in the `./Results` directory:
  - `simulation_one_ford_fulkerson_results.txt`
  - `simulation_one_algorithms_results.txt`
  - `simulation_two_ford_fulkerson_results.txt`
  - `simulation_two_algorithms_results.txt`

## Simulation Parameters
The simulation uses two sets of parameter configurations:
- Simulation 1: Graphs with 100-200 nodes, density 0.2-0.3, max capacities 8-64
- Simulation 2: Graphs with 150-250 nodes, density 0.25-0.35, max capacities 16-128

## Troubleshooting
- Ensure you're using Python 3.8+
- Check that all Python files are in the same directory
- Verify that you have write permissions in the project directory

## Understanding the Results
The results files contain:
- Graph properties
- Maximum flow
- Cost of flow
- Number of augmenting paths
- Mean path length
- Mean proportional path length