'''
1


2 2 2
2 1 2
2 2 2


3 3 3 3 3
3 2 2 2 3
3 2 1 2 3
3 2 2 2 3
3 3 3 3 3


4 4 4 4 4 4 4
4 3 3 3 3 3 4
4 3 2 2 2 3 4
4 3 2 1 2 3 4
4 3 2 2 2 3 4
4 3 3 3 3 3 4
4 4 4 4 4 4 4


5 5 5 5 5 5 5 5 5
5 4 4 4 4 4 4 4 5
5 4 3 3 3 3 3 4 5
5 4 3 2 2 2 3 4 5
5 4 3 2 1 2 3 4 5
5 4 3 2 2 2 3 4 5
5 4 3 3 3 3 3 4 5
5 4 4 4 4 4 4 4 5
5 5 5 5 5 5 5 5 5

'''


for n in range(1,10):
    l = []
    for i in range(1,n+1):
        if i == 1:
            l.append([1])
        else:
            length = len(l[0]) + 2
            for item in l:
                item.append(i)
                item.insert(0,i)
            temp = [i]*length
            l.insert(0,temp)
            l.append(temp[:])

            
    for j in l:
        t = list(map(str,j))
        print(" ".join(t))
    print('\n')
