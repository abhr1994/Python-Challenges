##Given an array of integers, check whether there is a subsequence with odd sum and if yes, then finding the maximum odd sum. If no subsequence contains odd sum, print -1.
##
##Input:
##First line of input contains a single integer T which denotes the number of test cases. Then T test cases follows. First line of each test case contains a single integer N which denotes the number of elements in the array. Second line of each test case contains N space separated integers.
##
##Output:
##For each test case print the maximum odd sum that can be obtained from any subsequence of the given array. If no subsequence contains odd sum, print -1.

import sys
def findMaxOddSum(array):
  isOdd=0
  
  min_odd=sys.maxsize
  sum=0
  for i in range(0,len(array)):
    if array[i]>0:
      sum+=array[i]
      #print ("element:",array[i],"sum:",sum)
      
    if array[i]%2 != 0:
      isOdd=1
     # print (array[i],"is odd")
      if min_odd>abs(array[i]):
        min_odd=abs(array[i])
        
  if isOdd == 0:
     # print ("not odd")
      return -1
 
  if sum%2 == 0:
      sum-=min_odd
        
  return sum
    
  
    
        
test_cases=int(input())    
while test_cases>0:
    n=int(input())
    array=[int(x) for x in input().split(" ") if x!='']
    val=findMaxOddSum(array)
    print (val)
    test_cases-=1


#######################2nd solution#########################

##cases = int(input())
##for t in range(cases):
##    n = int(input())
##    arr = list(map(int,input().split()))
##    def maxsum():
##        if not any([x&1 for x in arr]):
##            return -1
##        ans = sum([x for x in arr if x>0])
##        if ans&1: return ans
##        return ans-min([abs(x) for x in arr if x&1])
##    print(maxsum())
