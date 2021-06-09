#http://practice.geeksforgeeks.org/problems/maximum-rectangular-area-in-a-histogram/0
##Find the largest rectangular area possible in a given histogram where the largest rectangle can be made of a number of contiguous bars. For simplicity,
##assume that all bars have same width and the width is 1 unit.


t = int(input())

for _ in range(t):
    
    n = int(input())
    a = list(map(int,input().split()))
    
    maxArea = 0
    for i in range(n):
        length = 1
        width = a[i]
        
        #print "width",width
        for j in range(i-1,-1,-1):
            
            if a[j] < width:
                break
            
            length += 1
        
        for j in range(i+1,n):
            
            if a[j] < width:
                break
            
            length += 1
            
        #print "length",length    
        if width * length > maxArea:
            maxArea = width * length    
            
    print(maxArea)        
            
            
            
#########################################
##T=int(input())
##for case in range(T):
##    n=int(input())
##    a=list(map(int,input().strip().split()))
##    s,i,ans=[],0,0
##    while i<n or len(s)>0:
##        if i<n and (len(s)==0 or a[i]>=a[s[-1]]):
##            s.append(i)
##            i=i+1
##        else:
##            top=s.pop()
##            if len(s)==0:
##                ans=max(ans,a[top]*i)
##            else:
##                ans=max(ans,a[top]*(i-s[-1]-1))
##    print(ans)
##


