'''
Given two expressions in the form of strings. The task is to compare them and check if they are similar. Expressions consist of lowercase alphabets, '+', '-' and  '( )'.

Input:
The first line of input contains an integer T denoting the number of test cases. Then T test cases follow. Each test case contains two lines. And each line contains an expression.

Output
For each test case, print in a new line "YES"  if the expressions are similar else print "NO".

Constraints:
1<=T<=100
3<=|Expression length|<=100

Example:
Input:
2
-(a+b+c)
-a-b-c
a-b-(c-d)
a-b-c-d

Output:
YES
NO

The case should be satisfied for :

+a+b+c
a+c+b

-(a+b+c)
-a-b-c

a-b-(c-d)
a-b-c-d

(-(-(-(-(a+b+c))))
a+b+c

d-d+i+j+k-k+k
i+j+k
'''

#This is the function to return a value after multiplying sign to array. The return value will be excluding the brackets.
def f(arr,sign):
	if sign == '+':
		return arr[1:-1]
	else:
		b = arr[1:-1]
		out = ''
		for i in b:
			if i == '+':
				out = out+'-'
			elif i == '-':
				out = out+'+'
			else:
				out = out+i
		return out

#This is the function to simplify the array. Loop untill there is no group of brackets found
def simplify(a):
    b = a
    flag = 1
    while flag:
        l=[]
        l1=[]
        for i,j in enumerate(b):
            if j == '(':
                l.append(i)
            elif j == ')':
                out = l.pop()
                l1.append((out,i))
                break
            else:
                pass
        else:
            #print ('wrong bracketing, ex: (a+b+c   ')
            flag = 0
            return b.strip('(').strip(')')

        #l1 has list of tuples with open and close brackets
        if flag!=0:
            for j in l1:
                m = int(j[0])
                n = int(j[1])
                if m == 0:           #eg: (a+b+c)
                    sign = '+'
                else:
                    sign = b[m-1]    #eg: (a-(b+c))
                if not('+' in sign or '-' in sign):
                    sign = '+'       #eg: ((a+b-c))-((a-b-c))
                c = f(b[m:n+1],sign)
                if c.startswith('+') or c.startswith('-'):
                    if m == 0:
                        b = b[0:m]+c+b[n+1:]       # if m==0 b[0:-1] returns ulta string which is not necessary. 
                    else:
                        b = b[0:m-1]+c+b[n+1:]
                    
                else:
                    b = b[0:m]+c+b[n+1:]
    return b
        
for _ in range(int(input())):
    inp1 = input().strip()
    inp2 = input().strip()
    
    out1 = simplify(inp1).strip('+')     #Simplify input array and strip '+' in front
    out2 = simplify(inp2).strip('+')
    if not (out1[0]=='+' or out1[0]=='-'):
        out1 = '+'+out1
    if not (out2[0]=='+' or out2[0]=='-'):
        out2 = '+'+out2
    #print(out1)
    #print(out2)
    l1 = []
    l2 = []
    for i in range(0,len(out1),2):
        l1.append(out1[i:i+2])
    for i in range(0,len(out2),2):
        l2.append(out2[i:i+2])

    #l1 and l2 have elements with signs
    l1 = sorted(l1)
    l2 = sorted(l2)

    #check if elements get deleted. For eg: +d and -d
    for i in l1:
	    if i[0] == '+':
		    if '-'+i[1] in l1:
			    l1.remove(i)
			    l1.remove('-'+i[1])
	    else:
		    if '+'+i[1] in l1:
			    l1.remove(i)
			    l1.remove('+'+i[1])
    for i in l2:
	    if i[0] == '+':
		    if '-'+i[1] in l2:
			    l2.remove(i)
			    l2.remove('-'+i[1])
	    else:
		    if '+'+i[1] in l2:
			    l2.remove(i)
			    l2.remove('+'+i[1])
    if l1 == l2:
        print ('YES')
    else:
        print ('NO')
