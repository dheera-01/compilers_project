# #  eluer14.py - Project Euler problem 14
# N = 1000000
# N = N +1
# dp = [0]*N

# max_length= 0
# max_num = 0
# for i in range(2,N):
#     num = i
#     length = 0
#     while(num >= i):
#         if num % 2 == 0:
#             num = num // 2
#         else:
#             num = 3*num + 1
#         length = length + 1
    
#     dp[i] = length + dp[num]
#     if dp[i] > max_length:
#         max_length = dp[i]
#         max_num = i

# print (max_num)
# print (max_length)
# # print (dp)


import time
start = time.time()

def collatzSeq (n):
    chainNumber = 1
    n1 = n
    while n1 != 1:
        if n1 % 2 == 0:
            n1 = n1/2
            chainNumber += 1
        else:
            n1 = (3*n1) + 1
            chainNumber += 1
    return [chainNumber, n]

fullList = []
for i in range(2, 1000000):
    fullList.append(collatzSeq(i))
sortedList = sorted(fullList, reverse=True)
print(sortedList[:1])

print('Time:', 1000*(time.time() - start))