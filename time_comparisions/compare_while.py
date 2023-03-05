import time
import parser
# python code

no_of_iterations=3
mean_time_python=0

for iter in range(no_of_iterations):
    beg=time.time()
    i=0
    while(i<1000):
        print(i)
        i=i+1
    end=time.time()
    mean_time_python=mean_time_python+end-beg
mean_time_python=mean_time_python/no_of_iterations

mean_time_our_lang=0
for iter in range(no_of_iterations):
    beg=time.time()
    parser.parse_code_file('C:/Users/Sandeep/Desktop/2023 Spring/Compilers/compilers_project/time_comparisions/code_while.txt')
    end=time.time()
    mean_time_our_lang=mean_time_our_lang+end-beg
mean_time_our_lang=mean_time_our_lang/no_of_iterations

print("Mean time taken by python for "+str(no_of_iterations)+" iterations is: ",mean_time_python*1000)

print("Mean taken by our language for"+str(no_of_iterations)+" is: ",mean_time_our_lang*1000)
