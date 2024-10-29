import heapq
from .events import Event


class EventQueue:
    def __init__(self):
        self.queue = []

    def insert(self, event: Event):
        heapq.heappush(self.queue, event)

    def pop(self):
        return heapq.heappop(self.queue)

    def is_empty(self):
        return len(self.queue) == 0
