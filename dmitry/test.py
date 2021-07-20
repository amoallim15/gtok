from tokenizer import Tokenizer
from rules import TRules
from rules2 import TestRules


def case1():
    tok = Tokenizer(module=TRules)

    data = "supp --help func describe --args 4 True k=v 'text text' --test"
    tok.feed(data.split(" "))
    while True:
        token = tok.get_token()
        if not token:
            break
        print(token)


def case2():

    tok = Tokenizer(module=TestRules)
    tok.feed("y = 2 * (x - 2) + t")
    while True:
        token = tok.get_token()
        if not token:
            break
        print(token)


case1()
# case2()
