##Given a string without spaces, a character, and a count, the task is to print the string after the specified character has occurred count number of times.
##Print “Empty string” incase of any unsatisfying conditions.
##(Given character is not present, or present but less than given count, or given count completes on last index).
##If given count is 0, then given character doesn’t matter, just print the whole string.
##
## 
##
##Input:
##
##First line consists of T test cases. First line of every test case consists of String S.Second line of every test case consists of a character.Third line of every test case consists of an integer.
##
##
##Output:
##
##Single line output, print the remaining string or "Empty string".
##
##
##Constraints:
##
##1<=T<=200
##1<=|String|<=10000
##
##
##Example:
##
##Input:
##
##2
##Thisisdemostring
##i    
##3​
##geeksforgeeks
##e
##2
##
##Output:
##ng
##ksforgeeks

import re
T=int(input())
for _ in range(T):
    string = input().strip()
    ref = input().strip()
    count = int(input().strip())
    indices = [x.end() for x in re.finditer(ref, string)]
    if count == 0:
        print(string)
    else:
        if (ref not in string) or (count > len(indices)) or (indices[count-1]==len(string)):
            print("Empty string")
        
        else:
            print(string[indices[count-1]:])
