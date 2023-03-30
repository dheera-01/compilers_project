
from declaration import Function, Identifier, FunctionCall, NumLiteral, Return, Sequence, Environment,Print, StringLiteral, IfElse, ComparisonOp, BinOp
from eval_for_parser import eval

def test_func():
    env=Environment()

    body=Sequence([Return(NumLiteral(5))])
    func=Function(Identifier("test"),[],body)
    env.add(func.name,func)
    func_call=FunctionCall(Identifier("test"),[])
    assert eval(func_call,env)== NumLiteral(5)

def test_func_2():
    env=Environment()

    body=Sequence([Print(StringLiteral("Hello World"))])
    func=Function(Identifier("test"),[],body)
    env.add(func.name,func)
    func_call=FunctionCall(Identifier("test"),[])
    assert eval(func_call,env) is None

def test_func_3():
    env=Environment()

    body=Sequence([Return(NumLiteral(5)),Print(StringLiteral("Hello World"))])
    func=Function(Identifier("test"),[],body)
    env.add(func.name,func)
    func_call=FunctionCall(Identifier("test"),[])
    assert eval(func_call,env) == NumLiteral(5)

def test_func_4():
    env=Environment()
    if_branch=Sequence([Print(StringLiteral("Hello World"))])
    elif_list=[]
    else_branch=Sequence([Print(StringLiteral("Hello Mars"))])
    Variable=Identifier("i")
    c=ComparisonOp(Variable,">",NumLiteral(6))
    body=IfElse(c, if_branch, elif_list, else_branch)
    func=Function(Identifier("test"),[Identifier('i')],body)
    env.add(func.name,func)
    func_call=FunctionCall(Identifier("test"),[NumLiteral(7)])
    assert eval(func_call,env) is None

def test_func_5():
    env=Environment()

    c=ComparisonOp(Identifier('i'),'<',NumLiteral(2))

    if_branch=Sequence([Return(NumLiteral(1))])
    elif_list=[]

    f_call=FunctionCall(Identifier("test"),[BinOp(Identifier('i'),'-',NumLiteral(1))])
    fact = BinOp(Identifier('i'),'*',f_call)
    else_branch=Sequence([Return(fact)])
    body=IfElse(c, if_branch, elif_list, else_branch)
    func=Function(Identifier("test"),[Identifier('i')],body)
    env.add(func.name,func)
    func_call=FunctionCall(Identifier("test"),[NumLiteral(4)])
    eval(func_call,env)
    assert eval(func_call,env) == NumLiteral(24)

def test_func_6():
    # detect odd even number
    env=Environment()
    modulo=BinOp(Identifier('i'),'%',NumLiteral(2))
    c=ComparisonOp(modulo,'==',NumLiteral(0))
    if_branch=Sequence([Return(StringLiteral("Even"))])
    elif_list=[]
    else_branch=Sequence([Return(StringLiteral("Odd"))])
    body=IfElse(c, if_branch, elif_list, else_branch)
    func=Function(Identifier("test"),[Identifier('i')],body)
    env.add(func.name,func)
    func_call=FunctionCall(Identifier("test"),[NumLiteral(4)])
    assert eval(func_call,env) == StringLiteral("Even")

if __name__=="__main__":
    test_func()
    test_func_2()
    test_func_3()
    test_func_4()
    test_func_5()
    test_func_6()