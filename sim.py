from dataclasses import dataclass
from fractions import Fraction
from typing import Union, Mapping

@dataclass
class NumLiteral:
    value: Fraction
    def __init__(self, *args):
        self.value = Fraction(*args)

# Define a stringLiteral class for testing in test_print
@dataclass
class StringLiteral:
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
class Print:
    value: 'AST'

@dataclass
class Assignment:
    operator: str
    left: 'AST'
    right: 'AST'

AST = NumLiteral | BinOp | Variable | Let | Print | StringLiteral | Assignment

Value = Fraction | str

class InvalidProgram(Exception):
    pass

def PrintHelper(value):
    if isinstance(value, NumLiteral) or isinstance(value, StringLiteral) or isinstance(value, BinOp):
        print(eval(value))
        return eval(value)
    else:
        raise InvalidProgram()


def eval(program: AST, environment: Mapping[str, Value] = None) -> Value:
    if environment is None:
        environment = {}
    match program:
        case NumLiteral(value):
            return value
        case StringLiteral(value):
            return value
        case Variable(name):
            if name in environment:
                return environment[name]
            raise InvalidProgram()
        case Print(value):
            return PrintHelper(value)
        case Assignment("=", left, right):
            right_val = eval(right)
            environment[left.name] = right_val
            return right_val
        case Let(Variable(name), e1, e2):
            v1 = eval(e1, environment)
            return eval(e2, environment | { name: v1 })
        case BinOp("+", left, right):
            return eval(left, environment) + eval(right, environment)
        case BinOp("-", left, right):
            return eval(left, environment) - eval(right, environment)
        case BinOp("*", left, right):
            return eval(left, environment) * eval(right, environment)
        case BinOp("/", left, right):
            return eval(left, environment) / eval(right, environment)
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

def test_print():
    # Check on number literal
    e1 = NumLiteral(2)
    e2 = NumLiteral(5)
    assert eval(Print(e2)) == Fraction(5, 1)
    assert eval(Print(e1)) == Fraction(2, 1)

    # Check on string literal
    e3 = StringLiteral("Hello")
    assert eval(Print(e3)) == "Hello"

    # Check on binop
    e4 = BinOp("+", e1, e2)
    assert eval(Print(e4)) == Fraction(7, 1)

    
def test_assignment():
    a  = Variable("a")
    e1 = NumLiteral(2)
    e2 = Assignment("=", a, e1)

    assert eval(e2) == Fraction(2, 1)

    b = Variable("b")      
    e3 = NumLiteral(5)      
    e4 = Assignment("=", b, e3)     #b = 5
    assert eval(e4) == Fraction(5, 1)
    
    # Reassignment 
    e6 = Assignment("=", a, e3)
    assert eval(e6) == Fraction(5, 1)
