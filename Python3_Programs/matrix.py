n=4
n1=5
l=[[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]
l1=[[1,2,3,4,5],[6,7,8,9,10],[11,12,13,14,15],[16,17,18,19,20],[21,22,23,24,25]]
def matrix_to_list(l,n):
    lis = []
    for i in range(n//2):
        if i == 0:
            top=l[i][i:]
            right=[]
            left=[]
            for j in range(i+1,n-i-1):
                right.append(l[j][-(i+1)])
                left.append(l[j][i])
            bottom=l[-(i+1)][::-1]
            lis.append(top+right+bottom+left[::-1])
        else:
            top=l[i][i:-i]
            right=[]
            left=[]
            for j in range(i+1,n-i-1):
                right.append(l[j][-(i+1)])
                left.append(l[j][i])
            bottom=l[-(i+1)][i:-i][::-1]
            lis.append(top+right+bottom+left[::-1])
    return lis

def rotate(lis,t):
    for _ in range(t):
        for i in lis:
            i.insert(0,i.pop())
    return lis

def list_to_matrix(lis,n):
    out = []
    for i in range(n):
        out.append([None]*n)
    for i in range(n//2):
        cur = lis[i]
        num_rows_bet = (n-i-1) - i - 1
        mid = []
        for j in range(num_rows_bet):
            mid.append(i+j+1)
        rows = [i]*(n-2*i) + mid + [(n-i-1)]*(n-2*i) +  list(reversed(mid))
        top_col = list(range(i,n-i))
        columns = top_col + [n-i-1] * num_rows_bet + list(reversed(top_col)) + [i]*num_rows_bet
        t = 0
        for l,m in zip(rows,columns):
            out[l][m] = cur[t]
            t+=1
    return out

r = 2
out = list_to_matrix(rotate(matrix_to_list(l1,n1),r),n1)
if n1&1 == 1:
    out[n//2][n//2] = l1[n//2][n//2]

for row in l1:
    print(" ".join(map(str,row)))
print("\nAFTER "+str(r)+" ROTATION\n")
for row in out:
    print(" ".join(map(str,row)))
