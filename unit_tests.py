from my_parser import *
from my_lexer import *
from declaration import *
import sys
from my_VM import * 

def test_lexer_dot():
    text = """
    4
    4.5
    4.
     .5
    4.a
    4.5a
    4.a5
    4.LEN 
    4.TAIL 
    4.HEAD 
    4.APPEND 
    4.POP
    a.5
    a.a
    a.a5
    a.LEN
    a.TAIL
    a.HEAD
    a.APPEND
    a.POP
    """
    object_lexer = Lexer.from_stream(Stream.from_string(text))
    expected_tokens = ['NumLiteral(4)', 'FloatLiteral(4.5)', 'FloatLiteral(4.0)', 'FloatLiteral(0.5)', 'FloatLiteral(4.0)', 'Identifier(a, True)', 'FloatLiteral(4.5)', 'Identifier(a, True)', 'FloatLiteral(4.0)', 'Identifier(a5, True)', 'FloatLiteral(4.0)', 'Keyword(LEN)', 'FloatLiteral(4.0)', 'Keyword(TAIL)', 'FloatLiteral(4.0)', 'Keyword(HEAD)', 'FloatLiteral(4.0)', 'Keyword(APPEND)', 'FloatLiteral(4.0)', 'Keyword(POP)', 'Identifier(a, True)', 'FloatLiteral(0.5)', 'Identifier(a, True)', 'Operator(.)', 'Identifier(a, True)', 'Identifier(a, True)', 'Operator(.)', 'Identifier(a5, True)', 'Identifier(a, True)', 'Operator(.)', 'Keyword(LEN)', 'Identifier(a, True)', 'Operator(.)', 'Keyword(TAIL)', 'Identifier(a, True)', 'Operator(.)', 'Keyword(HEAD)', 'Identifier(a, True)', 'Operator(.)', 'Keyword(APPEND)', 'Identifier(a, True)', 'Operator(.)', 'Keyword(POP)']
    for token in object_lexer:
        assert str(token) == expected_tokens.pop(0)


# operator test
def test_lexer_operators():
    text = """
    #unary operator
    ++--6 
    + - / * % //   ** 
    < > <= >= == != 
    << >> = ++ -- += -= *= /= %= //= **=
    and or
    """
    object_lexer = Lexer.from_stream(Stream.from_string(text))
    expected_tokens = ['Operator(+)', 'Operator(+)', 'Operator(-)', 'Operator(-)', 'NumLiteral(6)', 'Operator(+)', 'Operator(-)', 'Operator(/)', 'Operator(*)', 'Operator(%)', 'Operator(//)', 'Operator(**)', 'Operator(<)', 'Operator(>)', 'Operator(<=)', 'Operator(>=)', 'Operator(==)', 'Operator(!=)', 'Operator(<<)', 'Operator(>>)', 'Operator(=)', 'Operator(+)', 'Operator(+)', 'Operator(-)', 'Operator(-)', 'Operator(+=)', 'Operator(-=)', 'Operator(*=)', 'Operator(/=)', 'Operator(%=)', 'Operator(//=)', 'Operator(**=)', 'Operator(and)', 'Operator(or)']

    for token in object_lexer:
        assert str(token) == expected_tokens.pop(0)

# data type test
def test_lexer_datatype():
    text = """
    12 5 9630 
    12.5 0.5 .5
    "HelloWorld" 'HelloWorld'
    True False
    true false
    abc
    """
    object_lexer = Lexer.from_stream(Stream.from_string(text))
    expected_tokens = ['NumLiteral(12)', 'NumLiteral(5)', 'NumLiteral(9630)', 'FloatLiteral(12.5)', 'FloatLiteral(0.5)', 'FloatLiteral(0.5)', 'StringLiteral("HelloWorld")', 'StringLiteral("HelloWorld")', 'BoolLiteral(True)', 'BoolLiteral(False)', 'Identifier(true, True)', 'Identifier(false, True)', 'Identifier(abc, True)']

    for token in object_lexer:
        assert str(token) == expected_tokens.pop(0)

