# mini_redis/hashmap.py

class HashNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class HashMap:
    def __init__(self, capacity=8):
        self.capacity = max(1, capacity)
        self.buckets = [None] * self.capacity
        self._size = 0

    def _hash(self, key):
        value = 0

        for char in key:
            value = (value * 31 + ord(char)) & 0xFFFFFFFF

        return value

    def _index(self, key):
        return self._hash(key) % self.capacity

    def put(self, key, value):
        index = self._index(key)
        current = self.buckets[index]

        while current:
            if current.key == key:
                current.value = value
                return current

            current = current.next

        node = HashNode(key, value)
        node.next = self.buckets[index]

        if self.buckets[index]:
            self.buckets[index].prev = node

        self.buckets[index] = node
        self._size += 1

        if self._size / self.capacity > 0.75:
            self._resize()

        return node

    def get(self, key):
        node = self._find_node(key)
        return node.value if node else None

    def get_node(self, key):
        return self._find_node(key)

    def remove(self, key):
        node = self._find_node(key)

        if node is None:
            return None

        self._unlink(node)
        return node.value

    def contains(self, key):
        return self._find_node(key) is not None

    def keys(self):
        result = []

        for bucket in self.buckets:
            current = bucket

            while current:
                result.append(current.key)
                current = current.next

        return result

    def size(self):
        return self._size

    def _find_node(self, key):
        index = self._index(key)
        current = self.buckets[index]

        while current:
            if current.key == key:
                return current

            current = current.next

        return None

    def _unlink(self, node):
        index = self._index(node.key)

        if node.prev:
            node.prev.next = node.next
        else:
            self.buckets[index] = node.next

        if node.next:
            node.next.prev = node.prev

        node.prev = None
        node.next = None
        self._size -= 1

    def _resize(self):
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [None] * self.capacity

        for bucket in old_buckets:
            current = bucket

            while current:
                next_node = current.next

                current.prev = None
                current.next = None

                index = self._index(current.key)
                current.next = self.buckets[index]

                if self.buckets[index]:
                    self.buckets[index].prev = current

                self.buckets[index] = current
                current = next_node