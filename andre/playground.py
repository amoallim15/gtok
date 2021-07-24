from parser import *

AND = Sequence
OR = OrderedChoice
LOOP = Loop
NOT = Not
RAISE = Raise

class Rules:
    #
    start = AND(
                "ALI", 
                OR(
                    AND("EMPTY", RAISE("TEST")),
                    AND("EMPTY", RAISE("HI")),
                    AND("EMPTY", "EMPTY", RAISE("HI")),
                labels=["TEST", "HI"]), 
                "ALI"
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
                return False, "FAILED"
            ctx.consume(1)
        return True, "ali"

    def EMPTY(ctx):
        if ctx.data[ctx.cursor] != " ":
            return False, "FAILED"
        ctx.consume(1)
        return True, " "


#############

data1 = "ali  ali"
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
