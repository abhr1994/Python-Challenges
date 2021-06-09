#!/usr/bin/python
import re,sys
sticker,name,count=sys.argv[1],sys.argv[2],1
sticker1=sticker
for i in name:
    if i in sticker: sticker = sticker.replace(i, "",1)
    else:
        sticker=sticker+sticker1
        sticker = sticker.replace(i, "",1)
        count+=1
print count

