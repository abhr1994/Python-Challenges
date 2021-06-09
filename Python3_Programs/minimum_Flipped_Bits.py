##Given a string containing 0’s and 1’s. The task is to find out minimum number of bits to be flipped such that 0’s and 1’s will be alternative.
##
##Input:
##The first line of input contains an integer T denoting the number of test cases. Then T test cases follow. Each test case contains a string.
##
##Output:
##For each test case, print the minimum number of flipped bits in a new line.
##
##Constraints:
##1<=T<=100
##1<=|string length|<=104
##
##Example:
##Input:
##2
##0011
##011000
##Output:
##2
##3

for i in range(int(input())):
    n=input()
    x=len(n)
    res1=[]
    res2=[]
    for j in range(x):
        if j%2==0:
            res1.append(0)
            res2.append(1)
        else:
            res1.append(1)
            res2.append(0)
    
    string1=''.join(str(p) for p in res1)
    string2=''.join(str(p) for p in res2)
    
    count1 = sum(1 for a, b in zip(string1, n) if a != b)
    count2 = sum(1 for a, b in zip(string2, n) if a != b)
    
    print(string1)
    print(string2)
    if count1<count2:
        print(count1)
    else:
        print(count2)
