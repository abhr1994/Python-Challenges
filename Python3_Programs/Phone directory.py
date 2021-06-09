# -*- coding: cp1252 -*-
'''
Given a list of contacts which exist in a phone directory. The task is to implement search query for the phone directory. The search query on a string ‘str’ displays all the contacts which prefix as ‘str’. One special property of the search function is that, when a user searches for a contact from the contact list then suggestions (Contacts with prefix as the string entered so for) are shown after user enters each character.

Input:
The first line of input contains an integer T denoting the number of test cases. Then T test cases follow. Each test case contains three lines. First line of each test case contains N i.e., number of contacts. Second line contains space separated all the contacts in the form of string. And third line contains query string.

Output
For each test case, print the query results in new line. If there is no match between query and contacts, print "0".

Constraints:
1<=T<=100
1<=N<=50
1<=|contact[i].length|<=50
1<=|query length|<=6

Example:
Input:
1
3
geeikistest geeksforgeeks geeksfortest
geeips

Output:

geeikistest geeksforgeeks geeksfortest 
geeikistest geeksforgeeks geeksfortest
geeikistest geeksforgeeks geeksfortest
geeikistest
0
0
Explanation:

By running the query on contact list, we get, 
Suggestions based on "g" are: 
geeikistest geeksforgeeks geeksfortest 
Suggestions based on "ge" are:
geeikistest geeksforgeeks geeksfortest
Suggestions based on "gee" are:
geeikistest geeksforgeeks geeksfortest
Suggestions based on "geei" are:
geeikistest
No Results Found for "geeip", So print "0".
No Results Found for "geeips", So print "0".   
'''

for _ in range(int(input())):
    n = int(input())
    arr1 = input().split()
    cmp = input().strip()
    
    for i in range(1,len(cmp)+1):
        out = []
        for j in arr1:
            if j.startswith(cmp[0:i]):
                out.append(j)
        out = list(set(out))
        out.sort()
        if len(out)>0:
            print(" ".join(out))
        else:
            print ('0')
        