# keyword and identifier test
def test_lexer_keywordAndIdentifier():
    text = """
    assign const None
    if elif then else while for print 
    a1 =                       False   True 
    """
    object_lexer = Lexer.from_stream(Stream.from_string(text))
    expected_token = ['Keyword(assign)', 'Keyword(const)', 'Identifier(None, True)', 'Keyword(if)', 'Keyword(elif)', 'Identifier(then, True)', 'Keyword(else)', 'Keyword(while)', 'Keyword(for)', 'Keyword(print)', 'Identifier(a1, True)', 'Operator(=)', 'BoolLiteral(False)', 'BoolLiteral(True)']

    for token in object_lexer:
        assert str(token) == expected_token.pop(0)

# comment, whitespace, end of line test
def test_lexer_comment_whitespace_eof():
    text = """
    # this is comment
    # this is comment
    a5 =       8       
    ;
    """
    object_lexer = Lexer.from_stream(Stream.from_string(text))
    expected_token = ['Identifier(a5, True)', 'Operator(=)', 'NumLiteral(8)', 'EndOfLine(;)']
    for token in object_lexer:
        assert str(token) == expected_token.pop(0)

# brackets test
def test_lexer_brackets():
    text = """
    ( ) [  {  } ] 
    """

    object_lexer = Lexer.from_stream(Stream.from_string(text))
    expected_token = ['Bracket(()', 'Bracket())', 'Bracket([)', 'Bracket({)', 'Bracket(})', 'Bracket(])']
    for token in object_lexer:
        assert str(token) == expected_token.pop(0)

# slicing test
def test_lexer_slice():
    print(f"\nTestcase 6")
    text = """
    slice("Hello":0:2:1)
    """

    object_lexer = Lexer.from_stream(Stream.from_string(text))
    expected_token = ['Keyword(slice)', 'Bracket(()', 'StringLiteral("Hello")', 'Operator(:)', 'NumLiteral(0)', 'Operator(:)', 'NumLiteral(2)', 'Operator(:)', 'NumLiteral(1)', 'Bracket())']
    for token in object_lexer:
        assert str(token) == expected_token.pop(0)

def test_lexer_func_def():
    print(f'\nTestcase 7')
    text = """
    func add(a, b){
        return a + b;
    }
    """
    object_lexer = Lexer.from_stream(Stream.from_string(text))
    expected_toekn=['Keyword(func)', 'Identifier(add, True)', 'Bracket(()', 'Identifier(a, True)', 'Operator(,)', 'Identifier(b, True)', 'Bracket())', 'Bracket({)', 'Keyword(return)', 'Identifier(a, True)', 'Operator(+)', 'Identifier(b, True)', 'EndOfLine(;)', 'Bracket(})']
    for token in object_lexer:
        assert str(token) == expected_toekn.pop(0)
#--------------------------------------------
# Parser Testcases

# Dummy lexer class and its methods
class DummyLexer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0

    def __iter__(self):
        return self

    def peek_current_token(self):
        if self.index < len(self.tokens):
            return self.tokens[self.index]
        else:
            return None

    def advance(self):
        self.index += 1

    def match(self, token):
        if self.peek_current_token() == token:
            return self.advance()
        else:
            return None

