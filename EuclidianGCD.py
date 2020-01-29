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

    r = p % q
    
    while r != 0:
        c = int(p / q) 
        print(f"{p} = ({c}){q} + {r}")
        p = q
        q = r
        r = p % q
    
    print(f"{p} = ({c}){q} + {r}")

    print(f"GCD: {q}")
    print(f"{x} = ({int(x/q)}){q}")
    print(f"{y} = ({int(y/q)}){q}")

    return q

        
    

def main():
    print("First number:")
    x = int(input())
    print("Second number:")
    y = int(input())

    (EuclidianGCD(x,y))

if __name__ == "__main__":
   main()
