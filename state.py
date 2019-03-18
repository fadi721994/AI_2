from direction import Direction
from board import Board


class State:
    def __init__(self, board, prev_state, step_taken, f_value, steps, depth):
        self.board = board
        self.f_value = f_value
        self.prev_state = prev_state
        self.steps = steps
        self.step_taken = step_taken
        self.depth = depth

    # Check if a state is a goal state.
    def goal_state(self):
        blocking_cars = self.board.calculate_blocking_cars()
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
    def create_expansion(self, step, data):
        board = Board(self.board.grid_to_str())
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
        new_state.f_value = new_state.board.calculate_f(new_state.steps, data)
        return new_state

    # Give a state, find the path to the beginning state.
    def get_solution_steps(self):
        steps = [self.step_taken]
        state = self
        while state.prev_state is not None:
            steps.append(state.prev_state.step_taken)
            state = state.prev_state
        return steps

    # Given steps list, create the string that should be printed to the output file.
    def create_solution_string(self, steps):
        steps = list(reversed(steps))
        solution_str = ''
        for step in steps:
            if step is not None:
                name = step.car_name
                direction = step.direction
                amount = step.amount
                direction_letter = ''
                if direction == Direction.DOWN:
                    direction_letter = 'D'
                elif direction == Direction.UP:
                    direction_letter = 'U'
                elif direction == Direction.LEFT:
                    direction_letter = 'L'
                elif direction == Direction.RIGHT:
                    direction_letter = 'R'
                solution_str = solution_str + name + direction_letter + str(amount) + ' '
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
