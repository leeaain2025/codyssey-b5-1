class DynamicArray:
    def __init__(self, capacity=4):
        self.capacity = max(1, capacity)
        self.size = 0
        self.data = [None] * self.capacity

    def append(self, value):
        if self.size == self.capacity:
            self._resize(self.capacity * 2)

        self.data[self.size] = value
        self.size += 1

    def get(self, index):
        self._check_index(index)
        return self.data[index]

    def set(self, index, value):
        self._check_index(index)
        self.data[index] = value

    def remove(self, index):
        self._check_index(index)

        value = self.data[index]

        for i in range(index, self.size - 1):
            self.data[i] = self.data[i + 1]

        self.data[self.size - 1] = None
        self.size -= 1

        return value

    def _resize(self, capacity):
        new_data = [None] * capacity

        for i in range(self.size):
            new_data[i] = self.data[i]

        self.data = new_data
        self.capacity = capacity

    def _check_index(self, index):
        if index < 0 or index >= self.size:
            raise IndexError("index out of range")

    def __len__(self):
        return self.size