import re
from functools import wraps


def regex(restr):
    restr = re.compile(restr)

    def decorator(func):
        @wraps(func)
        def wrapper(ctx, tb):
            #
            tb.pos, tb.padding = ctx.pos, 0
            m = restr.match(ctx.data, ctx.pos)
            if not m:
                tb.len, tb.value, tb.type = 0, "", None
            else:
                tb.value = m.group()
                tb.pos = m.end()
                tb.len = tb.pos - ctx.pos
                tb.matcher = m
            #
            return func(ctx, tb)
            #

        return wrapper

    return decorator