# arithmetic, unary operation, precedence and associativity
def test_parser_arithmetic_unary_precedence_associativity():
    # text = """
    # # unary operator
    # ++--6
    # i = -2**6**8; # exponent have high precedence
    # # simple expression
    # 8 / 6
    # # precedence
    # 8 + 9 * 10
    # 2 * (3+5)
    # # right associativity
    # 2 * 3 * 4
    # # right associativity
    # 2 ** 3 ** 3
    # """

    token_list = [Operator("+"), Operator("+"), Operator("-"), Operator("-"), NumLiteral(6), Identifier("i"), Operator("="), Operator("-"), NumLiteral(2), Operator("**"), NumLiteral(6), Operator("**"), NumLiteral(8), EndOfLine(";"), NumLiteral(8), Operator("/"), NumLiteral(6), NumLiteral(8), Operator("+"), NumLiteral(9), Operator("*"), NumLiteral(10), NumLiteral(2), Operator("*"), Bracket("("), NumLiteral(3), Operator("+"), NumLiteral(5), Bracket(")"), NumLiteral(2), Operator("*"), NumLiteral(3), Operator("*"), NumLiteral(4), NumLiteral(2), Operator("**"), NumLiteral(3), Operator("**"), NumLiteral(3), EndOfFile("EOF")]
    object_lexer = DummyLexer(token_list)
    obj_parser = Parser.from_lexer(object_lexer)

    expected_parsed = [UnaryOp("+", UnaryOp("+", UnaryOp("-", UnaryOp("-", NumLiteral(6))))), Update(Identifier("i"), Operator("="), UnaryOp("-", BinOp(NumLiteral(2), "**", BinOp(NumLiteral(6), "**", NumLiteral(8))))), BinOp(NumLiteral(8), "/", NumLiteral(6)), BinOp(NumLiteral(8), "+", BinOp(NumLiteral(9), "*", NumLiteral(10))), BinOp(NumLiteral(2), "*", BinOp(NumLiteral(3), "+", NumLiteral(5))), BinOp(BinOp(NumLiteral(2), "*", NumLiteral(3)), "*", NumLiteral(4)), BinOp(NumLiteral(2), "**", BinOp(NumLiteral(3), "**", NumLiteral(3)))]

    for i in obj_parser.parse_program().statements:
        assert i == expected_parsed.pop(0)


# test case assign and update
def test_parser_assign_udate():
    # text = """
    # assign i = i+5;
    # const assign j = i+5;
    # j = j + 1 * i;
    # """

    token_list = [Keyword("assign"), Identifier("i"), Operator("="), Identifier("i"), Operator("+"), NumLiteral(5),
                  EndOfLine(";"), Keyword("const"), Keyword("assign"), Identifier("j"), Operator("="), Identifier("i"),
                  Operator("+"), NumLiteral(5), EndOfLine(";"), Identifier("j"), Operator("="), Identifier("j"),
                  Operator("+"), NumLiteral(1), Operator("*"), Identifier("i"), EndOfLine(";"), EndOfFile("EOF")]

    object_lexer = DummyLexer(token_list)
    obj_parser = Parser.from_lexer(object_lexer)

    expected_paresed = ["""Assign((Identifier(i, True),) = (BinOp(Identifier(i, True) + NumLiteral(5)),))""",
                        """Assign((Identifier(j, False),) = (BinOp(Identifier(i, True) + NumLiteral(5)),))""",
                        """Update(Identifier(j, True) Operator(=) BinOp(Identifier(j, True) + BinOp(NumLiteral(1) * Identifier(i, True))))"""]

    for i in obj_parser.parse_program().statements:
        assert str(i) == expected_paresed.pop(0)

