import os
import sys
current_dir = os.getcwd()
sys.path.append(current_dir)

from parser_1 import *
from eval_for_parser import *
# print(f"syst path {sys.path}")


# operator test for eval
def test_case1():
    print(f"\nTestcase 1")
    text = """
    # all arithmetic operators
    print((5 + 2 * 8 // 3 - 2 ** 3 % 3)/2);
    # unary operator and right associativity of exponent
    print(-4**3**2);
    # conditional operator
    print(7>6);
    # unary operator
    print(++---6.69);
    print(True);
    print(False);
    print("True");
    print("hello");
    """
    parsed_output = Parser.from_lexer(Lexer.from_stream(
        Stream.from_string(text))).parse_program()
    # print(f"parsed_put: {parsed_output}")
    program_env = Environment()
    eval(parsed_output, program_env)
    # ans = eval(parsed_output)
    # print(ans)

# assignment test
def test_case2():
    print(f"\nTestcase 2")
    text = """
    assign i = 5;
    #assign i = 9;# will give error
    #i = i + j; #will give error
    assign j = 6;
    i += j;
    print(i);
    print(j);
    """
    parsed_output = Parser.from_lexer(Lexer.from_stream(
        Stream.from_string(text))).parse_program()
    # print(f"parsed output: {parsed_output}")
    program_env = Environment()
    eval(parsed_output, program_env)
    # ans = eval(parsed_output)
    
# if else test 
def test_case3():
    print(f"\nTestcase 3")
    text = """
    assign i = 8;
    if(i>6)
    {
        print("Hello");
    }
    else
    {
        print("else");
    }
    """
    parsed_output = Parser.from_lexer(Lexer.from_stream(
        Stream.from_string(text))).parse_program()
    program_env = Environment()
    eval(parsed_output, program_env)
    # ans = eval(parsed_output)

# scoping test
def test_case4():
    print(f"\nTestcase 4")
    text = """
    assign i = 6;
    if(i == 6)
    {
        i -= 10;
    }
    print(i);
    
    if(i == -4)
    {
        assign k = 5;
        assign i = 6;
        i = i * 9;
        print(i);
    }
    #print(k); # give error
    print(i);
    """
    parsed_output = Parser.from_lexer(Lexer.from_stream(
        Stream.from_string(text))).parse_program()
    program_env = Environment()
    eval(parsed_output, program_env)
    # ans = eval(parsed_output)

# for test
def test_case5():
    print(f"\nTestcase 5")
    text = """
    # calculating the factorial
    assign fact = 1;
    assign i = 1;
    # can also use
    # for(assign i = 0; i<5; i+= 1)
    for(i = 1; i<=5; i = i + 1;)
    {
        fact = fact*i;
    }
    #print(i);
    print(fact);
    #print(i);
    """
    parsed_output = Parser.from_lexer(Lexer.from_stream(
        Stream.from_string(text))).parse_program()
    # print(f"parsed output: {parsed_output}")
    program_env = Environment()
    eval(parsed_output, program_env)
    # ans = eval(parsed_output)

# while test
def test_case6():
    print(f"\nTestcase 6")
    text = """
    # calculating the factorial
    assign fact = 1;
    assign i = 1;
    while(i<=5)
    {
        fact = fact*i;
        i += 1;
    }
    #print(i);
    print(fact);
    #print(i);
    """
    parsed_output = Parser.from_lexer(Lexer.from_stream(
        Stream.from_string(text))).parse_program()
    program_env = Environment()
    eval(parsed_output, program_env)
    # ans = eval(parsed_output)

# slicing test
def test_case7():
    print(f"\nTestcase 7")
    text = """
        #1
        assign a = "Hello World!";
        print(a);
        a = slice(a: 0: 5: 1) + "Chirag";
        print(a);

        #3
        #slice("Hello World!": 0: 5: 1)
    """
    parsed_output = Parser.from_lexer(Lexer.from_stream(
        Stream.from_string(text))).parse_program()
    program_env = Environment()
    eval(parsed_output, program_env)
    # ans = eval(parsed_output)

# let test
def test_case8():
    print(f"\nTestcase 8")
    text = """
        assign a = let b = 5  (b ** 2);
        print(a);
        print(b);
    """
    parsed_output = Parser.from_lexer(Lexer.from_stream(
        Stream.from_string(text))).parse_program()
    # print(f"parsed output: {parsed_output}")
    program_env = Environment()
    eval(parsed_output, program_env)
    # ans = eval(parsed_output)

# nested while test
def test_case9():
    print(f"\nTestcase 9")
    text = """
    assign j = 0;
    while(j<5)
    {
        print(j);
        assign k = 10;
        while(k<12)
        {
            print(k);
            k = k + 1;
        }
        j = j +1;
    }
    """
    parsed_output = Parser.from_lexer(Lexer.from_stream(
        Stream.from_string(text))).parse_program()
    # print(f"parsed output: {parsed_output}")
    # program_env = Environment()
    # eval(parsed_output, program_env)
    # ans = eval(parsed_output)
    eval(parsed_output)

# and, or operator
def test_case10():
    print(f"\nTestcase 10")
    text = """
    assign i = 1;
    # and has high precedence 
    if(i == 1 and i == 0 or i > -1)
    {
        print("Inside if");
    }
    else
    {
        print("Inside else");
    }
    """
    parsed_output = Parser.from_lexer(Lexer.from_stream(
        Stream.from_string(text))).parse_program()
    eval(parsed_output)
    

if __name__ == "__main__":
    test_case1()
    test_case2()
    test_case3()
    test_case4()
    test_case5()
    test_case6()
    test_case7()
    test_case8()
    test_case9()
    test_case10()
    print(f"\nAll testcases passed")
