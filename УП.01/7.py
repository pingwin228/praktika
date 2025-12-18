# 07_calculator.py
def infix_to_rpn(expr):
    prec = {'+':1, '-':1, '*':2, '/':2}
    stack = []; out = []
    for t in expr.split():
        if t.isdigit(): out.append(t)
        elif t in prec:
            while stack and stack[-1] in prec and prec[stack[-1]] >= prec[t]:
                out.append(stack.pop())
            stack.append(t)
        elif t == '(': stack.append(t)
        elif t == ')':
            while stack and stack[-1] != '(': out.append(stack.pop())
            stack.pop()
    while stack: out.append(stack.pop())
    return out

def calc_rpn(tokens):
    stack = []
    for t in tokens:
        if t.isdigit(): stack.append(int(t))
        else:
            b, a = stack.pop(), stack.pop()
            if t=='+': stack.append(a+b)
            elif t=='-': stack.append(a-b)
            elif t=='*': stack.append(a*b)
            elif t=='/': stack.append(a/b)
    return stack[0]

expr = "3 + 4 * 2 / ( 1 - 5 )"
rpn = infix_to_rpn(expr)
print("ОПН:", rpn)
print("Результат =", calc_rpn(rpn))   # 2.5