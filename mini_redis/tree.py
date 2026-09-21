# mini_redis/tree.py

class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BinaryTree:
    def __init__(self, root=None):
        self.root = root

    def preorder(self):
        result = []

        def visit(node):
            if node is None:
                return

            result.append(node.data)
            visit(node.left)
            visit(node.right)

        visit(self.root)
        return result

    def inorder(self):
        result = []

        def visit(node):
            if node is None:
                return

            visit(node.left)
            result.append(node.data)
            visit(node.right)

        visit(self.root)
        return result

    def postorder(self):
        result = []

        def visit(node):
            if node is None:
                return

            visit(node.left)
            visit(node.right)
            result.append(node.data)

        visit(self.root)
        return result

    def levelorder(self):
        if self.root is None:
            return []

        queue = [self.root]
        result = []
        index = 0

        while index < len(queue):
            node = queue[index]
            index += 1

            result.append(node.data)

            if node.left:
                queue.append(node.left)

            if node.right:
                queue.append(node.right)

        return result