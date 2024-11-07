import unittest
from utils.arc import Arc, Site
from utils.voronoi_diagram import VoronoiDiagram


class Test_VoronoiDiagram(unittest.TestCase):
    def setUp(self):
        self.voronoi_diagram = VoronoiDiagram()
        self.site1 = Arc(Site(1, 0))
        self.site2 = Arc(Site(2, 1))
        self.site3 = Arc(Site(3, 3))
        self.site4 = Arc(Site(5, 4))
        self.sites = [self.site1, self.site2, self.site3, self.site4]

        self.voronoi_diagram.add_site_events(self.sites)

    def test_event_processing(self):
        print("Starting event processing...")
        while not self.voronoi_diagram.event_queue.is_empty():
            self.voronoi_diagram.process_next_event()
            arc = self.voronoi_diagram.beachline.first_arc
            sorted_queue = sorted(self.voronoi_diagram.event_queue.queue)
            for event in sorted_queue:
                print(event)
        print("Finished event processing...")

        vertices = self.voronoi_diagram.beachline.vertices
        edges = self.voronoi_diagram.beachline.edges
        print("Vertices:")
        for vertex in vertices:
            print(vertex)
        print("Edges:")
        for edge in edges:
            print(edge)

        face = self.voronoi_diagram.beachline.get_face(self.site1.site)
        print(face)
        edge = face.outer_component
        print("Edge:", edge)
        print("Edges of face:")
        while True:
            print(edge)
            edge = edge.next
            if edge == face.outer_component or edge is None:
                break
