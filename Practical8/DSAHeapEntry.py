class DSAHeapEntry:
    def __init__(self, priority, value):
        self._priority = priority
        self._value = value

    def getPriority(self):
        return self._priority

    def setPriority(self, priority):
        self._priority = priority

    def getValue(self):
        return self._value

    def setValue(self, value):
        self._value = value
