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
        self.max_sweep_line_value = 0

    def add_site_events(self, sites: list[Site]):
        for site in sites:
            event = SiteEvent(site)
            self.event_queue.insert(event)

    def set_bounding_box(self, lower_bound: Site, upper_bound: Site):
        self.bounding_box = [lower_bound, upper_bound]

    def process_next_event(self, debug_index=None):
        if debug_index:
            print(debug_index)
        event = self.event_queue.pop()
        self.sweep_y = event.site.y
        print("Current Event:", event)

        if isinstance(event, SiteEvent):
            new_arc = Arc(event.site)
            left, middle, right = self.beachline.insert_arc(new_arc)

            self.check_circle_event(left, self.sweep_y)
            self.check_circle_event(middle, self.sweep_y)
            self.check_circle_event(right, self.sweep_y)

        elif isinstance(event, CircleEvent):

            # sanity check, confirm that arcs that produced the event are actually next to each other when the event occurs
            found_arc = self.beachline.find_arc_by_ref(event.left_arc)
            if (
                not found_arc
                or found_arc.right_neighbor != event.middle_arc
                or found_arc.right_neighbor.right_neighbor != event.right_arc
            ):
                print("Arcs not next to each other")
                return

            arc_below = self.beachline.find_arc(event.site.x, self.sweep_y + 0.01)
            if (
                arc_below
                and arc_below != event.middle_arc
                and arc_below != event.left_arc
                and arc_below != event.right_arc
            ):
                print("Arc below doesn not appear in event")
                return

            left, deleted_middle, right = self.beachline.handle_circle_event(event)

            self.check_circle_event(left, self.sweep_y, event)
            self.check_circle_event(right, self.sweep_y, event)
            self.remove_circle_events(deleted_middle)

    def remove_circle_events(self, arc: Arc):
        for event in self.event_queue.queue:
            if not isinstance(event, CircleEvent):
                continue
            if (
                event.left_arc == arc
                or event.right_arc == arc
                or event.middle_arc == arc
            ):
                print("Removing event:", event)
                self.event_queue.queue.remove(event)

    def check_circle_event(self, middle: Arc, sweep_y, current_event=None):
        if middle and middle.left_neighbor and middle.right_neighbor:
            if middle.left_neighbor.site == middle.right_neighbor.site:
                return

            print(
                "Checking Circle event Left: ",
                middle.left_neighbor,
                "Middle:",
                middle,
                "Right:",
                middle.right_neighbor,
            )

            circle_event = self.make_circle_events(
                middle.left_neighbor, middle, middle.right_neighbor, sweep_y
            )

            if circle_event and current_event:
                if (
                    circle_event.circumcenter == current_event.circumcenter
                    or circle_event.site in self.beachline.vertices
                ):
                    print("Circle event already in queue")
                    return

            if circle_event:
                print("Inserting circle event:", circle_event)
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

        event_location = Site(circumcenter.x, circumcenter.y + circumradius)
        if event_location.y <= sweep_y:
            print("Event location below sweep line")
            return None

        return CircleEvent(
            event_location, left_arc, middle_arc, right_arc, circumcenter
        )
