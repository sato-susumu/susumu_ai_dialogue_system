import threading
from collections import deque


class LimitedFIFO:
    def __init__(self, maxsize):
        self.buffer = deque(maxlen=maxsize)

    def is_empty(self):
        with threading.Lock():
            return len(self.buffer) == 0

    def put(self, data):
        with threading.Lock():
            self.buffer.append(data)

    def get(self):
        with threading.Lock():
            if len(self.buffer) > 0:
                return self.buffer.popleft()
            else:
                return None
