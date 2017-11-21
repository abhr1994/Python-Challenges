import sys
##l=['a','b','c','a','b','c']
#l=['a','b','c']
#l=['a','b','c','a','b']
l=['a','a','a']

for i,j in enumerate(l[:]):
    l1=l[:]
    l1.remove(l[i])
    if not(j in l1):
        print j
        sys.exit()

