##Given an array. The task is to arrange the array such that odd elements occupy the odd positions and even elements occupy the even positions. The order of elements must remain same. Consider zero-based indexing. After printing according to conditions, if remaining, print the remaining elements as it is.
##
##Input:
##The first line of input contains an integer T denoting the number of test cases. Then T test cases follow. Each test case consists of two lines. First line of each test case contains an Integer N denoting size of array and the second line contains N space separated elements.
##
##Output:
##For each test case, in a new line print the arranged array.
##
##Constraints:
##1<=T<=100
##1<=N<=105
##1<=A[i]<=105
##
##Example:
##Input:
##2
##6
##1 2 3 4 5 6
##4
##3 2 4 1
##Output:
##2 1 4 3 6 5
##2 3 4 1

T=int(input())
for _ in range(T):
    N = int(input())
    l = input().strip().split()
    out = []
    odd=[i for i in l if int(i)&1]
    even=[i for i in l if not int(i)&1]

    for j,k in zip(even,odd):
        out.append(j)
        out.append(k)

    if len(even)>len(odd):
        out.append(even[-1])

    if len(odd)>len(even):
        out.append(odd[-1])
        
    print(' '.join(out))
