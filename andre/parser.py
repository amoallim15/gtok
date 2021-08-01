"""
EMPTY
TERMINAL
NON_TERMINAL
AND
OR
WHILE
NOT
THROW
ACT

1. back tracking algorithm. (concern seperation) [DONE]
2. how to write better grammar. (user friendliness)
3. how to do packrat. (efficiency concerns)
4. building abstract syntax tree. (result) [DONE]
"""


class Sequence:
    def __init__(self, *grammars):
        self.grammars = grammars

    def execute(self, parser):
        result = []
        print("AND INPUT      -> GRAMMAR::", self.grammars)
        for grm in self.grammars:
            predicate, output, error = parser.traverse(grm, is_raise=False)
            if not predicate:
                return (False, result, error)
            result.append(output)
        return (True, result, None)


class OrderedChoice:
    def __init__(self, *grammars, labels={"FAILED"}):
        self.grammars = grammars
        self.labels = labels

    def execute(self, parser):
        print("OR INPUT       -> GRAMMAR::", self.grammars)
        result, error = None, None
        for grm in self.grammars:
            predicate, result, error = parser.traverse(grm, is_raise=False)
            if predicate:
                return (True, result, None)
            if error not in self.labels:
                break
        return (False, result, error)


class Loop:
    def __init__(self, grammar):
        self.grammar = grammar

    def execute(self, parser):
        print("LOOP INPUT     -> GRAMMAR::", self.grammar)
        result = []
        while True:
            predicate, output, error = parser.traverse(self.grammar, is_raise=False)
            if not predicate:
                if error == "FAILED" and len(result) > 0:
                    return (True, result, None)
                return (False, result, error)
            result.append(output)


class Not:
    def __init__(self, grammar):
        self.grammar = grammar

    def execute(self, parser):
        print("NOT INPUT      -> GRAMMAR::", self.grammar)
        predicate, result, error = parser.traverse(self.grammar, is_raise=False)
        if error == "FAILED":
            return (True, result, None)
        return (False, None, error)


class Raise:
    def __init__(self, label):
        self.label = label

    def execute(self, parser):
        print("RAISE INPUT    -> GRAMMAR::", self.label)
        return (False, None, self.label)


class PContext:
    def __init__(self, data=""):
        self.data = data
        self.cursor = 0
        self.len = len(data)

    def consume(self, steps=1):
        self.cursor += steps

    def __repr__(self):
        return f"PContext({self.data}, {self.cursor}, {self.len})"


class Parser:
    def __init__(self, module):
        self.build(module)

    def build(self, module):
        attrs = vars(module)
        self.actions = dict()
        self.grammars = dict()
        for (name, value) in attrs.items():
            if name.startswith("_"):
                continue
            if callable(value):
                self.actions[name] = value
                continue
            self.grammars[name] = value

    def step(self):
        self.lookahead = self.ctx.cursor

    def backtrack(self, lookahead):
        self.lookahead = self.ctx.cursor = lookahead

    def parse(self, data):
        self.ctx = PContext(data)
        self.lookahead = self.ctx.cursor
        self.step()
        return self.traverse(self.grammars["start"], True)

    def traverse(self, grammar, is_raise=True):
        predicate, result, error, lookahead = False, None, None, self.lookahead
        # empty
        if isinstance(grammar, bool) and grammar == True:
            predicate, result, error = bool, None, None
        # terminal or literal
        if isinstance(grammar, str):
            try:
                # token
                if grammar == grammar.upper() and grammar in self.actions.keys():
                    predicate, result, error = self.actions[grammar](self.ctx)
                # literal
                else:
                    pass
                # if eof
            except IndexError:
                raise Exception("Unexpected EOF.")
        # action
        if callable(grammar) and grammar in self.actions.values():
            predicate, result, error = grammar(self)
        # buildin funcs
        if type(grammar) in [Sequence, OrderedChoice, Loop, Not, Raise]:
            predicate, result, error = grammar.execute(self)
        #
        if predicate:
            self.step()
        #
        if not predicate and error != "FAILED":
            self.backtrack(lookahead)
        #
        if not predicate and error == "FAILED" and is_raise:
            print(predicate, result, error)
            raise Exception("FAILED")
        #
        return predicate, result, error
