from action import Action
from direction import Direction
from orientation import Orientation
from a_star import AStar
import utils
import collections


class ReinforcementLearning:
    def __init__(self, board, data):
        self.board = board
        self.data = data
        self.actions = {}
        data.update_action_weights = True
        data.actions = self.actions
        self.solution = None
        self.data.actions = self.actions
        self.optimal_steps = self.data.min_cost_path.split(' ')[:-1]

    # Create all actions for current board.
    def initialize_actions(self):
        for car_name, car in self.board.cars.items():
            max_mov = 4
            if car.size == 3:
                max_mov = 3
            if car.orientation == Orientation.VERTICAL:
                for i in range(max_mov):
                    entry = car_name + utils.get_direction_initial(Direction.UP) + str(i + 1)
                    self.actions[entry] = Action(car, Direction.UP, i + 1)
                    entry = car_name + utils.get_direction_initial(Direction.DOWN) + str(i + 1)
                    self.actions[entry] = Action(car, Direction.DOWN, i + 1)
            else:
                for i in range(max_mov):
                    entry = car_name + utils.get_direction_initial(Direction.LEFT) + str(i + 1)
                    self.actions[entry] = Action(car, Direction.LEFT, i + 1)
                    entry = car_name + utils.get_direction_initial(Direction.RIGHT) + str(i + 1)
                    self.actions[entry] = Action(car, Direction.RIGHT, i + 1)

    def update_actions_depth(self):
        steps = self.data.min_cost_path.split(' ')[:-1]
        for i, step in enumerate(steps):
            self.actions[step].usage_depth.append(i + 1)

    def is_solution_optimal(self):
        if self.solution is None:
            return False
        if self.solution == self.data.min_cost_path:
            return True
        return False

    # Main function that solves the board and updates the actions weights
    def solve_board(self):
        while not self.is_solution_optimal():
            # print()
            # print()
            # print("Run")
            algorithm = AStar(self.board, self.data)
            self.solution = algorithm.solve_board()
            # print(self.solution)
            self.update_weights()
        self.write_output()
        return self.solution

    def update_weights(self):
        steps = self.solution.split(' ')[:-1]
        for i, step in enumerate(steps):
            # print(step + " " + str(self.data.actions[step].weight))
            if i < len(self.optimal_steps) and self.optimal_steps[i] == step:
                self.data.actions[step].weight = self.data.actions[step].weight - 1
            else:
                self.data.actions[step].weight = self.data.actions[step].weight + 1
            # print("Updated to " + step + " " + str(self.data.actions[step].weight))

    # Create the output file "reinforcement learning.txt"
    def write_output(self):
        h_file = self.data.heuristic.value
        with open("reinforcement_learning_h" + str(h_file) + ".txt", 'a') as file:
            file.write("=======================================================\n")
            file.write("Solution and weight for board number " + str(self.data.board_num + 1) + "\n")
            file.write("Solution: " + self.solution + "\n")
            file.write("Weights: \n")
            for action_name, action in self.actions.items():
                output_str = action.car.name
                if action.step.direction == Direction.UP:
                    output_str = output_str + " Up"
                elif action.step.direction == Direction.DOWN:
                    output_str = output_str + " Down"
                elif action.step.direction == Direction.RIGHT:
                    output_str = output_str + " Right"
                else:
                    output_str = output_str + " Left"
                output_str = output_str + " " + str(action.step.amount) + ":  " + str(action.weight)
                file.write("    " + output_str + "\n")
            file.close()
