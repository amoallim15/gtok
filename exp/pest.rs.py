# tuple => _AND_(): pass
# list  => _OR_(): pass
# set   => _IF_(): pass
# None  =>

# def _AND_(): pass # sequence operator
# def _OR_(): pass # alternative operator
# def _IF_(): pass # predicate operator


def _LOOP_():
    pass  # repition operator


def _PASS_():
    pass  # skip operator


def _TOKEN_():
    pass  # custom operator


class GrammarRules:
    # operators
    assignment_operator = "="
    opening_brace = "{"
    closing_brace = "}"
    opening_paren = "("
    closing_paren = ")"
    opening_brack = "["
    closing_brack = "]"

    start = ("SOF", grammar_rules, "EOF")
    grammar_rules = [grammar_rule, _LOOP_, grammar_rule]
    grammar_rule = (
        idenifier,
        assignment_operator,
        opening_brace,
        expression,
        closing_brace,
    )
    expression = ()
