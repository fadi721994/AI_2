from enum import Enum


class Heuristic(Enum):
    X_BLOCKING_CARS = 0
    X_BLOCKING_CARS_FINAL_POSITION_DISTANCE = 1
    X_BLOCKING_CARS_BLOCKING_CARS = 2
    X_BLOCKING_CARS_FINAL_POSITION_DISTANCE_BLOCKING_CARS = 3
    REINFORCEMENT_LEARNING = 4
