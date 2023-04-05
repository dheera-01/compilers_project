from my_parser import *
from static_typecheck import typecheck
import pytest

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
    # Test case where string_var is not a string
    with pytest.raises(Exception) as exception_1:
        ast = typecheck(Slice(FloatLiteral(3.14), NumLiteral(0), NumLiteral(3), NumLiteral(1)))
    assert str(exception_1.value) == 'Slice operand must be a string'

    # Test case where start index is not a number
    with pytest.raises(Exception) as exception_2:
        ast = typecheck(Slice(StringLiteral("hello"), BoolLiteral(True), NumLiteral(3), NumLiteral(1)))
    assert str(exception_2.value) == 'Slice start index must be a number'

    # Test case where end index is not a number
    with pytest.raises(Exception) as exception_3:
        ast = typecheck(Slice(StringLiteral("hello"), NumLiteral(0), FloatLiteral(3.0), NumLiteral(1)))
    assert str(exception_3.value) == 'Slice end index must be a number'

    # Test case where step index is not a number
    with pytest.raises(Exception) as exception_4:
        ast = typecheck(Slice(StringLiteral("hello"), NumLiteral(0), NumLiteral(3), BoolLiteral(False)))
    assert str(exception_4.value) == 'Slice step index must be a number'

    # Test case where all inputs are correct
    ast = typecheck(Slice(StringLiteral("hello"), NumLiteral(0), NumLiteral(3), NumLiteral(1)))
    assert ast == StringLiteral("")

    # Test case where all inputs are Identifier types
    ast = typecheck(Slice(Identifier("s"), Identifier("start"), Identifier("end"), Identifier("step")))
    assert ast == StringLiteral("")


def test_typecheck_ifelse():
    with pytest.raises(Exception) as exception_1:
        ast = typecheck(IfElse(NumLiteral(1), NumLiteral(2), [], NumLiteral(3)))
    assert str(exception_1.value) == 'TypeError: NumLiteral(1) is not a boolean'


def test_typecheck_comparison_op():
    # Test less than operator with numbers
    ast = typecheck(ComparisonOp(NumLiteral(2), "<", NumLiteral(3)))
    assert ast == BoolLiteral(True)

    ast = typecheck(ComparisonOp(NumLiteral(4), "<", NumLiteral(2)))
    assert ast == BoolLiteral(True)

    # Test greater than operator with floats
    ast = typecheck(ComparisonOp(FloatLiteral(1.5), ">", FloatLiteral(1.0)))
    assert ast == BoolLiteral(True)

    ast = typecheck(ComparisonOp(FloatLiteral(0.5), ">", FloatLiteral(3.0)))
    assert ast == BoolLiteral(True)

    # Test equality operator with identifiers
    ast = typecheck(ComparisonOp(Identifier("x"), "==", Identifier("y")))
    assert ast == BoolLiteral(True)

    ast = typecheck(ComparisonOp(Identifier("z"), "==", Identifier("w")))
    assert ast == BoolLiteral(True)

    # Test inequality operator with numbers and floats
    ast = typecheck(ComparisonOp(NumLiteral(1), "!=", NumLiteral(3)))
    assert ast == BoolLiteral(True)

    ast = typecheck(ComparisonOp(FloatLiteral(3.0), "!=", FloatLiteral(3.0)))
    assert ast == BoolLiteral(True)

    ast = typecheck(ComparisonOp(StringLiteral("test"), ">=", Identifier("x")))
    assert ast == BoolLiteral(True)

    # Test unsupported operators
    with pytest.raises(Exception) as exception_1:
        ast = typecheck(ComparisonOp(BoolLiteral(True), "and", NumLiteral(2)))
    assert str(exception_1.value) == "TypeError: and not supported between instances of BoolLiteral(True) and NumLiteral(2)"

    # Test operands with different types
    with pytest.raises(Exception) as exception_3:
        ast = typecheck(ComparisonOp(NumLiteral(1), "<=", StringLiteral("test")))
    assert str(exception_3.value) == """TypeError: <= not supported between instances of NumLiteral(1) and StringLiteral("test")"""



