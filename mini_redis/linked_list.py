class Node:
    def __init__(self, data):
        self.prev = None
        self.next = None
        self.data = data


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def insert_front(self, data):
        node = Node(data)

        if self.head is None:
            self.head = self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node

        self._size += 1
        return node

    def insert_back(self, data):
        node = Node(data)

        if self.tail is None:
            self.head = self.tail = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node

        self._size += 1
        return node

    def remove_front(self):
        if self.head is None:
            return None

        node = self.head
        self._remove(node)
        return node.data

    def remove_back(self):
        if self.tail is None:
            return None

        node = self.tail
        self._remove(node)
        return node.data

    def remove_node(self, node):
        if node is None:
            return None

        data = node.data
        self._remove(node)
        return data

    def _remove(self, node):
        if node.prev:
            node.prev.next = node.next
        else:
            self.head = node.next

        if node.next:
            node.next.prev = node.prev
        else:
            self.tail = node.prev

        node.prev = None
        node.next = None
        self._size -= 1

    def move_to_front(self, node):
        if node is None or node is self.head:
            return

        if node.prev:
            node.prev.next = node.next

        if node.next:
            node.next.prev = node.prev

        if node is self.tail:
            self.tail = node.prev

        node.prev = None
        node.next = self.head

        if self.head:
            self.head.prev = node

        self.head = node

    def size(self):
        return self._size

    def values(self):
        result = []
        current = self.head

        while current:
            result.append(current.data)
            current = current.next

        return result