from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Mapping
from my_lexer import *

@dataclass
class NumLiteral:
    value: int

    def __init__(self, *args):
        self.value = Fraction(*args)


# Define a StringLiteral class for testing in test_print
@dataclass
class StringLiteral:
    value: str

@dataclass
class BinOp:
    left: 'AST'
    operator: str
    right: 'AST'


@dataclass
class UniaryOp:
    operator: str
    operand: 'AST'

@dataclass
class Identifier:
    name: str


@dataclass
class Let:
    var: 'AST'
    e1: 'AST'
    e2: 'AST'

@dataclass
class Print:
    val: 'AST'
    
@dataclass
class Assignment:
    operator: str
    left: 'AST'
    right: 'AST'

@dataclass
class Slice:
    string_var: 'AST'
    start: 'AST'
    end: 'AST'
    step: 'AST'

@dataclass
class ComparisonOp:
    operand: str  # >,<
    left: 'AST'
    right: 'AST'

@dataclass
class IfElse:
    condition: ComparisonOp
    if_body: "AST"
    else_body: "AST"

@dataclass
class While:
    condition:ComparisonOp
    body:'AST'
    orelse:'AST'

@dataclass
class For:
    exp1: 'AST'
    condition:'AST'
    exp2:'AST'
    body : 'AST'

AST = NumLiteral | BinOp | Let | StringLiteral | Slice | Assignment | ComparisonOp | Identifier | IfElse

Value = Fraction | str | NumLiteral | StringLiteral | BinOp | float | bool | None | int

class InvalidProgram(Exception):
    print(Exception)



def eval(program: AST, environment: Mapping[str, Value] = None) -> Value:
    # print("eval")
    if environment is None:
        environment = {}

    match program:
        case NumLiteral(value):
            # print(value)
            return value        

        case FloatLiteral(value):
            return value
        case StringLiteral(value):
            return value
        case Identifier(name):
            if name in environment:
                return environment[name]
            raise InvalidProgram()
        case Let(Identifier(name), e1, e2):
            v1 = eval(e1, environment)
            return eval(e2, environment | {name: v1})

        case Print(val):
            # The print function will print the evaluated value of val and return the AST val
            if isinstance(val, NumLiteral) or isinstance(val, StringLiteral) or isinstance(val, BinOp):
                print(eval(val))
                return val
            else:
                raise InvalidProgram()

        case Assignment("=", left, right):
            right_val = eval(right)
            environment[left.name] = right_val
            return right_val

        case Slice(string_var, start, end, step):
            string_var = eval(string_var, environment)
            start = eval(start, environment)
            end = eval(end, environment)
            step = eval(step, environment)
            if isinstance(string_var, str) and isinstance(start, Fraction) and isinstance(end, Fraction) and isinstance(step, Fraction):
                return string_var[int(start):int(end):int(step)]
            else:
                raise InvalidProgram()

        case IfElse(condition_ast, if_ast, else_ast):
            condition_res = eval(condition_ast, environment)
            # print(f"The condition result {condition_res}")
            if condition_res == True:
                # print(f"Inside the if of IfElse")
                return eval(if_ast, environment)
            else:
                # print('Inside else of IfElse')
                return eval(else_ast, environment)

        case While(condition, body, orelse):
            cond = eval(condition)
            if (cond == True):
                eval(body)
                eval(While(condition, body))
            else:
                return eval(orelse)

        case For(exp1, condition, exp2, body):
            eval(exp1)
            cond = eval(condition)
            if (cond == True):
                eval(body)
                eval(exp2)
                eval(While(condition, body))

        # comperison operation
        case ComparisonOp(x, ">", const):
            if eval(x, environment) > eval(const, environment):
                # print("Inside If of >")
                return True
            # print("Inside else of >")
            return False

        case ComparisonOp(x, "<", const):
            if eval(x, environment) < eval(const, environment):
                # print("Inside If of <")
                return True
            # print("Inside else of <")
            return False

        case ComparisonOp(x, "==", const):
            if eval(x, environment) == eval(const, environment):
                # print("Inside If of ==")
                return True
            # print("Inside else of ==")
            return False

        case ComparisonOp(x, "!=", const):
            if eval(x, environment) != eval(const, environment):
                # print("Inside If of !=")
                return True
            # print("Inside else of !=")
            return False

        case ComparisonOp(x, "<=", const):
            if eval(x, environment) <= eval(const, environment):
                # print("Inside If of <=")
                return True
            # print("Inside else of <=")
            return False

        case ComparisonOp(x, ">=", const):
            if eval(x, environment) >= eval(const, environment):
                # print("Inside If of >=")
                return True
            # print("Inside else of >=")
            return False

        case UniaryOp("-", x):
            return eval(BinOp(NumLiteral(-1), "*", x))
        case UniaryOp("+", x):
            return eval(BinOp(NumLiteral(1), "*", x))
        # binary operation
        case BinOp(left, "+", right):
            eval_left = eval(left, environment)
            eval_right = eval(right, environment)
            if isinstance(eval_left, str) and isinstance(eval_right, str):
                return eval_left + eval_right
            elif isinstance(eval_left, Fraction) and isinstance(eval_right, Fraction):
                return eval_left + eval_right
            else:
                raise InvalidProgram(f"{type(eval_left)} and {type(eval_right)} cannot be added together")
        case BinOp(left, "-", right):
            eval_left = eval(left, environment)
            eval_right = eval(right, environment)
            if isinstance(eval_left, Fraction) and isinstance(eval_right, Fraction):
                return eval_left + eval_right
            else:
                raise InvalidProgram()
        case BinOp(left, "*", right):
            eval_left = eval(left, environment)
            eval_right = eval(right, environment)
            if isinstance(eval_left, Fraction) and isinstance(eval_right, Fraction):
                return eval_left * eval_right
            elif isinstance(eval_left, str) and isinstance(eval_right, Fraction):
                # Repeat the string eval_right times
                return eval_left * int(eval_right)
            else:
                raise InvalidProgram()
        case BinOp(left, "/", right):
            eval_left = eval(left, environment)
            eval_right = eval(right, environment)
            if isinstance(eval_left, Fraction) and isinstance(eval_right, Fraction):
                return eval_left / eval_right
            else:
                raise InvalidProgram()
        case BinOp(left, "//", right):
            return eval(left, environment) // eval(right, environment)
        case BinOp(left, "%",  right):
            return eval(left, environment) % eval(right, environment)
        case BinOp(left, "**", right):
            return eval(left, environment) ** eval(right, environment)

    raise InvalidProgram()


