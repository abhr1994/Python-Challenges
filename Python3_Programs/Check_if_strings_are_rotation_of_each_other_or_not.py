'''
Given strings s1 and s2, you need to find if s2 is a rotated version of the string s1. The strings are lowercase.

Input:
The first line of the input contains a single integer T, denoting the number of test cases. Then T test case follows. Each testcase contains two lines for s1 and s2.

Output:
For each testcase, you need to print 1 if s2 is a rotated version of s1; else print 0.

Constraints:
1<=T<=100
1<=|s1|,|s2|<=100

Example:

Input:
4
geeksforgeeks
forgeeksgeeks
mightandmagic
andmagicmigth
mushroomkingdom
itsamemario
geekofgeeks
geeksgeekof

Output:
1
0
0
1

Explanation:
For testcase 1: s1 is geeksforgeeks, s2 is forgeeksgeeks. Clearly, s2 is a rotated version of s1 as s2 can be obtained by left-rotating s1 by 5 units.
'''
#code
for _ in range(int(input())):
    s1 = input()
    s2 = input()
    t = s2
    i=1
    if s1 == s2:
        print('1')
        continue
    while i<=len(s2)-1:
        t = t[1:]+t[0]
        if s1 == t:
            print('1')
            break
        i+=1
    else:
        print('0')
