# -*- coding: utf-8 -*-
##For given string ‘str’ of digits, find length of the longest substring of ‘str’, such that the length of the substring is 2k digits and sum of left k digits is equal to the sum of right k digits.
## 
##
##Input:
##
##The first line of input contains an integer T denoting the number of test cases. The description of T test cases follows.
##Each test case contains a string string of length N.
##
##Output:
##
##Print length of the longest substring of length 2k such that sum of left k elements is equal to right k elements and if there is no such substring print 0.
##
##
##Constraints:
##
##1 ≤ T ≤ 100
##1 ≤ N ≤ 100
##
##Example:
##
##Input:
##2
##000000
##1234123
##
##Output:
##6
##4  

l=[1,2,3,4,1,2,3]
max = (len(l)/2)*2
ran_list = range(2,max+2,2)
ran_list.sort(reverse=True)
for i in ran_list:
    for j in range(len(l)):
            end = j+i
        if end >= len(l)+1:
            break
        l1 = l[j:end]
        if sum(l1[0:i/2]) == sum(l1[i/2:i]):
            print l1
else:
    print(0)
        
