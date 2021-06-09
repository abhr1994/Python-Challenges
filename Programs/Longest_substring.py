# -*- coding: cp1252 -*-

##Given two strings ‘X’ and ‘Y’, find the length of the longest common substring.
##
##Examples :
##
##Input : X = "GeeksforGeeks", y = "GeeksQuiz"
##Output : 5
##The longest common substring is "Geeks" and is of
##length 5.
##
##Input : X = "abcdxyz", y = "xyzabcd"
##Output : 4
##The longest common substring is "abcd" and is of
##length 4.
##
##Input : X = "zxabcdezy", y = "yzabcdezx"
##Output : 6
##The longest common substring is "abcdez" and is of
##length 6.
a="ayzabcdbcdxyz"
b="xyzabcd"
##a="abbbcddddfg"
##b="dddddfgabc"
##a='abc'
##b='aqbqc'
##a="GeeksforGeeks"
##b="GeeksQuiz"
l=[]
match=''
flag=0
if len(a)<len(b):
    a,b=b,a

for i in range(len(b)):
    for j in range(i+1,len(b)+1):
        if b[i:j] in a:
            #print b[i:j]
            match = b[i:j]
            flag = 1
        else:
            if flag == 1:
                #print match
                l.append(match)
                flag=0
                break
    else:
        if flag == 1:
            l.append(match)

print sorted(l,key=lambda x:len(x),reverse=True)[0]

        
