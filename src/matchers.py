import re
from functools import wraps


def regex(restr):
    restr = re.compile(restr)

    def decorator(func):
        @wraps(func)
        def wrapper(ctx, tb):
            #
            if not isinstance(ctx.data, str):
                raise TypeError("Regex matcher works only on Iterable of str type.")
            tb.pos, tb.padding = ctx.pos, 0
            m = restr.match(ctx.data, ctx.pos)
            if not m:
                tb.len, tb.value, tb.type = 0, "", None
                func(ctx, tb)
            else:
                tb.value = m.group()
                tb.pos = m.end()
                tb.len = tb.pos - ctx.pos
                tb.matcher = m
                func(ctx, tb)
                return True

        return wrapper

    return decorator
