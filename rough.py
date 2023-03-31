# # a = [""]
# # # a.append("")
# # print(a)
# # a[-1]+= "1";
# # a[-1]+= "5";
# # print(a)
# # with open('program.txt', 'r') as file:
# #     for line in file:
# #         print(line, end='')

# file = open('program.txt', 'r')
# for line in file:
#     print(line, end='')
# file.close()

def get_program_lines(program):
    lines = program.splitlines()
    return lines
program_file = open('program.txt', 'r')
program = program_file.read()
program_file.close()

lines = get_program_lines(program)
print(lines)
