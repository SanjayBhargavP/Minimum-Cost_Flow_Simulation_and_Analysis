# **Minimum-Cost Flow Simulation and Analysis**

This project implements and analyzes multiple algorithms for solving **maximum flow** and **minimum-cost flow** problems on directed graphs. It includes graph generation, algorithmic simulations, and performance evaluation.

---

## **Features**

1. **Graph Generation**:
   - Generates random directed graphs with configurable parameters: number of nodes, edge density, maximum capacity, and cost.
   - Saves graphs in edge-list format for easy reuse.

2. **Implemented Algorithms**:
- **Ford-Fulkerson**:
  - Finds the maximum flow using the Edmonds-Karp BFS-based method.
- **Successive Shortest Paths (SSP)**:
  - Iteratively augments the flow along shortest-cost paths.
- **Capacity Scaling (CS)**:
  - Focuses on augmenting high capacity paths greater than a threshold delta first to improve efficiency.
- **Successive Shortest Paths (SSP) with Capacity Scaling(SSPSC)**
  - Uses the shortest-cost paths from SSP and augments the flow by selecting capacity based on delta
- **Primal Dual**
  - The Primal-Dual Minimum Cost Flow Algorithm is an optimization technique designed to find the minimum-cost flow in a directed graph while satisfying flow constraints. 
  - It iteratively    adjusts primal (flow) and dual (potential) variables to ensure feasibility and optimality. Below is an overview of its functionality and workflow.

3. **Simulation**:
   - Processes multiple graph configurations and compares the performance of algorithms.
   - Outputs results, including flow values, costs, path metrics, and graph characteristics.

4. **Metrics Collection**:
   - Calculates graph properties such as the size of the largest connected component (LCC), in-degree and out-degree statistics, and graph density.

---

## **Directory Structure**

```
.
├── Graphs/                # Contains generated graphs (edge-list format)
├── Results/               # Simulation output files (flow and cost results)
├── main.py                # Main script for running simulations
├── utility.py             # Utility functions for graph loading, metrics, and I/O
├── source_sink_graph_generator.py # Random graph generation functions
```

---



### **How to Run**
1. Execute the main script:
   ```bash
   python main.py
   ```
---

## **Usage**

### **Graph Generation**
Graphs are generated using the `generate_sink_source_graph` function in `source_sink_graph_generator.py`. Customize parameters like:
- `n`: Number of nodes
- `r`: Edge density
- `upperCap`: Maximum edge capacity
- `upperCost`: Maximum edge cost

Example:
```python
from source_sink_graph_generator import generate_sink_source_graph

graph = generate_sink_source_graph(50, 0.2, 20, 100)
```

### **Run Simulations**
The main script (`main.py`) performs the following:
1. Generates graphs based on pre-defined parameter sets.
2. Runs algorithms (SSP, CS, SSCCP, PD) on each graph.
3. Saves results in the `Results/` directory.

Parameter sets are added in `main.py`:
```python
parameter_sets_simulation1 = [
    (100, 0.2, 8, 5),
    (200, 0.2, 8, 5),
]
```

### **Analyze Results**
Results are written to the below files:
- `simulation1_ford_fulkerson_results.txt`: Maximum flow metrics.
- `simulation1_algorithms_results.txt`: Minimum-cost flow for given parameters
- `simulation2_ford_fulkerson_results.txt`: Maximum flow metrics.
- `simulation2_algorithms_results.txt`: Minimum-cost flow results for denser graphs

Example file formats:
- **Maximum Flow Results**:
  ```
    Graph     	n    	r    	upperCap  	upperCost 	fmax      	|VLCC|    	∆out(LCC)   	∆in(LCC)    	k(LCC)     
    graph.txt 	N/A  	N/A  	N/A       	N/A       	1         	1         	97          	9           	9.0000    
    1         	100  	0.2  	8         	5         	3         	3         	99          	11          	14.0000  
  ```
- **Algorithm Results**:
  ```
  Algorithm    Graph   Flow   Cost   Paths   Mean Length   MPL
  SSP          1       45     100    10      3.5           0.7
  ```


### **Graph Metrics**
The project calculates the following metrics for each graph:
- **|VLCC|**: Number of nodes in the largest connected component.
- **∆out(LCC)**: Maximum out-degree in the LCC.
- **∆in(LCC)**: Maximum in-degree in the LCC.
- **k(LCC)**: Density of the LCC.

The algorithm calculates the following metrics for each graph:
- **Flow**: Maximum flow equal to demand.
- **Cost**: Cost of generating maximum flow.
- **Paths**: Number of augmented paths to generate maximum flow.
- **Mean Length**: Average length of augmented paths
- **Mean Propotional Length**: Average length of augmented paths as a fraction of longest acyclic paths from source to sink.
---



### **How to test your graph**

1. **Prepare Your Graph Files**:
   - Ensure your graph file is in **`.edge`** or **`.txt`** extentsion.
   - Place your file in any of the following folders:
     - `Graph/Simulation1`
     - `Graph/Simulation2`

2. **Set Parameters (Optional)**:
   - If you wish to specify parameters such as:
     - **n**: Number of nodes
     - **r**: A specific ratio or threshold
     - **upperCap**: Maximum capacity
     - **upperCost**: Maximum cost
   - Rename your file using the following naming convention:
     ```
     graph_1_n100_r0.2_cap8_cost5.edges
     ```
     Replace `100`, `0.2`, `8`, and `5` with your desired values for **n**, **r**, **upperCap**, and **upperCost**, respectively.
   - Example: `graph_1_n50_r0.1_cap10_cost2.edges`

3. **Run Without Parameters**:
   - If no specific parameters are required, simply name your file:
     ```
     graph.txt
     ```
     or
     ```
     graph.edge
     ```

---

### **Running the Simulation**

1. **Execute the Main Script**:
   - Run the following command in your terminal:
     ```bash
     python main.py
     ```
   - The script will process:
     - Your custom graph.
     - 8 additional randomly generated graphs.

2. **Output**:
   - Results will be generated in the output directory (or as specified in your script). These include processed graph metrics and visualizations.

