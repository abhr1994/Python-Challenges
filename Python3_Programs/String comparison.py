# -*- coding: cp1252 -*-
'''
In a native language the increasing order of priority of characters is a, b, c, d, e, f, g, h, i, j, k, l, m, n, ’ng’ , o, p, q, r, s, t, u, v, w, x, y, z. You are given two strings string1 and string2 and your task is to compare them on the basis of the given priority order.

Print ‘0’ if both the strings are equal, ‘1’ if string1 is greater than string2 and ‘-1’ if string1 is lesser than string2. All the strings consist of lowercase English alphabets only.

 

Input:

The first line of the input contains a single integer T denoting the number of test cases. Each of the test case consists of a single line containing space separated two strings string1 and string2. 
 

Output:

For each test case, print the required output in a new line. 
 

Constraints:

1 <= T <= 1000

1 <= |string1, string2| <= 10^8 
 

Example:

Input:

3

adding addio

abcng abcno

abngc abngc

Output:

-1

1

0

Explanation:

Assume 0-based indexing.

For the 1st test case:

The Strings differ at index = 4. Comparing ‘ng’ and ‘o’, we have string1 < string2.

For the 2nd test case:

The Strings differ at index = 3. Comparing ‘ng’ and ‘n’, we have string1 > string2.

For the 3rd test case:

Both the strings are same.
'''

############################First solution (Time > 0.5 seconds) Hence failed#################################
dic = {'ng': 15, 'a': 1, 'c': 3, 'b': 2, 'e': 5, 'd': 4, 'g': 7, 'f': 6, 'i': 9, 'h': 8, 'k': 11, 'j': 10, 'm': 13, 'l': 12, 'o': 16, 'n': 14, 'q': 18, 'p': 17, 's': 20, 'r': 19, 'u': 22, 't': 21, 'w': 24, 'v': 23, 'y': 26, 'x': 25, 'z': 27}
def f(a):
    i = 0
    l=[]
    while i<=len(a)-1:
	if a[i:i+2]=='ng':
	    l.append('ng')
	    i+=2
	else:
	    l.append(a[i])
	    i=i+1
    return l

for _ in range(int(input())):
    lflag = 0
    gflag = 0 
    inp = input().split()
    #inp[0] and inp[1] are 2 strings
    l1 = f(inp[0])
    l2 = f(inp[1])
    for i,j in zip(l1,l2):
        if dic[i]>dic[j]:
            print( 1 )
            break
        if dic[i]<dic[j]:
            print( -1 )
            break
    else:
        if len(l1)==len(l2):
            print( 0 )
            continue
        elif len(l1)<len(l2):
            print( -1 )
            continue
        else:
            print( 1 )
#####################2nd Solution (Time > 0.5 seconds) Hence failed########################
def f(a):
    i = 0
    l=[]
    while i<=len(a)-1:
	if a[i:i+2]=='ng':
	    l.append('ng')
	    i+=2
	else:
	    l.append(a[i])
	    i=i+1
    return l

for _ in range(int(input())):
    inp = input().split()
    #inp[0] and inp[1] are 2 strings
    l1 = f(inp[0])
    l2 = f(inp[1])
    for i,j in zip(l1,l2):
        if i>j:
            print( 1 )
            break
        if i<j:
            print( -1 )
            break
    else:
        if len(l1)==len(l2):
            print( 0 )
            continue
        elif len(l1)<len(l2):
            print( -1 )
            continue
        else:
            print( 1 )
########################Final solution  (Execution Time:0.02 seconds. Hence passed###############################
def f(a,b):
    if a > b:
        return 1
    elif a<b:
        return -1
    else:
        return 0
    
for _ in range(int(input())):
    inp = input().split()
    i=0
    flag = 0
    a,b=inp[0],inp[1]
    while i<=min(len(a),len(b))-1:
        if a[i:i+2] == 'ng' and b[i:i+2] == 'ng':
            i = i+2
            continue
        if a[i:i+2] == 'ng':
            if a[i:i+2] > b[i]:
                print (1)
            else:
                print (-1)
            flag = 1
            break
        if b[i:i+2] == 'ng':
            if a[i] > b[i:i+2]:
                print (1)
            else:
                print (-1)
            flag = 1
            break
        
        if a[i] > b[i]:
            print (1)
            flag = 1
            break
        elif a[i]<b[i]:
            print (-1)
            flag = 1
            break
        else:
            pass
        
        i+=1
    
    if flag == 0:
        if len(a)>len(b):
            print (1)
        elif len(a) < len(b):
            print (-1)
        else:
            print (0)
        
        
