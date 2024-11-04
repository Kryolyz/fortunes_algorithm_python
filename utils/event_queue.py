import heapq
from .events import Event


class EventQueue:
    def __init__(self):
        self.queue = []

    def insert(self, event: Event):
        # for existing_event in self.queue:
        #     print("Difference :", abs(existing_event.site.y - event.site.y))
        #     if abs(existing_event.site.y - event.site.y) < 0.0001:
        #         print("Event : ", event, " already in queue")
        #         return
        # print("New Event: ", event)
        heapq.heappush(self.queue, event)

    def pop(self):
        return heapq.heappop(self.queue)

    def is_empty(self):
        return len(self.queue) == 0
