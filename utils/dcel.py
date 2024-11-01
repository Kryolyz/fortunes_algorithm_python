from utils.arc import Site


class Vertex(Site):
    def __init__(self, site: Site):
        super().__init__(site.x, site.y)
        self.origin_sites: list[Site] = []

    def __str__(self):
        return f"Vertex({self.x}, {self.y})"

    def make_edge_directions(self):
        directions = []
        for origin1, origin2 in [
            (self.origin_sites[i], self.origin_sites[j])
            for i in range(3)
            for j in range(i + 1, 3)
        ]:
            midpoint = (origin1 + origin2) / 2
            direction = midpoint - self
            length = direction.length()
            directions.append(direction / length)
        return directions


class HalfEdge:
    def __init__(self, origin: Site, face=None):
        self.origin: Site = origin  # Start vertex of the half-edge
        self.twin: HalfEdge = None  # Opposite half-edge
        self.next: HalfEdge = None  # Next half-edge in the face
        self.prev: HalfEdge = None  # Previous half-edge in the face
        self.face: Face = face  # The face to the left of this half-edge

    def __str__(self):
        return f"HalfEdge(origin={self.origin}, face={self.face})"

    def calculate_direction(self):
        if not self.twin or not self.face or not self.twin.face:
            return [0, 0]
        midpoint = (self.face.site + self.twin.face.site) / 2
        direction = midpoint - self.origin
        length = (direction.x**2 + direction.y**2) ** 0.5
        return Site(direction.x / length, direction.y / length)


class Face:
    def __init__(self, site: Site):
        self.site = site  # The site (focus) associated with this face
        self.outer_component: HalfEdge = None  # A half-edge that bounds this face

    def __str__(self):
        return f"Face(site={self.site})"
