from tokenizer import Tokenizer
from matchers import regex


class NoPEGRules:
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

    @regex(r"[a-z]")
    def _variable(ctx, tb):
        # TODO: check (decorator | return) infinity loop error.
        pass
        # values = "abcdefghijklmnopqrstuvwxyz"
        # check = ctx.data[ctx.pos : ctx.pos + 1]
        # if check in values:
        #     tb.len = 1
        #     tb.value = check
        #     return True

    @regex(r"[\s\n\r\f\t]")
    def _ignore(ctx, tb):
        tb.ignore = True

    def error(ctx, tb):
        return True

    def eof(ctx, tb):
        return True


tok = Tokenizer(module=NoPEGRules)
tok.input("a := (a -> c<) -| b")
for token in tok.tokens():
    print(token)

print()

# tok.input("b := a -| a<")
# for token in tok.tokens():
#     print(token)

# print()

# tok.input("b := a -^ a")
# for token in tok.tokens():
#     print(token)
