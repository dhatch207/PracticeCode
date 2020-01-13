# Simple python implementation of Euler Phi function
# Math sourced from Elementary Number Theory by Kenneth H. Rosen
# 2020 Dominic Hatch dhatch207 dmh207@gmail.com

import BruteforceFactorization

def EulerPhi(n):
    # does the math. takes number, returns value of euler phi function
    x = n
    for i in BruteforceFactorization.pfactor(n):
        x = x * (1 - (1/i))

    return int(x)


def main():
    print("Enter number:")
    n = int(input())
    print("Euler Phi value:")
    print(EulerPhi(n))

if __name__ == "__main__":
   main()