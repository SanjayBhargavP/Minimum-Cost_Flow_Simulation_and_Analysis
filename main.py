import os
from algo_helper import GraphHelper
from capacity_scaling import capacity_scaling_with_metrics
from source_sink_graph_generator import generate_source_sink_networks
# from successive_shortest_paths import successive_shortest_paths_with_metrics

class Main:
    """Main class to handle graph loading and execute the Capacity Scaling Algorithm."""

    def __init__(self, filename, demand):
        """
        Initialize the Main class with a file containing graph data and the desired demand.

        :param filename: Path to the file containing graph data.
        :param demand: Flow demand for the capacity scaling algorithm.
        """
        self.filename = filename
        self.demand = demand
        self.graph = None
        self.source = None
        self.sink = None

    def load_graph(self):
        """Loads the graph, source, and sink from the file using the GraphHelper."""
        print(f"Loaded Graph: {os.path.basename(self.filename)}")
        self.graph, self.source, self.sink = GraphHelper.load_graph_from_file(self.filename)
        print(f"Source: {self.source}, Sink: {self.sink}")

    def run_capacity_scaling(self):
        """Executes the Capacity Scaling Algorithm with metrics."""
        print(f"Running Capacity Scaling Algorithm with demand = {self.demand}...")
        flow, cost, num_paths, mean_length, mean_proportional_length = capacity_scaling_with_metrics(
            self.graph, self.source, self.sink, self.demand
        )
        self.print_results(flow, cost, num_paths, mean_length, mean_proportional_length )

    def run_successive_shortest_paths(self):
        """Executes the Successive Shortest Paths Algorithm with metrics."""
        print(f"Running Capacity Scaling Algorithm with demand = {self.demand}...")
        flow, cost, num_paths, mean_length, mean_proportional_length = successive_shortest_paths_with_metrics(
            self.graph, self.source, self.sink, self.demand
        )
        print("\n=== Capacity Scaling Results ===")
        self.print_results(flow, cost, num_paths, mean_length, mean_proportional_length )

    def print_results(self,flow, cost, num_paths, mean_length, mean_proportional_length ):
        if flow is not None:
            print(f"Total Flow: {flow}")
            print(f"Total Cost: {cost}")
            print(f"Number of Augmenting Paths: {num_paths}")
            print(f"Mean Length of Paths: {mean_length}")
            print(f"Mean Proportional Length: {mean_proportional_length}")
        else:
            print("\nFailed to meet the flow demand.")
        print("=========================")

        

    @staticmethod
    def run(filename, demand):
        """
        Static method to run the Main workflow.

        :param filename: Path to the file containing graph data.
        :param demand: Flow demand for the capacity scaling algorithm.
        """
        main = Main(filename, demand)
        main.load_graph()
        main.run_capacity_scaling()
        # main.run_successive_shortest_paths()


# Example Usage
if __name__ == "__main__":

    current_folder = os.getcwd()
    flow_demand=5

    # Loop through all files in the current folder
    for filename in os.listdir(current_folder):
    # Get the full file path
        file_path = os.path.join(current_folder, filename)

        # Check if it's a file and has the '.edges' extension
        if os.path.isfile(file_path) and filename.endswith('.edges'):
            # Run the algorithm on the .edges file
            Main.run(file_path, flow_demand)

    
