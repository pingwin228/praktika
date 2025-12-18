# 05_stack.py
class Stack:
    def __init__(self): self.s = []
    def push(self, x): self.s.append(x)
    def pop(self): return self.s.pop() if self.s else None
    def peek(self): return self.s[-1] if self.s else None

def check_brackets(text):
    st = Stack()
    pairs = {')':'(', ']':'[', '}':'{'}
    for c in text:
        if c in '([{': st.push(c)
        elif c in ')]}':
            if not st.s or st.pop() != pairs[c]:
                return False
    return len(st.s) == 0

print(check_brackets("(([]){})"))  # True
print(check_brackets("([)]"))      # False