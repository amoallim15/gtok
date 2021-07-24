from parser import *

AND = Sequence
OR = OrderedChoice
LOOP = Loop
NOT = Not
RAISE = Raise

class Rules:
    #
    start = AND("ali", OR("ali", True))
    #
    # labels = {"FATAL"}
    # funcs are:
    # 1. terminal processors
    # 2. action functions

    # token
    def ali(ctx):
        test = "ali"
        for c in test:
            if ctx.data[ctx.cursor] != c:
                return False, "FAIL"
            ctx.step()
        return True, "ali"

    def empty(ctx):
        if ctx.data[ctx.cursor] != " ":
            return False, "FAIL"
        return True, None


#############

data1 = "ali ali"
data2 = "supp --help"
data3 = ["supp", "func", "True"]
data4 = ["supp", "--version"]
#
parser = Parser(Rules)
#

# result = parser.parse(data1)
print(data4)
# print(f"""Result is :: "{result}"\n""")
#
#
#
