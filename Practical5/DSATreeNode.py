class DSATreeNode:
    def __init__(self, key, value):
        if key is None:
            raise ValueError("Key cannot be None")
        self._key = key
        self._value = value
        self._left = None
        self._right = None

    def getKey(self):
        return self._key

    def getValue(self):
        return self._value

    def setValue(self, value):
        self._value = value

    def getLeft(self):
        return self._left

    def setLeft(self, new_left):
        self._left = new_left

    def getRight(self):
        return self._right

    def setRight(self, new_right):
        self._right = new_right

    def __str__(self):
        return "Key: " + str(self._key) + " Value: " + str(self._value)