# if else test
def test_parser_if_else():
    # text = """
    # # if else both
    # if("hello world" > "chirag" and "hi" == "hi")
    # {
    #     i = i + k +l;
    #     i = 10;
    # }
    # else
    # {
    #     "hello";
    # }
    #
    #
    # # only if
    # if(i>5 or j != 5)
    # {
    #     i = i +5;
    #     8+5;
    # }
    #
    # """

    token_list = [Keyword("if"), Bracket("("), StringLiteral("hello world"), Operator(">"), StringLiteral("chirag"), Operator("and"), StringLiteral("hi"), Operator("=="), StringLiteral("hi"), Bracket(")"), Bracket("{"), Identifier("i"), Operator("="), Identifier("i"), Operator("+"), Identifier("k"), Operator("+"), Identifier("l"), EndOfLine(";"), Identifier("i"), Operator("="), NumLiteral(10), EndOfLine(";"), Bracket("}"), Keyword("else"), Bracket("{"), StringLiteral("hello"), EndOfLine(";"), Bracket("}"), Keyword("if"), Bracket("("), Identifier("i"), Operator(">"), NumLiteral(5), Operator("or"), Identifier("j"), Operator("!="), NumLiteral(5), Bracket(")"), Bracket("{"), Identifier("i"), Operator("="), Identifier("i"), Operator("+"), NumLiteral(5), EndOfLine(";"), NumLiteral(8), Operator("+"), NumLiteral(5), EndOfLine(";"), Bracket("}"), EndOfFile("EOF")]

    object_lexer = DummyLexer(token_list)
    obj_parser = Parser.from_lexer(object_lexer)

    ast_1 = IfElse(ComparisonOp(ComparisonOp(StringLiteral("hello world"), ">", StringLiteral("chirag")), "and" ,ComparisonOp(StringLiteral("hi"), "==", StringLiteral("hi"))), Sequence([Update(Identifier("i"), Operator("="), BinOp(BinOp(Identifier("i"), "+", Identifier("k")), "+", Identifier("l"))), Update(Identifier("i"), Operator("="), NumLiteral(10))]),[], Sequence([StringLiteral("hello"), EndOfLine(";")]))

    ast_2 = IfElse(ComparisonOp(ComparisonOp(Identifier("i"), ">", NumLiteral(5)), "or" ,ComparisonOp(Identifier("j"), "!=", NumLiteral(5))), Sequence([Update(Identifier("i"), Operator("="), BinOp(Identifier("i"), "+", NumLiteral(5))), BinOp(NumLiteral(8), "+", NumLiteral(5)), EndOfLine(";")]),[], None)

    expected_paresed = [ast_1, ast_2]

    for i in obj_parser.parse_program().statements:
        assert i == expected_paresed.pop(0)

# elif test case
def test_parser_elif():
    # text = """
    # if(i>5)
    # {
    #     print("hello");
    # }
    # elif(i == 0)
    # {
    #     print("world");
    # }
    # """
    token_list = [Keyword("if"), Bracket("("), Identifier("i"), Operator(">"), NumLiteral(5), Bracket(")"), Bracket("{"), Keyword("print"), Bracket("("), StringLiteral("hello"), Bracket(")"), EndOfLine(";"), Bracket("}"), Keyword("elif"), Bracket("("), Identifier("i"), Operator("=="), NumLiteral(0), Bracket(")"), Bracket("{"), Keyword("print"), Bracket("("), StringLiteral("world"), Bracket(")"), EndOfLine(";"), Bracket("}"), EndOfFile("EOF")]

    object_lexer = DummyLexer(token_list)
    obj_parser = Parser.from_lexer(object_lexer)

    ast_1 = IfElse(ComparisonOp(Identifier("i"), ">", NumLiteral(5)), Sequence([Print(StringLiteral("hello"))]), [IfElse(ComparisonOp(Identifier("i"), "==", NumLiteral(0)), Sequence([Print(StringLiteral("world"))]),[], None)], None)

    expected_paresed = [ast_1]

    for i in obj_parser.parse_program().statements:
        assert i == expected_paresed.pop(0)

# for test
def test_parser_for():
    # text = """
    # for(i = i + 1 ; i< n; i+=1;)
    # {
    #     print(i>1);
    # }
    # """

    token_list = [Keyword("for"), Bracket("("), Identifier("i"), Operator("="), Identifier("i"), Operator("+"), NumLiteral(1), EndOfLine(";"), Identifier("i"), Operator("<"), Identifier("n"), EndOfLine(";"), Identifier("i"), Operator("+="), NumLiteral(1), EndOfLine(";"), Bracket(")"), Bracket("{"), Keyword("print"), Bracket("("), Identifier("i"), Operator(">"), NumLiteral(1), Bracket(")"), EndOfLine(";"), Bracket("}"), EndOfFile("EOF")]

    object_lexer = DummyLexer(token_list)
    obj_parser = Parser.from_lexer(object_lexer)

    ast_1 = For(Update(Identifier("i"), Operator("="), BinOp(Identifier("i"), "+", NumLiteral(1))), ComparisonOp(Identifier("i"), "<", Identifier("n")), Update(Identifier("i"), Operator("+="), NumLiteral(1)), Sequence([Print(ComparisonOp(Identifier("i"), ">", NumLiteral(1)))]))

    expected_paresed = [ast_1]

    for i in obj_parser.parse_program().statements:
        assert i == expected_paresed.pop(0)

