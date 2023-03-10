import io
import os
from contextlib import redirect_stdout

from parser_1 import *

tests = []
test_dir_inputs = "testcases/inputs"

for path in os.listdir(test_dir_inputs):
    if os.path.isfile(os.path.join(test_dir_inputs, path)):
        tests.append(path)

for test in tests:
    input_file = open(os.path.join("testcases/inputs/"+test), "r")
    output_file = open(os.path.join("testcases/outputs/"+test), "r")

    capturedOutput = io.StringIO()
    sys.stdout = capturedOutput

    program = input_file.read()
    obj_parser = Parser.from_lexer(
        Lexer.from_stream(Stream.from_string(program)))

    a = obj_parser.parse_program()
    program_env = Enviroment()
    ans = eval(a, program_env)

    sys.stdout = sys.__stdout__
    # f = io.StringIO()
    # # f.truncate(0)
    # print(f.getvalue())
    # #
    # # os.system('cls' if os.name == 'nt' else 'clear')
    # sys.stdout.flush()
    # with redirect_stdout(f):
    #     program = input_file.read()
    #     obj_parser = Parser.from_lexer(
    #         Lexer.from_stream(Stream.from_string(program)))
    #
    #     a = obj_parser.parse_program()
    #     program_env = Enviroment()
    #     ans = eval(a, program_env)
    #
    output = capturedOutput.getvalue()
    output_file_read = output_file.read()
    os.system('clear');

    try:
        assert output == output_file_read
        print(f"{test} PASSED")
    except:
        print(f"{test} FAILED")
        print(f"OUTPUT:")
        print(output)
        print(f"EXPECTED:")
        print(output_file_read)
