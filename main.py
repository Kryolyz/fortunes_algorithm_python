from utils.arc import Arc, Site
from utils.beachline import Beachline
from utils.event_queue import EventQueue
from utils.events import CircleEvent, SiteEvent


class VoronoiDiagram:
    def __init__(self):
        self.beachline = Beachline()
        self.event_queue = EventQueue()
        self.vertices = []
        # self.sweep_y = 0

    def add_site_events(self, sites: list[Site]):
        for site in sites:
            event = SiteEvent(site)
            self.event_queue.insert(event)

    def process_next_event(self):
        event = self.event_queue.pop()
        self.sweep_y = event.site.y

        if isinstance(event, SiteEvent):
            new_arc = Arc(event.site)
            left, middle, right = self.beachline.insert_arc(new_arc, event.site.y)
            self.check_circle_event(middle)
            self.check_circle_event(right)

        elif isinstance(event, CircleEvent):
            self.beachline.handle_circle_event(event)

    def check_circle_event(self, middle: Arc, sweep_y):
        if middle and middle.left_neighbor and middle.right_neighbor:
            left = middle.left_neighbor
            right = middle.right_neighbor

            circumcenter, circumradius = middle.site.find_circumcenter(
                left.site, right.site
            )

            if circumcenter and circle_event_y > sweep_y:
                circle_event_y = circumcenter.y + circumradius
                circle_event_location = Site(circumcenter.x, circle_event_y)

                circle_event = CircleEvent(
                    circle_event_location, left, middle, right, circumcenter
                )
                self.event_queue.insert(circle_event)
