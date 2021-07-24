import inspect

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

1. back tracking algorithm. (concern seperation) [DONE PARTIALLY]
2. how to write better grammar. (user friendliness)
3. how to do packrat. (efficiency concerns)
4. building abstract syntax tree. (result)
"""


class Sequence:
    def __init__(self, *grammars):
        self.grammars = grammars

    def execute(self, parser):
        print("AND INPUT      -> GRAMMAR::", self.grammars)
        for grm in self.grammars:
            predicate, error = parser.traverse(grm)
            if not predicate:
                return (False, error)
        return (True, None)


class OrderedChoice:
    def __init__(self, *grammars, labels={"FAILED"}):
        self.grammars = grammars
        self.labels = labels

    def execute(self, parser):
        print("OR INPUT       -> GRAMMAR::", self.grammars)
        error = None
        for grm in self.grammars:
            predicate, error = parser.traverse(grm)
            if predicate:
                return (True, None)
            if error not in self.labels:
                break
        return (False, error)


class Loop:
    def __init__(self, grammar):
        self.grammar = grammar

    def execute(self, parser):
        print("LOOP INPUT     -> GRAMMAR::", self.grammar)
        while True:
            predicate, error = parser.traverse(self.grammar)
            if not predicate:
                if error == "FAILED":
                    return (True, None)
                return (False, error)


class Not:
    def __init__(self, grammar):
        self.grammar = grammar

    def execute(self, parser):
        print("NOT INPUT      -> GRAMMAR::", self.grammar)
        predicate, error = parser.traverse(self.grammar)
        if error == "FAILED":
            return (True, None)
        return (False, error)


class Raise:
    def __init__(self, label):
        self.label = label

    def execute(self, parser):
        print("RAISE INPUT    -> GRAMMAR::", self.label)
        return (False, self.label)


def Token(self, token, action):
    print("TOKEN INPUT    -> GRAMMAR::", token)
    return action(ctx)


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
        self.checkpoints = []

    def build(self, module):
        attrs = vars(module)
        self.actions = dict()
        self.grammars = dict()
        for (name, value) in attrs.items():
            if name.startswith("_"):
                continue
            if inspect.isroutine(value):
                self.actions[name] = value
                continue
            self.grammars[name] = value

    def step(self, checkpoints):
        checkpoints.append(self.lookahead)
        self.lookahead = self.ctx.cursor

    def backtrack(self, checkpoints):
        if checkpoints:
            self.lookahead = checkpoints[0]
            self.ctx.cursor = self.lookahead

    def parse(self, data):
        self.ctx = PContext(data)
        self.lookahead = self.ctx.cursor
        self.step([])
        return self.traverse(self.grammars["start"])

    def traverse(self, grammar):
        predicate, error = False, None
        checkpoints = []
        print(
            "TRAVERSE INPUT ->",
            "GRAMMAR::",
            grammar,
            f"| TOKEN:: ('{self.ctx.data[self.ctx.cursor]}', {self.ctx.cursor})",
        )
        #

        # 1. check if empty. (True == epsilon)
        if grammar == True:
            return True, None

        # 2. check if token.
        if (
            isinstance(grammar, str)
            and grammar == grammar.upper()
            and grammar in self.actions.keys()
        ):
            predicate, error = self.actions[grammar](self.ctx)
            print(f"TRAVERSE TOKEN -> ('{error}')")

        # 3. check if an action
        if grammar in self.actions.values():
            predicate, error = self.actions[grammar](self)

        # if type(grammar) == Raise:
        #     return grammar.execute(self)
        # 4. check if one of the main 5 funcs or an action.
        if type(grammar) in [Sequence, OrderedChoice, Loop, Not, Raise]:
            predicate, error = grammar.execute(self)

        # 5. lookahead the parser or trackback.
        if predicate:
            self.step(checkpoints)

        if not predicate and error != "FAILED":
            print(checkpoints)
            self.backtrack(checkpoints)

        # 6. handle fatal errors.
        if not predicate and error == "FAILED":
            raise Exception(error)

        print(
            "TRAVERSE OUTPUT ->",
            "GRAMMAR::",
            grammar,
            f"| TOKEN:: ('{self.ctx.data[self.ctx.cursor]}', {self.ctx.cursor})",
        )
        return predicate, error


#
#
#
#
