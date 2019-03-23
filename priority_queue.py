import heapq
import math
from priority_queue_node import PriorityQueueNode
from bidirectional_direction import BidirectionalDirection


class PriorityQueue:
    def __init__(self):
        self.queue = []

    def push(self, state, bidirectional_direction=BidirectionalDirection.NONE, goal_board=None):
        priority = state.f_value
        if bidirectional_direction == BidirectionalDirection.BACKWARD:
            if state.board.calculate_bidirectional_heuristic_value(goal_board) == 0:
                priority = -math.inf
        elif state.goal_state():
            priority = -math.inf
        heapq.heappush(self.queue, PriorityQueueNode(priority, state))

    def pop(self):
        return heapq.heappop(self.queue)

    def is_not_empty(self):
        return len(self.queue) != 0
