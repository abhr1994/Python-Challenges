# -*- coding: cp1252 -*-
##Consider a big party where a log register for guest’s entry and exit times is maintained. Find the time at which there are maximum guests in the party. Note that entries in register are not in any order.
##
##Input:
##The first line of input contains an integer T denoting the number of test cases. Then T test cases follow. Each test case contains an integer n denoting the size of the entry and exit array. Then the next two line contains the entry and exit array respectively.
##
##Output:
##Print the maximum no of guests and the time at which there are maximum guests in the party.
##
##Constraints:
##1<=T<=10^5
##1<=N<=10^5
##1<=entry[i],exit[i]<=10^5
##
##Example:
##Input:
##2
##5
##1 2 10 5 5
##4 5 12 9 12
##7
##13 28 29 14 40 17 3 
##107 95 111 105 70 127 74 
##
##Output:
##3 5
##7 40

for _ in range(int(input())):
    count = 0
    time_member = {}
    n = int(input())
    arr1 = [int(i) for i in input().split()]
    arr2 = [int(i) for i in input().split()]
    arr3 = list(set(arr1+arr2))
    arr3.sort()
    for time in arr3:
        count = count + arr1.count(time)
        time_member[time] = count
        count = count - arr2.count(time)
        
        
    out = sorted(time_member.items(),key = lambda x:x[1],reverse=True)
    high = out[0][1]
    high_time = [(i,j)for i,j in out if j==high]
    high_time.sort()
    print(high_time[0][1],high_time[0][0])
