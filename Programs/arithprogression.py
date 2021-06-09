##import itertools
##T = input()
##for _ in range(int(T)):
##    entries = list(map(int,input().split()))
##    n1,n2,n = entries[0],entries[1],entries[2]
##    arr = []
##
##    for i in range(1,n+1):
##        num,x=[],0
##        if i == 1:
##            arr.append(i)
##            continue
##        l = [j for j in range(1,i) if j<i]
##
##        j_k_list = list(itertools.product(l,repeat = 2))
##        for j_k in j_k_list:
##            j = j_k[0]
##            k = j_k[1]
##            num.append((n1 * arr[k-1]) - (n2 * arr[j-1]))
##        x = arr[i-2]+1
##        while(x in num):
##            x = x + 1
##        arr.append(x)
##
##    print(" ".join(list(map(str,arr))))




##http://practice.geeksforgeeks.org/problems/arithmetic-progression/0
##Construct the sequence arr[1], arr[2], ... by the following rules. For i=1 we put arr[1]=1. Now let i >= 2. Then arr[i] is the least positive integer such that the following two conditions hold
##(i) arr[i] > arr[i - 1];
##(ii) for all k, j < i we have arr[i] is not equal to n1 * arr[k] - n2 * arr[j].
##Find the first n terms of this sequence.

def addrestricted(n,out,n1,n2,newadded):
    global restrict
    for i in out:
        r1 = n1*newadded -n2*i
        if((r1 > newadded) ):
            restrict[r1] = True
        r2 = n1*i -n2*newadded
        if((r2 > newadded)):
            restrict[r2] = True
    
t = int(raw_input().strip())
while(t>0):
    t = t-1
    [n1,n2,n] = [int(x) for x in (raw_input().strip()).split(' ')]
    out = [1]
    restrict = {}
    restrict[n1-n2]  =  True
    for i in range(0, n-1):
        newpossible = out[len(out)-1] + 1
        while(True):
            if(newpossible in restrict):
                newpossible = newpossible + 1 
            else:
                out = out + [newpossible]
                break
        newadded = newpossible
        addrestricted(n,out,n1,n2,newadded)
    for j in out:
        print j,
    print ""
