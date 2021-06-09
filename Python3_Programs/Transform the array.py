##Given an array containing integers, zero is considered an invalid number and rest all other numbers are valid. If two nearest valid numbers are equal then double the value of the first one and make the second number as 0.At last move all the valid numbers on the left.
##
##Input:
##The first line of input contains an integer T denoting the number of test cases. The first line of each test case consists of an integer n. The next line consists of n spaced integers.
##
##Output:
##Print the resultant array.
##
##Constraints: 
##1<=T<=100
##1<=N<=10000
##1<=A[i]<=10000
##
##Example:
##Input:
##1
##12
##2 4 5 0 0 5 4 8 6 0 6 8
##
##Output:
##2 4 10 4 8 12 8 0 0 0 0 0

for _ in range(int(input())):
    n = int(input())
    arr = [int(i) for i in input().split()]
    count_zero = arr.count(0)
    arr1 = [i for i in arr if i!=0]
    i = 0
    while i<len(arr1)-1:
        if arr1[i+1]==arr1[i]:
            arr1[i]=2*arr1[i]
            arr1[i+1]=0
            count_zero+=1
            arr1.pop(i+1)
        else:
            i+=1
    out = arr1 + [0]*count_zero
    print(' '.join(map(str,out)))
