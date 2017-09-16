from random import randint, random
from bisect import bisect_left

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
            output.append(rule.rule_or_self(self.rule).generate())
        return join(output)

class Rule():
    Self = object()
    def __init__(self, *productions):
        self.productions = productions
        self.post_proc = lambda s:s
        self.distribution = None

    def clone(self):
        copy = Rule(*self.productions)
        copy.post_proc = self.post_proc
        return copy

    def transform(self, func):
        self.productions = func(self.productions)
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

    def rule_or_self(self, rule):
        return self if rule == Rule.Self else rule

    def generate(self):
        production = self.productions[self.decide_prod()]
        if type(production) == list:
            output = []
            for symbol in production:
                output.append(self.gen_token(symbol))
            return self.post_proc(join(output))
        return self.post_proc(self.gen_token(production))

    def gen_token(self, sym):
        if type(sym) == str:
            return sym
        if type(sym) == Many:
            return sym.generate(self)
        return self.rule_or_self(sym).generate()

    def __repr__(self):
        return self.productions.__repr__()