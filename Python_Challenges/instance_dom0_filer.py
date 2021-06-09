#!/usr/bin/python
import sys,re,os
vm_name=sys.argv[1]
value=""
a=re.compile=('(\(|\'|\,|\)|:|\/|_)')
f=open("/storadmin/storage/sundar/mount.txt").readlines()
for line in f:
        if vm_name in line:
                line1=re.sub(a,' ',line)
                value+='\n'+" ".join([line1.strip().split()[x] for x in 1,3])

f=os.popen('/usr/local/git/bin/host-group -Field=physical_host'+' '+vm_name).read()
print vm_name,f
print value
