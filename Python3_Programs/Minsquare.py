###code
##Given a paper of size A x B. Task is to cut the paper into squares of any size. Find the minimum number of squares that can be cut from the paper.
##
##Input:
##The first line of input contains an integer T denoting the number of test cases. Then T test cases follow. Each test case contains two integer A and B denoting the two size of the paper.
##
##Output:
##Print the minimum number of squares that can be cut from the paper.
##
##Constraints:
##1<=T<=10^5
##1<=A<=10^5
##1<=B<=10^5
def dp(i,j):
    if i>j: i,j=j,i
    if i==0: return 0
    if (i,j) in memo: return memo[min(i,j),max(i,j)]
    memo[i,j]=min(min(dp(i-x,j)+dp(x,j) for x in range(1,i)),min(dp(i,j-x)+dp(i,x) for x in range(1,j)))
    return memo[i,j]
T=int(input().strip())
memo={}
for _ in range(T):
    m,n=list(map(int,input().strip().split(' ')))
    for p in zip(range(1,n+1),range(1,n+1)): memo[p]=1
    for p in range(1,n+1): memo[1,p]=p
    print(dp(m,n))

	
##m = 3 n =4
{(1, 2): 2, (1, 3): 3, (3, 3): 1, (4, 4): 1, (1, 4): 4, (2, 2): 1, (1, 1): 1}
dp(3,4)
i=3, j=4
if (3,4) in memo: False
memo[3,4]=min( dp(2,4)+dp(1,4)     x in [1,2]  ,    )
