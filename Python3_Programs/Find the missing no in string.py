'''
Given a string consisting of some numbers, not separated by any separator. The numbers are positive integers and the sequence increases by one at each number except the missing number. The task is to complete the function missingNumber which return's the missing number. The numbers will have no more than six digits. Print -1 if input sequence is not valid.

Note: Its is guaranteed that if the string is valid, then it is sure that atleast one number would be missing from the string.

Input:
The first line of input contains an integer T denoting the no of test cases. Then T test cases follow. Each test case contains an string s representing a number.

Output:
For each test case in a new line output will be the missing number. Output will be -1 if the input is invalid.

Constraints:
1<=T<=100
1<=Length of string<=100

Example(To be used only for expected output):
Input:
2
9899100102
1112141519

Output:
101
-1
'''
import sys
#string="98100101103"
#string="9101214"
#string="123457891011121516171820"
string='12345678910111213141516171920212223242526272829303132333435363738394041424344454647484950515253545556'
miss=[]
for i in range(1,7):
    first = int(string[0:i])
    second = first + 1
    third = first + 2
    if string.startswith((str(first)+str(second))) or string.startswith((str(first)+str(third))):
        #print(first)
        break
else:
    print ('-1')
    sys.exit()

iprev = 0
inext = iprev + len(str(first))
while iprev<=len(string)-1:
    #print(first,iprev,inext)
    if str(first) == string[iprev:inext]:
        first+=1
        iprev = inext
        inext = iprev + len(str(first))
    else:
	#print(str(first),string[iprev:inext])
        #print ("Missing: ",first)
        miss.append(first)
        first+=1
        inext=iprev+len(str(first))
        
print(miss)
