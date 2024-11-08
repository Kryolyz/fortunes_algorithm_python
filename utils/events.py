from utils.arc import Arc, Site


class Event:
    def __init__(self, site: Site):
        if isinstance(site, Arc):
            site = site.site
        self.site = site

    def __lt__(self, other: "Event"):
        return self.site.y < other.site.y


class SiteEvent(Event):
    def __init__(self, site: Site):
        super().__init__(site)

    def __str__(self):
        return f"SiteEvent {self.site.x} {self.site.y}"


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
        return f"CircleEvent {self.site.x} {self.site.y} (circumcenter: {self.circumcenter.x}, {self.circumcenter.y})"

    def __eq__(self, other):
        if not isinstance(other, CircleEvent):
            return NotImplemented
        return (
            self.site == other.site
            and self.circumcenter == other.circumcenter
            and self.left_arc == other.left_arc
            and self.middle_arc == other.middle_arc
            and self.right_arc == other.right_arc
        )
