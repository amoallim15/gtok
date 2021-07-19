from tokenizer import Tokenizer
from matchers import regex, custom_1
from rules import TRules
from rules2 import TestRules


def case1():
    tok = Tokenizer(module=TRules)

    tok.feed(["supp", "hello"])
    print(tok.token())
    print(tok.token())
    print(tok.token())
    print(tok.token())


def case2():

    tok = Tokenizer(module=TestRules)
    tok.feed("y = 2 * (x - 2) + t")
    print(tok.token())
    print(tok.token())
    print(tok.token())
    print(tok.token())
    print(tok.token())


# case1()

case2()
