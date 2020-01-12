# Simple python implementation of Pollard Rho method of factoring
# Currenly uses x^2+1
# Math sourced from Elementary Number Theory by Kenneth H. Rosen
# 2020 Dominic Hatch dhatch207 dmh207@gmail.com

import numpy, math

def compute(n,x):
    # does the math. takes number, returns list of factors
    factors = [1,]
    iterations = [x, ]
    i = 0
    factor = 1
   # while numpy.prod(factors) != n:
    while factor == 1:
        # find next iteration
        y = (iterations[i] * iterations[i] + 1) % n 
     #   if y == 0: y = n
        iterations.append(y)
        i = i + 1

        #check factors
        for x in iterations:
            diff = iterations[i]-x
            if diff < 1: break
            gcd = math.gcd(n,diff)
            if gcd != 1:
               factor = gcd
            #   factors.append(gcd)

    return factor


def main():
    print("Enter number to be factored")
    n = int(input())
    #print("Enter seed")
    #x = int(input())
    x = 2
    print(compute(n,x))
    #print(*compute(n,x), sep = ", ")

main()
