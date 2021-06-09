def f(n):
    l = range(1,n*2,2)
    mid = int(l[-1] / 2) + (l[-1] % 2 > 0)
    d={}
    m = range(1,n+1)
    d[m[0]] = [n]
    for i in m[1:]:
        lis = range(-(i-1),i,2)
        lis1 = [j+n for j in lis]
        d[i]=lis1
    return n,d

n,d = f(5)
l = range(1,n*2)
m = range(1,n+1)

for i in m:
    for j in l:
        temp=d[i]
        if j in temp:
            print "*",
        else:
            print " ",
            
    print '\n'
    

