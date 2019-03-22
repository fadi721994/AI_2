from action import Action
from direction import Direction
from orientation import Orientation


class ReinforcementLearning:
    def __init__(self, board, data):
        self.board = board
        self.data = data
        self.actions = []
        self.initialize_actions()

    def initialize_actions(self):
        for car_name, car in self.board.cars.items():
            if car.orientation == Orientation.VERTICAL:
                self.actions.append(Action(car, Direction.UP))
                self.actions.append(Action(car, Direction.DOWN))
            else:
                self.actions.append(Action(car, Direction.RIGHT))
                self.actions.append(Action(car, Direction.LEFT))

    def solve_board(self):
        for action in self.actions:
            print("Action " + action.car.name + " Direction " + str(action.direction))
