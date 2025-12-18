# 12_trie_advanced.py
# используем класс Trie из задания 10
# добавляем удаление и подсчёт слов по префиксу
from trie import Trie


def count_words_with_prefix(self, prefix):
    node = self.root
    for c in prefix:
        if c not in node.children: return 0
        node = node.children[c]
    def count(n):
        total = 1 if n.is_end else 0
        for ch in n.children.values(): total += count(ch)
        return total
    return count(node)

Trie.count_words_with_prefix = count_words_with_prefix