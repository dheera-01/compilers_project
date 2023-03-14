import os
import sys
current_dir = os.getcwd()
sys.path.append(current_dir)

import time
from my_parser import *
# python code

# no_of_iterations=3
# mean_time_python=0

# for iter in range(no_of_iterations):
#     beg=time.time()
#     for i in range(1000):
#         print(i)
#     end=time.time()
#     mean_time_python=mean_time_python+end-beg
# mean_time_python=mean_time_python/no_of_iterations

# mean_time_our_lang=0
# for iter in range(no_of_iterations):
#     beg=time.time()
#     parser_1.parse_code_file('time_comparisons/code_for.txt')
#     end=time.time()
#     mean_time_our_lang=mean_time_our_lang+end-beg
# mean_time_our_lang=mean_time_our_lang/no_of_iterations

# print("Mean time taken by python for "+str(no_of_iterations)+" iterations is: ",mean_time_python)

# print("Mean taken by our language for"+str(no_of_iterations)+" is: ",mean_time_our_lang)

# python
n = 1000000
fib_1 = 0
fib_2 = 1
fib = 0

time_taken_python = []
print("python")
for i in range(3):
    print("iteration: ", i)
    start_time = time.time()
    for i in range(1, n+1):
        fib = fib_1 + fib_2
        fib_1 = fib_2
        fib_2 = fib
    end_time = time.time()
    time_taken_python.append(end_time - start_time)
print("mean time taken by python is: ", sum(time_taken_python)/len(time_taken_python))


print("my language")
time_taken_my = []
for i in range(3):
    print("iteration: ", i)
    start_time = time.time()
    file = open("time_comparisions/code_for.txt", "r")
    text = file.read()
    parsed_output = Parser.from_lexer(Lexer.from_stream(
            Stream.from_string(text))).parse_program()
        # print(f"parsed_put: {parsed_output}")
    program_env = Environment()
    eval(parsed_output, program_env)
    end_time = time.time()
    # print(end_time - start_time )
    time_taken_my.append(end_time - start_time)
    file.close()
print("mean time taken by my language is: ", sum(time_taken_my)/len(time_taken_my))
