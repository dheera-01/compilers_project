import dis


def factorial(n, b, j=6):
    y = n + b + j
    def aff(n, h):
        return n + h
    return aff(y, 6) + aff(b, 6)
    # c = n  + j * b
    # return factorial(5, 6) + factorial(7,6)


print(dis.dis(factorial))



