'''
Imagine you have a special keyboard with the following keys: 
Key 1:  Prints 'A' on screen
Key 2: (Ctrl-A): Select screen
Key 3: (Ctrl-C): Copy selection to buffer
Key 4: (Ctrl-V): Print buffer on screen appending it
                 after what has already been printed. 

If you can only press the keyboard for N times (with the above four keys), write a program to produce maximum numbers of A's. That is to say, the input parameter is N (No. of keys that you can press), the output is M (No. of As that you can produce).

Input:

The first line of input contains an integer T denoting the number of test cases.
The first line of each test case is N,N is the number of key.

Output:

Print maximum number of A's.  Print -1, if N is greater than 75.

Constraints:

1 ≤ T ≤ 50
1 ≤ N ≤ 75

Example:

Input:
2
3
7

Output:
3
9

Explanation:

Input:  N = 3
Output: 3
We can at most get 3 A's on screen by pressing 
following key sequence.
A, A, A

Input:  N = 7
Output: 9
We can at most get 9 A's on screen by pressing 
following key sequence.
A, A, A, Ctrl A, Ctrl C, Ctrl V, Ctrl V
'''

#Hint: If N=7, Position of ctrl+a, ctrl+c is varied from (5,6)....(2,3)

for t in range(int(input())):
    n=int(input())
    dp=[0 for i in range(n+1)]
    if n<=6:
        print(n)
    elif n<=75:
        for i in range(7):
            dp[i] = i
        for i in range(7, n + 1):
            for b in range(i - 3, 0, -1):
                dp[i] = max(dp[i], (i - b - 1) * dp[b])
        print(dp)
        print(dp[n])
    else:
        print('-1')
