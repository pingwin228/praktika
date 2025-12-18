# 15_min_heap.py
class MinHeap:
    def __init__(self): self.h = []
    def insert(self, x):
        self.h.append(x)
        i = len(self.h)-1
        while i > 0:
            p = (i-1)//2
            if self.h[i] < self.h[p]:
                self.h[i], self.h[p] = self.h[p], self.h[i]
                i = p
            else: break
    def extract_min(self):
        if not self.h: return None
        mn = self.h[0]
        self.h[0] = self.h[-1]; self.h.pop()
        i = 0
        while True:
            l = 2*i+1; r = 2*i+2; small = i
            if l < len(self.h) and self.h[l] < self.h[small]: small = l
            if r < len(self.h) and self.h[r] < self.h[small]: small = r
            if small == i: break
            self.h[i], self.h[small] = self.h[small], self.h[i]
            i = small
        return mn

heap = MinHeap()
for x in [5,3,8,1,4]: heap.insert(x)
print([heap.extract_min() for _ in range(5)])  # [1,3,4,5,8]