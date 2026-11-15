def sq(a, b):
    if (a<0 or b<0):
        raise ValueError("Values aren't correct!")
    else:
        return a*b

def pr(a, b):
    if (a<0 or b<0):
            raise ValueError("Values aren't correct!")
    else:
         return (a + b)*2

if __name__ == "__main__":
    a = float(input("Length: "))
    b = float(input("Width: "))
    print("Sq = ", sq(a, b))
    print("pr = ", pr(a, b))