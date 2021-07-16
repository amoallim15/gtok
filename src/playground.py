from tokenizer import Tokenizer, regex

"""
exp := a -> b       # (a and b)     [sequence]
exp := a -| b       # (a or b)      [alternative]
exp := a -^ b       # (a if predicate b)  [conditional]
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
    def _test(ctx, tb):
        tb.rr = 5
        print(tb)
        return False

    @regex(r"->")
    def _and(ctx, tb):
        # TODO: check (decorator | return) infinity loop error.
        pass

    @regex(r"-\|")
    def _or(ctx, tb):
        pass

    @regex(r"-\^")
    def _predicate(ctx, tb):
        pass

    @regex(r":=")
    def _is(ctx, tb):
        pass

    @regex(r"<")
    def _more(ctx, tb):
        pass

    @regex(r"[()]")
    def _paren(ctx, tb):
        if tb.value == "(":
            tb.type = "PAREN_START"
        if tb.value == ")":
            tb.type = "PAREN_END"
        pass

    @regex(r"[a-z]+")
    def _identifier(ctx, tb):
        # TODO: check (decorator | return) infinity loop error.
        pass
        # values = "abcdefghijklmnopqrstuvwxyz"
        # check = ctx.data[ctx.pos : ctx.pos + 1]
        # if check in values:
        #     tb.len = 1
        #     tb.value = check
        #     return True

    @regex(r"[A-Z]+")
    def _token(ctx, tb):
        pass

    @regex(r"[\s\n\r\f\t]")
    def _ignore(ctx, tb):
        tb.ignore = True

    def error(ctx, tb):
        return True

    def eof(ctx, tb):
        return True


# tok = Tokenizer(module=NoPEGRules)
# tok.input("a := (a -> CC<) -| b")
# for token in tok.tokens():
#     print(token)

# print()

# tok.input("b := a -| a<")
# for token in tok.tokens():
#     print(token)

# print()

# tok.input("b := a -^ a")
# for token in tok.tokens():
#     print(token)


class Rules:
    @regex(r"[a-z]+")
    def var(ctx, tb):
        pass

    @regex(r"[1-9]+")
    def digit(ctx, tb):
        pass

    @regex(r"[()]")
    def paren(ctx, tb):
        if tb.value == "(":
            tb.type = "RIGHT_PAREN"
        elif tb.value == ")":
            tb.type = "RIGHT_PAREND"
        pass

    @regex(r"[+-/*=]")
    def op(ctx, tb):
        if tb.value == "+":
            tb.type = "PLUS"
        elif tb.value == "-":
            tb.type = "MINUS"
        elif tb.value == "*":
            tb.type = "TIMES"
        elif tb.value == "/":
            tb.type = "DIVIDE"
        elif tb.value == "=":
            tb.type = "EQUALS"
        pass

    @regex(r"[\s\n\r\f\t]")
    def discard(ctx, tb):
        tb.ignore = True

    # optional special function to handle errors.
    # The function must be called "error".
    def error(ctx, tb):
        print(f"Illegal character {ctx.data[ctx.pos]} at {ctx.pos}")
        return True

    # optional special function to handle end of file.
    # The function must be called "eof".
    def eof(ctx, tb):
        return True


tok = Tokenizer(module=Rules)
tok.input("y = 2 * (x - 2) + t")
for token in tok.tokens():
    print(token)
