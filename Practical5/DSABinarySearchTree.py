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

    def _findRec(self, key, cur):
        value = None
        if cur is None:
            raise KeyError("Key " + str(key) + " not found")
        elif key == cur.getKey():
            value = cur.getValue()
        elif key < cur.getKey():
            value = self._findRec(key, cur.getLeft())
        else:
            value = self._findRec(key, cur.getRight())
        return value

    def insert(self, key, value):
        self._root = self._insertRec(key, value, self._root)
        self._count += 1

    def _insertRec(self, key, value, cur):
        updateNode = cur
        if cur is None:
            updateNode = DSATreeNode(key, value)
        elif key == cur.getKey():
            raise ValueError("Duplicate key: " + str(key))
        elif key < cur.getKey():
            cur.setLeft(self._insertRec(key, value, cur.getLeft()))
        else:
            cur.setRight(self._insertRec(key, value, cur.getRight()))
        return updateNode

    def delete(self, key):
        self._root = self._deleteRec(key, self._root)
        self._count -= 1

    def _deleteRec(self, key, cur):
        updateNode = cur
        if cur is None:
            raise KeyError("Key " + str(key) + " not found")
        elif key == cur.getKey():
            updateNode = self._deleteNode(cur)
        elif key < cur.getKey():
            cur.setLeft(self._deleteRec(key, cur.getLeft()))
        else:
            cur.setRight(self._deleteRec(key, cur.getRight()))
        return updateNode

    def _deleteNode(self, delNode):
        updateNode = None
        if delNode.getLeft() is None and delNode.getRight() is None:
            updateNode = None
        elif delNode.getLeft() is not None and delNode.getRight() is None:
            updateNode = delNode.getLeft()
        elif delNode.getLeft() is None and delNode.getRight() is not None:
            updateNode = delNode.getRight()
        else:
            updateNode = self._promoteSuccessor(delNode.getRight())
            if updateNode != delNode.getRight():
                updateNode.setRight(delNode.getRight())
            updateNode.setLeft(delNode.getLeft())
        return updateNode

    def _promoteSuccessor(self, cur):
        successor = cur
        if cur.getLeft() is not None:
            successor = self._promoteSuccessor(cur.getLeft())
            if successor == cur.getLeft():
                cur.setLeft(successor.getRight())
        return successor

    def min(self):
        if self.isEmpty():
            raise ValueError("Tree is empty")
        return self._minRec(self._root)

    def _minRec(self, cur):
        if cur.getLeft() is not None:
            minKey = self._minRec(cur.getLeft())
        else:
            minKey = cur.getKey()
        return minKey

    def max(self):
        if self.isEmpty():
            raise ValueError("Tree is empty")
        return self._maxRec(self._root)

    def _maxRec(self, cur):
        if cur.getRight() is not None:
            maxKey = self._maxRec(cur.getRight())
        else:
            maxKey = cur.getKey()
        return maxKey

    def height(self):
        return self._heightRec(self._root)

    def _heightRec(self, cur):
        if cur is None:
            htSoFar = -1
        else:
            leftHt = self._heightRec(cur.getLeft())
            rightHt = self._heightRec(cur.getRight())
            if leftHt > rightHt:
                htSoFar = leftHt + 1
            else:
                htSoFar = rightHt + 1
        return htSoFar

    def balance(self):
        if self.isEmpty():
            percentage = 100.0
        else:
            h = self.height()
            if h == 0:
                percentage = 100.0
            else:
                maxNodes = (2 ** (h + 1)) - 1
                percentage = (self._count / maxNodes) * 100.0
        return percentage

    def inorder(self):
        queue = DSAQueue()
        self._inorderRec(self._root, queue)
        return queue

    def _inorderRec(self, cur, queue):
        if cur is not None:
            self._inorderRec(cur.getLeft(), queue)
            queue.enqueue(cur.getKey())
            self._inorderRec(cur.getRight(), queue)

    def preorder(self):
        queue = DSAQueue()
        self._preorderRec(self._root, queue)
        return queue

    def _preorderRec(self, cur, queue):
        if cur is not None:
            queue.enqueue(cur.getKey())
            self._preorderRec(cur.getLeft(), queue)
            self._preorderRec(cur.getRight(), queue)

    def postorder(self):
        queue = DSAQueue()
        self._postorderRec(self._root, queue)
        return queue

    def _postorderRec(self, cur, queue):
        if cur is not None:
            self._postorderRec(cur.getLeft(), queue)
            self._postorderRec(cur.getRight(), queue)
            queue.enqueue(cur.getKey())
