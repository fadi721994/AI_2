from direction import Direction
from board import Board
from indicator import Indicator
from bidirectional_direction import BidirectionalDirection
from heuristic import Heuristic
import utils


class State:
    def __init__(self, board, prev_state, step_taken, f_value, steps, depth):
        self.board = board
        self.f_value = f_value
        self.prev_state = prev_state
        self.steps = steps
        self.step_taken = step_taken
        self.depth = depth
        self.overall_h = 0

    # Check if a state is a goal state.
    def goal_state(self):
        blocking_cars = self.board.get_blocking_cars_num()
        # Check if goal state
        if blocking_cars == 0:
            return True
        return False

    # Expand a state, and return a list of all the possible states that can be reached from the state.
    def expand_state(self, data):
        list_of_expansions = []
        for car_name, car in self.board.cars.items():
            if self.board.can_car_move(car):
                valid_steps = self.board.find_car_valid_steps(car)
                for step in valid_steps:
                    expanded_state = self.create_expansion(step, data)
                    list_of_expansions.append(expanded_state)
        return list_of_expansions

    # Create expansion for a state, given a step.
    def create_expansion(self, step, data, calculate_f_value=True):
        board = Board(self.board.grid_to_str(), self.board.special_cells)
        new_state = State(board, self, step, 0, self.steps + step.amount, self.depth + 1)
        car = new_state.board.get_car_by_name(step.car_name)
        if step.direction == Direction.RIGHT:
            car.y = car.y + step.amount
        elif step.direction == Direction.LEFT:
            car.y = car.y - step.amount
        elif step.direction == Direction.DOWN:
            car.x = car.x + step.amount
        elif step.direction == Direction.UP:
            car.x = car.x - step.amount
        new_state.board.build_grid()
        new_state.overall_h = self.overall_h
        if calculate_f_value:
            new_state.f_value = new_state.calculate_f(data)
        return new_state

    # Evaluate the indicator for the overall free cars number.
    def evaluate_overall_free_cars(self):
        cur_blocked_cars = self.board.num_of_blocked_cars()
        prev_blocked_cars = self.prev_state.board.num_of_blocked_cars()
        if prev_blocked_cars < cur_blocked_cars:
            return 1
        elif prev_blocked_cars > cur_blocked_cars:
            return -1
        return 0

    # Evaluate the indicator for the board freedom degree.
    def evaluate_board_freedom_degree(self):
        if len(self.board.special_cells) == 0:
            return 0
        curr_special_cells = self.board.occupied_special_cells()
        prev_special_cells = self.prev_state.board.occupied_special_cells()
        if prev_special_cells < curr_special_cells:
            return 1
        elif prev_special_cells > curr_special_cells:
            return -1
        return 0

    # Evaluate an indicator that is sent to the function. Returns 0, -1, or 1.
    def evaluate_indicator(self, indicator):
        if self.prev_state is None:
            return 0
        if indicator == Indicator.BOARD_FREEDOM_DEGREE:
            return self.evaluate_board_freedom_degree()
        elif indicator == Indicator.OVERALL_FREE_CARS:
            return self.evaluate_overall_free_cars()
        return 0

    # Calculate the heuristic function and return its value.
    def calculate_h(self, data):
        if data.heuristic == Heuristic.REINFORCEMENT_LEARNING:
            if self.step_taken is not None:
                self.overall_h = self.overall_h + data.actions[self.step_taken.to_string()].weight
                return self.overall_h
            else:
                return 0
        if data.bidirectional_direction == BidirectionalDirection.BACKWARD:
            return self.board.calculate_backward_heuristic_value(data.heuristic, data.goal_board)
        heuristic_value = self.board.calculate_heuristic_value(data.heuristic)
        return heuristic_value

    # Calculate the f function.
    def calculate_f(self, data):
        h_value = self.calculate_h(data)
        for indicator in data.indicators:
            indicator_val = self.evaluate_indicator(indicator)
            if data.bidirectional_direction == BidirectionalDirection.BACKWARD:
                indicator_val = indicator_val * -1
            h_value = h_value + indicator_val
        data.heuristic_values.append(h_value)
        return self.steps + h_value

    # Give a state, find the path to the beginning state.
    def get_solution_steps(self, reverse=False):
        steps = [self.step_taken]
        state = self
        while state.prev_state is not None:
            if state.prev_state.step_taken is not None:
                steps.append(state.prev_state.step_taken)
            state = state.prev_state
        if reverse:
            steps.reverse()
        return steps

    # Given steps list, create the string that should be printed to the output file.
    def create_solution_string(self, steps, add_x=True, flip_dirs=False):
        steps = list(reversed(steps))
        solution_str = ''
        for step in steps:
            if step is not None:
                name = step.car_name
                direction = step.direction
                amount = step.amount
                direction_letter = ''
                if direction == Direction.DOWN:
                    if flip_dirs:
                        direction_letter = 'U'
                    else:
                        direction_letter = 'D'
                elif direction == Direction.UP:
                    if flip_dirs:
                        direction_letter = 'D'
                    else:
                        direction_letter = 'U'
                elif direction == Direction.LEFT:
                    if flip_dirs:
                        direction_letter = 'R'
                    else:
                        direction_letter = 'L'
                elif direction == Direction.RIGHT:
                    if flip_dirs:
                        direction_letter = 'L'
                    else:
                        direction_letter = 'R'
                solution_str = solution_str + name + direction_letter + str(amount) + ' '
        if add_x:
            exit_dist = self.calculate_exit_distance()
            solution_str = solution_str + 'XR' + str(exit_dist + 2)
        return solution_str.strip()

    # Return the distance of the red car from the exit.
    def calculate_exit_distance(self):
        exit_row = self.board.grid[2]
        distance = 0
        count = False
        for col in exit_row:
            if col == "X":
                count = True
            if count and col != "X":
                distance = distance + 1
        return distance

    # Check if a state exists in the closed list.
    def is_expansion_in_closed_list(self, closed_list):
        hash_num = hash(self.board.grid_to_str())
        if hash_num in closed_list:
            return True
        return False

    # Remove state from the closed list.
    def remove_state(self, closed_list):
        hash_num = hash(self.board.grid_to_str())
        if hash_num in closed_list:
            closed_list.remove(hash_num)

    # Receives state, and runs the minimum cost path on it to generate a goal state.
    def run_steps_on_board(self, data, reset_data=True, calculate_f_value=True):
        steps_list = utils.from_steps_str_to_object(data.min_cost_path)
        state = self
        for step in steps_list:
            state = state.create_expansion(step, data, calculate_f_value)
        if reset_data:
            state.f_value = 0
            state.prev_state = None
            state.steps = 0
            state.step_taken = None
            state.depth = 0
        return state