def test_if_else_eval():
    e1 = NumLiteral(5)
    e2 = NumLiteral(10)
    # assert eval(e2) == 10
    c1 = ComparisonOp(e1, ">", e2)  # e1(=5) > e2(10)
    o1 = NumLiteral(1)
    o2 = NumLiteral(0)  # return in false statement
    res1 = IfElse(c1, o1, o2)
    assert eval(res1) == 0, f"{eval(res1)} and other is {Fraction(6,1)}"
    c2 = ComparisonOp(e1, "<", e2)  # e1(=5) < e2(10)
    res2 = res1 = IfElse(c2, o1, o2)
    assert eval(res2) == 1, f"{eval(res2)} and other is {Fraction(6,1)}"
    # a = Identifier("a")


def test_eval():
    e1 = NumLiteral(2)
    e2 = NumLiteral(7)
    e3 = NumLiteral(9)
    e4 = NumLiteral(5)
    e5 = BinOp(e2, "+", e3)
    e6 = BinOp(e5, "/", e4)
    e7 = BinOp(e1, "*", e6)
    assert float(eval(e7)) == 6.4, f"{eval(e7)} and other is {FloatLiteral(6.4)} do not match"

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
    e4 = BinOp(e1,"+", e2)
    assert eval(eval(Print(e4))) == 7

    # Check on binop with print and nested print
    assert eval(eval(Print(eval(Print(e4))))) == Fraction(7, 1)

    assert eval(BinOp(eval(Print(e4)),"+",e1)) == Fraction(9, 1)

    assert eval(BinOp(eval(Print(e2)),"+", eval(Print(e1)))) == Fraction(7, 1)
    
def test_assignment():
    a  = Identifier("a")
    e1 = NumLiteral(2)
    e2 = Assignment("=", a, e1)

    assert eval(e2) == Fraction(2, 1)

    b = Identifier("b")      
    e3 = NumLiteral(5)      
    e4 = Assignment("=", b, e3)     #b = 5
    assert eval(e4) == Fraction(5, 1)
    
    # Reassignment 
    e6 = Assignment("=", a, e3)
    assert eval(e6) == Fraction(5, 1)

def test_strings():
    # For now using python typecasting for converting Fraction to int
    e1 = StringLiteral("Hello")
    e2 = StringLiteral("World!")
    assert eval(e1) == "Hello"
    assert eval(e2) == "World!"
    e3 = BinOp(e1,"+",e2)
    assert eval(e3) == "HelloWorld!"

    e3 = NumLiteral(2)
    e4 = BinOp(e1,"*",e3)
    assert eval(e4) == "HelloHello"

    e5 = StringLiteral("HelloWorld!")
    e6 = NumLiteral(2)
    e7 = NumLiteral(5)
    e8 = NumLiteral(1)
    e9 = Slice(e5,e6,e7,e8)
    assert eval(e9) == "llo"

    # e10 = NumLiteral(2)
    # e11 = StringLiteral("Hello")
    # e12 = BinOp(e11,"+",e10)
    # assert eval(e12) == "Hello2"

def test_uniary():
    e1 = NumLiteral(2)
    e2 = NumLiteral(-7)
    e5 = UniaryOp("+", e2)
    e6 = UniaryOp("-", e2)
    assert eval(e5) == -7, f"{eval(e5)} and other is {NumLiteral(-7)} do not match"
    assert eval(e6) == 7, f"{eval(e6)} and other is {NumLiteral(7)} do not match"


if __name__ == "__main__":
    test_eval()
    test_let_eval()
    test_if_else_eval()
    # test_uniary()
    print("All tests passed")
