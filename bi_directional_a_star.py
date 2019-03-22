from state import State
from bidirectional_direction import BidirectionalDirection
from priority_queue import PriorityQueue
from data import Data


class BiDirAStar:
    def __init__(self, board, data):
        self.board = board
        self.data = data

        self.forward_begin_state = State(self.board, None, None, 0, 0, 0)
        self.forward_data = Data(data.board_num, data.heuristic, data.time_limit, data.indicators, data.given_solution)
        self.forward_data.bidirectional_direction = BidirectionalDirection.FORWARD
        self.forward_f_values = dict()
        self.forward_open_list = PriorityQueue()
        self.forward_closed_list = set()

        state = self.forward_begin_state.run_steps_on_board(data, False, False)
        self.backward_begin_state = State(state.board, None, None, 0, 0, 0)
        self.backward_data = Data(data.board_num, data.heuristic, data.time_limit, data.indicators, data.given_solution)
        self.backward_data.bidirectional_direction = BidirectionalDirection.BACKWARD
        self.backward_f_values = dict()
        self.backward_open_list = PriorityQueue()
        self.backward_closed_list = set()

        self.forward_data.goal_board = self.backward_begin_state.board
        self.backward_data.goal_board = self.forward_begin_state.board

        f = self.forward_begin_state.calculate_f(self.forward_data)
        self.forward_f_values[hash(self.forward_begin_state.board.grid_to_str())] = f
        self.forward_open_list.push(self.forward_begin_state)
        f = self.backward_begin_state.calculate_f(self.backward_data)
        self.backward_f_values[hash(self.backward_begin_state.board.grid_to_str())] = f
        self.backward_open_list.push(self.backward_begin_state)

    def solve_board(self):
        while self.forward_open_list.is_not_empty() and self.backward_open_list.is_not_empty():
            forward_state = self.forward_step()
            if forward_state is not None:
                state = self.get_backward_state(forward_state)
                return self.get_solution(forward_state, state)
            backward_state = self.backward_step()
            if backward_state is not None:
                state = self.get_forward_state(backward_state)
                return self.get_solution(state, backward_state)
        return None

    def get_solution(self, forward_state, backward_state):
        forward_steps = forward_state.get_solution_steps()
        backward_steps = list(reversed(backward_state.get_solution_steps()))
        print("Forward " + str(len(forward_steps)))
        print("Backward " + str(len(backward_steps)))
        forward_solution_str = self.backward_begin_state.create_solution_string(forward_steps, False)
        backward_solution_str = self.backward_begin_state.create_solution_string(backward_steps, True, True)
        solution_str = forward_solution_str + ' ' + backward_solution_str
        self.finalize_data()
        for entry in self.backward_open_list.queue:
            self.forward_open_list.push(entry.state)
        self.data.finalize(solution_str, len(forward_steps + backward_steps), self.forward_open_list)
        return solution_str

    def forward_step(self):
        state = self.forward_open_list.pop().state
        self.forward_data.scanned_nodes = self.forward_data.scanned_nodes + 1
        self.forward_closed_list.add(hash(state.board.grid_to_str()))

        if hash(state.board.grid_to_str()) in self.backward_f_values:
            return state
        expanded_states = state.expand_state(self.forward_data)
        for expanded_state in expanded_states:
            if hash(expanded_state.board.grid_to_str()) not in self.forward_f_values:
                self.forward_open_list.push(expanded_state)
                self.forward_f_values[hash(expanded_state.board.grid_to_str())] = expanded_state.f_value
            else:
                # Step 6.3: If j was already on either OPEN or CLOSED, compare the f value just calculated for j
                # with the value previously associated with the node.
                if expanded_state.f_value < self.forward_f_values[hash(expanded_state.board.grid_to_str())]:
                    self.forward_f_values[hash(expanded_state.board.grid_to_str())] = expanded_state.f_value
                    # Step 6.3.1: Substitute it for the old value.
                    if expanded_state.is_expansion_in_closed_list(self.forward_closed_list):
                        # Step 6.3.2: Point j back to i instead of to its previously found predecessor.
                        # Step 6.3.3: If node j was on the CLOSED list, move it back to OPEN
                        self.forward_open_list.push(expanded_state)
                        expanded_state.remove_state(self.forward_closed_list)
        return None

    def backward_step(self):
        state = self.backward_open_list.pop().state
        self.backward_data.scanned_nodes = self.backward_data.scanned_nodes + 1
        self.backward_closed_list.add(hash(state.board.grid_to_str()))

        if hash(state.board.grid_to_str()) in self.forward_f_values:
            return state
        expanded_states = state.expand_state(self.backward_data)
        for expanded_state in expanded_states:
            if hash(expanded_state.board.grid_to_str()) not in self.backward_f_values:
                self.backward_open_list.push(expanded_state)
                self.backward_f_values[hash(expanded_state.board.grid_to_str())] = expanded_state.f_value
            else:
                # Step 6.3: If j was already on either OPEN or CLOSED, compare the f value just calculated for j
                # with the value previously associated with the node.
                if expanded_state.f_value < self.backward_f_values[hash(expanded_state.board.grid_to_str())]:
                    self.backward_f_values[hash(expanded_state.board.grid_to_str())] = expanded_state.f_value
                    # Step 6.3.1: Substitute it for the old value.
                    if expanded_state.is_expansion_in_closed_list(self.backward_closed_list):
                        # Step 6.3.2: Point j back to i instead of to its previously found predecessor.
                        # Step 6.3.3: If node j was on the CLOSED list, move it back to OPEN
                        self.backward_open_list.push(expanded_state)
                        expanded_state.remove_state(self.backward_closed_list)
        return None

    def get_backward_state(self, state):
        hash_str = hash(state.board.grid_to_str())
        for node in self.backward_open_list.queue:
            if hash(node.state.board.grid_to_str()) == hash_str:
                return node.state
        return None

    def get_forward_state(self, state):
        hash_str = hash(state.board.grid_to_str())
        for node in self.forward_open_list.queue:
            if hash(node.state.board.grid_to_str()) == hash_str:
                return node.state
        return None

    def finalize_data(self):
        self.data.scanned_nodes = self.forward_data.scanned_nodes + self.backward_data.scanned_nodes
        self.data.heuristic_values = self.forward_data.heuristic_values + self.backward_data.heuristic_values
