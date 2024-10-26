import math
from . import arc, avl_tree

# from avl_tree import AVL_Tree


class Beachline:
    def __init__(self):
        self.tree = AVL_Tree()
        # self.root = None

    def intersect_x(self, arc, other_arc, sweep_y):
        # This uses the quadratic formula based on the difference of two parabolas
        if arc.site.y == sweep_y or other_arc.site.y == sweep_y:
            return None  # Handle edge case when site is on the sweep line

        # Calculate the a, b, c coefficients for the intersection quadratic equation
        a = 1 / (2 * (arc.site.y - sweep_y)) - 1 / (2 * (other_arc.site.y - sweep_y))
        b = 2 * (
            other_arc.site.x / (2 * (other_arc.site.y - sweep_y))
            - arc.site.x / (2 * (arc.site.y - sweep_y))
        )
        c = (
            arc.site.x**2 / (2 * (arc.site.y - sweep_y)) - (arc.site.y + sweep_y) / 2
        ) - (
            other_arc.site.x**2 / (2 * (other_arc.site.y - sweep_y))
            - (other_arc.site.y + sweep_y) / 2
        )

        # Solve the quadratic equation for x
        discriminant = b**2 - 4 * a * c
        if discriminant < 0:
            return None  # No real solutions means no intersection
        x1 = (-b + math.sqrt(discriminant)) / (2 * a)
        x2 = (-b - math.sqrt(discriminant)) / (2 * a)

        # Return the x-coordinate that is within range
        # (Choose based on beachline position or sweep line orientation)
        return max(x1, x2) if arc.site.y < other_arc.site.y else min(x1, x2)

    def find_arc(self, x, sweep_y):
        node = self.tree.root
        while node:

            # get intersection on both sides to find the range of the current arc
            left_intersection = self.get_left_intersection(node, sweep_y)
            right_intersection = self.get_right_intersection(node, sweep_y)

            # we can assume that all nodes are valid leafs because old ones get deleted, so no need to check if they are valid leafs
            if left_intersection <= x <= right_intersection:
                return node

            if x < left_intersection:
                node = node.left
            else:
                node = node.right

        return None

    def insert_arc(self, new_site, sweep_y):
        # get the arc below the current site to be able to split it into three
        arc_to_split = self.find_arc(new_site.x, sweep_y)

        # insert new arcs for splitting. The old one is split in two, so the left and right arcs originate from the same site
        left_arc = Arc(arc_to_split.site)
        middle_arc = Arc(new_site)
        right_arc = Arc(arc_to_split.site)

        self.replace_arc(arc_to_split, left_arc, middle_arc, right_arc)

    def get_left_intersection(self, arc, sweep_y):
        if not arc.left:
            return float("-inf")

        return self.intersect_x(arc, arc.left, sweep_y)

    def get_right_intersection(self, arc, sweep_y):
        if not arc.right:
            return float("inf")

        return self.intersect_x(arc, arc.right, sweep_y)

    # def replace_arc(self, arc, left_arc, middle_arc, right_arc):
    #   self.tree.
