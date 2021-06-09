for _ in range(int(input())):
    N = int(input())
    arr = list(map(int,input().split()))
    cost = int(input())
    amount = 0
    total = 0
    arr.insert(0,0)
    for i in range(len(arr)-1):
        if arr[i]>arr[i+1]:
            print('great')
            diff = arr[i] - arr[i+1]
            total = total + diff
        if arr[i]<arr[i+1]:
            print('less')
            diff = arr[i+1]-arr[i]
            if total<diff:
                amount = amount + (diff-total)*cost
                total = diff
            else:
                total = total - diff
        if arr[i]==arr[i+1]:
            pass
        print(i,amount)
    
