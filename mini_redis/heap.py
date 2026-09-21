# mini_redis/heap.py

class MinHeap:
    def __init__(self):
        self.data = []

    def push(self, item):
        self.data.append(item)
        self._heapify_up(len(self.data) - 1)

    def pop(self):
        if not self.data:
            return None

        if len(self.data) == 1:
            return self.data.pop()

        root = self.data[0]
        self.data[0] = self.data.pop()
        self._heapify_down(0)

        return root

    def peek(self):
        return self.data[0] if self.data else None

    def size(self):
        return len(self.data)

    def _heapify_up(self, index):
        while index > 0:
            parent = (index - 1) // 2

            if self.data[parent] <= self.data[index]:
                break

            self.data[parent], self.data[index] = (
                self.data[index],
                self.data[parent],
            )

            index = parent

    def _heapify_down(self, index):
        size = len(self.data)

        while True:
            left = index * 2 + 1
            right = index * 2 + 2
            smallest = index

            if left < size and self.data[left] < self.data[smallest]:
                smallest = left

            if right < size and self.data[right] < self.data[smallest]:
                smallest = right

            if smallest == index:
                break

            self.data[index], self.data[smallest] = (
                self.data[smallest],
                self.data[index],
            )

            index = smallest