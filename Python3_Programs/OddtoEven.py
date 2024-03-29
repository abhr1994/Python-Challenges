##Given an odd number in the form of string, the task is to make largest even number possible from the given number provided one is allowed to do only one swap operation, if no such number is possible then print the input string itself.
##
##Examples:
##
##Input : 1235785
##Output :1535782
##Swap 2 and 5.
##Input:
##Thr first line of the input contains a single integer T, denoting the number of test cases. Then T test case follows, the only line of the input contains an odd number in the form of string.
##
##Output:
##For each test case print the largest possible even number that could be formed by using one swap operation only.
##
##Constraints:
##1<=T<=100
##1<=N<=106
##
##Example:
##Input:
##3
##789
##536425
##1356425
##Output:
##798
##536524
##1356524


T=int(input())
for _ in range(T):
    inp = input().strip()
    indices = [i for i,j in enumerate(inp) if int(j)%2==0]
    if len(indices)==0:
        print(inp)
    else:
        print (max([int(inp[:index]+inp[-1]+inp[index+1:-1]+inp[index])for index in indices]))
