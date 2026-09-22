import numpy as np

from DSAHashEntry import DSAHashEntry


class DSAHashTable:
    def __init__(self, initial_size=11):
        if initial_size < 3:
            initial_size = 3

        self._minimum_size = self._nextPrime(initial_size)
        self._table_size = self._minimum_size
        self._hash_array = self._createArray(self._table_size)
        self._count = 0
        self._upper_threshold = 70
        self._lower_threshold = 20

    def _createArray(self, size):
        hash_array = np.empty(size, dtype=object)
        index = 0
        while index < size:
            hash_array[index] = DSAHashEntry()
            index += 1
        return hash_array

    def _isPrime(self, number):
        if number < 2:
            return False
        if number == 2:
            return True
        if number % 2 == 0:
            return False

        divisor = 3
        prime = True
        while divisor * divisor <= number and prime:
            if number % divisor == 0:
                prime = False
            divisor += 2
        return prime

    def _nextPrime(self, number):
        candidate = number
        if candidate < 3:
            candidate = 3
        if candidate % 2 == 0:
            candidate += 1

        while not self._isPrime(candidate):
            candidate += 2
        return candidate

    def _normaliseKey(self, key):
        if key is None:
            raise ValueError("Key cannot be None")

        key_string = str(key)
        if len(key_string) == 0:
            raise ValueError("Key cannot be empty")
        return key_string

    def _rawHash(self, key):
        key_string = self._normaliseKey(key)
        hash_value = 0
        index = 0

        while index < len(key_string):
            hash_value = (hash_value * 31) + ord(key_string[index])
            index += 1

        return hash_value

    def hash(self, key):
        return self._rawHash(key) % self._table_size

    def _stepHash(self, key):
        return 1 + (self._rawHash(key) % (self._table_size - 1))

    def _probeIndex(self, key, attempt):
        first_index = self.hash(key)
        step_size = self._stepHash(key)
        return (first_index + (attempt * step_size)) % self._table_size

    def _findIndex(self, key):
        key_string = self._normaliseKey(key)
        attempt = 0

        while attempt < self._table_size:
            index = self._probeIndex(key_string, attempt)
            entry = self._hash_array[index]

            if entry.isFree():
                return -1
            if entry.isUsed() and entry.key() == key_string:
                return index

            attempt += 1

        return -1

    def _findInsertionIndex(self, key):
        key_string = self._normaliseKey(key)
        first_tombstone = -1
        attempt = 0

        while attempt < self._table_size:
            index = self._probeIndex(key_string, attempt)
            entry = self._hash_array[index]

            if entry.isUsed():
                if entry.key() == key_string:
                    return index
            elif entry.isPreviouslyUsed():
                if first_tombstone == -1:
                    first_tombstone = index
            else:
                if first_tombstone != -1:
                    return first_tombstone
                return index

            attempt += 1

        return first_tombstone

    def _insertWithoutResize(self, key, value):
        index = self._findInsertionIndex(key)
        if index == -1:
            return False

        entry = self._hash_array[index]
        entry.setKey(key)
        entry.setValue(value)
        entry.setState(DSAHashEntry.USED)
        self._count += 1
        return True

    def _needsGrowth(self):
        return (self._count + 1) * 100 > self._table_size * self._upper_threshold

    def put(self, key, value):
        key_string = self._normaliseKey(key)
        existing_index = self._findIndex(key_string)

        if existing_index != -1:
            self._hash_array[existing_index].setValue(value)
            return

        if self._needsGrowth():
            self.resize(self._table_size * 2)

        inserted = self._insertWithoutResize(key_string, value)
        if not inserted:
            self.resize(self._table_size * 2)
            inserted = self._insertWithoutResize(key_string, value)

        if not inserted:
            raise RuntimeError("Hash table could not insert key")

    def hasKey(self, key):
        return self._findIndex(key) != -1

    def get(self, key):
        index = self._findIndex(key)
        if index == -1:
            raise KeyError("Key not found: " + str(key))
        return self._hash_array[index].value()

    def remove(self, key):
        index = self._findIndex(key)
        if index == -1:
            raise KeyError("Key not found: " + str(key))

        entry = self._hash_array[index]
        entry.setKey(None)
        entry.setValue(None)
        entry.setState(DSAHashEntry.PREVIOUSLY_USED)
        self._count -= 1

        if (self._table_size > self._minimum_size and
                self._count * 100 < self._table_size * self._lower_threshold):
            smaller_size = self._table_size // 2
            if smaller_size < self._minimum_size:
                smaller_size = self._minimum_size
            self.resize(smaller_size)

    def resize(self, requested_size):
        new_size = self._nextPrime(requested_size)
        if new_size < self._minimum_size:
            new_size = self._minimum_size

        while new_size <= self._count:
            new_size = self._nextPrime(new_size * 2)

        old_array = self._hash_array
        old_size = self._table_size
        self._table_size = new_size
        self._hash_array = self._createArray(new_size)
        self._count = 0

        index = 0
        while index < old_size:
            old_entry = old_array[index]
            if old_entry.isUsed():
                inserted = self._insertWithoutResize(
                    old_entry.key(), old_entry.value())
                if not inserted:
                    raise RuntimeError("Hash table rehash failed")
            index += 1

    def clear(self):
        self._table_size = self._minimum_size
        self._hash_array = self._createArray(self._table_size)
        self._count = 0

    def getCount(self):
        return self._count

    def getSize(self):
        return self._table_size

    def loadFactor(self):
        return self._count / self._table_size

    def _loadLine(self, line):
        line_length = len(line)
        while (line_length > 0 and
               (line[line_length - 1] == "\n" or
                line[line_length - 1] == "\r")):
            line_length -= 1

        if line_length == 0:
            return

        comma_index = -1
        index = 0
        while index < line_length and comma_index == -1:
            if line[index] == ",":
                comma_index = index
            else:
                index += 1

        if comma_index == -1:
            raise ValueError("CSV line must contain a comma")

        key = line[:comma_index]
        value = line[comma_index + 1:line_length]
        self.put(key, value)

    def load(self, filename):
        self.clear()
        with open(filename, "r") as input_file:
            line = input_file.readline()
            while line != "":
                self._loadLine(line)
                line = input_file.readline()

    def save(self, filename):
        with open(filename, "w") as output_file:
            index = 0
            while index < self._table_size:
                entry = self._hash_array[index]
                if entry.isUsed():
                    output_file.write(
                        str(entry.key()) + "," + str(entry.value()) + "\n")
                index += 1

    def __str__(self):
        result = ""
        index = 0
        while index < self._table_size:
            result += str(index) + ": " + str(self._hash_array[index]) + "\n"
            index += 1
        return result
