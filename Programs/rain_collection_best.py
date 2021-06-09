t=int(input())
while(t!=0):
    n=int(input())
    arr=list(map(int,input().strip().split(' ')))
    sum=0
    for i in range(1,n-1):
        a=max(arr[0:i])
        b=max(arr[i+1:n])
        if (min(a,b)-arr[i])>0:
            sum=sum+(min(a,b)-arr[i])
    print(sum)
    t=t-1
