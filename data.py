import math
import time
import utils
from bidirectional_direction import BidirectionalDirection
from difficulty import Difficulty


class Data:
    def __init__(self, board_num, heuristic, time_limit, indicators, given_solution, min_cost, use_difficulty=False):
        self.board_num = board_num
        self.min_cost_path = min_cost
        self.min_cost_path_steps = utils.from_steps_str_to_object(self.min_cost_path)
        self.difficulty = self.get_difficulty()
        self.use_difficulty = use_difficulty
        if self.use_difficulty:
            self.difficulty_depth_limit = self.get_difficulty_depth_limit()
            self.difficulty_depth_min = self.get_difficulty_depth_min()
        else:
            self.difficulty_depth_limit = math.inf
            self.difficulty_depth_min = -math.inf
        self.heuristic = heuristic
        self.indicators = indicators
        self.solution = ''
        self.scanned_nodes = 0
        self.solution_depth = 0
        self.max_depth = 0
        self.min_depth = math.inf
        self.depths = []
        self.avg_depth = 0
        self.start_time = time.time()
        self.end_time = 0
        self.run_time = 0
        self.heuristic_values = []
        self.heuristic_avg = 0
        self.time_limit = time_limit
        self.optimal = 0
        self.given_solution = given_solution
        self.bidirectional_direction = BidirectionalDirection.NONE
        self.goal_board = None
        self.update_action_weights = False
        self.actions = []

    def get_difficulty_depth_limit(self):
        if self.difficulty == Difficulty.BEGINNER:
            return 20
        elif self.difficulty == Difficulty.INTERMEDIATE:
            return 30
        elif self.difficulty == Difficulty.ADVANCED:
            return 40
        else:
            return 60

    def get_difficulty_depth_min(self):
        if self.difficulty == Difficulty.BEGINNER:
            return 6
        elif self.difficulty == Difficulty.INTERMEDIATE:
            return 9
        elif self.difficulty == Difficulty.ADVANCED:
            return 19
        else:
            return 35

    def get_difficulty(self):
        if self.board_num < 10:
            return Difficulty.BEGINNER
        elif self.board_num < 20:
            return Difficulty.INTERMEDIATE
        elif self.board_num < 30:
            return Difficulty.ADVANCED
        return Difficulty.EXPERT

    # Given the open list, find the tree depths data, minimum, maximum and average.
    def find_tree_depth_data(self, open_list):
        for entry in open_list.queue:
            state = entry.state
            self.depths.append(state.depth)
        self.min_depth = min(self.depths)
        self.max_depth = max(self.depths)
        self.avg_depth = sum(self.depths)/len(self.depths)

    def get_penetrance(self):
        return self.solution_depth / self.scanned_nodes

    def get_ebf(self):
        return self.scanned_nodes ** (1 / self.solution_depth)

    # Finalize the data and write to the output files.
    def finalize(self, solution, sol_depth, open_list=None):
        self.end_time = time.time()
        self.run_time = self.end_time - self.start_time
        self.solution = solution
        self.solution_depth = sol_depth
        self.heuristic_avg = sum(self.heuristic_values) / len(self.heuristic_values)
        penetrance = self.get_penetrance()
        if open_list is not None and solution != "FAILED":
            ebf = self.get_ebf()
            self.find_tree_depth_data(open_list)
        else:
            ebf = 0
            self.solution = "FAILED"
        if self.run_time > self.time_limit:
            self.solution = "FAILED"

        h_file = self.heuristic.value
        with open("output_h" + str(h_file) + ".txt", 'a') as file:
            file.write(self.solution + "\n")
        with open("detailed_output_h" + str(h_file) + ".txt", 'a') as file:
            file.write("Board number " + str(self.board_num + 1) + "\n")
            file.write("---------------------------------------------------------------\n")
            file.write("Solution: " + self.solution + "\n")
            file.write("Solution depth: " + str(self.solution_depth) + "\n")
            file.write("Scanned nodes: " + str(self.scanned_nodes) + "\n")
            file.write("Penetrance: " + str(penetrance) + "\n")
            file.write("Run time: " + str(self.run_time) + "\n")
            file.write("Heuristic function average: " + str(self.heuristic_avg) + "\n")
            file.write("EBF: " + str(ebf) + "\n")
            if open_list is not None:
                file.write("Minimum tree depth: " + str(self.min_depth + 1) + "\n")
                file.write("Average tree depth: " + str(self.avg_depth + 1) + "\n")
                file.write("Maximum tree depth: " + str(self.max_depth + 1) + "\n")

    # Append to the data detailed output file whether the solution is optimal or not.
    def add_optimality(self, solution, suggested_solution):
        opt_str = ''
        if solution is None:
            opt_str = 'Failed to find solution'
        else:
            self.optimal = utils.validate_solution(suggested_solution, solution)
            if self.optimal == 1:
                opt_str = 'Solution has less steps than the suggested solution'
            elif self.optimal == 0:
                opt_str = 'Solution has the same amount of steps as the suggested solution'
            elif self.optimal == -1:
                opt_str = 'Solution has more steps than the suggested solution'
        h_file = self.heuristic.value
        with open("detailed_output_h" + str(h_file) + ".txt", 'a') as file:
            file.write(opt_str + "\n")
            file.write("---------------------------------------------------------------\n\n\n")

    def reinforcement_learning(self, state):
        step = state.step_taken
        if step is None:
            return
        action = self.get_action(step)
        if self.is_action_in_sol_path(action):
            action.weight = action.weight - 1
        else:
            action.weight = action.weight + 1

    def is_action_in_sol_path(self, action):
        for step in self.min_cost_path_steps:
            if step.direction == action.direction and step.car_name == action.car.name:
                return True
        return False

    def get_action(self, step):
        for action in self.actions:
            if action.car.name == step.car_name and action.direction == step.direction:
                return action
