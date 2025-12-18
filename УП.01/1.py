# 01_static_array.py
class StaticArray:
    def __init__(self, capacity=10):
        self.array = [None] * capacity
        self.size = 0

    def pushBack(self, value):      # O(1)
        if self.size == len(self.array): raise OverflowError("Переполнен")
        self.array[self.size] = value; self.size += 1

    def pushFront(self, value):     # O(n)
        if self.size == len(self.array): raise OverflowError("Переполнен")
        for i in range(self.size, 0, -1): self.array[i] = self.array[i-1]
        self.array[0] = value; self.size += 1

    def insert(self, index, value): # O(n)
        if index < 0 or index > self.size: raise IndexError()
        if self.size == len(self.array): raise OverflowError()
        for i in range(self.size, index, -1): self.array[i] = self.array[i-1]
        self.array[index] = value; self.size += 1

    def remove(self, index):        # O(n)
        if index < 0 or index >= self.size: raise IndexError()
        for i in range(index, self.size-1): self.array[i] = self.array[i+1]
        self.size -= 1

    def find(self, value):          # O(n)
        for i in range(self.size):
            if self.array[i] == value: return i
        return -1

    def __str__(self): return str(self.array[:self.size])

# Тест
arr = StaticArray(10)
arr.pushBack(11); arr.pushBack(22); arr.pushBack(33)
arr.pushFront(0)
arr.insert(2, 999)
arr.remove(1)
print(arr)
print("find 22 →", arr.find(22))