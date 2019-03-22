from board import Board
from a_star import AStar
from ida_star import IDAStar
from heuristic import Heuristic
from bi_directional_a_star import BiDirAStar
from reinforcement_learning import ReinforcementLearning
from direction import Direction
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
    parser.add_argument('-t', default=25, help='Time limit')
    parser.add_argument('-a', default=2, help='Algorithm number')
    args = parser.parse_args()
    try:
        time_limit = int(args.t)
        if time_limit < 0:
            print("Input entered for time cannot be negative")
            exit(1)
    except ValueError:
        print("Input entered for time limit is not a number.")
        exit(1)
    try:
        algorithm = int(args.a)
        if algorithm > 3:
            print("Algorithm can be either 0 for A star, 1 for IDA star, 2 for bi-directional A star or 3"
                  " reinforcement learning")
            exit(1)
    except ValueError:
        print("Input entered for algorithm is not a number")
        exit(1)
    return time_limit, algorithm


def delete_existing_files():
    heuristics_num = len(Heuristic)
    for num in range(heuristics_num):
        file_num = num + 1
        if os.path.isfile("./output_h" + str(file_num) + ".txt"):
            os.remove("./output_h" + str(file_num) + ".txt")
        if os.path.isfile("./detailed_output_h" + str(file_num) + ".txt"):
            os.remove("./detailed_output_h" + str(file_num) + ".txt")


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
