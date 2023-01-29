from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Mapping

@dataclass
class NumLiteral:
    value: Fraction
    def __init__(self, *args):
        self.value = Fraction(*args)

@dataclass
class StrLiteral:
    value: str

@dataclass
class BinOp:
    operator: str
    left: 'AST'
    right: 'AST'

@dataclass
class Variable:
    name: str

@dataclass
class Let:
    var: 'AST'
    e1: 'AST'
    e2: 'AST'

@dataclass
class Slice:
    string_var: 'AST'
    start: 'AST'
    end: 'AST'
    step: 'AST'

AST = NumLiteral | BinOp | Variable | Let | StrLiteral | Slice

Value = Fraction | str

class InvalidProgram(Exception):
    print(Exception)

def eval(program: AST, environment: Mapping[str, Value] = None) -> Value:
    if environment is None:
        environment = {}
    match program:
        case NumLiteral(value):
            return value
        case StrLiteral(value):
            return value
        case Variable(name):
            if name in environment:
                return environment[name]
            raise InvalidProgram()
        case Let(Variable(name), e1, e2):
            v1 = eval(e1, environment)
            return eval(e2, environment | { name: v1 })
        case Slice(string_var, start, end, step):
            string_var = eval(string_var, environment)
            start = eval(start, environment)
            end = eval(end, environment)
            step = eval(step, environment)
            if isinstance(string_var, str) and isinstance(start, Fraction) and isinstance(end, Fraction) and isinstance(step, Fraction):
                return string_var[int(start):int(end):int(step)]
            else:
                raise InvalidProgram()
        case BinOp("+", left, right):
            eval_left = eval(left, environment)
            eval_right = eval(right, environment)
            if isinstance(eval_left, str) and isinstance(eval_right, str):
                return eval_left + eval_right
            elif isinstance(eval_left, Fraction) and isinstance(eval_right, Fraction):
                return eval_left + eval_right
            else:
                raise InvalidProgram()
        case BinOp("-", left, right):
            eval_left = eval(left, environment)
            eval_right = eval(right, environment)
            if isinstance(eval_left, Fraction) and isinstance(eval_right, Fraction):
                return eval_left + eval_right
            else:
                raise InvalidProgram()
        case BinOp("*", left, right):
            eval_left = eval(left, environment)
            eval_right = eval(right, environment)
            if isinstance(eval_left, Fraction) and isinstance(eval_right, Fraction):
                return eval_left * eval_right
            elif isinstance(eval_left, str) and isinstance(eval_right, Fraction):
                # Repeat the string eval_right times
                return eval_left * int(eval_right)
            else:
                raise InvalidProgram()
        case BinOp("/", left, right):
            eval_left = eval(left, environment)
            eval_right = eval(right, environment)
            if isinstance(eval_left, Fraction) and isinstance(eval_right, Fraction):
                return eval_left / eval_right
            else:
                raise InvalidProgram()
    raise InvalidProgram()

def test_eval():
    e1 = NumLiteral(2)
    e2 = NumLiteral(7)
    e3 = NumLiteral(9)
    e4 = NumLiteral(5)
    e5 = BinOp("+", e2, e3)
    e6 = BinOp("/", e5, e4)
    e7 = BinOp("*", e1, e6)
    assert eval(e7) == Fraction(32, 5)

def test_let_eval():
    a  = Variable("a")
    e1 = NumLiteral(5)
    e2 = BinOp("+", a, a)
    e  = Let(a, e1, e2)
    assert eval(e) == 10
    e  = Let(a, e1, Let(a, e2, e2))
    assert eval(e) == 20
    e  = Let(a, e1, BinOp("+", a, Let(a, e2, e2)))
    assert eval(e) == 25
    e  = Let(a, e1, BinOp("+", Let(a, e2, e2), a))
    assert eval(e) == 25
    e3 = NumLiteral(6)
    e  = BinOp("+", Let(a, e1, e2), Let(a, e3, e2))
    assert eval(e) == 22

def test_strings():
    # For now using python typecasting for converting Fraction to int
    e1 = StrLiteral("Hello")
    e2 = StrLiteral("World!")
    assert eval(e1) == "Hello"
    assert eval(e2) == "World!"
    e3 = BinOp("+",e1,e2)
    assert eval(e3) == "HelloWorld!"

    e3 = NumLiteral(2)
    e4 = BinOp("*",e1,e3)
    assert eval(e4) == "HelloHello"

    e5 = StrLiteral("HelloWorld!")
    e6 = NumLiteral(2)
    e7 = NumLiteral(5)
    e8 = NumLiteral(1)
    e9 = Slice(e5,e6,e7,e8)
    assert eval(e9) == "llo"