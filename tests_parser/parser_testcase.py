from parser_1 import *

def test_parse_fact():
    print("test_parse_fact")
    text = """
    assign i = 1;
    assign fact = 1;
    while(i <5) {assign i = i + 1; assign fact = fact * i; fact;};
    """
    obj_parser = Parser.from_lexer(
        Lexer.from_stream(Stream.from_string(text)))
    # print(obj_parser)
    a = obj_parser.parse_program()
    print("Program\n",a)
    lst = [
        None, 
        None, 
        [[None, None, 2], [None, None, 6], [None, None, 24], [None, None, 120]]]
    print("ans",eval(a))
    assert eval(a) == lst
    # print("ans",ans)
    # for i in ans:
    #     print(i)

if __name__ == "__main__":
    # test_eval()
    test_parse_fact()
    print("All tests passed")
