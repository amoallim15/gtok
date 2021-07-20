import re
from functools import wraps


def regex(re_str):
    re_cmp = re.compile(re_str)

    def decorator(func):
        @wraps(func)
        def wrapper(ctx):
            m = re_cmp.match(ctx.data, ctx.cursor)
            if not m:
                return func(ctx, ctx.result(value=None))
            result = ctx.result(
                value=m.group(),
                length=m.end() - m.start(),
                start=m.start(),
                end=m.end(),
                matcher=m,
            )
            return func(ctx, result)

        return wrapper

    return decorator


def custom1(re_str):
    re_cmp = re.compile(re_str)

    def decorator(func):
        @wraps(func)
        def wrapper(ctx):
            m = re_cmp.match(ctx.data[ctx.cursor])
            if not m:
                return func(ctx, ctx.result(value=None))
            result = ctx.result(
                value=m.group(),
                length=m.end() - m.start(),
                start=m.start(),
                end=m.end(),
                matcher=m,
            )
            return func(ctx, result)

        return wrapper

    return decorator
