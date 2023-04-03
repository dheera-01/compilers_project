from my_parser import *
from my_lexer import *
from declaration import *

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
    expected_tokens = ['NumLiteral(12)', 'NumLiteral(5)', 'NumLiteral(9630)', 'FloatLiteral(12.5)', 'FloatLiteral(0.5)', 'FloatLiteral(0.5)', 'StringLiteral("HelloWorld")', 'StringLiteral("HelloWorld")', 'BoolLiteral(True)', 'BoolLiteral(False)', 'Identifier(true)', 'Identifier(false)', 'Identifier(abc)']

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
    expected_token = ['Keyword(assign)', 'Keyword(const)', 'Identifier(None)', 'Keyword(if)', 'Keyword(elif)', 'Identifier(then)', 'Keyword(else)', 'Keyword(while)', 'Keyword(for)', 'Keyword(print)', 'Identifier(a1)', 'Operator(=)', 'BoolLiteral(False)', 'BoolLiteral(True)']

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
    expected_token = ['Identifier(a5)', 'Operator(=)', 'NumLiteral(8)', 'EndOfLine(;)']
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

# def test_dummy_lexer():
#     tokens = [NumLiteral(1), EndOfFile("EOF")]
#     object_lexer = DummyLexer(tokens)
#     obj_parser = Parser.from_lexer(object_lexer)
#     assert obj_parser.parse_program() == Sequence([NumLiteral(1)])
#     print(obj_parser)

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
        assert str(i) == str(expected_parsed.pop(0))


# test case assign and update
def test_parser_assign_udate():
    # text = """
    # assign i = i+5;
    # const assign j = i+5;
    # j = j + 1 * i;
    # """

    token_list = [Keyword("assign"), Identifier("i"), Operator("="), Identifier("i"), Operator("+"), NumLiteral(5), EndOfLine(";"), Keyword("const"), Keyword("assign"), Identifier("j"), Operator("="), Identifier("i"), Operator("+"), NumLiteral(5), EndOfLine(";"), Identifier("j"), Operator("="), Identifier("j"), Operator("+"), NumLiteral(1), Operator("*"), Identifier("i"), EndOfLine(";"), EndOfFile("EOF")]

    object_lexer = DummyLexer(token_list)
    obj_parser = Parser.from_lexer(object_lexer)

    expected_paresed = ["""Assign((Identifier(i),) = (BinOp(Identifier(i) + NumLiteral(5)),))""", """Assign((Identifier(j),) = (BinOp(Identifier(i) + NumLiteral(5)),))""", """Update(Identifier(j) Operator(=) BinOp(Identifier(j) + BinOp(NumLiteral(1) * Identifier(i))))"""]

    for i in obj_parser.parse_program().statements:
        assert str(i) == expected_paresed.pop(0)

# if else test
def test_parser_if_else():
    text = """
    # if else both
    if("hello world" > "chirag" and "hi" == "hi")
    {
        i = i + k +l;
        i = 10;
    }
    else 
    {
        "hello";
    }


    # only if
    if(i>5 or j != 5)
    {
        i = i +5;
        8+5;
    }

    """

    token_list = [Keyword("if"), Bracket("("), StringLiteral("hello world"), Operator(">"), StringLiteral("chirag"), Operator("and"), StringLiteral("hi"), Operator("=="), StringLiteral("hi"), Bracket(")"), Bracket("{"), Identifier("i"), Operator("="), Identifier("i"), Operator("+"), Identifier("k"), Operator("+"), Identifier("l"), EndOfLine(";"), Identifier("i"), Operator("="), NumLiteral(10), EndOfLine(";"), Bracket("}"), Keyword("else"), Bracket("{"), StringLiteral("hello"), EndOfLine(";"), Bracket("}"), Keyword("if"), Bracket("("), Identifier("i"), Operator(">"), NumLiteral(5), Operator("or"), Identifier("j"), Operator("!="), NumLiteral(5), Bracket(")"), Bracket("{"), Identifier("i"), Operator("="), Identifier("i"), Operator("+"), NumLiteral(5), EndOfLine(";"), NumLiteral(8), Operator("+"), NumLiteral(5), EndOfLine(";"), Bracket("}"), EndOfFile("EOF")]

    object_lexer = DummyLexer(token_list)
    obj_parser = Parser.from_lexer(object_lexer)

    

    for i in obj_parser.parse_program().statements:
        assert str(i) == expected_output.pop(0)

# elif test case
def test_case3_1():
    print("\nTest case 3.1")
    text = """
    assign i = 4;
    if(i>5)
    {
        print("i<2 and i < 5");
    } 
    elif(i == 0)
    {
        print(heello);
    }
    elif(k != 5)
    {
        assign k = k +5;
    }
    else
    {
        print("not");
    }
    """
    obj_parser = Parser.from_lexer(Lexer.from_stream(Stream.from_string(text)))
    for i in obj_parser.parse_program().statements:
        print(i)


# for test
def test_case4():
    print("\nTest case 4")
    text = """
    assign  i = 7
    ;
    assign n = 10;
    for(i = i + 1 ; i< n; i+=1;)
    {
        print(i>1);    
    }
    """
    obj_parser = Parser.from_lexer(Lexer.from_stream(Stream.from_string(text)))
    for i in obj_parser.parse_program().statements:
        print(i)


# while test
def test_case5():
    print(f"\nTest Case 5")
    text = """
    assign j = 0;
    while(j<5)
    {
        print(j);
        assign k = 0;
        while(k<2)
        {
            print(k);
            k = k + 1;
        }
        j = j +1;
    }
    """
    obj_parser = Parser.from_lexer(Lexer.from_stream(Stream.from_string(text)))
    a = obj_parser.parse_program()
    for i in a.statements:
        print(i)


# string test
def test_case6():
    print(f"\nTest Case 6")
    text = """
        #1
        assign a = "Hello World!";
        print(a);

        #2
        a = "Hello World!";
        a = slice(a: 0: 5: 1);
        print(a);

        #3
        #slice("Hello World!": 0: 5: 1)
    """
    obj_parser = Parser.from_lexer(Lexer.from_stream(Stream.from_string(text)))
    a = obj_parser.parse_program()
    for i in a.statements:
        print(i)


# let test
def test_case7():
    print(f"\nTest Case 7")
    text = """
    let x=1+2*3 (x+1)
    let y=2 (let x=2 (x+y));
    print(x);
    print("hello");
    let x=2 (let y=3 (let z=4 (x+y+z)));
    assign v=let u=2
    (
        let t=2
            (let a=2(u+ a*t))
    );
    print(v);
    """
    obj_parser = Parser.from_lexer(Lexer.from_stream(Stream.from_string(text)))
    a = obj_parser.parse_program()
    for i in a.statements:
        print(i)