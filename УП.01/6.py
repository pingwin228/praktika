# 06_queues.py
# 1) Циклическая очередь
class CircularQueue:
    def __init__(self, cap=5):
        self.q = [None]*cap; self.front = self.rear = -1; self.size = 0; self.cap = cap
    def enqueue(self, x):
        if self.size == self.cap: print("Full"); return
        if self.front == -1: self.front = 0
        self.rear = (self.rear + 1) % self.cap
        self.q[self.rear] = x; self.size += 1
    def dequeue(self):
        if self.size == 0: return None
        val = self.q[self.front]
        self.front = (self.front + 1) % self.cap
        self.size -= 1
        return val

# 2) Очередь на двух стеках
class QueueTwoStacks:
    def __init__(self):
        self.inp = []; self.out = []
    def enqueue(self, x): self.inp.append(x)
    def dequeue(self):
        if not self.out:
            while self.inp: self.out.append(self.inp.pop())
        return self.out.pop() if self.out else None

q = QueueTwoStacks()
for i in range(5): q.enqueue(i)
print([q.dequeue() for _ in range(5)])  # [0,1,2,3,4]