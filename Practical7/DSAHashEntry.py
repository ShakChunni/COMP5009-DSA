class DSAHashEntry:
    """A single slot in a hash table.

    Each slot holds the key, the value and a state that tells us what the
    slot means:

        FREE             - the slot has never been used
        USED             - the slot currently holds a key/value pair
        PREVIOUSLY_USED  - a pair was here but was removed (a "tombstone").
                           We cannot mark this slot FREE again, because
                           removing it would break the probing chain of keys
                           that probed past this slot to reach a later slot.
    """

    FREE = 0
    USED = 1
    PREVIOUSLY_USED = 2

    def __init__(self, key=None, value=None, state=FREE):
        self._key = key
        self._value = value
        self._state = state

    def isFree(self):
        return self._state == DSAHashEntry.FREE

    def isUsed(self):
        return self._state == DSAHashEntry.USED

    def isPreviouslyUsed(self):
        return self._state == DSAHashEntry.PREVIOUSLY_USED

    def isOccupied(self):
        return self._state != DSAHashEntry.FREE

    def key(self):
        return self._key

    def value(self):
        return self._value

    def setKey(self, key):
        self._key = key

    def setValue(self, value):
        self._value = value

    def setState(self, state):
        self._state = state

    def __str__(self):
        if self._state == DSAHashEntry.FREE:
            return "[FREE]"
        if self._state == DSAHashEntry.PREVIOUSLY_USED:
            return "[tombstone]"
        return "[USED] key={0} value={1}".format(self._key, self._value)
