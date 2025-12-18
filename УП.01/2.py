# 02_dynamic_array.py
class DynamicArray:
    def __init__(self):
        self.capacity = 1
        self.size = 0
        self.arr = [None] * self.capacity

    def _resize(self, new_cap):
        new_arr = [None] * new_cap
        for i in range(self.size):
            new_arr[i] = self.arr[i]
        self.arr = new_arr
        self.capacity = new_cap

    def pushBack(self, val):        # амортизировано O(1)
        if self.size == self.capacity:
            self._resize(self.capacity * 2)
        self.arr[self.size] = val
        self.size += 1

    def __str__(self): return str(self.arr[:self.size])

# Тест + замер времени
import time
start = time.time()
a = DynamicArray()
for i in range(100_000):
    a.pushBack(i)
print("100000 вставок за", time.time() - start, "сек")
print("Первые 10:", str(a)[:50])