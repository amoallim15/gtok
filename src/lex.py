import inspect


class Lexer:
    def __init__(self, module=None):
        self.module = module

        #
        self.rules = self.getattrs(module)

    def getattrs(self, module):
        return {
            x: y
            for x, y in inspect.getmembers(
                module,
                lambda x: inspect.isroutine(x) and (x.__name__.startswith("m_")),
            )
        }





















# ---------------

class Rules:

    fn1 = lambda x: x
    fn2 = lambda x: x ** 2

    def m_f(): pass

# print(dir(Rules))
# inspect.getmembers(Rules, lambda x: inspect.isroutine(x) and print(x.__name__))
a = Lexer(Rules)

print(a.rules)
