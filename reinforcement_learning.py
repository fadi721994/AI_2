from action import Action
from direction import Direction
from orientation import Orientation
from a_star import AStar
import utils


class ReinforcementLearning:
    def __init__(self, board, data):
        self.board = board
        self.actions = {}
        self.initialize_actions()
        data.update_action_weights = True
        data.actions = self.actions
        self.data = data

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
                    entry = car_name + utils.get_direction_initial(Direction.UP) + str(i + 1)
                    self.actions[entry] = Action(car, Direction.DOWN, i + 1)
            else:
                for i in range(max_mov):
                    entry = car_name + utils.get_direction_initial(Direction.LEFT) + str(i + 1)
                    self.actions[entry] = Action(car, Direction.LEFT, i + 1)
                    entry = car_name + utils.get_direction_initial(Direction.RIGHT) + str(i + 1)
                    self.actions[entry] = Action(car, Direction.RIGHT, i + 1)

    # Main function that solves the board and updates the actions weights
    def solve_board(self):
        algorithm = AStar(self.board, self.data)
        solution = algorithm.solve_board()
        self.write_output(solution)
        return solution

    # Create the output file "reinforcement learning.txt"
    def write_output(self, solution):
        h_file = self.data.heuristic.value + 1
        with open("reinforcement_learning_h" + str(h_file) + ".txt", 'a') as file:
            file.write("=======================================================\n")
            file.write("Solution and weight for board number " + str(self.data.board_num + 1) + "\n")
            file.write("Solution: " + solution + "\n")
            file.write("Weights: \n")
            for action in self.actions:
                output_str = action.car.name
                if action.direction == Direction.UP:
                    output_str = output_str + " Up"
                elif action.direction == Direction.DOWN:
                    output_str = output_str + " Down"
                elif action.direction == Direction.RIGHT:
                    output_str = output_str + " Right"
                else:
                    output_str = output_str + " Left"
                output_str = output_str + ": " + str(action.weight)
                file.write("    " + output_str + "\n")
            file.close()
