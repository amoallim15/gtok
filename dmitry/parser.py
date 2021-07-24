import inspect
from functools import wraps
from tokenizer import Tokenizer
from rules import TRules


class And:
    def __init__(self, *args):
        self.args = args

    def execute(self, parser):
        presult_list = []
        for arg in self.args:
            print("AND", arg, parser.lookahead)
            if isinstance(arg, bool):
                continue  # , presult
            predicate = parser.traverse(
                arg
            )  # predicate, presult = parser.traverse(arg)
            if not predicate:
                return False
                # raise Exception(f"Invalid token {parser.lookahead}")
            # presult_list.append(presult)
        return True  # , presult_list


class Or:
    def __init__(self, *args):
        self.args = args

    def execute(self, parser):
        presult_list = []
        for arg in self.args:
            print("OR", arg, parser.lookahead)
            if isinstance(arg, bool):
                return True  # , presult
            predicate = parser.traverse(
                arg
            )  # predicate, presult = parser.traverse(arg)
            if predicate:
                # presult_list.append(presult)
                return True  # , presult_list
        return False
        # raise Exception(f"Invalid token {parser.lookahead}")


class Parser:
    # operators = ["AND", "OR", "IF", "LOOP", "ACTION"]
    operators = [And, Or]

    def __init__(self, tmodule=None, gmodule=None, context=None):
        #
        self.build_rules(tmodule, gmodule, context)

    def build_rules(self, tmodule, gmodule, context):
        self.tok = Tokenizer(tmodule, context)
        attrs = vars(gmodule)
        self.grammars = {
            name: grammar
            for name, grammar in attrs.items()
            if not inspect.isroutine(grammar) and not name.startswith("_")
        }
        # print(self.grammars)

    def step(self):
        self.lookahead = self.tok.get_token()
        return self.lookahead

    def parse(self, data):
        self.tok.feed(data)
        self.step()
        self.start = self.grammars["start"]
        return self.traverse(self.start)

    def traverse(self, grammar):
        if not self.lookahead:
            raise Exception("Invalid EOF", grammar)
        #
        predicate = False
        if isinstance(grammar, str):  # TODO:
            if self.lookahead[1].upper() != grammar.upper():
                return False
            self.step()
            return True
        #
        if type(grammar) in self.operators:
            predicate = grammar.execute(
                self
            )  # predicate, result = grammar.execute(self)
        #
        print("End of Traverse", grammar, self.lookahead, predicate)

        return predicate


class GRules:
    start = And("SUPP", Or(And("FLAG", "FLAG")), "IDENTIFIER", "IDENTIFIER", True)


# TODO: and for and other operators have to pass errors to parent operator.
prs = Parser(TRules, GRules)
prs.parse("supp --help --args a b t".split(" "))
# print(prs.lookahead)


#  the issue...
"""
assume we have 
a = OR(1, 2, AND(3, 4), True)




"""
