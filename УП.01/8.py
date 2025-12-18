# 08_hashmap.py
class HashMap:
    def __init__(self, size=10):
        self.table = [[] for _ in range(size)]
    def _hash(self, key):
        h = 0
        for c in str(key): h = (h*31 + ord(c)) % len(self.table)
        return h
    def put(self, k, v):
        i = self._hash(k)
        for pair in self.table[i]:
            if pair[0] == k: pair[1] = v; return
        self.table[i].append([k, v])
    def get(self, k, default=None):
        i = self._hash(k)
        for pair in self.table[i]:
            if pair[0] == k: return pair[1]
        return default
    def remove(self, k):
        i = self._hash(k)
        for j, pair in enumerate(self.table[i]):
            if pair[0] == k: del self.table[i][j]

hm = HashMap()
hm.put("age", 25); hm.put("name", "Иван")
print(hm.get("age"))
print(hm.table)