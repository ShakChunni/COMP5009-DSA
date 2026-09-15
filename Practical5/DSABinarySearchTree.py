from DSATreeNode import DSATreeNode
from DSAQueue import DSAQueue


class DSABinarySearchTree:
    def __init__(self):
        self._root = None
        self._count = 0

    def isEmpty(self):
        return self._root is None

    def count(self):
        return self._count

    def find(self, key):
        return self._findRec(key, self._root)

    def _findRec(self, key, current_node):
        value = None
        if current_node is None:
            raise KeyError("Key " + str(key) + " not found")
        elif key == current_node.getKey():
            value = current_node.getValue()
        elif key < current_node.getKey():
            value = self._findRec(key, current_node.getLeft())
        else:
            value = self._findRec(key, current_node.getRight())
        return value

    def insert(self, key, value):
        self._root = self._insertRec(key, value, self._root)
        self._count += 1

    def _insertRec(self, key, value, current_node):
        update_node = current_node
        if current_node is None:
            update_node = DSATreeNode(key, value)
        elif key == current_node.getKey():
            raise ValueError("Duplicate key: " + str(key))
        elif key < current_node.getKey():
            current_node.setLeft(self._insertRec(key, value, current_node.getLeft()))
        else:
            current_node.setRight(self._insertRec(key, value, current_node.getRight()))
        return update_node

    def delete(self, key):
        self._root = self._deleteRec(key, self._root)
        self._count -= 1

    def _deleteRec(self, key, current_node):
        update_node = current_node
        if current_node is None:
            raise KeyError("Key " + str(key) + " not found")
        elif key == current_node.getKey():
            update_node = self._deleteNode(current_node)
        elif key < current_node.getKey():
            current_node.setLeft(self._deleteRec(key, current_node.getLeft()))
        else:
            current_node.setRight(self._deleteRec(key, current_node.getRight()))
        return update_node

    def _deleteNode(self, delete_node):
        update_node = None
        if delete_node.getLeft() is None and delete_node.getRight() is None:
            update_node = None
        elif delete_node.getLeft() is not None and delete_node.getRight() is None:
            update_node = delete_node.getLeft()
        elif delete_node.getLeft() is None and delete_node.getRight() is not None:
            update_node = delete_node.getRight()
        else:
            update_node = self._promoteSuccessor(delete_node.getRight())
            if update_node != delete_node.getRight():
                update_node.setRight(delete_node.getRight())
            update_node.setLeft(delete_node.getLeft())
        return update_node

    def _promoteSuccessor(self, current_node):
        successor = current_node
        if current_node.getLeft() is not None:
            successor = self._promoteSuccessor(current_node.getLeft())
            if successor == current_node.getLeft():
                current_node.setLeft(successor.getRight())
        return successor

    def min(self):
        if self.isEmpty():
            raise ValueError("Tree is empty")
        return self._minRec(self._root)

    def _minRec(self, current_node):
        if current_node.getLeft() is not None:
            min_key = self._minRec(current_node.getLeft())
        else:
            min_key = current_node.getKey()
        return min_key

    def max(self):
        if self.isEmpty():
            raise ValueError("Tree is empty")
        return self._maxRec(self._root)

    def _maxRec(self, current_node):
        if current_node.getRight() is not None:
            max_key = self._maxRec(current_node.getRight())
        else:
            max_key = current_node.getKey()
        return max_key

    def height(self):
        return self._heightRec(self._root)

    def _heightRec(self, current_node):
        if current_node is None:
            height_so_far = -1
        else:
            left_height = self._heightRec(current_node.getLeft())
            right_height = self._heightRec(current_node.getRight())
            if left_height > right_height:
                height_so_far = left_height + 1
            else:
                height_so_far = right_height + 1
        return height_so_far

    def balance(self):
        if self.isEmpty():
            percentage = 100.0
        else:
            tree_height = self.height()
            if tree_height == 0:
                percentage = 100.0
            else:
                max_nodes = (2 ** (tree_height + 1)) - 1
                percentage = (self._count / max_nodes) * 100.0
        return percentage

    def inorder(self):
        queue = DSAQueue()
        self._inorderRec(self._root, queue)
        return queue

    def _inorderRec(self, current_node, queue):
        if current_node is not None:
            self._inorderRec(current_node.getLeft(), queue)
            queue.enqueue(current_node.getKey())
            self._inorderRec(current_node.getRight(), queue)

    def preorder(self):
        queue = DSAQueue()
        self._preorderRec(self._root, queue)
        return queue

    def _preorderRec(self, current_node, queue):
        if current_node is not None:
            queue.enqueue(current_node.getKey())
            self._preorderRec(current_node.getLeft(), queue)
            self._preorderRec(current_node.getRight(), queue)

    def postorder(self):
        queue = DSAQueue()
        self._postorderRec(self._root, queue)
        return queue

    def _postorderRec(self, current_node, queue):
        if current_node is not None:
            self._postorderRec(current_node.getLeft(), queue)
            self._postorderRec(current_node.getRight(), queue)
            queue.enqueue(current_node.getKey())
