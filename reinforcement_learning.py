from a_star import AStar


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
            print(self.solution)
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
                self.update_single_action_entry(i, step, -1)
            else:
                self.update_single_action_entry(i, step, 1)

    # Update the action weight with +1 or -1
    def update_single_action_entry(self, depth, step, value):
        if depth in self.data.actions:
            steps_hash = self.data.actions[depth]
            if step in steps_hash:
                steps_hash[step] = steps_hash[step] + value
            else:
                steps_hash[step] = value
        else:
            self.data.actions[depth] = dict()
            steps_hash = self.data.actions[depth]
            steps_hash[step] = value

    # Create the output file "reinforcement learning.txt"
    def write_output(self):
        h_file = self.data.heuristic.value
        with open("reinforcement_learning_h" + str(h_file) + ".txt", 'a') as file:
            file.write("=======================================================\n")
            file.write("Solution and weight for board number " + str(self.data.board_num + 1) + "\n")
            if self.solution is None:
                self.solution = 'Not Found'
            file.write("Solution: " + self.solution + "\n")
            for depth, action_list in self.data.actions.items():
                is_print = False
                for step, weight in action_list.items():
                    if weight != 0:
                        is_print = True
                if not is_print:
                    continue
                file.write("At Depth " + str(depth) + ":\n")
                for step, weight in action_list.items():
                    if weight == 0:
                        continue
                    output_str = step[0]
                    if step[1] == "U":
                        output_str = output_str + " Up"
                    elif step[1] == "D":
                        output_str = output_str + " Down"
                    elif step[1] == "R":
                        output_str = output_str + " Right"
                    else:
                        output_str = output_str + " Left"
                    output_str = output_str + " " + step[2] + ":  " + str(weight)
                    file.write("    " + output_str + "\n")
            file.close()
