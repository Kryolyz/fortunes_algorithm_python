from utils.arc import Site


class HalfEdge:
    def __init__(self, origin: Site, face=None):
        self.origin: Site = origin  # Start vertex of the half-edge
        self.twin: HalfEdge = None  # Opposite half-edge
        self.next: HalfEdge = None  # Next half-edge in the face
        self.prev: HalfEdge = None  # Previous half-edge in the face
        self.face: Face = face  # The face to the left of this half-edge


class Face:
    def __init__(self, site: Site):
        self.site = site  # The site (focus) associated with this face
        self.outer_component: HalfEdge = None  # A half-edge that bounds this face
