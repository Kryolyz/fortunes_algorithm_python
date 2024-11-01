from .arc import Arc, Site
from .beachline import Beachline
from .event_queue import EventQueue
from .events import CircleEvent, SiteEvent


class VoronoiDiagram:
    def __init__(self):
        self.beachline: Beachline = Beachline()
        self.event_queue: EventQueue = EventQueue()
        self.bounding_box: list[Site] = [Site(0, 0), Site(10, 10)]
        self.sweep_y = 0

    def add_site_events(self, sites: list[Site]):
        for site in sites:
            event = SiteEvent(site)
            self.event_queue.insert(event)

    def set_bounding_box(self, lower_bound: Site, upper_bound: Site):
        self.bounding_box = [lower_bound, upper_bound]

    def process_next_event(self):
        event = self.event_queue.pop()
        self.sweep_y = event.site.y

        if isinstance(event, SiteEvent):
            new_arc = Arc(event.site)
            left, middle, right = self.beachline.insert_arc(new_arc)

            # self.check_circle_event(left, new_arc.site.y)
            self.check_circle_event(middle, self.sweep_y)
            self.check_circle_event(right, self.sweep_y)

        elif isinstance(event, CircleEvent):
            left, deleted_middle, right = self.beachline.handle_circle_event(event)

            if left.left_neighbor == deleted_middle:
                print("Gosh darn copies at it again")
            print(
                "Left arc:",
                left,
                "Left Left neighbor:",
                left.left_neighbor,
                "Left Right neighbor:",
                left.right_neighbor,
            )
            print("Deleted middle arc:", deleted_middle)
            # self.check_circle_event(left, self.sweep_y)
            # self.check_circle_event(right, self.sweep_y)
            self.remove_circle_events(deleted_middle)

    def remove_circle_events(self, arc: Arc):
        # print("Event queue pre-processing:", self.event_queue.queue)
        self.event_queue.queue = [
            event
            for event in self.event_queue.queue
            if not isinstance(event, CircleEvent)
            or (
                event.left_arc != arc
                and event.middle_arc != arc
                and event.right_arc != arc
            )
        ]
        # print("Event queue post-processing:", self.event_queue.queue)

    def check_circle_event(self, middle: Arc, sweep_y):
        if middle and middle.left_neighbor and middle.right_neighbor:
            if middle.left_neighbor.site == middle.right_neighbor.site:
                return

            circle_event = self.make_circle_events(
                middle.left_neighbor, middle, middle.right_neighbor, sweep_y
            )
            if circle_event:
                self.event_queue.insert(circle_event)

    def make_circle_events(
        self, left_arc: Arc, middle_arc: Arc, right_arc: Arc, sweep_y: float
    ) -> CircleEvent:
        circumcenter, circumradius = middle_arc.site.find_circumcenter(
            left_arc.site, right_arc.site
        )
        if circumcenter == float("inf"):
            print("Circumcenter not found")
            return None

        if (
            circumcenter.x < self.bounding_box[0].x
            or circumcenter.x > self.bounding_box[1].x
            or circumcenter.y < self.bounding_box[0].y
            or circumcenter.y > self.bounding_box[1].y
        ):
            print("Circumcenter out of bounds")
            return None

        event_location = Site(circumcenter.x, circumcenter.y + circumradius)
        if event_location.y < sweep_y:
            print("Event location below sweep line")
            return None

        return CircleEvent(
            event_location, left_arc, middle_arc, right_arc, circumcenter
        )
