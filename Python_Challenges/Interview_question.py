##Given an input stream of n characters consisting only of small case alphabets the task is to find the first non repeating character each time a character is inserted to the stream.
##
##Example
##
##Flow in stream : a, a, b, c
##a goes to stream : 1st non repeating element a (a)
##a goes to stream : no non repeating element -1 (5, 15)
##b goes to stream : 1st non repeating element is b (a, a, b)
##c goes to stream : 1st non repeating element is b (a, a, b, c)

import re
def non_rep(inp):
    l=[]
    lis=[]
    for i in inp:
        if i not in l:
            l.append(i)

    for i in l:
        j=i+'+'
        m=re.search(j,inp)
        lis.append(m.group(0))

    for element in lis:
        if len(element)==1:
            break
    else:
        return -1

    return element


##def rep(inp):
##	l=[]
##	for i in inp:
##		if i not in l:
##			l.append(i)
##		else:
##			l.remove(i)
##	return l

inp_main = raw_input("Enter the stream: ")
l_abhi=[]
for i in inp_main:
    if len(l_abhi) == 0:
        l_abhi.append(i)
        print i
    else:
        l_abhi.append(i)
        out = non_rep(''.join(l_abhi))
        print out
