import inspect
from collections.abc import Iterable
import heapq


class DefaultContext:
    def __init__(self, data=""):
        self.reset(data)

    def reset(self, data):
        self._data = data
        self._cursor = -1
        self._len = len(data)

    def consume(self, steps):
        self._cursor += steps

    def __repr__(self):
        return f"Context({self._data}, {self._cursor}, {self._len})"


class Tokenizer:
    helpers = ["soi", "eoi", "err"]

    def __init__(self, module=None, context=None):
        if not context:
            self.ctx = DefaultContext()
        #
        self.build_rules(module)

    def build_rules(self, module):
        attrs = vars(module)
        self.rules = [
            (priority, func)  # (_, priority, func)
            for priority, (_, func) in enumerate(attrs.items())
            if inspect.isroutine(func)
            and not func.__name__.startswith("_")
            and not func.__name__ in Tokenizer.helpers
        ]
        for helper in self.helpers:
            func = attrs.get(helper, None)
            if not inspect.isroutine(func):
                self.__setattr__(helper, None)
            self.__setattr__(helper, func)

    def feed(self, data):
        if not isinstance(data, Iterable):
            raise ValueError(f"Input is not of type <Iterable>, {type(data)}.")
        self.ctx.reset(data)

    def token(self):
        if self.ctx._cursor < 0:
            if self.soi:
                predicate, token = self.soi(self._ctx)
                self.ctx._cursor = 0
                if predicate and token:
                    return token
            self.ctx._cursor = 0
        #
        if self.ctx._cursor == self.ctx._len:
            if self.eoi:
                predicate, token = self.eoi(self._ctx)
                self.ctx._cursor += 1
                if predicate and token:
                    return token
            self.ctx._cursor += 1
            # input has been consumed.
            return None
        #
        if self.ctx._cursor > self.ctx._len:
            return None
        #
        matches = []
        for (priority, func) in self.rules:
            predicate, token = func(self.ctx)
            if predicate:
                (_value, _type, _cursor) = token
                heapq.heappush(matches, (-len(_value), priority, token))
            continue
        #
        if len(matches) > 0:
            (_, _, token) = heapq.heappop(matches)
            self.ctx._cursor = token[2]
            (_value, _type, _cursor) = token
            print(token)
            if _type:
                return token
            return self.token()
        #
        if self.err:
            predicate, token = self.err(ctx)
            if predicate:
                self.ctx._cursor += 1
                if token:
                    return token
                return self.token()

        token = self.ctx._data[self.ctx._cursor]
        raise ValueError(f"Unexpected token at {self.ctx._cursor} '{token}'.")
