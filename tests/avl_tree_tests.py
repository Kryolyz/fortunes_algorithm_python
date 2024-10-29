import unittest
import coverage

# cov = coverage.Coverage()
# cov.start()

from utils.avl_tree import AVL_Tree
from utils.arc import Site, Arc


class TestAVL_Tree(unittest.TestCase):
    def setUp(self):
        self.tree = AVL_Tree()

    def test_add(self):
        self.tree.add_site(Site(10, 10))
        self.tree.add_site(Site(20, 20))
        self.tree.add_site(Site(30, 30))
        self.assertEqual(self.tree.root.site.y, 20)
        self.assertEqual(self.tree.root.left_child.site.y, 10)
        self.assertEqual(self.tree.root.right_child.site.y, 30)

    def test_left_rotate(self):
        root = Arc(Site(10, 10))
        root.right_child = Arc(Site(20, 20))
        root.right_child.right_child = Arc(Site(30, 30))
        new_root = self.tree.rotate_left(root)
        self.assertEqual(new_root.site.y, 20)
        self.assertEqual(new_root.left_child.site.y, 10)
        self.assertEqual(new_root.right_child.site.y, 30)

    def test_right_rotate(self):
        root = Arc(Site(30, 30))
        root.left_child = Arc(Site(20, 20))
        root.left_child.left_child = Arc(Site(10, 10))
        new_root = self.tree.rotate_right(root)
        self.assertEqual(new_root.site.y, 20)
        self.assertEqual(new_root.left_child.site.y, 10)
        self.assertEqual(new_root.right_child.site.y, 30)

    def test_get_height(self):
        self.tree.add_site(Site(10, 10))
        self.tree.add_site(Site(5, 5))
        self.assertEqual(self.tree.get_height(self.tree.root), 2)
        self.tree.add_site(Site(15, 15))
        self.assertEqual(self.tree.get_height(self.tree.root), 2)

    def test_get_balance(self):
        self.tree.add_site(Site(10, 10))
        self.tree.add_site(Site(5, 5))
        self.tree.add_site(Site(15, 15))
        self.assertEqual(self.tree.get_balance(self.tree.root), 0)
        self.tree.add_site(Site(2, 2))
        self.assertEqual(self.tree.get_balance(self.tree.root), 1)

    def test_more_balancing(self):
        self.tree.add_site(Site(0, 4))
        self.tree.add_site(Site(0, 2))
        self.tree.add_site(Site(0, 18))
        self.tree.add_site(Site(0, 5))
        self.tree.add_site(Site(0, 12))

    def test_delete(self):
        self.tree.add_site(Site(0, 10))
        self.tree.add_site(Site(0, 5))
        self.tree.add_site(Site(0, 15))
        self.tree.add_site(Site(0, 20))
        self.tree.add_site(Site(0, 3))
        self.tree.add_site(Site(0, 12))
        self.tree.add_site(Site(0, 18))

        self.tree.remove(Arc(Site(0, 5)))
        self.assertEqual(self.tree.root.site.y, 15)
        self.assertEqual(self.tree.root.left_child.site.y, 10)
        self.assertEqual(self.tree.root.right_child.site.y, 20)

        self.tree.remove(Arc(Site(0, 10)))
        self.assertEqual(self.tree.root.site.y, 15)
        self.assertEqual(self.tree.root.left_child.site.y, 12)
        self.assertEqual(self.tree.root.right_child.site.y, 20)

        self.tree.remove(Arc(Site(0, 15)))
        self.assertEqual(self.tree.root.site.y, 18)
        self.assertEqual(self.tree.root.left_child.site.y, 12)
        self.assertEqual(self.tree.root.right_child.site.y, 20)

        self.tree.remove(Arc(Site(0, 12)))
        self.assertEqual(self.tree.root.site.y, 18)
        self.assertEqual(self.tree.root.left_child.site.y, 3)
        self.assertEqual(self.tree.root.right_child.site.y, 20)

        self.tree.remove(Arc(Site(0, 3)))
        self.assertEqual(self.tree.root.site.y, 18)
        self.assertEqual(self.tree.root.left_child, None)
        self.assertEqual(self.tree.root.right_child.site.y, 20)

        self.tree.remove(Arc(Site(0, 18)))
        self.assertEqual(self.tree.root.site.y, 20)

    def test_circumcenter_calculation(self):
        self.A = Site(0, 0)
        self.B = Site(4, 0)
        self.C = Site(0, 3)
        expected_circumcenter = Site(2, 1.5)
        calculated_circumcenter, circumradius = self.A.find_circumcenter(self.B, self.C)

        self.assertAlmostEqual(expected_circumcenter.x, calculated_circumcenter.x)
        self.assertAlmostEqual(expected_circumcenter.y, calculated_circumcenter.y)


if __name__ == "__main__":
    unittest.main()