# while test
def test_parser_while():
    # text = """
    # while(j<5)
    # {
    #     print(j);
    #     while(k<2)
    #     {
    #         print(k);
    #         k = k + 1;
    #     }
    #     j = j +1;
    # }
    # """

    token_list = [Keyword("while"), Bracket("("), Identifier("j"), Operator("<"), NumLiteral(5), Bracket(")"), Bracket("{"), Keyword("print"), Bracket("("), Identifier("j"), Bracket(")"), EndOfLine(";"), Keyword("while"), Bracket("("), Identifier("k"), Operator("<"), NumLiteral(2), Bracket(")"), Bracket("{"), Keyword("print"), Bracket("("), Identifier("k"), Bracket(")"), EndOfLine(";"), Identifier("k"), Operator("="), Identifier("k"), Operator("+"), NumLiteral(1), EndOfLine(";"), Bracket("}"), Identifier("j"), Operator("="), Identifier("j"), Operator("+"), NumLiteral(1), EndOfLine(";"), Bracket("}"), EndOfFile("EOF")]

    object_lexer = DummyLexer(token_list)
    obj_parser = Parser.from_lexer(object_lexer)

    ast_1 = While(ComparisonOp(Identifier("j"), "<", NumLiteral(5)), Sequence([Print(Identifier("j")), While(ComparisonOp(Identifier("k"), "<", NumLiteral(2)), Sequence([Print(Identifier("k")), Update(Identifier("k"), Operator("="), BinOp(Identifier("k"), "+", NumLiteral(1)))])), Update(Identifier("j"), Operator("="), BinOp(Identifier("j"), "+", NumLiteral(1)))]))

    expected_paresed = [ast_1]

    for i in obj_parser.parse_program().statements:
        assert i == expected_paresed.pop(0)

# string test
def test_parser_slice():
    # text = """
    #     print(slice("Hello World!": 0: 5: 1));
    # """

    token_list = [Keyword("print"), Bracket("("), Keyword("slice"), Bracket("("), StringLiteral("Hello World!"), Operator(":"), NumLiteral(0), Operator(":"), NumLiteral(5), Operator(":"), NumLiteral(1), Bracket(")"), Bracket(")"), EndOfLine(";"), EndOfFile("EOF")]

    object_lexer = DummyLexer(token_list)
    obj_parser = Parser.from_lexer(object_lexer)

    ast_1 = Print(Slice(StringLiteral("Hello World!"), NumLiteral(0), NumLiteral(5), NumLiteral(1)))

    expected_paresed = [ast_1]

    for i in obj_parser.parse_program().statements:
        print(i)
        assert i == expected_paresed.pop(0)

