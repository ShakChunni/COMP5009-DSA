class DSATreeNode:
    def __init__(self, inKey, inValue):
        if inKey is None:
            raise ValueError("Key cannot be None")
        self._key = inKey
        self._value = inValue
        self._left = None
        self._right = None

    def getKey(self):
        return self._key

    def getValue(self):
        return self._value

    def setValue(self, inValue):
        self._value = inValue

    def getLeft(self):
        return self._left

    def setLeft(self, newLeft):
        self._left = newLeft

    def getRight(self):
        return self._right

    def setRight(self, newRight):
        self._right = newRight

    def __str__(self):
        return "Key: " + str(self._key) + " Value: " + str(self._value)
