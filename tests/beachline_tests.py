import unittest
import coverage

from utils.avl_tree import AVL_Tree
from utils.beachline import Beachline
from utils.arc import Site, Arc
from utils.events import CircleEvent


class Test_Beachline(unittest.TestCase):
    def setUp(self) -> None:
        self.beachline = Beachline()

    # def test_insert(self):
    #     site = Arc(Site(0, 0))
    #     self.beachline.insert_arc(site, 0)
    #     self.assertEqual(self.beachline.tree.root, site)
    #     site_2 = Arc(Site(1, 10))
    #     self.beachline.insert_arc(site_2, 0)
    #     self.assertEqual(self.beachline.tree.root.right_child, site_2)

    # def test_remove(self):
    #     arc = Arc(Site(0, 0))
    #     self.beachline.insert_arc(arc, 0)
    #     arc_2 = Arc(Site(1, 10))
    #     self.beachline.insert_arc(arc_2, 0)
    #     self.assertEqual(self.beachline.tree.root.right_child, arc_2)
    #     self.beachline.remove_arc(arc)

    #     # need to test against site because internal motion
    #     self.assertEqual(self.beachline.tree.root.site, arc_2.site)

    # def test_intersect(self):
    #     site = Arc(Site(0, 0))
    #     left, middle, right = self.beachline.insert_arc(site, 0)
    #     site_2 = Arc(Site(0, 10))
    #     left_2, middle_2, right_2 = self.beachline.insert_arc(site_2, 2)
    #     self.assertIsNotNone(left_2)
    #     self.assertIsNotNone(middle_2)
    #     self.assertIsNotNone(right_2)
    #     self.assertEqual(self.beachline.intersect_x(left_2, middle_2, 2), 4.0)

    # def test_site_event_processing(self):
    #     site1 = Arc(Site(0, 0))
    #     site2 = Arc(Site(0, 10))

    # def test_circle_event_processing(self):
    #     site1 = Arc(Site(0, 0))
    #     site2 = Arc(Site(20, 10))
    #     site3 = Arc(Site(0, 20))
    #     circumcenter, circumradius = site2.site.find_circumcenter(
    #         site1.site, site3.site
    #     )

    #     # circumcenter = Site(0, 15)
    #     loc_y = circumcenter.y + circumradius
    #     event_location = Site(circumcenter.x, loc_y)

    #     event = CircleEvent(event_location, site1, site2, site3, circumcenter)
    #     self.beachline.handle_circle_event(event)

    def test_insert_arc_propagation(self):
        # test insertion and propagation of neighbors and edges
        site1 = Arc(Site(0, 0))
        site2 = Arc(Site(3, 1))
        site3 = Arc(Site(3, 2))

        left, middle, right = self.beachline.insert_arc(site1, 1)
        print("Left Arc:", left)
        print("Middle Arc:", middle)
        print("Right Arc:", right)
        left, middle, right = self.beachline.insert_arc(site2, 2)
        print("Left Arc:", left)
        print("Middle Arc:", middle)
        print("Right Arc:", right)
        arc = self.beachline.first_arc
        while arc:
            print("Arc:", arc)
            arc = arc.right_neighbor
        left, middle, right = self.beachline.insert_arc(site3, 3)
        print("Left Arc:", left)
        print("Middle Arc:", middle)
        print("Right Arc:", right)
        arc = self.beachline.first_arc
        while arc:
            print("Arc:", arc)
            arc = arc.right_neighbor

        print("Left Neighbor of Left Arc:", left.left_neighbor)
        print("Right Neighbor of Left Arc:", left.right_neighbor)
        print("Left Neighbor of Middle Arc:", middle.left_neighbor)
        print(
            "Right Neighbor of Middle Arc:",
            middle.right_neighbor,
        )
        print("Left Neighbor of Right Arc:", right.left_neighbor)
        print(
            "Right Neighbor of Right Arc:",
            ("None" if right.right_neighbor is None else (right.right_neighbor)),
        )

        self.assertEqual(left.left_neighbor, site2)
        self.assertEqual(left.right_neighbor, middle)
        self.assertEqual(middle.left_neighbor, left)
        self.assertEqual(middle.right_neighbor, right)
        self.assertEqual(right.left_neighbor, middle)
        self.assertEqual(right.right_neighbor, None)

        self.assertEqual(left.left_edge, site2.right_edge)
        self.assertEqual(left.right_edge, middle.left_edge)
        self.assertEqual(middle.left_edge, left.right_edge)
        self.assertEqual(middle.right_edge, right.left_edge)
        self.assertEqual(right.left_edge, middle.right_edge)
        self.assertEqual(right.right_edge, None)


if __name__ == "__main__":
    unittest.main()
