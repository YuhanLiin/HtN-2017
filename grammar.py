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

    def generate(self):   # Pass in rule in case a self reference is made
        output = []
        for i in range(randint(self.low, self.high)):
            output.append(self.rule.generate())
        return join(output)

def maybe(rule):
    return Many(rule, 0, 1)

# Can contain strings, Manys, and Rules
class Production():
    def __init__(self, *symbols):
        self.symbols = symbols
        self.pre_procs = []

    def generate(self):
        output = []
        for symbol in self.symbols:
            output.append(gen_token(symbol))
        for proc in self.pre_procs:
            proc(output)
        return join(output)

    # Mutates output list on the spot with all symbols rendered
    def add_pre(self, func):
        self.pre_procs.append(func)
        return self


# A rule consists of productions, strings, and Manys.
class Rule():
    @staticmethod
    def declare_all(n):
        return [Rule() for _ in range(n)]

    def __init__(self):
        self.productions = []
        self.post_procs = []
        self.distribution = None

    # Defines all productions
    def define(self, *productions):
        self.productions = productions
        return self

    def clone(self):
        copy = Rule()
        copy.productions = self.productions
        copy.post_procs = self.post_procs
        copy.distribution = self.distribution
        return copy

    def transform(self, process):
        self.productions = process(self.productions)
        return self

    def add_post(self, func):
        self.post_procs.append(func)
        return self

    # Takes list of floats that add up to 1 representing chance of each production being generated
    def set_distr(self, *distribution):
        self.distribution = []
        prev = 0
        for chance in distribution:
            prev = prev + chance
            self.distribution.append(prev)
        return self

    def decide_prod(self):
        if self.distribution:
            return bisect_left(self.distribution, random())
        return randint(0, len(self.productions) - 1)

    def generate(self):
        production = self.productions[self.decide_prod()]
        if type(production) == Production:
            output = production.generate()
        else:
            output = gen_token(production)
        for proc in self.post_procs:
            output = proc(output)
        return output

    def __repr__(self):
        return self.productions.__repr__()

def gen_token(sym):
    if type(sym) == str:
        return sym
    if type(sym) == Many:
        return sym.generate()
    return sym.generate()