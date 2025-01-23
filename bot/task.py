import sys


def main():
    n = int(input())
    ls = list(map(int, input().split()))

    last = 0
    ind = 0

    for i in range(n):

        new = ls[last]

        if new == -1:
            print("NO")
            return 0
        
        if (new == ind):
            print("YES")
            return 0

        ind = new

    print("NO")
    return 0
            
            
      


if __name__ == '__main__':
    main()