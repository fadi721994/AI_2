import math
import time
from bidirectional_direction import BidirectionalDirection
from difficulty import Difficulty
from step import Step
import utils


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
        self.actions = {}

    # The limit of the difficulty that the solution cannot be longer than.
    def get_difficulty_depth_limit(self):
        if self.difficulty == Difficulty.BEGINNER:
            return 20
        elif self.difficulty == Difficulty.INTERMEDIATE:
            return 30
        elif self.difficulty == Difficulty.ADVANCED:
            return 40
        else:
            return 60

    # The minimum length of solution for a specific difficulty.
    def get_difficulty_depth_min(self):
        if self.difficulty == Difficulty.BEGINNER:
            return 5
        elif self.difficulty == Difficulty.INTERMEDIATE:
            return 7
        elif self.difficulty == Difficulty.ADVANCED:
            return 9
        else:
            return 30

    # Get difficulty according to board number.
    def get_difficulty(self):
        if self.board_num < 10:
            return Difficulty.BEGINNER
        elif self.board_num < 20:
            return Difficulty.INTERMEDIATE
        elif self.board_num < 30:
            return Difficulty.ADVANCED
        return Difficulty.EXPERT

    def get_penetrance(self):
        return self.solution_depth / self.scanned_nodes

    def get_ebf(self):
        return self.scanned_nodes ** (1 / self.solution_depth)

    # Finalize the data and write to the output files.
    def finalize(self, solution, sol_depth):
        self.end_time = time.time()
        self.run_time = self.end_time - self.start_time
        self.solution = solution
        self.solution_depth = sol_depth
        self.heuristic_avg = sum(self.heuristic_values) / len(self.heuristic_values)
        penetrance = self.get_penetrance()
        if solution != "FAILED":
            ebf = self.get_ebf()
            self.avg_depth = sum(self.depths) / len(self.depths)
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
            file.write("Minimum tree depth: " + str(self.min_depth) + "\n")
            file.write("Average tree depth: " + str(self.avg_depth) + "\n")
            file.write("Maximum tree depth: " + str(self.max_depth) + "\n")

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

    def get_action_weight(self, solution):
        steps = solution.split(' ')
        overall = 0
        for i, step in enumerate(steps):
            solution_str = utils.get_solution_string(i, steps)
            if solution_str in self.actions:
                overall = overall + self.actions[solution_str]
        return overall

    def get_depth_best_moves(self, depth, cars):
        if depth not in self.actions:
            self.actions[depth] = utils.initialize_actions(cars)
        steps_hash = self.actions[depth]
        min_step_list = []
        min_value = int(min(steps_hash.items(), key=lambda x: x[1])[1])
        for key, value in steps_hash.items():
            if value == min_value:
                min_step_list.append(key)
        valid_steps = []
        for step in min_step_list:
            valid_steps.append(step)
        return valid_steps
