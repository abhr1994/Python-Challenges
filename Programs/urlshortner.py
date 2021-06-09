# -*- coding: utf-8 -*-
##Design a system that takes big URLs like “http://www.geeksforgeeks.org/count-sum-of-digits-in-numbers-from-1-to-n/” and converts them into a short 6 character URL. It is given that URLs are stored in database and every URL has an associated integer id.  So your program should take an integer id and generate a 6 character long URL. 
##
##A URL character can be one of the following
##1) A lower case alphabet [‘a’ to ‘z’], total 26 characters
##2) An upper case alphabet [‘A’ to ‘Z’], total 26 characters
##3) A digit [‘0′ to ‘9’], total 10 characters
##
##There are total 26 + 26 + 10 = 62 possible characters.
##
##So the task is to convert an integer (database id) to a base 62 number where digits of 62 base are "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
##
##Input:
##
##The first line of input contains an integer T denoting the number of test cases.
##
##And the second line consists of a long integer.
##
##Input:
##
##1
##12345
##
##Output:
##
##dnh
##12345



a="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
def base_62(num):
    l=[]
    i=63
    while i > 62:
        div = num/62
        rem = num%62
        num = div
        l.append(rem)
        i=div
    l.append(i)
    return l

l = base_62(12345)
for i in l[::-1]:
    print a[int(i)],
