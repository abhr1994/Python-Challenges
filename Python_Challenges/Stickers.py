import operator
d={'AAA':'2','AA':'2','A':'4','BB':'2','B':'4','CC':'2','C':'4'}
stickers = 0
a= raw_input("Enter your name: ")
l = list()
j = 0
for i in range(1,len(a)):
    if a[i]==a[i-1]:
        if i == len(a)-1:
            l.append(a[j:len(a)])
    else:
        l.append(a[j:i])
        j=i
        if i == len(a)-1:
            l.append(a[i])
print(l)
a=sorted(d.items(), key=operator.itemgetter(0),reverse=True)
print a
for name in l:
    l=[]
    m=[]
    for i in a:
        if name[0] in i[0]:
            l.append(i[0])
            m.append(i[1])

    tot=0
    length = len(name)
    for k,i in enumerate(l):
        for j in range(int(m[k])):
            if int(m[k]) > 0:
                tot = len(i)*1
                if tot > length:
                    break
                else:
                    print "One ",i," is used"
                    stickers = stickers + 1
                    m[k]=int(m[k])-1
                    length = length - len(i)
                
    if length != 0:
        print "INSUFFICIENT STICKERS"
        sys.exit()

print "The number of stickers used to write the name is: ",stickers