# let test
def test_parser_let():
    # text = """
    # let x=1+2*3 (x+1)
    # let y=2 (let x=2 (x+y));
    # print(x);
    # print("hello");
    # let x=2 (let y=3 (let z=4 (x+y+z)));
    # assign v=let u=2
    # (
    #     let t=2
    #         (let a=2(u+ a*t))
    # );
    # print(v);
    # """

    token_list = [Keyword("let"), Identifier("x"), Operator("="), NumLiteral(1), Operator("+"), NumLiteral(2), Operator("*"), NumLiteral(3), Bracket("("), Identifier("x"), Operator("+"), NumLiteral(1), Bracket(")"), Keyword("let"), Identifier("y"), Operator("="), NumLiteral(2), Bracket("("), Keyword("let"), Identifier("x"), Operator("="), NumLiteral(2), Bracket("("), Identifier("x"), Operator("+"), Identifier("y"), Bracket(")"), Bracket(")"), EndOfLine(";"), Keyword("print"), Bracket("("), Identifier("x"), Bracket(")"), EndOfLine(";"), Keyword("print"), Bracket("("), StringLiteral("hello"), Bracket(")"), EndOfLine(";"), Keyword("let"), Identifier("x"), Operator("="), NumLiteral(2), Bracket("("), Keyword("let"), Identifier("y"), Operator("="), NumLiteral(3), Bracket("("), Keyword("let"), Identifier("z"), Operator("="), NumLiteral(4), Bracket("("), Identifier("x"), Operator("+"), Identifier("y"), Operator("+"), Identifier("z"), Bracket(")"), Bracket(")"), Bracket(")"), EndOfLine(";"), Keyword("assign"), Identifier("v"), Operator("="), Keyword("let"), Identifier("u"), Operator("="), NumLiteral(2), Bracket("("), Keyword("let"), Identifier("t"), Operator("="), NumLiteral(2), Bracket("("), Keyword("let"), Identifier("a"), Operator("="), NumLiteral(2), Bracket("("), Identifier("u"), Operator("+"), Identifier("a"), Operator("*"), Identifier("t"), Bracket(")"), Bracket(")"), Bracket(")"), EndOfLine(";"), Keyword("print"), Bracket("("), Identifier("v"), Bracket(")"), EndOfLine(";"), EndOfFile("EOF")]

    object_lexer = DummyLexer(token_list)
    obj_parser = Parser.from_lexer(object_lexer)

    expected_paresed = ["""Let Identifier(x) = BinOp(NumLiteral(1) + BinOp(NumLiteral(2) * NumLiteral(3))) in BinOp(Identifier(x) + NumLiteral(1)))""", """Let Identifier(y) = NumLiteral(2) in Let Identifier(x) = NumLiteral(2) in BinOp(Identifier(x) + Identifier(y))))""", """EndOfLine(;)""", """Print(Identifier(x))""", """Print(StringLiteral("hello"))""", """Let Identifier(x) = NumLiteral(2) in Let Identifier(y) = NumLiteral(3) in Let Identifier(z) = NumLiteral(4) in BinOp(BinOp(Identifier(x) + Identifier(y)) + Identifier(z)))))""", """EndOfLine(;)""", """Assign((Identifier(v),) = (Let Identifier(u) = NumLiteral(2) in Let Identifier(t) = NumLiteral(2) in Let Identifier(a) = NumLiteral(2) in BinOp(Identifier(u) + BinOp(Identifier(a) * Identifier(t)))))),))""", """Print(Identifier(v))"""]

    for i in obj_parser.parse_program().statements:
        assert str(i) == expected_paresed.pop(0)


# def test_parse_func_def():
#     token_list = [Keyword("func"), Identifier("add", True), Bracket('('), Identifier("a", True), Operator(','),
#                       Identifier('b', True), Bracket(')'), Bracket('{'), Keyword('return'), Identifier('a', True),
#                       Operator('+'), Identifier('b', True), EndOfLine(';'), Bracket('}')]
#     object_lexer=DummyLexer(token_list)
#
#
#     obj_parser = Parser.from_lexer(object_lexer)
#     print(obj_parser.parse_program().statements)
#
#     expected_parsed=["""Function(Identifier(add), [Identifier(a), Identifier(b)], Return(BinOp(Identifier(a) + Identifier(b))))"""]
#     for i in obj_parser.parse_program().statements:
#         assert str(i) == expected_parsed.pop(0)



#--------------------------------------------
# Eval testcases

def test_eval_let():
    parsed_program = Let(Identifier("x"), NumLiteral(1), BinOp(Identifier("x"), "+", NumLiteral(1)))
    assert eval(parsed_program) == NumLiteral(2)

def test_eval_assing(capsys):
    parsed_program = Assign((Identifier("x"),Identifier("y"),), (NumLiteral(1),NumLiteral(2),))
    parsed_program = Sequence([parsed_program, Print(Identifier("x")), Print(Identifier("y"))])
    eval(parsed_program)
    assert capsys.readouterr().out == "1\n2\n"

