from parser_1 import *

def test_parse_assign():
    text = "x = 5, y = 6, z = 7"
    obj_parser = Parser.from_lexer(Lexer.from_stream(Stream.from_string(text)))
    assignments = obj_parser.parse_assign()
    assert len(assignments) == 3
    assert isinstance(assignments[0], tuple)
    assert isinstance(assignments[1], tuple)
    assert isinstance(assignments[2], tuple)
    assert assignments[0][0] == "x"
    assert assignments[0][1] == 5
    assert assignments[1][0] == "y"
    assert assignments[1][1] == 6
    assert assignments[2][0] == "z"
    assert assignments[2][1] == 7