def test_typecheck_unary_op():
    # Test addition and subtraction with numbers
    ast = typecheck(UnaryOp("+", NumLiteral(2)))
    assert ast == NumLiteral(0)

    ast = typecheck(UnaryOp("-", NumLiteral(3)))
    assert ast == NumLiteral(0)

    # Test addition and subtraction with floats
    ast = typecheck(UnaryOp("+", FloatLiteral(2.0)))
    assert ast == FloatLiteral(0.0)

    ast = typecheck(UnaryOp("-", FloatLiteral(3.0)))
    assert ast == FloatLiteral(0.0)

    # Test addition and subtraction with identifiers
    ast = typecheck(UnaryOp("+", Identifier("x")))
    assert ast == NumLiteral(0)

    ast = typecheck(UnaryOp("-", Identifier("y")))
    assert ast == NumLiteral(0)

    # Test invalid operands
    with pytest.raises(Exception) as exception_1:
        ast = typecheck(UnaryOp("+", BoolLiteral(True)))
    assert str(exception_1.value) == "TypeError: + not supported for instances of BoolLiteral(True)"

    with pytest.raises(Exception) as exception_2:
        ast = typecheck(UnaryOp("-", StringLiteral('test')))
    assert str(exception_2.value) == """TypeError: - not supported for instances of StringLiteral("test")"""


def test_typecheck_binop_plus():
    # Test valid inputs
    ast = typecheck(BinOp(NumLiteral(2), "+", NumLiteral(3)))
    assert ast == NumLiteral(0)

    ast = typecheck(BinOp(FloatLiteral(2.5), "+", NumLiteral(3)))
    assert ast == FloatLiteral(0.0)

    ast = typecheck(BinOp(NumLiteral(2), "+", FloatLiteral(3.5)))
    assert ast == FloatLiteral(0.0)

    ast = typecheck(BinOp(StringLiteral("hello"), "+", StringLiteral("world")))
    assert ast == StringLiteral("")

    ast = typecheck(BinOp(StringLiteral("hello"), "+", NumLiteral(123)))
    assert ast == StringLiteral("")

    ast = typecheck(BinOp(NumLiteral(123), "+", StringLiteral("hello")))
    assert ast == StringLiteral("")

    ast = typecheck(BinOp(Identifier("a"), "+", NumLiteral(2)))
    assert ast == NumLiteral(0)

    with pytest.raises(Exception) as exception_2:
        ast = typecheck(BinOp(FloatLiteral(2.5), "+", BoolLiteral(True)))
    assert str(
        exception_2.value) == 'TypeError: + not supported between instances of FloatLiteral(2.5) and BoolLiteral(True)'

    with pytest.raises(Exception) as exception_3:
        ast = typecheck(BinOp(StringLiteral("hello"), "+", BoolLiteral(False)))
    assert str(
        exception_3.value) == 'TypeError: + not supported between instances of StringLiteral("hello") and BoolLiteral(False)'

def test_typecheck_binop_subtract():
    # Test valid cases
    ast = typecheck(BinOp(NumLiteral(10), "-", NumLiteral(2)))
    assert ast == NumLiteral(0)

    ast = typecheck(BinOp(FloatLiteral(3.14), "-", NumLiteral(2)))
    assert ast == FloatLiteral(0.0)

    ast = typecheck(BinOp(NumLiteral(10), "-", FloatLiteral(2.5)))
    assert ast == FloatLiteral(0.0)

    # Test cases with Identifier type
    ast = typecheck(BinOp(Identifier("a"), "-", NumLiteral(2)))
    assert ast == NumLiteral(0)

    ast = typecheck(BinOp(NumLiteral(10), "-", Identifier("b")))
    assert ast == NumLiteral(0)

    ast = typecheck(BinOp(Identifier("c"), "-", Identifier("d")))
    assert ast == NumLiteral(0)

    # Test invalid cases
    with pytest.raises(Exception) as exception_1:
        ast = typecheck(BinOp(NumLiteral(10), "-", StringLiteral("hello")))
    assert str(exception_1.value) == 'TypeError: - not supported between instances of NumLiteral(10) and StringLiteral("hello")'

    with pytest.raises(Exception) as exception_2:
        ast = typecheck(BinOp(BoolLiteral(True), "-", NumLiteral(2)))
    assert str(exception_2.value) == 'TypeError: - not supported between instances of BoolLiteral(True) and NumLiteral(2)'

    with pytest.raises(Exception) as exception_3:
        ast = typecheck(BinOp(FloatLiteral(3.14), "-", BoolLiteral(False)))
    assert str(exception_3.value) == 'TypeError: - not supported between instances of FloatLiteral(3.14) and BoolLiteral(False)'

