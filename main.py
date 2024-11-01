from utils.arc import Arc, Site
from utils.beachline import Beachline
from utils.event_queue import EventQueue
from utils.events import CircleEvent, SiteEvent
from utils.voronoi_diagram import VoronoiDiagram


def main():
    voronoi_diagram = VoronoiDiagram()
    sites = [
        Site(1, 0),
        Site(2, 1),
        Site(3, 3),
        Site(5, 4),
    ]
    voronoi_diagram.add_site_events(sites)
    while not voronoi_diagram.event_queue.is_empty():
        voronoi_diagram.process_next_event()


if __name__ == "__main__":
    main()
