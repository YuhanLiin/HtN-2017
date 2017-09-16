from random import randint, random
from bisect import bisect_left

no_op = lambda x:x

def join(lis):
    string = ''
    for s in lis:
        if s != '':
            string += ' ' + s
    return string[1:]

class Many():
    def __init__(self, rule, lo, hi):
        self.rule = rule
        self.low = lo
        self.high = hi

    def generate(self, rule):   # Pass in rule in case a self reference is made
        output = []
        for i in range(randint(self.low, self.high)):
            output.append(self.rule.generate())
        return join(output)

# Can contain strings, Manys, and Rules
class Production():
    def __init__(self, *symbols):
        self.symbols = symbols
        self.pre_proc = no_op

    def generate(self, rule):
        output = []
        for symbol in self.symbols:
            output.append(rule.gen_token(symbol))
        self.pre_proc(output)
        return join(output)

    # Mutates output list on the spot with all symbols rendered
    def set_pre(self, func):
        self.pre_proc = func
        return self


# A rule consists of productions, strings, and Manys.
class Rule():
    @staticmethod
    def declare_all(n):
        return [Rule() for _ in range(n)]

    def __init__(self):
        self.productions = []
        self.post_proc = no_op
        self.distribution = None

    # Defines all productions
    def define(self, *productions):
        self.productions = productions
        return self

    def clone(self):
        copy = Rule()
        copy.productions = self.productions
        copy.post_proc = self.post_proc
        copy.distribution = self.distribution
        return copy

    def transform(self, process):
        self.productions = process(self.productions)
        return self

    def set_post(self, func):
        self.post_proc = func
        return self

    # Takes list of floats that add up to 1 representing chance of each production being generated
    def set_distr(self, distribution):
        self.distribution = []
        prev = 0
        for chance in distribution:
            prev = prev + chance
            self.distribution.append(prev)
        return self

    # # Constraint on the grammar. Int removes production positionally
    # def exclude(self, prod):
    #     if type(prod) == int:
    #         newProd = [self.productions[i] for i in len(self.productions) if i!=prod]
    #     else:
    #         self.productions.remove(prod)
    #     return self

    def decide_prod(self):
        if self.distribution:
            return bisect_left(self.distribution, random())
        return randint(0, len(self.productions) - 1)

    def generate(self):
        production = self.productions[self.decide_prod()]
        if type(production) == Production:
            return self.post_proc(production.generate(self))
        return self.post_proc(self.gen_token(production))

    def gen_token(self, sym):
        if type(sym) == str:
            return sym
        if type(sym) == Many:
            return sym.generate(self)
        return sym.generate()

    def __repr__(self):
        return self.productions.__repr__()