#Print jumping numbers. That is 10,12,21,32,23 etc. Difference between adjacent should be 1.

def bfs(num, x):
    #print(num,'number')
    #print(x,'x')
    q = [num]
    #print (q)
    while q != []:
        #print (q,'inside while')
        n = q.pop()
        ld = n % 10
        if n <= x:
            print(n, end=' ')
            if ld == 0:
                q = [n * 10 + ld + 1] + q
            elif ld == 9:
                q = [n * 10 + ld - 1] + q
            else:
                q = [n * 10 + ld - 1] + q
                q = [n * 10 + ld + 1] + q

def jumping(x):
    print(0, end=' ')
    for i in range(1, min(x, 9) + 1):
        bfs(i, x)
    print()

def main():
    for _ in range(int(input())):
        jumping(int(input()))

if __name__ == '__main__':
    main()
