#!/usr/bin/python
a=open("/storadmin/storage/sundar/mount.txt", 'r')
d=list(a)
i=0
c=open("test1", 'r')
b=list(c)
values=[x for x in d if any(y.strip() in x for y in b)]
for x in values:
        print x.strip()
