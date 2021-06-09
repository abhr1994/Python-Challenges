# -*- coding: cp1252 -*-
##Given an array A of size N, find all combination of four elements in the array
##whose sum is equal to a given value K.
##For example, if the given array is {10, 2, 3, 4, 5, 9, 7, 8} and K = 23,
##one of the quadruple is “3 5 7 8” (3 + 5 + 7 + 8 = 23).



n=[10,2,3,4,5,9,7,8]
k = 23
n.sort()
for i,j in enumerate(n):
    k = i
    while k+3 < 8:
        print n[i],n[k+1],n[k+2],n[k+3]
        val = n[i]+n[k+1]+n[k+2]+n[k+3]
        if val == 23:
            print n[i],n[k+1],n[k+2],n[k+3]
        k = k+1
       
