from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Mapping
from my_lexer import *

# @dataclass
# class NumLiteral:
#     value: int

#     def __init__(self, *args):
#         self.value = Fraction(*args)


@dataclass
class BinOp:
    operator: str
    left: 'AST'
    right: 'AST'


# @dataclass
# class Variable:
#     name: str


@dataclass
class Let:
    var: 'AST'
    e1: 'AST'
    e2: 'AST'


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



AST = NumLiteral | BinOp | Let | ComparisonOp | Identifier | IfElse
# AST = NumLiteral | BinOp | Variable | Let | ComparisonOp

Value = float | bool | str | None | int


class InvalidProgram(Exception):
    pass


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
        case Identifier(name):
            if name in environment:
                return environment[name]
            raise InvalidProgram()
        case Let(Identifier(name), e1, e2):
            v1 = eval(e1, environment)
            return eval(e2, environment | {name: v1})

        case IfElse(condition_ast, if_ast, else_ast):
            condition_res = eval(condition_ast, environment)
            # print(f"The condition result {condition_res}")
            if condition_res == True:
                # print(f"Inside the if of IfElse")
                return eval(if_ast,environment)
            else:
                # print('Inside else of IfElse')
                return eval(else_ast,environment)

        # comperison operation
        case ComparisonOp(">", x, const):
            if eval(x, environment) > eval(const, environment):
                # print("Inside If of >")
                return True
            # print("Inside else of >")
            return False
        
        case ComparisonOp("<", x, const):
            if eval(x, environment) < eval(const, environment):
                # print("Inside If of <")
                return True
            # print("Inside else of <")
            return False
        
        case ComparisonOp("==", x, const):
            if eval(x, environment) == eval(const, environment):
                # print("Inside If of ==")
                return True
            # print("Inside else of ==")
            return False
        
        case ComparisonOp("!=", x, const):
            if eval(x, environment) != eval(const, environment):
                # print("Inside If of !=")
                return True
            # print("Inside else of !=")
            return False
        
        case ComparisonOp("<=", x, const):
            if eval(x, environment) <= eval(const, environment):
                # print("Inside If of <=")
                return True
            # print("Inside else of <=")
            return False
        
        case ComparisonOp(">=", x, const):
            if eval(x, environment) >= eval(const, environment):
                # print("Inside If of >=")
                return True
            # print("Inside else of >=")
            return False
        
        # binary operation
        case BinOp("+", left, right):
            return eval(left, environment) + eval(right, environment)
        case BinOp("-", left, right):
            return eval(left, environment) - eval(right, environment)
        case BinOp("*", left, right):
            return eval(left, environment) * eval(right, environment)
        case BinOp("/", left, right):
            return eval(left, environment) / eval(right, environment)
        case BinOp("//", left, right):
            return eval(left, environment) // eval(right, environment)
        case BinOp("%", left, right):
            return eval(left, environment) % eval(right, environment)
        case BinOp("**", left, right):
            return eval(left, environment) ** eval(right, environment)

    raise InvalidProgram()

def test_if_else_eval():
    e1 = NumLiteral(5)
    e2 = NumLiteral(10)
    # assert eval(e2) == 10
    c1 = ComparisonOp(">", e1, e2)  # e1(=5) > e2(10)
    o1 = NumLiteral(1)
    o2 = NumLiteral(0) # return in false statement
    res1 = IfElse(c1, o1, o2)
    assert eval(res1) ==0, f"{eval(res1)} and other is {Fraction(6,1)}"
    c2 = ComparisonOp("<", e1, e2)  # e1(=5) < e2(10)
    res2 = res1 = IfElse(c2, o1, o2)
    assert eval(res2) == 1, f"{eval(res2)} and other is {Fraction(6,1)}"
    # a = Identifier("a")
    
    
    


def test_eval():
    e1 = NumLiteral(2)
    e2 = NumLiteral(7)
    e3 = NumLiteral(9)
    e4 = NumLiteral(5)
    e5 = BinOp("+", e2, e3)
    e6 = BinOp("/", e5, e4)
    e7 = BinOp("*", e1, e6)
    assert eval(e7) == 6.4, f"{eval(e7)} and other is {FloatLiteral(6.4)} do not match"


def test_let_eval():
    a = Identifier("a")
    e1 = NumLiteral(5)
    e2 = BinOp("+", a, a)
    e = Let(a, e1, e2)
    assert eval(e) == 10
    e = Let(a, e1, Let(a, e2, e2))
    assert eval(e) == 20
    e = Let(a, e1, BinOp("+", a, Let(a, e2, e2)))
    assert eval(e) == 25
    e = Let(a, e1, BinOp("+", Let(a, e2, e2), a))
    assert eval(e) == 25
    e3 = NumLiteral(6)
    e = BinOp("+", Let(a, e1, e2), Let(a, e3, e2))
    assert eval(e) == 22


if __name__ == "__main__":
    test_eval()
    test_let_eval()
    test_if_else_eval()
    print("All tests passed")