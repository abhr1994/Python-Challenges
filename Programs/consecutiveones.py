# -*- coding: cp1252 -*-
#Count number of binary strings without consecutive 1’s

##import math
##inp = raw_input("Enter the value of N: ")
##l = range(int(math.pow(2,int(inp))))
##for num in l:
##    flag = 0
##    form = '{0:'+inp+'b'+'}'
##    a = form.format(num)
##    #print a
##    for i in range(len(a)):
##        if i < len(a)-1:
##            if a[i]=='1' and a[i+1]=='1':
##                break
##    else:
##        print 'found',a
##
##t_cases = int(input())
##for i in range(t_cases):
##    num = int(input())
##    arr = []
##    if num == 0:
##        print(1)
##    elif num == 1:
##        print(2)
##    else:
##        k = 1000000007
##        arr.append(1)
##        arr.append(2)
##        for j in range(2,num + 1):
##            arr.append((arr[j - 1] + arr[j - 2]) % k)
##        print((arr[len(arr) - 1]) % k)
##    


for _ in range(int(input())):
    D = [1, 1]
    N = int(input())
    for i in range(2, N+1):
        D = [D[0]+D[1], D[0]]
    print(sum(D)%1000000007)
