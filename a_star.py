from state import State
from priority_queue import PriorityQueue
import math


class AStar:
    def __init__(self, board, data):
        self.board = board
        self.data = data

    # The main function. Used to solve the board.
    def solve_board(self, f_limit=math.inf):
        steps = 0
        root_state = State(self.board, None, None, 0, steps, 0)
        f_values = dict()
        f = root_state.calculate_f(self.data)
        f_values[hash(self.board.grid_to_str())] = f

        open_list = PriorityQueue()
        closed_list = set()

        # Step 1: Put the start node on a list called OPEN of unexpanded nodes.
        # Calculate f(s) and associate its value with node s.
        open_list.push(root_state)
        # Step 2: If OPEN is empty, exit with failure, no solution exists.
        while open_list.is_not_empty():
            # Step 3: Select from OPEN a node i at which f is minimum. If several nodes qualify,
            # choose a goal node if there is one, otherwise choose among them arbitrarily.
            state = open_list.pop().state

            # Step 4: Remove node i from OPEN and place it on a list called CLOSED, of expanded nodes.
            self.data.scanned_nodes = self.data.scanned_nodes + 1
            closed_list.add(hash(state.board.grid_to_str()))

            # Step 5: If i is a goal node, exit with success; a solution has been found.
            if state.depth >= self.data.difficulty_depth_min:
                if state.goal_state():
                    solution_steps = state.get_solution_steps()
                    solution_str = state.create_solution_string(solution_steps)
                    self.data.finalize(solution_str, len(solution_steps), open_list)
                    return solution_str

            # Step 6: Expand node i, creating nodes for all of its successors. For every successor node j of i:
            # Step 6.1: Calculate f(j)

            if state.depth <= self.data.difficulty_depth_limit:
                expanded_states = state.expand_state(self.data)
                for expanded_state in expanded_states:
                    # Step 6.2: If j is neither in OPEN nor in CLOSED, then add it to OPEN with its f value.
                    # Attach a pointer from j back to its predecessor i
                    # Also, for IDA star, if the f value of the state is larger that the limit, don't add it.
                    if expanded_state.f_value > f_limit:
                        continue
                    if hash(expanded_state.board.grid_to_str()) not in f_values:
                        open_list.push(expanded_state)
                        f_values[hash(expanded_state.board.grid_to_str())] = expanded_state.f_value
                    else:
                        # Step 6.3: If j was already on either OPEN or CLOSED, compare the f value just calculated for j
                        # with the value previously associated with the node.
                        if expanded_state.f_value < f_values[hash(expanded_state.board.grid_to_str())]:
                            f_values[hash(expanded_state.board.grid_to_str())] = expanded_state.f_value
                            # Step 6.3.1: Substitute it for the old value.
                            if expanded_state.is_expansion_in_closed_list(closed_list):
                                # Step 6.3.2: Point j back to i instead of to its previously found predecessor.
                                # Step 6.3.3: If node j was on the CLOSED list, move it back to OPEN
                                open_list.push(expanded_state)
                                expanded_state.remove_state(closed_list)
        if f_limit == math.inf:
            self.data.finalize("FAILED", 0, open_list)
        return None
