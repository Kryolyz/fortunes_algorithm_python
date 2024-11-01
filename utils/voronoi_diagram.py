from .arc import Arc, Site
from .beachline import Beachline
from .event_queue import EventQueue
from .events import CircleEvent, SiteEvent


class VoronoiDiagram:
    def __init__(self):
        self.beachline = Beachline()
        self.event_queue = EventQueue()

    def add_site_events(self, sites: list[Site]):
        for site in sites:
            event = SiteEvent(site)
            self.event_queue.insert(event)

    def process_next_event(self):
        event = self.event_queue.pop()
        self.sweep_y = event.site.y

        if isinstance(event, SiteEvent):
            new_arc = Arc(event.site)
            left, middle, right = self.beachline.insert_arc(new_arc)

            self.check_circle_event(middle, new_arc.site.y)
            self.check_circle_event(right, new_arc.site.y)

        elif isinstance(event, CircleEvent):
            self.beachline.handle_circle_event(event)

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
            return None

        event_location = Site(circumcenter.x, circumcenter.y + circumradius)
        if event_location.y < sweep_y:
            return None

        return CircleEvent(
            event_location, left_arc, middle_arc, right_arc, circumcenter
        )
