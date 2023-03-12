import os, sys
current_dir = os.getcwd()
sys.path.append(current_dir)
# print(f"syst path {sys.path}")

from lexer import *

# operator test
def test_case1():
    print(f"\nTestcase 1")
    text = """
    #unary operator
    ++--6 
    + - / * % //   ** 
    < > <= >= == != 
    << >> = ++ -- += -= *= /= %= //= **=
    and or
    """
    object_lexer = Lexer.from_stream(Stream.from_string(text))
    for token in object_lexer:
        print(token)
    
# data type test
def test_case2():
    print(f"\nTestcase 2")
    text = """
    12 5 9630 
    12.5 0.5 .5
    "HelloWorld" 'HelloWorld'
    True False
    true false
    """
    object_lexer = Lexer.from_stream(Stream.from_string(text))
    for token in object_lexer:
        print(token)


# keyword and identifier test
def test_case3():
    print(f"\nTestcase 3")
    text = """
    assign const None
    if elif then else while for print 
    a1 =                       False   True 
    """
    object_lexer = Lexer.from_stream(Stream.from_string(text))
    for token in object_lexer:
        print(token)

# comment, whitespace, end of line test
def test_case4():
    print(f"\nTestcase 4")
    text = """
    # this is comment
    # this is comment
    a5 =       8       
    ;
    """
    object_lexer = Lexer.from_stream(Stream.from_string(text))
    for token in object_lexer:
        print(token)


# brackets test
def test_case5():
    print(f"\nTestcase 5")
    text = """
    ( ) [  {  } ] 
    """
    # brackets matching is done by lexer
    # text = """
    # ( ) [ ] { 
    # """ this is error as { is not closed
    
    object_lexer = Lexer.from_stream(Stream.from_string(text))
    for token in object_lexer:
        print(token)

# slicing test
def test_case6():
    print(f"\nTestcase 6")
    text = """
    slice("Hello":0:2:1)
    """
    
    object_lexer = Lexer.from_stream(Stream.from_string(text))
    for token in object_lexer:
        print(token)



if __name__ == "__main__":
    test_case1()
    test_case2()
    test_case3()
    test_case4()
    test_case5()
    test_case6()
    print("\nAll tests passed")