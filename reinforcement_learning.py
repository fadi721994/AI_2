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
        sol = algorithm.solve_board()
        print(sol)
        for action in self.actions:
            print("Car " + action.car.name + " Direction " + str(action.direction) + " Weight " + str(action.weight))