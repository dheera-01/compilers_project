import os
from my_parser import *

tests = []
test_dir_inputs = "testcases/inputs"

for path in os.listdir(test_dir_inputs):
    if os.path.isfile(os.path.join(test_dir_inputs, path)):
        tests.append(path)

tests.sort()
total_tests = len(tests)
passed_tests = 0
failed_tests = 0
passed_tests_lst = []
failed_tests_lst = []

failed_tests_lst_expected = []
failed_tests_lst_output = []

for test in tests:
    input_file = open(os.path.join("testcases/inputs/"+test), "r").read()
    output_file = open(os.path.join("testcases/outputs/"+test), "r").read()

    parsed_output = Parser.from_lexer(Lexer.from_stream(Stream.from_string(input_file))).parse_program()
    display_output.clear()
    eval(parsed_output)

    output_file_lst = []
    for line in output_file.split('\n'):
        output_file_lst.append(line)

    if display_output == output_file_lst:
        passed_tests += 1
        passed_tests_lst.append(test)
    else:
        failed_tests += 1
        failed_tests_lst.append(test)
        failed_tests_lst_expected.append(output_file_lst)
        failed_tests_lst_output.append(display_output.copy())


def print_failed_comparison():
    print(f"\033[1;31;48m")
    for i in range(len(failed_tests_lst)):
        print(f"{i}. {failed_tests_lst[i]}")
        print(f"        Output:")
        print(f"            {failed_tests_lst_output[i]}")
        print(f"        Expected:")
        print(f"            {failed_tests_lst_expected[i]}")


def print_passed():
    print(f"\033[1;32;48m")
    for i in range(len(passed_tests_lst)):
        print(f"{i}. {passed_tests_lst[i]}")


def print_total_report():
    print(f"--------------------Testcases Report--------------------")
    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")


print_total_report()
print_passed()
print_failed_comparison()