'''
https://practice.geeksforgeeks.org/problems/first-non-repeating-character-in-a-stream/0

Given an input stream of n characters consisting only of small case alphabets the task is to find the first non repeating character each time a character is inserted to the stream.

Example

Flow in stream : a, a, b, c
a goes to stream : 1st non repeating element a (a)
a goes to stream : no non repeating element -1 (5, 15)
b goes to stream : 1st non repeating element is b (a, a, b)
c goes to stream : 1st non repeating element is b (a, a, b, c)

Input:
The first line of input contains an integer T denoting the no of test cases. Then T test cases follow. Each test case contains an integer N denoting the size of the stream. Then in the next line are x characters which are inserted to the stream.

Output:
For each test case in a new line print the first non repeating elements separated by spaces present in the stream at every instinct when a character is added to the stream, if no such element is present print -1.

Constraints:
1<=T<=200
1<=N<=500

Example:
Input:
2
4
a a b c
3
a a c 
Output:
a -1 b b
a -1 c
 
'''
def non_rep(arr):
    l=[]
    for i in arr:
        if i not in l:
            if arr.count(i)==1:
                return i
            else:
                l.append(i)
    return '-1'
for _ in range(int(input())):
    n = int(input())
    out = []
    inp = input().split()
    for i in range(1,n+1):
        out.append(non_rep(inp[0:i]))
    
    print(" ".join(out))
