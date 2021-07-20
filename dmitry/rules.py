from matchers import regex


class TRules:
    @regex(r"^(supp)$")
    def app(ctx, tresult):
        if tresult.value:
            tresult.length = 1
            tresult.token = (tresult.value, "PROGRAM", ctx.cursor)
            return tresult

    @regex(r"^(describe)$")
    def reserved_keywords(ctx, tresult):
        if tresult.value:
            tresult.length = 1
            tresult.token = (tresult.value, "CMD", ctx.cursor)
            return tresult

    @regex(r"^(--(version|help|list|args)|-(v|h|l|a))$")
    def reserved_flag(ctx, tresult):
        if tresult.value:
            tresult.length = 1
            tresult.token = (tresult.value, "FLAG", ctx.cursor)
            return tresult

    @regex(r"^--\w+$")
    def arg_key_flag_type(ctx, tresult):
        if tresult.value:
            tresult.length = 1
            tresult.token = (tresult.value.strip("-"), "ARG_KEY_FLAG", ctx.cursor)
            return tresult

    @regex(r"^\w+=\s\S+$")
    def arg_eq_type(ctx, tresult):
        if tresult.value:
            tresult.length = 1
            tresult.token = (tresult.value.split("="), "ARG_EQ", ctx.cursor)
            return tresult

    @regex(r"^[0-9]+$")
    def numeric_type(ctx, tresult):
        if tresult.value:
            tresult.length = 1
            tresult.token = (int(tresult.value), "NUMERIC", ctx.cursor)
            return tresult

    @regex(r"^(True|False)$")
    def boolean_type(ctx, tresult):
        if tresult.value:
            tresult.length = 1
            _value = False if tresult.value == "False" else True
            tresult.token = (_value, "BOOLEAN", ctx.cursor)
            return tresult

    @regex(r"^\w+$")
    def identifier_type(ctx, tresult):
        if tresult.value:
            tresult.length = 1
            tresult.token = (tresult.value, "IDENTIFIER", ctx.cursor)
            return tresult

    @regex(r"^[\s\S]+$")
    def string_type(ctx, tresult):
        if tresult.value:
            tresult.length = 1
            tresult.token = (tresult.value, "STRING", ctx.cursor)
            return tresult


class PRules:
    pass
