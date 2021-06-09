##http://practice.geeksforgeeks.org/problems/kadanes-algorithm/0
##Given an array containing both negative and positive integers. Find the contiguous sub-array with maximum sum.
## 
##Input:
##The first line of input contains an integer T denoting the number of test cases. The description of T test cases follows. The first line of each test case contains a single integer N denoting the size of array. The second line contains N space-separated integers A1, A2, ..., AN denoting the elements of the array.
## 
##Output:
##Print the maximum sum of the contiguous sub-array in a separate line for each test case.

##inp = raw_input("Enter the list: ")
##arr = list(map(int,inp.split()))
##tot = 0
##d={}
##l=[]
##for i in range(1,len(arr)+1):
##    sum_temp = sum(arr[0:i])
##    d[sum_temp] = i
##    l.append(sum_temp)
##
##l.sort(reverse=True)
##i = d[l[0]]
##arr = list(map(str,arr))
##print " ".join(arr[0:i])
    
      
def kadane(arr):
    max_c=max_g=arr[0]
    for i in range(1,len(arr)):
        max_c=max(arr[i],max_c+arr[i])
        if max_c>max_g:
            max_g=max_c
    return max_g
t=int(input())
while(t!=0):
    n=int(input())
    ar=list(map(int,input().strip().split(' ')))
    k=kadane(ar)
    print(k)
    t=t-1
