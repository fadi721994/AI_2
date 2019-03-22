from a_star import AStar
from state import State


class IDAStar:
    def __init__(self, board, data):
        self.board = board
        self.data = data
        self.expanded_nodes = dict()

    # The main function. Used to solve the board.
    def solve_board(self):
        a_star = AStar(self.board, self.data)
        root_state = State(self.board, None, None, 0, 0, 0)
        f_limit = root_state.calculate_f(self.data)
        while True:
            solution_str = a_star.solve_board(f_limit)
            if solution_str is not None:
                return solution_str
            f_limit = f_limit + 2
        return None