def test_typecheck_multiply():
    with pytest.raises(Exception) as exception_1:
        ast = typecheck(BinOp(Identifier("a"), "*", BoolLiteral(True)))
    assert str(exception_1.value) == 'TypeError: * not supported between instances of Identifier(a) and BoolLiteral(True)'

    ast = typecheck(BinOp(NumLiteral(2), "*", NumLiteral(3)))
    assert ast == NumLiteral(0)

    ast = typecheck(BinOp(FloatLiteral(1.5), "*", NumLiteral(2)))
    assert ast == FloatLiteral(0.0)

    ast = typecheck(BinOp(NumLiteral(3), "*", FloatLiteral(1.5)))
    assert ast == FloatLiteral(0.0)

    ast = typecheck(BinOp(StringLiteral("abc"), "*", NumLiteral(2)))
    assert ast == StringLiteral("")

    ast = typecheck(BinOp(NumLiteral(2), "*", Identifier("i")))
    assert ast == NumLiteral(0)

    ast = typecheck(BinOp(FloatLiteral(1.5), "*", Identifier("i")))
    assert ast == FloatLiteral(0.0)

    ast = typecheck(BinOp(Identifier("i"), "*", FloatLiteral(1.5)))
    assert ast == FloatLiteral(0.0)

    ast = typecheck(BinOp(Identifier("s"), "*", Identifier("i")))
    assert ast == NumLiteral(0)

def test_typecheck_binop_div():
    with pytest.raises(Exception) as exception_1:
        ast = typecheck(BinOp(NumLiteral(1), "/", BoolLiteral(True)))
    assert str(exception_1.value) == 'TypeError: / not supported between instances of NumLiteral(1) and BoolLiteral(True)'

    ast = typecheck(BinOp(FloatLiteral(3.0), "/", NumLiteral(2)))
    assert ast == FloatLiteral(0.0)

    ast = typecheck(BinOp(NumLiteral(3), "/", FloatLiteral(2.0)))
    assert ast == FloatLiteral(0.0)

    ast = typecheck(BinOp(NumLiteral(3), "//", NumLiteral(2)))
    assert ast == NumLiteral(1)

    ast = typecheck(BinOp(FloatLiteral(3.5), "%", NumLiteral(2)))
    assert ast == NumLiteral(1)

    ast = typecheck(BinOp(FloatLiteral(3.5), "//", FloatLiteral(2.0)))
    assert ast == NumLiteral(1)


def test_typecheck_binop_exponent():
    pass


def test_typecheck_indexer():
    with pytest.raises(Exception) as exception_1:
        ast = typecheck(Indexer(Identifier("s"), FloatLiteral(0.0)))
    assert str(exception_1.value) == 'TypeError: FloatLiteral(0.0) is not an integer'

    with pytest.raises(Exception) as exception_2:
        ast = typecheck(Indexer(Identifier("s"), BoolLiteral(True)))
    assert str(exception_2.value) == 'TypeError: BoolLiteral(True) is not an integer'

    ast = typecheck(Indexer(Identifier("s"), NumLiteral(1)))
    assert ast == Identifier("s")

    ast = typecheck(Indexer(Identifier("s"), Identifier("i")))
    assert ast == Identifier("s")
