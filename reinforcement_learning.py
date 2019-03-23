from action import Action
from direction import Direction
from orientation import Orientation
from a_star import AStar


class ReinforcementLearning:
    def __init__(self, board, data):
        self.board = board
        self.actions = []
        self.initialize_actions()
        data.update_action_weights = True
        data.actions = self.actions
        self.data = data

    def initialize_actions(self):
        for car_name, car in self.board.cars.items():
            if car.orientation == Orientation.VERTICAL:
                self.actions.append(Action(car, Direction.UP))
                self.actions.append(Action(car, Direction.DOWN))
            else:
                self.actions.append(Action(car, Direction.RIGHT))
                self.actions.append(Action(car, Direction.LEFT))

    def solve_board(self):
        algorithm = AStar(self.board, self.data)
        solution = algorithm.solve_board()
        self.write_output(solution)
        return solution

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
