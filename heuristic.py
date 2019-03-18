from enum import Enum


class Heuristic(Enum):
    BLOCKING_CARS = 0
    BLOCKING_CARS_MOVE_DISTANCE = 1
    BLOCKED_BLOCKING_CARS_MOVE_DISTANCE = 2
