# Simple bruteforce factorization of a number
# 2020 Dominic Hatch dhatch207 dmh207@gmail.com

import EuclidianGCD

def factor(n):
    # takes number, returns list of factors
    factors = []
    for i in range(n):
        if n % (i+1) == 0:
            factors.append(i+1)

    return factors

def pfactor(n):
    # takes number, returns list of prime factors
    pfactors = []
    for x in factor(n):
        if x == 1: continue
        prime = True
        for i in pfactors:
            if EuclidianGCD.EuclidianGCD(i,x) != 1:
                prime = False 
        if prime:
            pfactors.append(x)

    return pfactors

def pdegrees(n):
    #takes number, returns list of degrees of factors 
    pfactors = pfactor(n)
    l = len(pfactors)
    pdegrees = [1] * l
    for x in range(l):
        x = l-x-1
        q = n / pfactors[x]
        while q % pfactors[x] == 0:
            pdegrees[x] = pdegrees[x] + 1
            q = q / pfactors[x]

    return pdegrees

def main():
    print("Enter number to be factored")
    n = int(input())
    print("Factors:")
    print(*factor(n), sep = ", ")
    print("Prime factors:")
    print(*pfactor(n), sep = ", ")
    print("Degree of prime factors:")
    print(*pdegrees(n), sep = ", ")

if __name__ == "__main__":
   main()