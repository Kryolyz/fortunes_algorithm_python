import unittest

from utils.avl_tree import AVL_Tree
from utils.beachline import Beachline
from utils.arc import Site, Arc
from utils.events import CircleEvent


def make_circle_event(middle_arc: Arc, left_arc: Arc, right_arc: Arc) -> CircleEvent:
    circumcenter, circumradius = middle_arc.site.find_circumcenter(
        left_arc.site, right_arc.site
    )
    if circumcenter == float("inf"):
        return None
    event_location = Site(circumcenter.x, circumcenter.y + circumradius)
    return CircleEvent(event_location, left_arc, middle_arc, right_arc, circumcenter)


class Test_Beachline(unittest.TestCase):
    def setUp(self) -> None:
        self.beachline = Beachline()

    def test_insert_arc_propagation(self):
        # test insertion and propagation of neighbors and edges
        site1 = Arc(Site(1, 0))
        site2 = Arc(Site(2, 1))
        site3 = Arc(Site(3, 3))
        site4 = Arc(Site(5, 4))
        sites = [site1, site2, site3, site4]

        for site in sites:
            left, middle, right = self.beachline.insert_arc(site)

        reference_order = [site1, site2, site3, site4, site3, site2, site1]
        arc = self.beachline.first_arc
        for reference in reference_order:
            self.assertEqual(arc.site, reference.site)
            arc = arc.right_neighbor

        self.assertEqual(left.left_neighbor.site, site2.site)
        self.assertEqual(left.right_neighbor, middle)
        self.assertEqual(middle.left_neighbor, left)
        self.assertEqual(middle.right_neighbor, right)
        self.assertEqual(right.left_neighbor, middle)
        self.assertEqual(right.right_neighbor.site, site2.site)

        # iterate through the arc linked list to get the second one
        second_arc = self.beachline.first_arc.right_neighbor
        self.beachline.remove_arc(second_arc)
        reference_order = [site1, site3, site4, site3, site2, site1]

        arc = self.beachline.first_arc
        for reference in reference_order:
            self.assertEqual(arc.site, reference.site)
            arc = arc.right_neighbor


if __name__ == "__main__":
    unittest.main()
