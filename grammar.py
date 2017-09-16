from random import randint

class Many():
    def __init__(self, rule, lo, hi):
        self.rule = rule
        self.low = lo
        self.high = hi

class Rule():
    Self = object()
    @staticmethod
    def join(lis):
        string = ''
        for s in lis:
            if s != '':
                string += ' ' + s
        return string[1:]
    def __init__(self, *productions):
        self.productions = productions
        self.post_proc = lambda s:s

    def clone(self):
        copy = Rule(*self.productions)
        copy.post_proc = self.post_proc
        return copy

    def transform(self, func):
        copy = self.clone()
        copy.productions = func(self.productions)
        return copy

    def set_post(self, func):
        copy = self.clone()
        copy.post_proc = func
        return copy

    # # Constraint on the grammar. Int removes production positionally
    # def exclude(self, prod):
    #     if type(prod) == int:
    #         newProd = [self.productions[i] for i in len(self.productions) if i!=prod]
    #     else:
    #         self.productions.remove(prod)
    #     return self

    def rule_or_self(self, rule):
        return self if rule == Rule.Self else rule

    def generate(self):
        production = self.productions[randint(0, len(self.productions) - 1)]
        if type(production) == list:
            output = []
            for symbol in production:
                output.append(self.gen_token(symbol))
            return self.post_proc(Rule.join(output))
        return self.post_proc(self.gen_token(production))

    def gen_token(self, sym):
        if type(sym) == str:
            return sym
        if type(sym) == Many:
            output = []
            for i in range(randint(sym.low, sym.high)):
                output.append(self.rule_or_self(sym.rule).generate())
            return Rule.join(output)
        return self.rule_or_self(sym).generate()

    def __repr__(self):
        return self.productions.__repr__()