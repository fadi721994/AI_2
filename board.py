from orientation import Orientation
from direction import Direction
from car import Car
from heuristic import Heuristic
from special_cell import SpecialCell
from bidirectional_direction import BidirectionalDirection

class Board:
    def __init__(self, board_line, special_cells, width=6, height=6):
        if len(board_line) % width != 0 or len(board_line) / width != height:
            raise Exception("Board input " + board_line + " cannot be split into 6 rows")
        board_line = [board_line[i:i + width] for i in range(0, len(board_line), width)]
        self.width = width
        self.height = height
        self.grid = board_line
        self.cars = dict()
        self.create_cars()
        self.build_grid()
        if special_cells is None:
            self.initialize_special_cells()
        else:
            self.special_cells = special_cells

    # Read the grid lines and create car objects and add them to list.
    def create_cars(self):
        assert(len(self.grid) == 6)
        for row_num, row in enumerate(self.grid):
            for col_num, col in enumerate(row):
                if col == ".":
                    continue
                name = row[col_num]
                x = row_num
                y = col_num
                if self.car_name_exists(name):
                    continue
                if col_num < 4 and row[col_num] == row[col_num + 1] == row[col_num + 2]:
                    size = 3
                    orientation = Orientation.HORIZONTAL
                    car = Car(name, x, y, size, orientation)
                    self.cars[name] = car
                elif col_num < 5 and row[col_num] == row[col_num + 1]:
                    size = 2
                    orientation = Orientation.HORIZONTAL
                    car = Car(name, x, y, size, orientation)
                    self.cars[name] = car
                elif row_num < 4 and self.grid[row_num][col_num] == self.grid[row_num + 1][col_num]\
                        == self.grid[row_num + 2][col_num]:
                    size = 3
                    orientation = Orientation.VERTICAL
                    car = Car(name, x, y, size, orientation)
                    self.cars[name] = car
                elif row_num < 5 and self.grid[row_num][col_num] == self.grid[row_num + 1][col_num]:
                    size = 2
                    orientation = Orientation.VERTICAL
                    car = Car(name, x, y, size, orientation)
                    self.cars[name] = car

    # Check if a car exists on the board using its name
    def car_name_exists(self, name):
        if name in self.cars:
            return True
        return False

    # Build the grid using where the cars are placed.
    def build_grid(self):
        self.grid = [[".", ".", ".", ".", ".", "."], [".", ".", ".", ".", ".", "."], [".", ".", ".", ".", ".", "."],
                     [".", ".", ".", ".", ".", "."], [".", ".", ".", ".", ".", "."], [".", ".", ".", ".", ".", "."]]
        for car_name, car in self.cars.items():
            if car.orientation == Orientation.HORIZONTAL:
                for i in range(car.size):
                    self.grid[car.x][car.y + i] = car.name
            elif car.orientation == Orientation.VERTICAL:
                for i in range(car.size):
                    self.grid[car.x + i][car.y] = car.name

    # Return a car object when queried with a car name
    def get_car_by_name(self, car_name):
        return self.cars[car_name]

    # Get the number of cars blocking X
    def get_blocking_cars_num(self):
        exit_row = self.grid[2]
        blocking_cars = 0
        count = False
        for col in exit_row:
            if col == "X":
                count = True
            if count and col != "X" and col != ".":
                blocking_cars = blocking_cars + 1
        return blocking_cars

    # Calculate the number of cars blocking X. If count_blocked is True, we add 1 for each blocking car that is blocked.
    def calculate_heuristic_value(self, heuristic):
        exit_row = self.grid[2]
        value = 0
        count = False
        if heuristic == Heuristic.BLOCKING_CARS:
            return self.get_blocking_cars_num()
        for col in exit_row:
            if col == "X":
                count = True
            if count and col != "X" and col != ".":
                if heuristic == Heuristic.BLOCKED_BLOCKING_CARS:
                    # Add one for the original blocking car:
                    value = value + 1
                    value = value + self.cars_blocking_blocking_car_num(car)
                if heuristic == Heuristic.BLOCKING_CARS_MOVE_DISTANCE or \
                        heuristic == Heuristic.BLOCKED_BLOCKING_CARS_MOVE_DISTANCE:
                    car = self.get_car_by_name(col)
                    if car is None:
                        assert 0
                    value = value + car.steps_to_clear_path()
                if heuristic == Heuristic.BLOCKED_BLOCKING_CARS_MOVE_DISTANCE:
                    value = value + self.cars_blocking_blocking_car_num(car)
        return value

    def cars_blocking_blocking_car_num(self, car):
        cars_blocking = 0
        if car.size == 2 \
                and ((car.x == 1 and self.grid[0][car.y] != '.') or (car.x == 2 and self.grid[4][car.y] != '.')):
            cars_blocking = cars_blocking + 1
        else:
            if self.grid[5][car.y] != '.' and self.grid[5][car.y] != car.name:
                cars_blocking = cars_blocking + 1
            if self.grid[4][car.y] != '.' and self.grid[4][car.y] != car.name:
                cars_blocking = cars_blocking + 1
            if self.grid[3][car.y] != '.' and self.grid[3][car.y] != car.name:
                cars_blocking = cars_blocking + 1
        return cars_blocking

    def calculate_bidirectional_heuristic_value(self, goal_board):
        overall = 0
        for car_name, car in self.cars.items():
            goal_car = goal_board.get_car_by_name(car_name)
            x_diff = abs(goal_car.x - car.x)
            y_diff = abs(goal_car.y - car.y)
            overall = overall + x_diff + y_diff
        return overall

    # Calculate the heuristic function and return its value.
    # Parameter "calc_blocked_blocking", if true, we add 1 for each X-blocking car that is also blocked.
    def calculate_h(self, heuristic, bidirectional_direction, goal_board):
        if bidirectional_direction != BidirectionalDirection.NONE:
            return self.calculate_bidirectional_heuristic_value(goal_board)
        heuristic_value = self.calculate_heuristic_value(heuristic)
        return heuristic_value

    def pretty_print(self):
        for line in self.grid:
            row = ''
            for entry in line:
                row = row + entry + " "
            print(row)

    def num_of_blocked_cars(self):
        blocked_cars = 0
        for car_name, car in self.cars.items():
            if self.can_car_move(car):
                blocked_cars = blocked_cars + 1
        return blocked_cars

    # Check if a car can move.
    def can_car_move(self, car):
        x = car.x
        y = car.y
        if car.orientation == Orientation.HORIZONTAL:
            if y == 0:
                if self.grid[x][y + car.size] != ".":
                    return False
            elif y + car.size == 6:
                if self.grid[x][y - 1] != ".":
                    return False
            else:
                if self.grid[x][y - 1] != "." and self.grid[x][y + car.size] != ".":
                    return False
        elif car.orientation == Orientation.VERTICAL:
            if x == 0:
                if self.grid[x + car.size][y] != ".":
                    return False
            elif x + car.size == 6:
                if self.grid[x - 1][y] != ".":
                    return False
            else:
                if self.grid[x - 1][y] != "." and self.grid[x + car.size][y] != ".":
                    return False
        return True

    def can_one_car_only_reach(self, x, y):
        reaching_cars = 0
        name = ''
        for car_name, car in self.cars.items():
            if (car.x == x and car.orientation == Orientation.HORIZONTAL) or \
                    (car.y == y and car.orientation == Orientation.VERTICAL):
                name = car.name
                reaching_cars = reaching_cars + 1
        if reaching_cars == 1 and name == 'X':
            return False, None
        if reaching_cars == 1:
            return True, name
        return False, None

    def initialize_special_cells(self):
        self.special_cells = []
        for y in range(6):
            for x in range(6):
                is_special, car_name = self.can_one_car_only_reach(x, y)
                if is_special:
                    self.special_cells.append(SpecialCell(x, y, car_name))

    def occupied_special_cells(self):
        occupied = 0
        for cell in self.special_cells:
            if self.grid[cell.x][cell.y] not in ['.', 'X']:
                occupied = occupied + 1
        return occupied

    # Given a car object, return a list of all the possible steps it can take. A step is an object.
    def find_car_valid_steps(self, car):
        steps = []
        x = car.x
        y = car.y
        if car.orientation == Orientation.HORIZONTAL:
            row = self.grid[x]
            reversed_row = list(reversed(self.grid[x]))
            # Find right steps:
            car.find_direction_steps(row, Direction.RIGHT, steps)
            # Find left steps:
            car.find_direction_steps(reversed_row, Direction.LEFT, steps)
            return steps
        if car.orientation == Orientation.VERTICAL:
            transpose_grid = [list(i) for i in zip(*self.grid)]
            col = transpose_grid[y]
            reversed_col = list(reversed(transpose_grid[y]))
            # Find right steps:
            car.find_direction_steps(col, Direction.DOWN, steps)
            # Find left steps:
            car.find_direction_steps(reversed_col, Direction.UP, steps)
            return steps

    # Change a grid to a string in order to hash the string.
    def grid_to_str(self):
        grid_line = ''
        for line in self.grid:
            line = ''.join(line)
            grid_line = grid_line + line
        return grid_line
