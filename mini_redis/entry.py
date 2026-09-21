# mini_redis/entry.py

class Entry:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.expire_at = None
        self.lru_node = None

    def memory_size(self):
        return len(self.key.encode("utf-8")) + len(
            self.value.encode("utf-8")
        )