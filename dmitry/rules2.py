from matchers import regex, custom_1


class TestRules:
    @regex(r"[a-z]+")
    def identifier(ctx, m):
        predicate, token = m
        if not predicate:
            return False, None
        return True, (token[0], "IDENTIFIER", token[2])

    @regex(r"[1-9]+")
    def numeric(ctx, m):
        predicate, token = m
        if not predicate:
            return False, None
        return True, (int(token[0]), "NUMERIC", token[2])

    @regex(r"[()]")
    def paren(ctx, m):
        predicate, token = m
        if not predicate:
            return False, None
        if token[0] == "(":
            _type = "RIGHT_PAREN"
        elif token[0] == ")":
            _type = "RIGHT_PAREND"
        return True, (token[0], _type, token[2])

    @regex(r"[+-/*=]")
    def op(ctx, m):
        predicate, token = m
        if not predicate:
            return False, None
        if token[0] == "+":
            _type = "PLUS"
        elif token[0] == "-":
            _type = "MINUS"
        elif token[0] == "*":
            _type = "TIMES"
        elif token[0] == "/":
            _type = "DIVIDE"
        elif token[0] == "=":
            _type = "EQUALS"
        return True, (token[0], _type, token[2])


    @regex(r"[\s\n\r\f\t]")
    def discard(ctx, m):
        predicate, token = m
        if not predicate:
            return False, None
        return True, (token[0], None, token[2])