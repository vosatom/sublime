import ast
import operator as op
import functools
import math
import urllib.request

from re import sub

class ShouldAskWolfram(Exception):
    pass

API_KEY = ""

# supported operators
operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
             ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor,
             ast.USub: op.neg }

def ask_wolfram(question):
    return int(urllib.request.urlopen("https://api.wolframalpha.com/v1/result?i={question}&appid={api}".format(question = question, api = API_KEY)).read())

def eval_expr(expr):
    """
    >>> eval_expr('2^6')
    4
    >>> eval_expr('2**6')
    64
    >>> eval_expr('1 + 2*3**(4^5) / (6 + -7)')
    -5.0
    """

    expr = sub(r'(\d+)!', r'F(\1)', expr)
    expr = sub(r's1\(', 'StirlingS1(', expr)
    expr = sub(r's2\(', 'StirlingS2(', expr)
    try:
        return eval_(ast.parse(expr, mode='eval').body)
    except ShouldAskWolfram as e:
        return ask_wolfram(expr)

def F(n) -> int:
    if n.n > 20:
        raise ShouldAskWolfram("Too big n")
    return math.factorial(n.n)

def gcd(a, b) -> int:
    a = a.n
    b = b.n
    if a > 50000 or b > 50000:
        raise ShouldAskWolfram("Too big a or b")
    while b:
        a, b = b, a%b
    return a

def StirlingS1(i, n) -> int:
    raise ShouldAskWolfram()

def StirlingS2(i, n) -> int:
    raise ShouldAskWolfram()

def _binomial_cooefficient(n: int, k: int) -> int:
    n_fac = math.factorial(n)
    k_fac = math.factorial(k)
    n_minus_k_fac = math.factorial(n - k)
    return n_fac/(k_fac*n_minus_k_fac)

def binomial_cooefficient(n, k) -> int:
    if n.n > 20 or k.n > 20:
        raise ShouldAskWolfram("Too big n or k")
    return _binomial_cooefficient(n.n, k.n)

def eval_(node):
    # print(dir(node))
    if isinstance(node, ast.Call): # <number>
        # print(node.func.id)
        if node.func.id == "C":
            return binomial_cooefficient(*node.args)
        elif node.func.id == "F":
            return F(*node.args)
        elif node.func.id == "gcd":
            return gcd(*node.args)
        elif node.func.id == "StirlingS1":
            return StirlingS1(*node.args)
        elif node.func.id == "StirlingS1":
            return StirlingS1(*node.args)
        else:
            raise NameError("name '{name}' is not defined".format(name = node.func.id))
    elif isinstance(node, ast.Num): # <number>
        return node.n
    elif isinstance(node, ast.BinOp): # <left> <operator> <right>
        return operators[type(node.op)](eval_(node.left), eval_(node.right))
    elif isinstance(node, ast.UnaryOp): # <operator> <operand> e.g., -1
        return operators[type(node.op)](eval_(node.operand))
    elif isinstance(node, ast.Name): # <operator> <operand> e.g., -1
        return node.id
    else:
        # print(dir(node))
        raise TypeError('unsupported expression')

# def power(a, b):
#     if any(abs(n) > 100 for n in [a, b]):
#         raise ValueError((a,b))
#     return op.pow(a, b)
# operators[ast.Pow] = power

def limit(max_=None):
    """Return decorator that limits allowed returned values."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            ret = func(*args, **kwargs)
            try:
                mag = abs(ret)
            except TypeError:
                pass # not applicable
            else:
                if mag > max_:
                    raise ValueError(ret)
            return ret
        return wrapper
    return decorator

eval_ = limit(max_=10**10)(eval_)



# def test():
#     # print(eval_expr("C(5,3)"))
    # print(eval_expr("C(6,5)"))

# print(eval_expr("4!"))