##Given an array of numbers, the task is to print only those numbers which have only 1, 2 and 3 as their digits.
##
##Input:
##The first line of input contains an integer T denoting the number of test cases. Then T test cases follow. Each test case consists of two lines. First line of each test case contains an integer N and the second line contains N space separated array elements.
##
##Output:
##For each test case, In new line print the required elements in increasing order. if there is no such element present in the array print "-1".
##
##Constraints:
##1<=T<=100
##1<=N<=106
##1<=A[i]<=106
##
##Example:
##Input:
##2
##3
##4 6 7
##4
##1 2 3 4
##
##Output:
##
##-1
##1 2 3

import re
com = re.compile('1|2|3')
t = int(input())
for _ in range(t):
    N = input()
    inp = input().split()
    out = [int(i) for i in inp if com.sub('',i)=='']
    out.sort()
    out = [str(i) for i in out]
    if len(out)==0:
        print('-1')
    else:
        print(' '.join(out))
