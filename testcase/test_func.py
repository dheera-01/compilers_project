from declaration import Function,FunctionCall, Environment, NumLiteral, Print, Identifier,StringLiteral,Sequence, BinOp
from parser_1 import eval

def test_case_func_1():
    env=Environment()
    hello_world = Function(name="hello_world", args= [Identifier("a")],body= Print(Identifier("a")), return_value=None)
    env.add_function(hello_world)

    func_call=FunctionCall("hello_world",[NumLiteral(2)])
    assert eval(func_call,env) is None
def test_case_func_2():
    env=Environment()
    echo=Function(name="echo",args=[Identifier("a")],body=Sequence([]),return_value=Identifier("a"))
    env.add_function(echo)
    echo_call=FunctionCall("echo",[StringLiteral("echo this")])
    assert eval(echo_call,env) == StringLiteral("echo this")

def test_case_func_3():
    env=Environment()
    addition=Function(name="addition",args=[Identifier("a"),Identifier("b")],body=Sequence([]),return_value=BinOp(Identifier("a"),"+",Identifier("b")))
    env.add_function(addition)
    addition_call=FunctionCall("addition",[NumLiteral(4),NumLiteral(5)])
    assert eval(addition_call,env) ==NumLiteral(9)
if __name__ == "__main__":

    test_case_func_1()
    test_case_func_2()
    test_case_func_3()