# def test_eval_update(capsys):
#     parsed_program = Sequence([Assign((Identifier("x"),), (NumLiteral(1),)), Update(Identifier("x"), Operator("="), BinOp(Identifier("x"), "+", NumLiteral(1))), Print(Identifier("x"))])
#     eval(parsed_program)
#     assert capsys.readouterr().out == "2\n"
#
#     parsed_program = Sequence([Assign((Identifier("x"),), (NumLiteral(1),)), Update(Identifier("x"), Operator("+="), BinOp(Identifier("x"), "+", NumLiteral(1))), Print(Identifier("x"))])
#     eval(parsed_program)
#     assert capsys.readouterr().out == "3\n"
#
#     parsed_program = Sequence([Assign((Identifier("x"),), (NumLiteral(1),)), Update(Identifier("x"), Operator("-="), BinOp(Identifier("x"), "+", NumLiteral(1))), Print(Identifier("x"))])
#     eval(parsed_program)
#     assert capsys.readouterr().out == "-1\n"
#
#     parsed_program = Sequence([Assign((Identifier("x"),), (NumLiteral(1),)), Update(Identifier("x"), Operator("*="), BinOp(Identifier("x"), "+", NumLiteral(1))), Print(Identifier("x"))])
#     eval(parsed_program)
#     assert capsys.readouterr().out == "2\n"
#
#     parsed_program = Sequence([Assign((Identifier("x"),), (NumLiteral(1),)), Update(Identifier("x"), Operator("/="), BinOp(Identifier("x"), "+", NumLiteral(1))), Print(Identifier("x"))])
#     eval(parsed_program)
#     assert capsys.readouterr().out == "0.5\n"
#
#     parsed_program = Sequence([Assign((Identifier("x"),), (NumLiteral(1),)), Update(Identifier("x"), Operator("%="), BinOp(Identifier("x"), "+", NumLiteral(1))), Print(Identifier("x"))])
#     eval(parsed_program)
#     assert capsys.readouterr().out == "0\n"
#
#     parsed_program = Sequence([Assign((Identifier("x"),), (NumLiteral(1),)), Update(Identifier("x"), Operator("**="), BinOp(Identifier("x"), "+", NumLiteral(1))), Print(Identifier("x"))])
#     eval(parsed_program)
#     assert capsys.readouterr().out == "1\n"

def test_eval_print(capsys):
    parsed_program = Sequence([Print(NumLiteral(1)), Print(StringLiteral("hello"))])
    eval(parsed_program)
    assert capsys.readouterr().out == "1\nhello\n"

    parsed_program = Sequence([Print(NumLiteral(1)), Print(StringLiteral("hello")), Print(NumLiteral(2))])
    eval(parsed_program)
    assert capsys.readouterr().out == "1\nhello\n2\n"

def test_eval_while(capsys):
    parsed_program = Sequence([Assign((Identifier("x"),), (NumLiteral(1),)), While(ComparisonOp(Identifier("x"), "<", NumLiteral(10)), Sequence([Print(Identifier("x")), Update(Identifier("x"), Operator("+="), NumLiteral(1))]))])
    eval(parsed_program)
    assert capsys.readouterr().out == "1\n2\n3\n4\n5\n6\n7\n8\n9\n"

def test_eval_for(capsys):
    parser_program = Sequence([Assign((Identifier("x"),), (NumLiteral(1),)), For(Assign((Identifier("x"),),(NumLiteral(1),)), ComparisonOp(Identifier("x"),"<",NumLiteral(10)), Update(Identifier("x"), Operator("+="), NumLiteral(1)),Sequence([Print(Identifier("x"))]))])
    eval(parser_program)
    assert capsys.readouterr().out == "1\n2\n3\n4\n5\n6\n7\n8\n9\n"

