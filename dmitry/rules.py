from matchers import regex, custom_1


class TRules:
    @custom_1(r"^(supp)$")
    def app(ctx, m):
        predicate, token = m
        if not predicate:
            return False, None
        return True, (token[0], "PROGRAM", token[2])

    @custom_1(r"^(describe)$")
    def reserved_keywords(ctx, m):
        predicate, token = m
        if not predicate:
            return False, None
        return True, (token[0], "CMD", token[2])

    @custom_1(r"^(--(version|help|list|args)|-(v|h|l|a))$")
    def reserved_flag(ctx, m):
        predicate, token = m
        if not predicate:
            return False, None
        return True, (token[0], "FLAG", token[2])

    @custom_1(r"^--\w+$")
    def arg_key_flag_type(ctx, m):
        predicate, token = m
        if not predicate:
            return False, None
        return True, (token[0].strip("-"), "FLAG", token[2])

    @custom_1(r"^\w+=\s\S+$")
    def arg_eq_type(ctx, m):
        predicate, token = m
        if not predicate:
            return False, None
        return True, (token[0].split("="), "FLAG", token[2])

    @custom_1(r"^[0-9]+$")
    def numeric_type(ctx, m):
        predicate, token = m
        if not predicate:
            return False, None
        return True, (token[0], "NUMERIC", token[2])

    @custom_1(r"^(True|False)$")
    def bolean_type(ctx, m):
        predicate, token = m
        if not predicate:
            return False, None
        value = False if token[0] == "False" else True
        return True, (value, "BOOLEAN", token[2])

    @custom_1(r"^\w+$")
    def identifier_type(ctx, m):
        predicate, token = m
        if not predicate:
            return False, None
        return True, (token[0], "IDENTIFIER", token[2])

    @custom_1(r"^[\s\S]+$")
    def string_type(ctx, m):
        predicate, token = m
        if not predicate:
            return False, None
        return True, (token[0], "STRING", token[2])


class PRules:
    pass
