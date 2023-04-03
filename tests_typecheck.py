from my_parser import *
from static_typecheck import typecheck

def test_typecheck_numliteral():
    ast = NumLiteral(42)
    assert typecheck(ast) == ast

def test_typecheck_floatliteral():
    ast = FloatLiteral(3.14)
    assert typecheck(ast) == ast

def test_typecheck_stringliteral():
    ast = StringLiteral("hello")
    assert typecheck(ast) == ast

def test_typecheck_boolliteral():
    ast = BoolLiteral(True)
    assert typecheck(ast) == ast

def test_typecheck_identifier():
    ast = Identifier("x")
    assert typecheck(ast) == ast

# def test_typecheck_let():
#     ast = Let([Identifier("x")], [NumLiteral(42)]),
#     assert typecheck(ast) == NumLiteral(42)

def test_typecheck_assign():
    ast = Assign([Identifier("x")], [NumLiteral(42)])
    assert typecheck(ast) is None

def test_typecheck_update():
    ast = Update(Identifier("x"), "+=", NumLiteral(1))
    assert typecheck(ast) is None

def test_typecheck_print():
    ast = Print(NumLiteral(42))
    assert typecheck(ast) is None

def test_typecheck_while():
    ast = While(BoolLiteral(True), NumLiteral(42))
    assert typecheck(ast) is None

def test_typecheck_for():
    ast = For(NumLiteral(0), BoolLiteral(True), NumLiteral(1), NumLiteral(42))
    assert typecheck(ast) is None

def test_typecheck_slice():
    ast = Slice(Identifier("s"), NumLiteral(0), NumLiteral(1), NumLiteral(2))
    assert typecheck(ast) == StringLiteral("")

# def test_typecheck_ifelse():
#     ast = IfElse(BoolLiteral(True),Assign([Identifier("x")], [NumLiteral(42)]),[IfElse(BoolLiteral(False, Assign([Identifier("x")], [NumLiteral(42)]))],Assign([Identifier("x")], [NumLiteral(42)]))
#     assert typecheck(ast) is None

def test_typecheck_comparisonop():
    ast = ComparisonOp(NumLiteral(42), "==", NumLiteral(42))
    assert typecheck(ast) == BoolLiteral(True)

def test_typecheck_unaryop():
    ast = UnaryOp("-", NumLiteral(42))
    assert typecheck(ast) == NumLiteral(42)

def test_typecheck_binop():
    ast = BinOp(NumLiteral(42), "+", NumLiteral(42))
    assert typecheck(ast) == NumLiteral(0)