def test_eval_slice(capsys):
    parsed_program = Sequence([Print(Slice(StringLiteral("Hello"),NumLiteral(1), NumLiteral(3), NumLiteral(1)))])
    eval(parsed_program)
    assert capsys.readouterr().out == "el\n"

def test_eval_ifelse(capsys):
    parsed_program = Sequence([IfElse(ComparisonOp(NumLiteral(1), "==", NumLiteral(1)), Print(NumLiteral(1)), [], [Print(NumLiteral(2))])])
    eval(parsed_program)
    assert capsys.readouterr().out == "1\n"

    parsed_program = Sequence([IfElse(ComparisonOp(NumLiteral(1), "==", NumLiteral(2)), Print(NumLiteral(1)), [], Sequence([Print(NumLiteral(2))]))])
    eval(parsed_program)
    assert capsys.readouterr().out == "2\n"

def test_eval_comparisonOp():
    assert eval(ComparisonOp(NumLiteral(1), "==", NumLiteral(1))) == BoolLiteral(True)
    assert eval(ComparisonOp(NumLiteral(1), "!=", NumLiteral(1))) == BoolLiteral(False)
    assert eval(ComparisonOp(NumLiteral(1), "<", NumLiteral(1))) == BoolLiteral(False)
    assert eval(ComparisonOp(NumLiteral(1), ">", NumLiteral(1))) == BoolLiteral(False)
    assert eval(ComparisonOp(NumLiteral(1), "<=", NumLiteral(1))) == BoolLiteral(True)
    assert eval(ComparisonOp(NumLiteral(1), ">=", NumLiteral(1))) == BoolLiteral(True)

def test_eval_binOp():
    assert eval(BinOp(NumLiteral(1), "+", NumLiteral(1))) == NumLiteral(2)
    assert eval(BinOp(NumLiteral(1), "-", NumLiteral(1))) == NumLiteral(0)
    assert eval(BinOp(NumLiteral(1), "*", NumLiteral(1))) == NumLiteral(1)
    assert eval(BinOp(NumLiteral(1), "/", NumLiteral(1))) == FloatLiteral(1.0)
    assert eval(BinOp(NumLiteral(1), "%", NumLiteral(1))) == NumLiteral(0)
    assert eval(BinOp(NumLiteral(1), "**", NumLiteral(1))) == NumLiteral(1)

def test_eval_unaryOp():
    assert eval(UnaryOp("-", NumLiteral(1))) == NumLiteral(-1)


def test_eval_func_def():
    env = Environment()
    body = Sequence([Return(NumLiteral(5)), Print(StringLiteral("Hello World"))])
    func = Function(Identifier("test"), [], body)
    env.add(func.name, func)
    func_call = FunctionCall(Identifier("test"), [])
    assert eval(func_call, env) == NumLiteral(5)

# def test_eval_indexer(capsys):
#     parsed_program = Sequence([Assign((Identifier("x"),), (NumLiteral(1),)), Assign((Identifier("y"),), (NumLiteral(2),)), Assign((Identifier("z"),), (NumLiteral(3),)), Assign((Identifier("a"),), (ListLiteral((Identifier("x"), Identifier("y"), Identifier("z"))),)), Print(Indexer(Identifier("a"), NumLiteral(0)))])
#     eval(parsed_program)
#     assert capsys.readouterr().out == "1\n"



def test_vm():
     program = Sequence(
         [
             Assign((Identifier("i"), Identifier("j")), (NumLiteral(0), NumLiteral(0))),
             While(ComparisonOp(Identifier("i"), '<',  NumLiteral(10)), 
                   Sequence([Print(Identifier("i")), 
                             While(ComparisonOp(Identifier("j"), '<=',  NumLiteral(3)), Sequence([Print(StringLiteral("Hi")), Update(Identifier("j"), Operator("="), BinOp(Identifier("j"), "+", NumLiteral(1)))])),
                             Update(Identifier("i"), Operator("="), BinOp(Identifier("i"), "+", NumLiteral(1)))]
                            ))
         ]
     )


     code = codegen(program)
     vm = VM()
     vm.load(code)
     vm.execute()