# 09_word_frequency_fixed.py
# Полностью рабочая версия частотного словаря на своей HashMap

class HashMap:
    def __init__(self, size=100):
        self.table = [[] for _ in range(size)]
    
    def _hash(self, key):
        h = 0
        for c in str(key):
            h = (h * 31 + ord(c)) % len(self.table)
        return h
    
    def put(self, key, value):
        idx = self._hash(key)
        for pair in self.table[idx]:
            if pair[0] == key:
                pair[1] = value      # обновляем значение
                return
        self.table[idx].append([key, value])
    
    def get(self, key, default=None):
        idx = self._hash(key)
        for pair in self.table[idx]:
            if pair[0] == key:
                return pair[1]
        return default

# ------------------- ЧАСТОТНЫЙ СЛОВАРЬ -------------------
text = ("яблоко банан яблоко апельсин банан банан яблоко "
        "груша яблоко апельсин груша груша груша ананас").lower()

words = text.split()
freq = HashMap()                     # используем только свой HashMap

for word in words:
    current = freq.get(word, 0)
    freq.put(word, current + 1)

# Собираем все пары (частота, слово) и сортируем
all_items = []
for bucket in freq.table:
    for pair in bucket:
        all_items.append((pair[1], pair[0]))   # (частота, слово)

all_items.sort(reverse=True)   # по убыванию частоты

print("Топ-10 самых частых слов:")
for i in range(min(10, len(all_items))):
    count, word = all_items[i]
    print(f"{i+1}. {word} — {count} раз")

# Вывод примера:
# 1. яблоко — 4 раза
# 2. груша — 4 раза
# 3. банан — 3 раза
# 4. апельсин — 2 раза
# ...