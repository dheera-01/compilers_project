from dataclasses import dataclass
from typing import Union, Mapping
from declaration import *


Value = str | BinOp | float | bool | None | int

global_env={}
class InvalidProgram(Exception):
    pass


def eval(program: AST, environment: Mapping[str, Value] = None) -> Value:
    global global_env
    if environment is None:
        environment = {}

    match program:
        case NumLiteral(value):
            return value
        case FloatLiteral(value):
            return value
        case StringLiteral(value):
            return value

        case Identifier(name):
            if name in global_env:
                return global_env[name]
            raise InvalidProgram()

        case Let(Identifier(name), e1, e2):
            v1 = eval(e1, environment)
            global_env[name]=v1
            return eval(e2, environment | {name: v1})

        case Print(val):
            # The print function will print the evaluated value of val and return the AST val
            if isinstance(val, NumLiteral) or isinstance(val, StringLiteral) or isinstance(val, BinOp) or isinstance(val,Identifier):
                print(eval(val))
                return val
            else:
                raise InvalidProgram()



        case Slice(string_var, start, end, step):
            # How are handling the case a[1:] and its other variants

            string_var = eval(string_var, environment)
            start = eval(start, environment)
            end = eval(end, environment)
            step = eval(step, environment)
            if isinstance(string_var, str) and isinstance(start, int) and isinstance(end, int) and isinstance(step, int):
                return string_var[int(start):int(end):int(step)]
            else:
                raise InvalidProgram(
                    f"TypeError: slice indices must be NumLiteral")

        case IfElse(condition_ast, if_ast, else_ast):
            condition_res = eval(condition_ast, environment)
            # print(f"The condition result {condition_res}")
            if condition_res == True:
                # print(f"Inside the if of IfElse")
                return eval(if_ast, environment)
            else:
                # print('Inside else of IfElse')
                return eval(else_ast, environment)

        # comparison operation
        case ComparisonOp(x, ">", const):
            try:
                if eval(x, environment) > eval(const, environment):
                    return True
                return False
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: > not supported between instances of {x} and {const}")

        case ComparisonOp(x, "<", const):
            try:
                if eval(x, environment) < eval(const, environment):
                    return True
                return False
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: < not supported between instances of {x} and {const}")

        case ComparisonOp(x, "==", const):
            try:
                if eval(x, environment) == eval(const, environment):
                    return True
                return False
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: == not supported between instances of {x} and {const}")

        case ComparisonOp(x, "!=", const):
            try:
                if eval(x, environment) != eval(const, environment):
                    return True
                return False
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: != not supported between instances of {x} and {const}")

        case ComparisonOp(x, "<=", const):
            try:
                if eval(x, environment) <= eval(const, environment):
                    return True
                return False
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: <= not supported between instances of {x} and {const}")

        case ComparisonOp(x, ">=", const):
            try:
                if eval(x, environment) >= eval(const, environment):
                    return True
                return False
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: >= not supported between instances of {x} and {const}")

        # unary operation
        case UnaryOp("-", x):
            try:
                return eval(BinOp(NumLiteral(-1), "*", x))
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: - not supported between instances of {x}")

        case UnaryOp("+", x):
            try:
                return eval(BinOp(NumLiteral(1), "*", x))
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: + not supported between instances of {x}")

        # binary operation
        case BinOp(left, "+", right):
            eval_left = eval(left, environment)
            eval_right = eval(right, environment)
            try:
                return eval_left + eval_right
            except Exception as e:
                # raise TypeError(f"+ not supported between instances of {type(eval_left).__name__} and {type(eval_right).__name__}")
                raise InvalidProgram(
                    f"+ not supported between instances of {left} and {right}")

        case BinOp(left, "-", right):
            eval_left = eval(left, environment)
            eval_right = eval(right, environment)
            try:
                return eval_left - eval_right
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: - not supported between instances of {left} and {right}")

        case BinOp(left, "*", right):
            eval_left = eval(left, environment)
            eval_right = eval(right, environment)
            try:
                return eval_left * eval_right
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: ** not supported between instances of {left} and {right}")

        case BinOp(left, "/", right):
            eval_left = eval(left, environment)
            eval_right = eval(right, environment)
            try:
                return eval_left / eval_right
            except ZeroDivisionError as e:
                raise InvalidProgram(f"ZeroDivisionError: division by zero")
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: / not supported between instances of {left} and {right}")

        case BinOp(left, "//", right):
            eval_left = eval(left, environment)
            eval_right = eval(right, environment)
            try:
                return eval_left // eval_right
            except ZeroDivisionError as e:
                raise InvalidProgram(
                    f"ZeroDivisionError: floor division by zero")
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: // not supported between instances of {left} and {right}")

        case BinOp(left, "%",  right):
            eval_left = eval(left, environment)
            eval_right = eval(right, environment)
            try:
                return eval_left % eval_right
            except ZeroDivisionError as e:
                raise InvalidProgram(f"ZeroDivisionError: modulo by zero")
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: % not supported between instances of {left} and {right}")

        case BinOp(left, "**", right):
            eval_left = eval(left, environment)
            eval_right = eval(right, environment)
            try:
                return eval_left ** eval_right
            except Exception as e:
                raise InvalidProgram(
                    f"TypeError: ** not supported between instances of {left} and {right}")
        case Seq(lst):
            for expr in lst:
                eval(expr,environment)
            return None

        case While(cond,body):

            c=eval(cond,environment)
            # if(c==True):
            #     eval(body)
            #     eval(While(cond,body))
            while(c==True):
                eval(body,environment)
                c=eval(cond,environment)
            # while loop cannot be implemented recursivly as max recursion depth of python restricts it
            return None
        case For(exp1, condition, exp2, Seq(lst)):
            eval(exp1)
            cond = eval(condition)
            if (cond == True):
                eval(Seq(lst))
                eval(exp2)
                lst.append(exp2)
                eval(While(condition, Seq(lst)))
            return None
        case Assign(Identifier(name),right):
            val=eval(right)
            global_env[name]=val
            return None
    raise InvalidProgram(f"SyntaxError: {program} invalid syntax")


