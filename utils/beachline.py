import math

from .dcel import Face, HalfEdge, Vertex
from .avl_tree import AVL_Tree
from .arc import Arc, Site
from .events import CircleEvent, SiteEvent


class Beachline:
    def __init__(self):
        self.first_arc = None
        self.faces: dict[Site, Face] = {}
        self.vertices: list[Vertex] = []
        self.edges: list[HalfEdge] = []

    def intersect_x(self, arc, other_arc, sweep_y):
        """
        Returns the x-coordinate of the intersection between the two given arcs.

        Note that this function assumes that the two arcs are adjacent in the beachline.
        It also assumes that the sweep line is horizontal and moving upwards.

        :param arc: The first arc
        :param other_arc: The adjacent arc
        :param sweep_y: The y-coordinate of the sweep line
        :return: The x-coordinate of the intersection, or None if there is no intersection
        """
        # print("Intersecting arcs:", arc, other_arc)
        if arc.site.y == sweep_y or other_arc.site.y == sweep_y:
            return None, None  # Handle edge case when site is on the sweep line

        if arc.site.y == other_arc.site.y:
            x = arc.site.x + (other_arc.site.x - arc.site.x) / 2
            return x, x

        p = (
            -arc.site.x * other_arc.site.y
            + arc.site.x * sweep_y
            + other_arc.site.x * arc.site.y
            - other_arc.site.x * sweep_y
        ) / (arc.site.y - other_arc.site.y)
        q = (
            (arc.site.y - sweep_y)
            * (other_arc.site.y - sweep_y)
            * (
                arc.site.x**2
                - 2 * arc.site.x * other_arc.site.x
                + other_arc.site.x**2
                + arc.site.y**2
                - 2 * arc.site.y * other_arc.site.y
                + other_arc.site.y**2
            )
        )
        if q < 0:
            return None, None  # No real solutions means no intersection
        q = math.sqrt(q) / (arc.site.y - other_arc.site.y)

        x1 = p + q
        x2 = p - q

        return x1, x2

    def find_arc(self, x, sweep_y):
        """
        Finds the arc that is currently intersecting with the sweep line at given x value.

        The function iterates through the beachline and checks if the current arc's range
        overlaps with the given x value. If it does, it returns the arc. If not, it continues
        to the next arc (either the left neighbor or the right neighbor, depending on the
        comparison result).

        If no node exists yet, it returns None.

        :param x: The x-coordinate of the sweep line
        :param sweep_y: The y-coordinate of the sweep line
        :return: The arc that intersects with the sweep line at given x value, or None if there is no intersection
        """
        node = self.first_arc
        while node:
            # get intersection on both sides to find the range of the current arc
            left_intersection = self.get_left_intersection(node, sweep_y)
            right_intersection = self.get_right_intersection(node, sweep_y)

            # we can assume that all nodes are valid leafs because old ones get deleted, so no need to check if they are valid leafs
            if left_intersection <= x <= right_intersection:
                return node

            if x < left_intersection:
                node = node.left_neighbor
            else:
                node = node.right_neighbor

        return None

    def find_arc_by_ref(self, arc: Arc):
        node = self.first_arc
        while node:
            if node == arc:
                return node
            if node != arc:
                node = node.right_neighbor
        return None

    def get_beachline(self, sweep_y, positions: list[float]):
        y_values = []
        node = self.first_arc

        for x in positions:
            while node:
                left_intersection = self.get_left_intersection(node, sweep_y)
                right_intersection = self.get_right_intersection(node, sweep_y)

                # print("Left intersection:", left_intersection)
                # print("Right intersection:", right_intersection)

                if left_intersection <= x <= right_intersection:
                    y_values.append(node.evaluate_arc(x, sweep_y))
                    break

                if x < left_intersection:
                    node = node.left_neighbor
                else:
                    node = node.right_neighbor

        return y_values

    def get_face(self, site: Site):
        if site not in self.faces.keys():
            # print("Creating new face for site:", site)
            self.faces[site] = Face(site)
        return self.faces[site]

    def insert_arc(self, new_arc) -> tuple[Arc, Arc, Arc]:
        """
        Inserts a new arc into the beachline.

        Given a new site, it finds the arc below the site using the AVL tree of the beachline.
        If no arc is found (i.e., the site is outside of the beachline), it creates a new arc and adds it to the tree.
        If an arc is found, it splits the arc into three and inserts the new arc into the tree.

        :param new_site: The new site to be inserted
        :param sweep_y: The current y-coordinate of the sweep line
        :return: The left, middle and right arcs of the new site, or None if no arc is found
        """

        sweep_y = new_arc.site.y + 0.01
        arc_to_split = self.find_arc(new_arc.site.x, sweep_y)

        if not arc_to_split:
            self.first_arc = new_arc
            return None, new_arc, None

        # insert new arcs for splitting. The old one is split in two, so the left and right arcs originate from the same site
        left_arc = Arc(arc_to_split.site)

        # if split arc was first arc, make left arc the first arc
        if arc_to_split is self.first_arc:
            self.first_arc = left_arc

        middle_arc = new_arc
        right_arc = Arc(arc_to_split.site)

        left_arc.right_neighbor = middle_arc
        middle_arc.left_neighbor = left_arc
        middle_arc.right_neighbor = right_arc
        right_arc.left_neighbor = middle_arc

        if arc_to_split.right_neighbor:
            right_arc.right_neighbor = arc_to_split.right_neighbor
            right_arc.right_neighbor.left_neighbor = right_arc
        if arc_to_split.left_neighbor:
            left_arc.left_neighbor = arc_to_split.left_neighbor
            left_arc.left_neighbor.right_neighbor = left_arc

        if arc_to_split.left_edge:
            left_arc.left_edge = arc_to_split.left_edge
        if arc_to_split.right_edge:
            right_arc.right_edge = arc_to_split.right_edge

        return left_arc, middle_arc, right_arc

    def remove_arc(self, arc: Arc):
        if arc.left_neighbor:
            arc.left_neighbor.right_neighbor = arc.right_neighbor
        if arc.right_neighbor:
            arc.right_neighbor.left_neighbor = arc.left_neighbor

    def get_left_intersection(self, arc: Arc, sweep_y):
        if not arc.left_neighbor:
            return float("-inf")

        return self.intersect_x(arc, arc.left_neighbor, sweep_y)[1]

    def get_right_intersection(self, arc: Arc, sweep_y):
        if not arc.right_neighbor:
            return float("inf")

        return self.intersect_x(arc, arc.right_neighbor, sweep_y)[0]

    def handle_circle_event(self, circle_event: CircleEvent):
        self.remove_arc(circle_event.middle_arc)

        vertex = Vertex(circle_event.circumcenter)
        vertex.origin_sites = [
            circle_event.left_arc.site,
            circle_event.middle_arc.site,
            circle_event.right_arc.site,
        ]
        self.vertices.append(vertex)

        # get both faces
        left_face = self.get_face(circle_event.left_arc.site)
        right_face = self.get_face(circle_event.right_arc.site)

        # make new edges
        left_half_edge = HalfEdge(vertex, left_face)
        right_half_edge = HalfEdge(vertex, right_face)
        self.edges.append(left_half_edge)
        self.edges.append(right_half_edge)

        # link the twins
        left_half_edge.twin = right_half_edge
        right_half_edge.twin = left_half_edge

        if not left_face.outer_component:
            left_face.outer_component = left_half_edge
        if not right_face.outer_component:
            right_face.outer_component = right_half_edge

        if circle_event.left_arc.right_edge:
            left_half_edge.prev = circle_event.left_arc.right_edge
            circle_event.left_arc.right_edge.next = left_half_edge

        if circle_event.right_arc.left_edge:
            right_half_edge.prev = circle_event.right_arc.left_edge
            circle_event.right_arc.left_edge.next = right_half_edge

        circle_event.left_arc.right_edge = left_half_edge
        circle_event.right_arc.left_edge = right_half_edge

        if circle_event.left_arc.right_neighbor:
            circle_event.left_arc.right_neighbor = circle_event.right_arc
        if circle_event.right_arc.left_neighbor:
            circle_event.right_arc.left_neighbor = circle_event.left_arc

        return circle_event.left_arc, circle_event.middle_arc, circle_event.right_arc
