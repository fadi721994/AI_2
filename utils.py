from board import Board
from a_star import AStar
from ida_star import IDAStar
from heuristic import Heuristic
from bi_directional_a_star import BiDirAStar
from reinforcement_learning import ReinforcementLearning
from direction import Direction
from indicator import Indicator
from step import Step
import argparse
import os


# Read the boards from rh.txt file and provide a list of object "board"
def parse_list_of_boards(file="./problems.txt"):
    list_of_boards = []
    with open(file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            board = Board(line, None)
            list_of_boards.append(board)
    return list_of_boards


# Get the algorithm object that should run
def get_algorithm(algorithm_num, board, data):
    if algorithm_num == 0:
        return AStar(board, data)
    elif algorithm_num == 1:
        return IDAStar(board, data)
    elif algorithm_num == 2:
        return BiDirAStar(board, data)
    elif algorithm_num == 3:
        return ReinforcementLearning(board, data)
    else:
        print("Algorithm cannot be: " + str(algorithm_num))
        exit(1)


# Count the steps of a solution.
def count_steps(sol):
    step_sum = 0
    for c in sol:
        if c.isdigit():
            step_sum += int(c)
    return step_sum


# Check if a solution is optimal. 1 means optimal, 0 means same as suggested, -1 means not optimal.
def validate_solution(real_sol, my_sol):
    real_steps = count_steps(real_sol)
    my_steps = count_steps(my_sol)
    if real_steps > my_steps:
        return 1
    elif real_steps < my_steps:
        return -1
    else:
        return 0


# Read suggested solutions.
def read_solutions():
    solutions = []
    with open("given_solutions.txt", 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            solutions.append(line)
    return solutions


def read_min_cost_paths():
    solutions = []
    with open("minimum_cost_path.txt", 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            solutions.append(line)
    return solutions


# Calculate average of a list.
def calc_avg(data_list):
    return str(sum(data_list)/len(data_list))


def parse_cmd():
    parser = argparse.ArgumentParser()
    parser.add_argument('-T', default=10, help='Time limit')
    parser.add_argument('-A', default=0, help='Algorithm number')
    parser.add_argument('-I', default=0, help='Indicator number')
    parser.add_argument('-H', default=0, help='Heuristic number')
    parser.add_argument('-D', default=0, help='Use difficulty as input')
    args = parser.parse_args()
    try:
        time_limit = int(args.T)
        if time_limit < 0:
            print("Input entered for time cannot be negative")
            exit(1)
    except ValueError:
        print("Input entered for time limit is not a number.")
        exit(1)
    try:
        algorithm = int(args.A)
        if algorithm > 3:
            print("Algorithm can be either 0 for A star, 1 for IDA star, 2 for bi-directional A star or 3"
                  " reinforcement learning")
            exit(1)
    except ValueError:
        print("Input entered for algorithm is not a number")
        exit(1)
    try:
        indicator = int(args.I)
        if indicator > 3:
            print("Indicator can be either 0 for 'No indicator', 1 for 'Board freedom degree', "
                  "2 for 'Overall free cars' or 3 for both 1 and 2."
                  " reinforcement learning")
            exit(1)
    except ValueError:
        print("Input entered for indicator is not a number")
        exit(1)
    try:
        heuristic_num = int(args.H)
        if heuristic_num > 3:
            print("Heuristic can be either 0 for 'Blocking cars', 1 for 'Blocked blocking cars', 2 for 'Blocking cars"
                  " and their move distance' or 3 for 'Blocked blocking cars and their move distance'.")
            exit(1)
    except ValueError:
        print("Input entered for heuristic is not a number")
        exit(1)
    try:
        difficulty = int(args.D)
        if difficulty > 1:
            print("'Use difficulty' can be either 0 for False or 1 for True.")
            exit(1)
    except ValueError:
        print("Input entered for difficulty is not a number")
        exit(1)
    return time_limit, algorithm, indicator, heuristic_num, difficulty


def delete_existing_files(heuristic):
    file_num = heuristic.value + 1
    if os.path.isfile("./output_h" + str(file_num) + ".txt"):
        os.remove("./output_h" + str(file_num) + ".txt")
    if os.path.isfile("./detailed_output_h" + str(file_num) + ".txt"):
        os.remove("./detailed_output_h" + str(file_num) + ".txt")
    if os.path.isfile("./reinforcement_learning_h" + str(file_num) + ".txt"):
        os.remove("./reinforcement_learning_h" + str(file_num) + ".txt")


def from_steps_str_to_object(steps):
    steps_strs = steps.split(' ')[:-1]
    steps_objs = []
    for step in steps_strs:
        if step[1] == 'R':
            direction = Direction.RIGHT
        elif step[1] == 'L':
            direction = Direction.LEFT
        elif step[1] == 'D':
            direction = Direction.DOWN
        else:
            direction = Direction.UP
        step_obj = Step(step[0], direction, int(step[2]))
        steps_objs.append(step_obj)
    return steps_objs


def get_indicators_list(indicator_num):
    if indicator_num == 0:
        return []
    elif indicator_num == 1:
        return [Indicator.BOARD_FREEDOM_DEGREE]
    elif indicator_num == 2:
        return [Indicator.OVERALL_FREE_CARS]
    elif indicator_num == 3:
        return [Indicator.BOARD_FREEDOM_DEGREE, Indicator.OVERALL_FREE_CARS]
    return []


def get_heuristic_list(heuristic_num):
    if heuristic_num == 0:
        return [Heuristic.BLOCKING_CARS]
    elif heuristic_num == 1:
        return [Heuristic.BLOCKED_BLOCKING_CARS]
    elif heuristic_num == 2:
        return [Heuristic.BLOCKING_CARS_MOVE_DISTANCE]
    elif heuristic_num == 3:
        return [Heuristic.BLOCKED_BLOCKING_CARS_MOVE_DISTANCE]
    return [Heuristic.BLOCKING_CARS]
