from tokenizer import Tokenizer
from rules import TRules
from rules2 import TestRules


def case1():
    tok = Tokenizer(module=TRules)

    tok.feed(["supp", "hello"])
    print(tok.get_token())
    print(tok.get_token())
    print(tok.get_token())
    print(tok.get_token())


def case2():

    tok = Tokenizer(module=TestRules)
    tok.feed("y = 2 * (x - 2) + t")
    while True:
        token = tok.get_token()
        if not token:
            break
        print(token)
    # print(tok.get_token())
    # print(tok.get_token())
    # print(tok.get_token())


# case1()
case2()
