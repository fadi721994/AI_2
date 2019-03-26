import heapq
import math
from priority_queue_node import PriorityQueueNode
from bidirectional_direction import BidirectionalDirection


class PriorityQueue:
    def __init__(self):
        self.queue = []

    def push(self, state, other_list=None, bidirectional_direction=BidirectionalDirection.NONE):
        priority = state.f_value
        if bidirectional_direction != BidirectionalDirection.NONE:
            if hash(state.board.grid_to_str()) in other_list:
                priority = -math.inf
        elif state.goal_state():
            priority = -math.inf
        heapq.heappush(self.queue, PriorityQueueNode(priority, state))

    def pop(self):
        return heapq.heappop(self.queue)

    def is_not_empty(self):
        return len(self.queue) != 0

    def update_predecessor(self, state, other_list=None, bidirectional_direction=BidirectionalDirection.NONE):
        hash_str = hash(state.board.grid_to_str())
        removed = False
        for node in self.queue:
            if hash(node.state.board.grid_to_str()) == hash_str:
                self.queue.remove(node)
                removed = True
                break
        if removed:
            self.push(state, other_list, bidirectional_direction)
