# 03_singly_linked_list.py
class Node:
    def __init__(self, val): self.val = val; self.next = None

class SinglyLinkedList:
    def __init__(self): self.head = None

    def pushFront(self, val):       # O(1)
        n = Node(val); n.next = self.head; self.head = n

    def pushBack(self, val):        # O(n)
        n = Node(val)
        if not self.head: self.head = n; return
        cur = self.head
        while cur.next: cur = cur.next
        cur.next = n

    def remove(self, val):          # O(n)
        if not self.head: return
        if self.head.val == val: self.head = self.head.next; return
        cur = self.head
        while cur.next and cur.next.val != val: cur = cur.next
        if cur.next: cur.next = cur.next.next

    def reverse(self):              # O(n)
        prev = None
        cur = self.head
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        self.head = prev

    def __str__(self):
        vals = []
        cur = self.head
        while cur: vals.append(str(cur.val)); cur = cur.next
        return " → ".join(vals)

# Тест
lst = SinglyLinkedList()
for x in [3,2,1]: lst.pushFront(x)
lst.pushBack(4)
print(lst)
lst.reverse()
print("После разворота:", lst)