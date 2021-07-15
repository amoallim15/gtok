from tokenizer import Tokenizer
from matchers import regex


class NoPEGRules:
    @regex(r"->")
    def _and(ctx, tb):
        # TODO: check (decorator | return) infinity loop error.
        pass

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

# tok.input("b := a -| a<")
# for token in tok.tokens():
#     print(token)

# print()

# tok.input("b := a -^ a")
# for token in tok.tokens():
#     print(token)
