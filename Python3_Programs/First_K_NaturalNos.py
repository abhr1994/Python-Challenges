##Given an array of size n and a number k, we need to print first k natural numbers that are not there in given array.
##
##Input:
##First line consists of T test case. First line of every test case consists of N and K. Second line consists of elements of array.
##
##Output:
##Single line output, print the K missing numbers.
##
##Constraints:
##1<=T<=100
##1<=N<=10^4
##-1000<=Ai<=1000
##
##Example:
##Input:
##2
##3 3
##1 4 3
##3 3
##-5 -6 1
##Output:
##2 5 6 
##2 3 4 

def read_record():
    return map(int, input().split())

for _ in range(int(input())):
    n, k = read_record()
    missing = set(range(1, n + k + 1))
    missing.difference_update(read_record())
    print(*sorted(missing)[:k])

	
	
	###OR####
T = input()
for _ in range(int(T)):
    inp = input()
    n = int(inp.split()[0])
    k = int(inp.split()[1])
    arr = input().split()
    l = []
    i = 0
    while len(l)!=k:
        i = i+1
        if str(i) not in arr:
            l.append(str(i))
    
    print(' '.join(l))
