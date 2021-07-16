# GTok

Gtok is a general purpose tokenizer written in python with purpose on fexibility.
It takes any input of type `Iterable` to be tokenized.

## Rationale

I have been working on a side project that needed a REPL and a command-line arguments tokenizer.

## Getting started

The tokenizer is fairly simple, and it extract tokens based on the following two rules:
1. Use the longest matching rule.
2. If there is a tie, use based on rules precedence.

## Example

The following is an example of rules for an algebric expression.

```python
from tokenizer import Tokenizer, regex

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

```

This produces the following output:

```bash
('y', 'VAR', 0)
('=', 'EQUALS', 2)
('2', 'DIGIT', 4)
('*', 'TIMES', 6)
('(', 'RIGHT_PAREN', 8)
('x', 'VAR', 9)
('-', 'MINUS', 11)
('2', 'DIGIT', 13)
(')', 'RIGHT_PAREND', 14)
('+', 'PLUS', 16)
('t', 'VAR', 18)
('', 'EOF', 19)
```

The Tokenizer class takes two arguments as input:
1. a module/class scope that hoels all rules.
2. a context object that keep track of the tokenization logic.

You can override the context class for advanced purpose.
The regex decorator works on `Iterable` input of type `str` only.
The work on lists and others, you may implement a rule as follows:

```python

class Rules:

    def rule1(ctx, tb):
        # ctx: is tokenization context.
        # tb: is the object used for building a token.
        if ctx.data[ctx.pos] not in ["$100", "$50", "$10", "$5", "$1"]:
            return False

        tb.value = ctx.data[ctx.pos]
        tb.type = "AMOUNT"
        # a rule must return True it notify the tokenizer we got a match!
        return True
    
    def rule2(ctx, tb):
        #...
        pass
```

For more details please explore the source-code, or submit a new issue for support.

