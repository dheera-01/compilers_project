from declaration import Function,FunctionCall, Environment, NumLiteral, Print, Identifier,StringLiteral
from parser_1 import eval

def test_case11():
    env=Environment()
    hello_world = Function(name="hello_world", args= [Identifier("a")],body= Print(Identifier("a")), return_value=Identifier("a"))
    env.add_function(hello_world)

    func_call=FunctionCall("hello_world",[NumLiteral(2)])
    assert eval(func_call,env)==NumLiteral(2)

if __name__=="__main__":
    test_case11()