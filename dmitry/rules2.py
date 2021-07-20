from matchers import regex


class TestRules:
    @regex(r"[a-z]+")
    def identifier(ctx, tresult):
        if tresult.value:
            tresult.token = (tresult.value, "IDENTIFIER", tresult.start)
            return tresult

    @regex(r"[1-9]+")
    def numeric(ctx, tresult):
        if tresult.value:
            tresult.token = (tresult.value, "NUMERIC", tresult.start)
            return tresult

    @regex(r"[()]")
    def paren(ctx, tresult):
        if tresult.value:
            if tresult.value == "(":
                _type = "RIGHT_PAREN"
            elif tresult.value == ")":
                _type = "RIGHT_PAREND"
            tresult.token = (tresult.value, _type, tresult.start)
            return tresult

    @regex(r"[+-/*=]")
    def op(ctx, tresult):
        if tresult.value:
            if tresult.value == "+":
                _type = "PLUS"
            elif tresult.value == "-":
                _type = "MINUS"
            elif tresult.value == "*":
                _type = "TIMES"
            elif tresult.value == "/":
                _type = "DIVIDE"
            elif tresult.value == "=":
                _type = "EQUALS"
            tresult.token = (tresult.value, _type, tresult.start)
            return tresult

    @regex(r"[\s\n\r\f\t]")
    def ignore(ctx, tresult):
        if tresult.value:
            tresult.token = None
            return tresult
