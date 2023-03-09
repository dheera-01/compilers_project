import os, sys
current_dir = os.getcwd()
sys.path.append(current_dir)
# print(f"syst path {sys.path}")

from parser_1 import *

# arithmetic, unary operation, precedence and associativity
def test_case1():
    print("\nTest case 1")
    text = """
    # unary operator
    ++--6 
    i = -2**6**8; # exponent have high precedence
    # simple expression
    8 / 6
    # precedence
    8 + 9 * 10
    2 * (3+5)
    # right associativity
    2 * 3 * 4
    # right associativity
    2 ** 3 ** 3
    """
    obj_parser = Parser.from_lexer(Lexer.from_stream(Stream.from_string(text)))
    for i in obj_parser.parse_program().statements:
        print(i)
        

# test case assign and update
def test_case2():
    print("\nTest case 2")
    text = """
    assign i = i+5;
    const assign j = i+5;
    j = j + 1 * i;
    """
    obj_parser = Parser.from_lexer(Lexer.from_stream(Stream.from_string(text)))
    for i in obj_parser.parse_program().statements:
        print(i)


# if else test
def test_case3():
    print("\nTest case 3")
    text = """
    # if else both
    if("hello world" > "chirag" and "hi" == "hi")
    {
        i = i + k +l;
        i = 10;
    }
    else 
    {
        "hello"
    }
    
    
    # only if
    if(i>5 or j != 5)
    {
        i = i +5;
        8+5
    }
   
    """
    obj_parser = Parser.from_lexer(Lexer.from_stream(Stream.from_string(text)))
    for i in obj_parser.parse_program().statements:
        print(i)
        
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


#string test
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
    



if __name__ == "__main__":

    test_case1()
    test_case2()
    test_case3()
    test_case3_1()
    test_case4()
    test_case5()
    test_case6()
    test_case7()
    print("\nAll test cases passed")
    pass