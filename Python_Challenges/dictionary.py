start="sat"
end="pan"
l=['rat','san','ran','dam','pan']
d={}
lis=[]

def mismatch(temp):
    temp_list=[]
    for word in l:
        mismatch = [i for i in xrange(len(word)) if temp[i] != word[i]]
        if len(mismatch)==1:
            temp_list.append(word)
    return temp_list

def f(word):
    lis.append(word)
    temp = mismatch(word)
    #print temp
    d[word]=temp
    if end not in temp:
        for i in temp:
            f(i)
        return
    else:
        lis.append(end)
        return

f(start)
lis.remove(start)
k=0
for j in [i for i in range(len(lis)) if lis[i] == end]:
    print lis[k:j]
    k=j+1
##keys=d.keys()
##values=d.values()
##for i,j in zip(keys,values):
####    if end in j:
##        lis.append(i)
##
##for i,j in zip(keys,values):
    
