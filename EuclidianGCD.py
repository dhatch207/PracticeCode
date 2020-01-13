# Simple python implementation of Euclidian method for finding GCD
# Math sourced from Elementary Number Theory by Kenneth H. Rosen
# 2020 Dominic Hatch dhatch207 dmh207@gmail.com

def EuclidianGCD(x,y):
    p = x
    q = y
    if x == y: return y
    if x < y:
        p = y
        q = x

    s = p % q
    
    while s != 0:
        p = q
        q = s
        s = p % q

    return q

        
    

def main():
    print("First number:")
    x = int(input())
    print("Second number:")
    y = int(input())
    print("GCD:")
    print(EuclidianGCD(x,y))

if __name__ == "__main__":
   main()
