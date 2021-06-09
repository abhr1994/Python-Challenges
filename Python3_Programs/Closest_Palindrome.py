'''
https://practice.geeksforgeeks.org/problems/closest-palindrome/0

Given a number N. our task is to find the closest Palindrome number whose absolute difference with given number is minimum.

Input:
The first line of the input contains integer T denoting the number of test cases. Each test case contains a  number N.

Output:
For each test case, the print the closest palindrome number.
Note:  If the difference of two closest palindromes numbers is equal then we print smaller number as output.

Constraints:
1<=T<=1000
1<=n<=10^14

Input :
2
9
489

output:
8
484

Explanation :

Test Case 1: closest palindrome number is 8.
'''
import sys
def f(inp):

    l=[]
    for i in range(1,len(inp)//2):
        if int(inp[i])-1 >=0:
            if int(inp[i])+1 <=9:
                temp = (str(int(inp[i])-1),inp[i],str(int(inp[i])+1))
            else:
                temp = ('0',str(int(inp[i])-1),inp[i])
        else:
            temp = (inp[i],str(int(inp[i])+1))
        l.append(temp)

    if len(inp)&1 :
        if int(inp[len(inp)//2])-1 >= 0:
            if int(inp[len(inp)//2])+1 <=9:
                temp = (inp[len(inp)//2],str(int(inp[len(inp)//2])-1),str(int(inp[len(inp)//2])+1))
            else:
                temp = (inp[len(inp)//2],str(int(inp[len(inp)//2])-1),'0')
        else:
            temp = (inp[len(inp)//2],'9',str(int(inp[len(inp)//2])+1))
        l.append(temp)
    #print(l)
    
    out = [inp[0]]
    for i in l:
        t = out[::]
        out = []
        for j in i:
            for k in t:
                out.append(k+j)
    return out   

for _ in range(int(input())):
    inp = input()
    if len(inp)==1:
        print(int(inp)-1)
        continue
    if len(inp) == inp.count('9'):
        print('1'+(len(inp)-1)*'0'+'1')
        continue
    if inp.startswith('1') and inp.endswith('1') and inp.count('0')==len(inp)-2:
	    print ('9'*(len(inp)-1))
	    continue
    out = f(inp)
    if len(inp)&1:  ##ODD
        out1 = [i+i[-2::-1] for i in out]
    else:
        out1 = [i+i[::-1] for i in out]
    
    answer = sys.maxsize
    m = int(inp)
    #print(out1)
    if len(out1)==1:
        s = out1[0]
        if s==inp:
            if len(s)&1:
                print(s[0:len(s)//2]+str(int(s[len(s)//2])-1)+s[len(s)//2+1:])
                continue
            else:
                print(s[0:len(s)//2-1]+str(int(s[len(s)//2])-1)*2+s[len(s)//2+1:])
                continue
    try:
        for i in out1:
            if abs(m-int(i)) < abs(answer-m):
                if m!=int(i):
                    answer = int(i)
    except:
        print(out1)
        print('error')
    print(answer)
    
    
