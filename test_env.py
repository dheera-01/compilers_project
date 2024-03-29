import declaration
import eval_for_parser


def test_environment():
    main_environment = declaration.Environment()

    i = declaration.Identifier("i")
    e = declaration.Assign(i, declaration.NumLiteral(0))

    eval_for_parser.eval(e, main_environment)
    assert eval_for_parser.eval(i, main_environment)== 0


def test_seq_let():

    main_environment = declaration.Environment()

    e1=declaration.NumLiteral(1)
    i=declaration.Identifier("i")
    assign=declaration.Assign(i,e1)
    e2=declaration.BinOp(i, "+", declaration.NumLiteral(3))
    let_stmt=declaration.Let(assign,e2)
    assert eval_for_parser.eval(let_stmt, main_environment)== 4


def test_seq_let_2():
    main_environment = declaration.Environment()

    e1 = declaration.NumLiteral(1)
    i = declaration.Identifier("i")
    assign = declaration.Assign(i, e1)
    e2 = declaration.BinOp(i, "+", i)
    let_stmt = declaration.Let(assign, e2)
    assert eval_for_parser.eval(let_stmt, main_environment) == 2

def test_nested_let():
    main_environment = declaration.Environment()
    x=declaration.Identifier("x")
    y=declaration.Identifier("y")
    e1=declaration.NumLiteral(2)
    assign_x=declaration.Assign(x,e1)
    e2=declaration.NumLiteral(3)
    assign_y = declaration.Assign(y, e2)
    e3=declaration.BinOp(x,"+",y)
    inner_let=declaration.Let(assign_y,e3)
    outer_let=declaration.Let(assign_x,inner_let)
    assert eval_for_parser.eval(outer_let, main_environment)== 5

def test_let_lexical():
    # let
    # a = 1 in let
    # b = a in let
    # a = a + 1 in a + b

    main_environment = declaration.Environment()
    a=declaration.Identifier("a")
    b=declaration.Identifier("b")
    e1=declaration.NumLiteral(1)
    assign_a=declaration.Assign(a,e1)
    assign_b=declaration.Assign(b,a)
    a_b=declaration.BinOp(a,"+",b)
    inc_a=declaration.BinOp(a,"+",declaration.NumLiteral(1))
    assign_inc_a=declaration.Assign(a,inc_a)
    inner_let=declaration.Let(assign_inc_a,a_b)
    middle_let=declaration.Let(assign_b,inner_let)
    outer_let=declaration.Let(assign_a,middle_let)

    assert eval_for_parser.eval(outer_let, main_environment)== 3

