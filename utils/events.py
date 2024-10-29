from utils.arc import Arc, Site


class Event:
    def __init__(self, site: Site):
        self.site = site

    def __lt__(self, other: "Event"):
        return self.site.x < other.site.x


class SiteEvent(Event):
    def __init__(self, site: Site):
        super().__init__(Site)

    def __str__(self):
        return f"SiteEvent {self.x} {self.y}"


class CircleEvent(Event):
    def __init__(
        self,
        site: Site,
        left_arc: Arc,
        middle_arc: Arc,
        right_arc: Arc,
        circumcenter: Site,
    ):
        super().__init__(site)
        self.left_arc = left_arc
        self.middle_arc = middle_arc
        self.right_arc = right_arc
        self.circumcenter = circumcenter

    def __str__(self):
        return f"CircleEvent {self.x} {self.y}"
