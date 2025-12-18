# 10_trie_autocomplete.py
class TrieNode:
    def __init__(self):
        self.children = {}
        self.freq = 0
        self.is_end = False

class Trie:
    def __init__(self): self.root = TrieNode()
    def insert(self, word, freq=1):
        node = self.root
        for c in word:
            if c not in node.children: node.children[c] = TrieNode()
            node = node.children[c]
        node.is_end = True; node.freq = freq
    def autocomplete(self, prefix):
        node = self.root
        for c in prefix:
            if c not in node.children: return []
            node = node.children[c]
        res = []
        def dfs(n, path):
            if n.is_end: res.append((n.freq, path))
            for c,ch in n.children.items():
                dfs(ch, path+c)
        dfs(node, prefix)
        res.sort(reverse=True)
        return [word for freq,word in res]

t = Trie()
words = [("яблоко",100), ("яблоко",50), ("яблоня",30), ("ящерица",10)]
for w,f in words: t.insert(w,f)
print(t.autocomplete("ябл"))   # ['яблоко', 'яблоко', 'яблоня']