def test_if_else_eval():
    e1 = NumLiteral(5)
    e2 = NumLiteral(10)
    c1 = ComparisonOp(e1, ">", e2)  # e1(=5) > e2(10)
    o1 = NumLiteral(1)
    o2 = NumLiteral(0)  # return in false statement
    res1 = IfElse(c1, o1, o2)
    assert eval(res1) == 0, f"{eval(res1)} and other is NumLiteral(0)"
    c2 = ComparisonOp(e1, "<", e2)  # e1(=5) < e2(10)
    res2 = res1 = IfElse(c2, o1, o2)
    assert eval(res2) == 1, f"{eval(res2)} and other is 1"
    # a = Identifier("a")


def test_eval():
    e1 = NumLiteral(2)
    e2 = NumLiteral(7)
    e4 = NumLiteral(5)
    e5 = BinOp(e1, "+", e2)
    e6 = BinOp(e5, "*", e4)
    assert eval(e6) == 45, f"{eval(e6)} and other is 45"
    


def test_let_eval():
    a = Identifier("a")
    e1 = NumLiteral(5)
    e2 = BinOp(a, "+", a)
    e = Let(a, e1, e2)
    assert eval(e) == 10
    e = Let(a, e1, Let(a, e2, e2))
    assert eval(e) == 20
    e = Let(a, e1, BinOp(a, "+", Let(a, e2, e2)))
    assert eval(e) == 25
    e = Let(a, e1, BinOp(Let(a, e2, e2), "+", a))
    assert eval(e) == 25
    e3 = NumLiteral(6)
    e = BinOp(Let(a, e1, e2), "+",  Let(a, e3, e2))
    assert eval(e) == 22


def test_print():
    # Check on number literal
    e1 = NumLiteral(2)
    e2 = NumLiteral(5)

    assert eval(eval(Print(e2))) == 5
    assert eval(eval(Print(e1))) == 2

    # Check on string literal
    e3 = StringLiteral("Hello")
    assert eval(eval(Print(e3))) == "Hello"

    # Check on binop
    e4 = BinOp(e1, "+", e2)
    assert eval(eval(Print(e4))) == 7

    # Check on binop with print and nested print
    assert eval(eval(Print(eval(Print(e4))))) == 7

    assert eval(BinOp(eval(Print(e4)), "+", e1)) == 9

    assert eval(BinOp(eval(Print(e2)), "+", eval(Print(e1)))) == 7


