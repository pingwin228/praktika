# 11_bst.py
class Node:
    def __init__(self, v): self.v = v; self.l = self.r = None

class BST:
    def __init__(self): self.root = None
    def insert(self, v):
        if not self.root: self.root = Node(v); return
        cur = self.root
        while True:
            if v < cur.v:
                if cur.l: cur = cur.l
                else: cur.l = Node(v); return
            else:
                if cur.r: cur = cur.r
                else: cur.r = Node(v); return
    def inorder(self):
        res = []
        def go(n): 
            if n: go(n.l); res.append(n.v); go(n.r)
        go(self.root)
        return res

tree = BST()
for x in [50,30,70,20,40,60,80]: tree.insert(x)
print(tree.inorder())