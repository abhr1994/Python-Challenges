'''
Given two numbers. Add the numbers and find the count of carries in their addition.

Input:
The first line of input contains an integer T denoting the number of test cases. Then T test cases follow. Each test case contains two integer N and M as input.

Output:
For each test case, In new line print the count of carries.

Constraints:
1<=T<=1000
1<=N,M<=1018

Example:
Input:
2
345 234
2345 535

Output:
0
1
'''

for _ in range(int(input())):
    inp = input().split()
    counter = 0
    diff = abs(len(inp[0])-len(inp[1]))
    zero = diff*'0'
    a = ''
    b = ''
    if len(inp[0])>len(inp[1]):
        a = inp[0]
        b = zero + inp[1]
    elif len(inp[0])<len(inp[1]):
        a = zero + inp[0]
        b = inp[1]
    else:
        a = inp[0]
        b = inp[1]
    
    count = 0
    for i in range(-1,-(len(a)+1),-1):
        if int(a[i])+int(b[i])+count >=10:
            count = 1
            counter+=1
        else:
            count = 0
    
    print(counter)
