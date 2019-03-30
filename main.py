from utils import *
from data import Data
from indicator import Indicator
from overall_data import OverallData
import cProfile, pstats, io
from heuristic import Heuristic


def main():
    time_limit, algorithm_num, indicator_num, heuristic_num, difficulty = parse_cmd()
    heuristics = get_heuristic_list(heuristic_num, algorithm_num)
    indicators = get_indicators_list(indicator_num)
    use_difficulty = difficulty == 1
    list_of_boards = parse_list_of_boards()
    list_of_solutions = read_solutions()
    minimum_cost_paths = read_min_cost_paths()
    for heuristic in heuristics:
        delete_existing_files(heuristic)
        heuristic_data = OverallData(heuristic)
        print("Running with heuristic function " + str(heuristic.value))
        for i, board in enumerate(list_of_boards):
            print("Solving board number " + str(i + 1))
            data = Data(i, heuristic, time_limit, indicators, list_of_solutions[i], minimum_cost_paths[i],
                        use_difficulty)
            algorithm = get_algorithm(algorithm_num, board, data)
            solution = algorithm.solve_board()
            data.add_optimality(solution, list_of_solutions[i])
            if solution is not None and heuristic != Heuristic.REINFORCEMENT_LEARNING:
                heuristic_data.add_data(data)
        if heuristic != Heuristic.REINFORCEMENT_LEARNING:
            heuristic_data.print_avgs()
    print("Finished")


pr = cProfile.Profile()
pr.enable()
main()
pr.disable()
s = io.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())
