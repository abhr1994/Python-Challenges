import math,operator
f=open('dataset2.txt','r')
value = f.readline().strip().split(',')
f.close()
name_index=value.index('NAME')
stride_length_index=value.index('STRIDE_LENGTH')

f1=open('dataset1.txt').readlines()
leg_length_index=f1[0].split(',').index('LEG_LENGTH')
d={}
speed_value=0

def speed(STRIDE_LENGTH,LEG_LENGTH):
    g = 9.8
    return ((float(STRIDE_LENGTH)/float(LEG_LENGTH)) - 1) * math.sqrt(float(LEG_LENGTH) * g)

f=open('dataset2.txt','r')
for line in f:
    if 'bipedal' in line:
        for i in f1:
            if line.split(',')[name_index] in i:
                d[line.split(',')[name_index]]=speed(line.split(',')[stride_length_index],i.split(',')[leg_length_index])

lis = sorted(d.items(), key=operator.itemgetter(1),reverse=True)
for i,j in lis:
    print i
