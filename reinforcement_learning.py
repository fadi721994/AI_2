from a_star import AStar
import utils


class ReinforcementLearning:
    def __init__(self, board, data):
        self.board = board
        self.data = data
        self.data.update_action_weights = True
        self.solution = None
        self.data.actions = {}
        self.optimal_steps = self.data.min_cost_path.split(' ')[:-1]

    # Check if solution is optimal.
    def is_solution_optimal(self):
        if self.solution is None:
            return False
        if self.solution == self.data.min_cost_path:
            return True
        return False

    # Main function that solves the board and updates the actions weights
    def solve_board(self):
        while not self.is_solution_optimal():
            algorithm = AStar(self.board, self.data)
            self.solution = algorithm.solve_board()
            self.update_weights()
        self.write_output()
        return self.solution

    # Update the weights of the actions according to whether the step is optimal or not.
    def update_weights(self):
        if self.solution is None:
            return
        steps = self.solution.split(' ')[:-1]
        for i, step in enumerate(steps):
            if i < len(self.optimal_steps) and self.optimal_steps[i] == step:
                solution_str = utils.get_solution_string(i, steps)
                if solution_str in self.data.min_cost_path:
                    self.update_single_action_entry(i, steps, -1)
                else:
                    self.update_single_action_entry(i, steps, 1)
            else:
                self.update_single_action_entry(i, steps, 1)

    # Update the action weight with +1 or -1
    def update_single_action_entry(self, depth, steps, value):
        solution = ''
        for i in range(depth + 1):
            solution = solution + steps[i] + ' '
        solution = solution.strip()
        if solution in self.data.actions:
            self.data.actions[solution] = self.data.actions[solution] + value
        else:
            self.data.actions[solution] = value

    # Create the output file "reinforcement learning.txt"
    def write_output(self):
        h_file = self.data.heuristic.value
        with open("reinforcement_learning_h" + str(h_file) + ".txt", 'a') as file:
            file.write("=======================================================\n")
            file.write("Solution and weight for board number " + str(self.data.board_num + 1) + "\n")
            if self.solution is None:
                self.solution = 'Not Found'
            file.write("Solution: " + self.solution + "\n")
            for solution, action_list in self.data.actions.items():
                file.write(str(solution) + ": " + str(action_list) + "\n")
            file.close()
