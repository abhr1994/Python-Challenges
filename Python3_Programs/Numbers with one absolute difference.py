'''
Given a number N. The task is to print all the numbers less than or equal to N in increasing order, with the fact that absolute difference between any adjacent digits of number should be 1.

Input:
The first line of input contains an integer T denoting the number of test cases. Then T test cases follow. Each test case contains an integer N.

Output:
In new line print all the required numbers. if there is no such number less than or equal to N then print "-1".

Constraints:
1<=T<=100
1<=N<=1012

Example:
Input:
2
20
9
Output:
10 12
-1

'''
global lis
global out
lis = []
def f(n):       #n is passed as string
    l=[]
    if int(n[-1])-1 >=0:
	    a = int(n[-1])-1
	    l.append(n+str(a))
    if int(n[-1])+1 <= 9:
	    a = int(n[-1])+1
	    l.append(n+str(a))
    return l

for i in range(1,10):
    for j in f(str(i)):
	    lis.append(j)

for _ in range(int(input())):
    inp = input()
    count = 0
    flag = 0
    out = []
    if int(inp) <10:
        print('-1')
        continue
    elif int(inp) < 100:
    	for i in lis:
    	    if int(i)<=int(inp):
                out.append(i)
    	    else:
                print(" ".join(out))
                break
    else:
        end = False
        temp = lis[:]
        out1 = []
        while end == False:
            for i in temp:
                for j in f(i):
                    if int(j) <= int(inp):
                        out.append(j)
                    else:
                        flag = 1
                        break
                if flag == 1:
                    end = True
                    break
            temp = out
            out1 = out1 + out
            out = []
        
        out1 = lis + out1
        print(" ".join(out1))
