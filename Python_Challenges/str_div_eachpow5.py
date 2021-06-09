##Logic used:
##Input the string
##Define a function which says whether decimal is power of 5 or not
##Functon 'f' is called repetively and if any part of input is found to be power
##of 5 it is appended to the list
##Now the same procedure is repeated with remaining part of the input by subtracting
##the items in list from the input.
##The contents of list will have the required output

import math
l=[]
str_bytes = raw_input("Enter the string of bits: ")
temp = str_bytes
temp1=temp
lis_item = ""
count = 0
def f(string):
    i = len(string)
    a = int(string,2)
    d = math.log(a)/math.log(5)
    if d == int(d):
        print "The number is ",d,"th power of 5"
        l.append(string)
    else:
        print a," is not a power of 5"
        f(temp[0:i-1])
        
while temp1 != "":
    count = count + 1
    print count
    f(temp1)
    if len(l)==0:
        break
    x = lis_item
    lis_item = ''.join(l)
    temp1 = temp1[len(lis_item):len(temp1)]
    if x == lis_item :
        break

##To convert decimal to binary
##l=[]
##x=26
##conv=""
##remainder = 1
##while x>1:
##	remainder = x%2
##	x=x/2
##	l.append(remainder)
##l.append(1)
##for i in reversed(l):
##    conv=conv+str(i)
##
##print conv
