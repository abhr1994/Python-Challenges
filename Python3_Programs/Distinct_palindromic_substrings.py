'''
Given a string of lowercase ASCII characters, find all distinct continuous palindromic sub-strings of it.

Input:
The first line of input contains an integer T denoting the number of test cases. Then T test cases follow. Each test case contains a string.

Output:
Print the count of distinct continuous palindromic sub-strings of it.

Constraints:
1<=T<=10^5
1<=length of string<=10^5

Example:
Input:
2
abaaa
geek

Output:
5
4
'''
#code

def index_ret(arr,ch,k):
    l = []
    for i,j in enumerate(arr):
        if j == ch:
            if i>k:
                l.append(i)
    return l
    
for _ in range(int(input())):
    out = []
    inp = input().strip()
    count = len(list(set(inp)))
    for i in range(len(inp)-1):
        l = index_ret(inp,inp[i],i)
        for j in l:
            t = inp[i:j+1]
            t_rev = t[::-1]
            if t == t_rev:
                if t not in out:
                    out.append(t)
                
    print(count+len(out))
        
    
    
    