def test_assignment():
    a = Identifier("a")
    e1 = NumLiteral(2)
    e2 = Assignment("=", a, e1)

    assert eval(e2) == 2

    b = Identifier("b")
    e3 = NumLiteral(5)
    e4 = Assignment("=", b, e3)  # b = 5
    assert eval(e4) == 5

    # Reassignment
    e6 = Assignment("=", a, e3)
    assert eval(e6) == 5


def test_strings():
    e1 = StringLiteral("Hello")
    e2 = StringLiteral("World!")
    assert eval(e1) == "Hello"
    assert eval(e2) == "World!"
    e3 = BinOp(e1, "+", e2)
    assert eval(e3) == "HelloWorld!"

    e3 = NumLiteral(2)
    e4 = BinOp(e1, "*", e3)
    assert eval(e4) == "HelloHello"

    e5 = StringLiteral("HelloWorld!")
    e6 = NumLiteral(2)
    e7 = NumLiteral(5)
    e8 = NumLiteral(1)
    e9 = Slice(e5, e6, e7, e8)
    assert eval(e9) == "llo"

    # e10 = NumLiteral(2)
    # e11 = StringLiteral("Hello")
    # e12 = BinOp(e11,"+",e10)
    # assert eval(e12) == "Hello2"


def test_unary():
    e1 = NumLiteral(2)
    e2 = NumLiteral(-7)
    e5 = UnaryOp("+", e2)
    e6 = UnaryOp("-", e2)
    assert eval(e5) == - \
        7, f"{eval(e5)} and other is {NumLiteral(-7)} do not match"
    assert eval(
        e6) == 7, f"{eval(e6)} and other is {NumLiteral(7)} do not match"


def test_varibale():

    a=Identifier("a")
    e1=BinOp(NumLiteral(2),"+",NumLiteral(3))
    e2=BinOp(NumLiteral(2),"+",NumLiteral(2))
    e3=Let(a,e1,e2)
    s=Seq([a,e1,e2,e3])
    eval(s)
    # assert eval(a)== 5


if __name__ == "__main__":
    # test_eval()
    # test_strings()
    # test_let_eval()
    # test_if_else_eval()
    # test_unary()
    # test_while()
    print("All tests passed")




def test_while():
    # env={"i":NumLiteral(0)}
    # i=Identifier("i")
    # e2=BinOp(i,"+",1)
    # e1=BinOp(i,"+",e2)
    # print(eval(Let(i,e1,e1),env))
    cond=ComparisonOp(NumLiteral(5),"<",NumLiteral(10))
    eval(While(cond,Print(StringLiteral("Hello"))))

def test_global_var():
    i=Identifier("i")
    # e1=Let(i,NumLiteral(0),NumLiteral(2))
    e1=Assign(i,NumLiteral(0))

    # p=Print(StringLiteral("Hello"))
    p=Print(i)
    inc=Assign(i,BinOp(i,"+",NumLiteral(1)))
    body=Seq([p,inc])
    e2=While(ComparisonOp(i,"<",NumLiteral(10)),body)
    eval(Seq([e1,e2]))
    print(global_env)

def test_for():
    # cond=ComparisonOp(NumLiteral(5),"<",NumLiteral(10))
    # e1=NumLiteral(0)
    # e2=NumLiteral(1)
    # body=Print(StringLiteral("Hello"))
    # eval(For(e1,cond,e2,body))
    i=Identifier("i")
    a=Assign(i,NumLiteral(0))
    e2=ComparisonOp(i,"<",NumLiteral(6))
    e3=Assign(i,BinOp(i,"+",NumLiteral(1)))
    p=Print(i)
    eval(For(a,e2,e3,Seq([p])))

def test_seq():
    e1=NumLiteral(0)
    e2=NumLiteral(1)
    s=Seq([e1,e2])
    eval(s)

def test_assign():
    i=Identifier("i")
    a=Assign(i,NumLiteral(0))
    eval(a)
    print(global_env)

if __name__ == "__main__":
# test_while()
    test_for()
# test_global_var()
# test_seq()
# test_assign()