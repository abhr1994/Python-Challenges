'''
Given a Linked List of integers, write a function to modify the linked list such that all even numbers appear before all the odd numbers in the modified linked list. Also, keep the order of even and odd numbers same.

Input:

The first line of input contains an integer T denoting the number of test cases.
The first line of each test case is N,N is the number of elements in Linked List.
The second line of each test case contains N input,elements in Linked List.

Output:

Print the all even numbers then odd numbers in the modified Linked List.

Constraints:

1 ≤ T ≤ 100
1 ≤ N ≤ 100
1 ≤ size of elements ≤ 1000

Example:

Input
3
7
17 15 8 9 2 4 6
4
1 3 5 7
7
8 12 10 5 4 1 6

Output
8 2 4 6 17 15 9
1 3 5 7
8 12 10 4 6 5 1
'''

#code
for _ in range(int(input())):
    N = int(input())
    arr = list(map(int,input().split()))
    j = 0
    for i in range(N):
        if arr[i]&1==0:
            arr.insert(j,arr.pop(i))
            j+=1
            
    print(' '.join(list(map(str,arr))))



#    even = [i for i in arr if i&1 !=1]
#    odd = [i for i in arr if i&1 ==1]
#    out = even+odd
#    print(' '.join(list(map(str,out))))
