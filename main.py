from utils import *
from data import Data
from heuristic import Heuristic
from indicator import Indicator
from overall_data import OverallData
import cProfile, pstats, io


def main():
    time_limit, algorithm_num = parse_cmd()
    delete_existing_files()
    heuristics = [Heuristic.BLOCKING_CARS]
    indicators = []
    use_difficulty = True
    list_of_boards = parse_list_of_boards()
    list_of_solutions = read_solutions()
    minimum_cost_paths = read_min_cost_paths()
    for j, heuristic in enumerate(heuristics):
        heuristic_data = OverallData()
        print("Running with heuristic function " + str(j + 1))
        for i, board in enumerate(list_of_boards):
            print("Solving board number " + str(i + 1))
            data = Data(i, heuristic, time_limit, indicators, list_of_solutions[i], minimum_cost_paths[i],
                        use_difficulty)
            algorithm = get_algorithm(algorithm_num, board, data)
            solution = algorithm.solve_board()
            data.add_optimality(solution, list_of_solutions[i])
            if solution is not None:
                heuristic_data.add_data(data)
        heuristic_data.print_avgs()
    print("Finished")


# pr = cProfile.Profile()
# pr.enable()
main()
# pr.disable()
# s = io.StringIO()
# sortby = 'cumulative'
# ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
# ps.print_stats()
# print(s.getvalue())
