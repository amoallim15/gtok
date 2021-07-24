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
        print("AND ::", self.grammars)
        for grm in self.grammars:
            predicate, error = parser.traverse(grm)
            if not predicate:
                return (False, error)


class OrderedChoice:
    def __init__(self, *grammars, labels={}):
        self.grammars = grammars
        self.labels = labels

    def execute(self, parser):
        print("OR ::", self.grammars)
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
        print("LOOP ::", self.grammar)
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
        print("NOT ::", self.grammar)
        predicate, error = parser.traverse(self.grammar)
        if error == "FAILED":
            return (True, None)
        return (False, error)


class Raise:
    def __init__(self, label):
        self.label = label

    def execute(self, parser):
        print("RAISE ::", self.label)
        return (False, label)


class PContext:
    def __init__(self, data=""):
        self.data = data
        self.cursor = -1
        self.len = len(data)

    def consume(self, steps=1):
        self.__cursor += steps


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
            if inspect.isroutine(value):
                self.actions[name] = value
                continue
            self.grammars[name] = value

    # def terminal(self):
    #     pass

    def checkpoint(self):
        pass

    def parse(self, data):
        self.ctx = PContext(data)
        return self.traverse(self.grammars["start"])

    def traverse(self, grammar):
        pass
