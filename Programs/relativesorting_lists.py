##Given two array A1[] and A2[], sort A1 in such a way that the relative order among the elements will be same as those are in A2. For the elements not present in A2. Append them at last in sorted order.
##
##Input:
##
##The first line of input contains an integer T denoting the number of test cases.
##The first line of each test case is M and N,M is the number of elements in A1 and N is the number of elements in A2.
##The second line of each test case contains M elements.
##The third line of each test case contains N elements.
##
##Output:
##
##Print the sorted array according order defined by another array.
##

#!/usr/bin/python
l = [2, 1, 2, 5, 7, 1, 9, 3, 6, 8, 8]
l1 = [2, 1, 8, 3]
l2=[]
l3=[]
for i in l:
    if i not in l1:
        l2.append(i)

try:
    [l.remove(i) for i in l2]
except ValueError:
    pass

l2.sort()
for i in l1:
    for j in l:
        if j == i:
            l3.append(i)

l3=l3+l2
print l3
