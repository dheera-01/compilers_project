import declaration
import eval_for_parser


def test_environment():
    main_enviroment = declaration.Enviroment()

    i = declaration.Identifier("i")
    e = declaration.Assign(i, declaration.NumLiteral(0))

    eval_for_parser.eval(e, main_enviroment)
    assert eval_for_parser.eval(i, main_enviroment)== 0


def test_seq_let():

    main_enviroment = declaration.Enviroment()

    e1=declaration.NumLiteral(1)
    i=declaration.Identifier("i")
    assign=declaration.Assign(i,e1)
    e2=declaration.BinOp(i, "+", declaration.NumLiteral(3))
    let_stmt=declaration.Let(assign,e2)
    assert eval_for_parser.eval(let_stmt, main_enviroment)== 4


def test_seq_let_2():
    main_enviroment = declaration.Enviroment()

    e1 = declaration.NumLiteral(1)
    i = declaration.Identifier("i")
    assign = declaration.Assign(i, e1)
    e2 = declaration.BinOp(i, "+", i)
    let_stmt = declaration.Let(assign, e2)
    assert eval_for_parser.eval(let_stmt, main_enviroment) == 2

def test_nested_let():
    main_enviroment = declaration.Enviroment()
    x=declaration.Identifier("x")
    y=declaration.Identifier("y")
    e1=declaration.NumLiteral(2)
    assign_x=declaration.Assign(x,e1)
    e2=declaration.NumLiteral(3)
    assign_y = declaration.Assign(y, e2)
    e3=declaration.BinOp(x,"+",y)
    inner_let=declaration.Let(assign_y,e3)
    outer_let=declaration.Let(assign_x,inner_let)
    assert eval_for_parser.eval(outer_let, main_enviroment)== 5

