class DSAHashEntry:
    FREE = 0
    USED = 1
    DELETED = 2

    def __init__(self):
        self.key = None
        self.value = None
        self.state = self.FREE
