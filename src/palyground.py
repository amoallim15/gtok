from tokenizer import Tokenizer

"""
Ordered PEG:
exp := a -> b       # (a and b)     [sequence]
exp := a -| b       # (a or b)      [alternative]
exp := a -^ b       # (a if not b)  [conditional]
# 
exp := > -> a       # (skip and a)  [jump]
exp := > -| a       # (skip or a)   [optional]
exp := > -^ a       # (skip if predicate a) [constrained skip]
# 
exp := > -> a <     # (skip and a {n} times) [repition]
exp := > -| a <     # (skip or a {n} times) [zero or more]
exp := > -^ a <     # (skip if predicate a {n} times) [skip if predicate repeated a]
# 
exp := a -> a <     # (a and a {n} times) [one or more greedy]
exp := a -| a <     # (a or a {n} times) [one or more non greedy]
exp := a -^ a <     # (a if predicate a {n} times) [match if only once]
"""


class NoPEGRules:
    def _and(ctx, tb):
        check = ctx.data[ctx.pos : ctx.pos + 2]
        if check == "->":
            tb.len = 2
            tb.value = "->"
            return True

    def _or(ctx, tb):
        check = ctx.data[ctx.pos : ctx.pos + 2]
        if check == "-|":
            tb.len = 2
            tb.value = "-|"
            return True

    def _predicate(ctx, tb):
        check = ctx.data[ctx.pos : ctx.pos + 2]
        if check == "-^":
            tb.len = 2
            tb.value = "-^"
            return True

    def _is(ctx, tb):
        check = ctx.data[ctx.pos : ctx.pos + 2]
        if check == ":=":
            tb.len = 2
            tb.value = ":="
            return True

    def _more(ctx, tb):
        check = ctx.data[ctx.pos : ctx.pos + 1]
        if check == "<":
            tb.len = 1
            tb.value = "<"
            return True

    def _variable(ctx, tb):
        values = "abcdefghijklmnopqrstuvwxyz"
        check = ctx.data[ctx.pos : ctx.pos + 1]
        if check in values:
            tb.len = 1
            tb.value = check
            return True

    def _ignore(ctx, tb):
        check = ctx.data[ctx.pos : ctx.pos + 1]
        if check in " \n\r\f\t":
            tb.len = 1
            tb.value = check
            tb.ignore = True
            return True

    def error(ctx, tb):
        return True

    def eof(ctx, tb):
        return True


tok = Tokenizer(module=NoPEGRules)
tok.input("a := a -> a<")
for token in tok.tokens():
    print(token)

print()

tok.input("b := a -| a<")
for token in tok.tokens():
    print(token)

print()

tok.input("b := a -^ a")
for token in tok.tokens():
    print(token)
