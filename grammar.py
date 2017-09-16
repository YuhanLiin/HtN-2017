from random import randint

class Many():
    def __init__(self, rule, lo, hi):
        self.rule = rule
        self.low = lo
        self.high = hi

class Rule():
    Self = object()
    punctuation = {}
    def __init__(self, productions, post_proc=lambda s:s):
        self.productions = productions
        self.post_proc = post_proc

    def transform(self, func):
        return Rule(func(self.productions), self.post_proc)

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
            output = ''
            for symbol in production:
                token = self.gen_token(symbol)
                if token[:-1] in Rule.punctuation:
                    output = output[:-1] + token
                else:
                    output += token
        else: 
            output = self.gen_token(production)
        return self.post_proc(output)

    def gen_token(self, sym):
        if type(sym) == str:
            return sym + ' '
        if type(sym) == Many:
            output = ''
            for i in range(randint(sym.low, sym.high)):
                output += self.rule_or_self(sym.rule).generate()
            return output
        return self.rule_or_self(sym).generate()