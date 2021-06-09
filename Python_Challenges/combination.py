##import itertools
##
##l = ['a','b','c','d','e']
##for n in range(1,len(l)):
##    for i in itertools.combinations(range(len(l)),n):
##        for k in i:
##            print l[int(k)],
##        print ""
##    print ""
##

global l
l = ['a','b','c','d','e']
global out
out = []
def f(n):
    if n==1:
        out.append(l)
    else:
        temp = []
        try:
            for i in out[n-2]:
                ind = l.index(i[-1])
                if ind<len(l):
                    for j in range(ind+1,len(l)):
                        temp.append(i+l[j])
        except:
            print 'error'
        out.append(temp)
for i in range(1,len(l)+1):
    f(i)

for i in out:
    print " ".join(i)
