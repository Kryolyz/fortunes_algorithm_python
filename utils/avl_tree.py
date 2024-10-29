from .arc import Arc, Site


class AVL_Tree:
    def __init__(self):
        self.root = None

    def insert(self, root, arc: Arc):
        if not root:
            return arc

        if arc.site.y > root.site.y:
            root.right_child = self.insert(root.right_child, arc)
        else:
            root.left_child = self.insert(root.left_child, arc)

        root.height = 1 + max(
            self.get_height(root.left_child), self.get_height(root.right_child)
        )
        return self.rebalance(root)

    def add_site(self, site: Site):
        self.root = self.insert(self.root, Arc(site))

    def add(self, arc: Arc):
        self.root = self.insert(self.root, arc)

    def delete(self, root, arc: Arc):
        if not root:
            return root
        if arc.site.y < root.site.y:
            root.left_child = self.delete(root.left_child, arc)
        elif arc.site.y > root.site.y:
            root.right_child = self.delete(root.right_child, arc)
        else:
            if not root.left_child or not root.right_child:
                return root.left_child if root.left_child else root.right_child

            temp = self.get_min_value_node(root.right_child)
            root.site = temp.site
            root.right_child = self.delete(root.right_child, temp)

        root.height = 1 + max(
            self.get_height(root.left_child), self.get_height(root.right_child)
        )
        return self.rebalance(root)

    def remove(self, arc: Arc):
        self.root = self.delete(self.root, arc)

    def rotate_left(self, root: Arc):
        new_root = root.right_child
        new_right = root.right_child.left_child

        new_root.left_child = root
        root.right_child = new_right

        root.height = 1 + max(
            self.get_height(root.left_child), self.get_height(root.right_child)
        )
        new_root.height = 1 + max(
            self.get_height(new_root.left_child), self.get_height(new_root.right_child)
        )

        return new_root

    def rotate_right(self, root: Arc):
        new_root = root.left_child
        new_left = root.left_child.right_child

        new_root.right_child = root
        root.left_child = new_left

        root.height = 1 + max(
            self.get_height(root.left_child), self.get_height(root.right_child)
        )
        new_root.height = 1 + max(
            self.get_height(new_root.left_child), self.get_height(new_root.right_child)
        )

        return new_root

    def get_height(self, node: Arc):

        if not node:
            return 0

        return node.height

    def get_balance(self, node: Arc):
        if not node:
            return 0

        return self.get_height(node.left_child) - self.get_height(node.right_child)

    def get_min_value_node(self, node: Arc):
        current = node
        while current.left_child is not None:
            current = current.left_child
        return current

    def rebalance(self, node: Arc):
        balance = self.get_balance(node)

        if balance > 1:
            if self.get_balance(node.left_child) >= 0:
                return self.rotate_right(node)
            else:
                node.left_child = self.rotate_left(node.left_child)
                return self.rotate_right(node)

        if balance < -1:
            if self.get_balance(node.right_child) <= 0:
                return self.rotate_left(node)
            else:
                node.right_child = self.rotate_right(node.right_child)
                return self.rotate_left(node)

        return node

    def get_predecessor(self, node: Arc):
        current = self.root
        predecessor = None
        value = node.site.y if isinstance(node, Arc) else node
        while current:
            if value > current.site.y:
                predecessor = current
                current = current.right
            else:
                current = current.left

        return predecessor

    def get_successor(self, node: Arc):
        current = self.root
        successor = None
        value = node.site.y if isinstance(node, Arc) else node

        while current:
            if value < current.site.y:
                successor = current
                current = current.left
            else:
                current = current.right

        return successor
