import inspect
from collections.abc import Iterable
import heapq


class TResult:
    def __init__(self, **kwargs):
        for kw, arg in kwargs.items():
            self.__setattr__(kw, arg)


class DefaultTContext:
    def __init__(self, data=""):
        self.reset(data)

    def reset(self, data):
        if not isinstance(data, Iterable):
            raise ValueError(f"Data is not of type {type(Iterable)}, {type(data)}.")
        #
        self.data = data
        self.cursor = -1

    def result(self, **kwargs):
        return TResult(**kwargs)

    def consume(self, tresult):
        # self.cursor = max(self.cursor, tresult.cursor + tresult.length)
        self.cursor += tresult.length

    def __repr__(self):
        return f"Context({self.data}, {self.cursor}, {len(self.data)})"


class Tokenizer:
    helpers = ["soi", "eoi", "err"]

    def __init__(self, module=None, context=None):
        if not context:
            self.ctx = DefaultTContext()
        #
        self.build_rules(module)

    def build_rules(self, module):
        attrs = vars(module)
        self.rules = [
            (priority, func)  # (name, priority, func)
            for priority, func in enumerate(
                attrs.values()
            )  # for priority, (name, func) in enumerate(attrs.items())
            if inspect.isroutine(func)
            and not func.__name__.startswith("_")
            and not func.__name__ in Tokenizer.helpers
        ]
        for helper in self.helpers:
            func = attrs.get(helper, None)
            if not inspect.isroutine(func):
                # TODO: print warning, that valuse of helper names is overwritten to None.
                self.__setattr__(helper, None)
            self.__setattr__(helper, func)

    def feed(self, data):
        self.ctx.reset(data)

    def get_token(self):
        if self.ctx.cursor < 0:
            if self.soi:
                tresult = self.soi(self.ctx)
                self.ctx.consume(tresult)
                if tresult.token:
                    return token
            self.ctx.cursor = 0
        #
        if self.ctx.cursor == len(self.ctx.data):
            if self.eoi:
                tresult = self.eoi(self.ctx)
                self.ctx.consume(tresult)
                if tresult.token:
                    return token
            self.ctx.cursor += 1
            # input has been consumed.
            return None
        #
        if self.ctx.cursor > len(self.ctx.data):
            return None
        #
        matches = []
        for (priority, func) in self.rules:
            tresult = func(self.ctx)
            if tresult:
                heapq.heappush(matches, (-tresult.length, priority, tresult))
            continue
        #
        if len(matches) > 0:
            (_, _, tresult) = heapq.heappop(matches)
            self.ctx.consume(tresult)
            if tresult.token:
                return tresult.token
            return self.get_token()
        #
        if self.err:
            tresult = self.err(ctx)
            if tresult:
                self.ctx.consume(tresult)
                if tresult.token:
                    return tresult.token
                return self.get_token()
        #
        token_value, token_cursor = self.ctx.data[self.ctx.cursor], self.ctx.cursor
        raise ValueError(f"""Unexpected token "{token_value}" at {token_cursor}.""")
