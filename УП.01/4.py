# 04_doubly_linked_list.py
class DNode:
    def __init__(self, val):
        self.val = val; self.next = None; self.prev = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None; self.tail = None

    def insertAfter(self, node, val):   # O(1)
        new = DNode(val)
        new.next = node.next
        new.prev = node
        if node.next: node.next.prev = new
        node.next = new
        if node == self.tail: self.tail = new

    def remove(self, node):             # O(1)
        if node.prev: node.prev.next = node.next
        else: self.head = node.next
        if node.next: node.next.prev = node.prev
        else: self.tail = node.prev

    def __iter__(self):
        cur = self.head
        while cur:
            yield cur.val
            cur = cur.next

# Тест
a = DNode(1); b = DNode(2); c = DNode(3)
dll = DoublyLinkedList()
dll.head = a; a.next = b; b.prev = a; b.next = c; c.prev = b; dll.tail = c

dll.insertAfter(b, 999)
print(list(dll))  # [1, 2, 999, 3]