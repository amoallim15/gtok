from parser import *

AND = Sequence
OR = OrderedChoice
LOOP = Loop
NOT = Not
RAISE = Raise


class Rules:
    #
    start = AND(
        LOOP("ALI"),
        LOOP("EMPTY"),
    )
    #
    # labels = {"FATAL"}
    # funcs are:
    # 1. terminal processors
    # 2. action functions

    # token
    def ALI(ctx):
        for c in ["a", "l", "i"]:
            if ctx.data[ctx.cursor] != c:
                return False, None, "FAILED"
            ctx.consume(1)
        return True, "ali", None

    def EMPTY(ctx):
        if ctx.data[ctx.cursor] != " ":
            return False, None, "FAILED"
        ctx.consume(1)
        return True, " ", None


#############

data1 = "aliali t"
data2 = "supp --help"
data3 = ["supp", "func", "True"]
data4 = ["supp", "--version"]
#
parser = Parser(Rules)
#

result = parser.parse(data1)
print(f"Result is :: {result}\n")
#
#
#
