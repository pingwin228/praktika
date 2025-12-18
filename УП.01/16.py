# 16_priority_queue.py
from min_heap import MinHeap


class PriorityQueue:
    def __init__(self): self.heap = MinHeap()
    def push(self, val, prio): self.heap.insert((prio, val))
    def pop(self):
        if not self.heap.h: return None
        return self.heap.extract_min()[1]

pq = PriorityQueue()
pq.push("низкий", 3)
pq.push("высокий", 1)
pq.push("средний", 2)
print(pq.pop())  # высокий
print(pq.pop())  # средний
print(pq.pop())  # низкий