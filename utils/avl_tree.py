from .arc import Arc


class AVL_Tree:
    def __init__(self):
        self.root = None

    def insert(self, root, site):
        if not root:
            return Arc(site)

        if site.y > root.site.y:
            root.right = self.insert(root.right, site)
        else:
            root.left = self.insert(root.left, site)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        return self.rebalance(root)

    def add(self, site):
        self.root = self.insert(self.root, site)

    def delete(self, root, site):
        if not root:
            return root

        if site.y < root.site.y:
            root.left = self.delete(root.left, site)
        elif site.y > root.site.y:
            root.right = self.delete(root.right, site)
        else:
            if not root.left:
                return root.right
            elif not root.right:
                return root.left

            temp = self.get_min_value_node(root.right)
            root.site = temp.site
            root.right = self.delete(root.right, temp.site)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        return self.rebalance(root)

    def remove(self, site):
        self.root = self.delete(self.root, site)

    def rotate_left(self, root):

        new_root = root.right
        new_right = root.right.left

        new_root.left = root
        root.right = new_right

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        new_root.height = 1 + max(
            self.get_height(new_root.left), self.get_height(new_root.right)
        )

        return new_root

    def rotate_right(self, root):
        new_root = root.left
        new_left = root.left.right

        new_root.right = root
        root.left = new_left

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        new_root.height = 1 + max(
            self.get_height(new_root.left), self.get_height(new_root.right)
        )

        return new_root

    def get_height(self, node: Arc):
        if not node:
            return 0

        return node.height

    def get_balance(self, node: Arc):
        if not node:
            return 0

        return self.get_height(node.left) - self.get_height(node.right)

    def get_min_value_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def rebalance(self, node):
        balance = self.get_balance(node)

        if balance > 1:
            if self.get_balance(node.left) >= 0:
                return self.rotate_right(node)
            else:
                node.left = self.rotate_left(node.left)
                return self.rotate_right(node)

        if balance < -1:
            if self.get_balance(node.right) <= 0:
                return self.rotate_left(node)
            else:
                node.right = self.rotate_right(node.right)
                return self.rotate_left(node)

        return node
