import re
from functools import wraps


def regex(re_str):
    re_cmp = re.compile(re_str)

    def decorator(func):
        @wraps(func)
        def wrapper(ctx):
            if not isinstance(ctx._data, str):
                raise TypeError(
                    f"Iterable type {type(ctx._data)} is not of type <class 'str'>."
                )
            m = re_cmp.match(ctx._data, ctx._cursor)
            result = (False, None)
            if not m:
                return func(ctx, result)
            else:
                result = (True, (m.group(), None, m.end()))
                return func(ctx, result)

        return wrapper

    return decorator


def custom_1(re_str):
    re_cmp = re.compile(re_str)

    def decorator(func):
        @wraps(func)
        def wrapper(ctx):
            if not isinstance(ctx._data, list):
                raise TypeError(
                    f"Iterable type {type(ctx._data)} is not of type  <class 'list'>."
                )
            print(ctx, ctx._cursor, func)
            m = re_cmp.match(ctx._data[ctx._cursor])
            result = (False, None)
            if not m:
                return func(ctx, result)
            else:
                result = (True, (m.group(), None, ctx._cursor + 1))
                return func(ctx, result)

        return wrapper

    return decorator
