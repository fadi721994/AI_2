from utils import calc_avg


class OverallData:
    def __init__(self, heuristic):
        self.solution_depth = []
        self.scanned_nodes = []
        self.penetrance = []
        self.run_time = []
        self.heuristic_avg = []
        self.ebf = []
        self.min_tree_depth = []
        self.max_tree_depth = []
        self.avg_tree_depth = []
        self.heuristic = heuristic

    # Add data for all the relevant fields from the run.
    def add_data(self, data):
        self.solution_depth.append(data.solution_depth)
        self.scanned_nodes.append(data.scanned_nodes)
        self.penetrance.append(data.get_penetrance())
        self.run_time.append(data.run_time)
        self.heuristic_avg.append(data.heuristic_avg)
        self.ebf.append(data.get_ebf())
        self.min_tree_depth.append(data.min_depth)
        self.max_tree_depth.append(data.max_depth)
        self.avg_tree_depth.append(data.avg_depth)

    # Add the overall heuristic run averages to the details output files.
    def print_avgs(self):
        h_file = self.heuristic.value
        with open("detailed_output_h" + str(h_file) + ".txt", 'a') as file:
            file.write("Overall summary\n")
            file.write("---------------------------------------------------------------\n")
            file.write("Solution depth avg: " + calc_avg(self.solution_depth) + "\n")
            file.write("Scanned nodes avg: " + calc_avg(self.scanned_nodes) + "\n")
            file.write("Penetrance avg: " + calc_avg(self.penetrance) + "\n")
            file.write("Run time avg: " + calc_avg(self.run_time) + "\n")
            file.write("Heuristic overall avg: " + calc_avg(self.heuristic_avg) + "\n")
            file.write("EBF avg: " + calc_avg(self.ebf) + "\n")
            file.write("Min tree depth avg: " + calc_avg(self.min_tree_depth) + "\n")
            file.write("Max tree depth avg: " + calc_avg(self.max_tree_depth) + "\n")
            file.write("Overall tree depth avg: " + calc_avg(self.avg_tree_depth) + "\n")
            file.write("---------------------------------------------------------------\n")
