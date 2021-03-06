import inspect
from collections.abc import Iterable
import heapq
import re
from functools import wraps


class TokenizerError(Exception):
    pass


class Context:
    def __init__(self, data=""):
        self.overwrite(data)

    def overwrite(self, data):
        self.__data = data
        self.__pos = 0
        self.__len = len(data)

    @property
    def data(self):
        return self.__data

    @property
    def pos(self):
        return self.__pos

    @property
    def len(self):
        return self.__len

    def consume(self, tb):
        self.__pos = max(self.pos, tb.pos + tb.len + tb.padding)
        if not tb.ignore:
            return tb.build()

    def __repr__(self):
        return f"Context({self.__data}, {self.__pos}, {self.__len})"


class TokenBuilder:
    def __init__(self, **kwargs):
        self.padding = kwargs.get("padding", 0)
        self.pos = kwargs.get("pos", 0)
        self.len = kwargs.get("len", 0)
        self.value = kwargs.get("value", "")
        self.ignore = False
        self.type = kwargs.get("type", None)
        self.matcher = kwargs.get("matcher", None)

    def build(self):
        return (self.value, self.type, self.pos)

    def __repr__(self):
        return f'TokenBuilder("{self.value}", {self.type}, {self.pos}, {self.len})'


class Rule:
    def __init__(self, name, action, priority=0):
        self.name = name
        self.token = name.upper()
        self.action = action
        self.priority = priority

    def __repr__(self):
        return f"Rule({self.name}, {self.token}, {self.priority}, {self.action})"


def regex(restr):
    restr = re.compile(restr)

    def decorator(func):
        @wraps(func)
        def wrapper(ctx, tb):
            #
            if not isinstance(ctx.data, str):
                raise TypeError("Regex matcher works on Iterable of str type only.")
            tb.pos, tb.padding = ctx.pos, 0
            m = restr.match(ctx.data, ctx.pos)
            if not m:
                tb.len, tb.value, tb.type = 0, "", None
                func(ctx, tb)
            else:
                tb.value = m.group()
                tb.pos = m.start()
                tb.len = m.end() - m.start()
                tb.matcher = m
                func(ctx, tb)
                return True

        return wrapper

    return decorator


class Tokenizer:
    helpers = ["error", "eof"]

    def __init__(self, module=None, context=Context):
        self.ctx = context()
        self.err_rule = None
        self.eof_rule = None
        self.rules = None
        #
        self.build_rules(module)

    def build_rules(self, module):
        attrs = vars(module)
        self.rules = [
            Rule(n, f, p)
            for p, (n, f) in enumerate(attrs.items())
            if inspect.isroutine(f)
            and not f.__name__.startswith("__")
            and not f.__name__ in self.helpers
        ]
        # special rules, they dont need name or token type.
        self.err_handler = attrs.get("error", None)
        self.eof_handler = attrs.get("eof", None)

    def input(self, data):
        if not isinstance(data, Iterable):
            raise ValueError(f'Input is not of type Iterable error. \n"{data}"')
        self.ctx.overwrite(data)

    def tokens(self):
        while self.ctx.pos < self.ctx.len:
            matches = []
            for rule in self.rules:
                tb = TokenBuilder(pos=self.ctx.pos, type=rule.token)
                token_predicate = rule.action(self.ctx, tb)
                if token_predicate:
                    match = (-tb.len, rule.priority, tb)
                    heapq.heappush(matches, match)
                continue
            if len(matches) > 0:
                _, _, tb = heapq.heappop(matches)
                token = self.ctx.consume(tb)
                if token:
                    yield token
                continue
            else:
                if inspect.isroutine(self.err_handler):
                    tb = TokenBuilder(
                        value=self.ctx.data[self.ctx.pos],
                        pos=self.ctx.pos,
                        type="ERROR",
                        len=1,
                    )
                    token_predicate = self.err_handler(self.ctx, tb)
                    if token_predicate:
                        token = self.ctx.consume(tb)
                        yield token
                    continue
                raise TokenizerError(
                    f'Illegal element "{self.ctx.data[self.ctx.pos]}" at [{self.ctx.pos}].'
                )
        if self.ctx.pos == self.ctx.len:
            if inspect.isroutine(self.eof_handler):
                tb = TokenBuilder(
                    value="",
                    pos=self.ctx.pos,
                    type="EOF",
                    len=1,
                )
                token_predicate = self.eof_handler(self.ctx, tb)
                if token_predicate:
                    token = self.ctx.consume(tb)
                    yield token
        # raise StopIteration("Input has been fully consumed.")
        return
