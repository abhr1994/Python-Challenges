##Link: http://practice.geeksforgeeks.org/problems/trapping-rain-water/0
##Given n non-negative integers in array representing an elevation map where the width of each bar is 1, compute how much water it is able to trap after raining.
##For example:
##Input:
##3
##2 0 2
##Output:
##2
##Structure is like below
##| |
##|_|
##We can trap 2 units of water in the middle gap.


arr = "8 8 2 4 5 5 1"
#arr = "7 4 0 9"
#arr = "6 9 9"

#make * and . structure for array
l = arr.split()
l = [int(i) for i in l]
l1=l[:]
l1.sort(reverse=True)
max_length = l1[0]
slabs=[]
for i in l:
    if i < max_length:
        stars = ('* '*i).split()
        space = ('~ '*(max_length-i)).split()
        st_sp = stars+space
        slabs.append(st_sp)
    else:
        stars = ('* '*i).split()
        slabs.append(stars)

#For elements from 1:-1, if any slab has . then it means there is space.
#If water needs to filled there then towards left and right there shuld be *
        
count = 0
for k,element in enumerate(slabs):
    if k==0 or k==len(slabs)-1:
        continue
    for i,j in enumerate(element):
        if j != '*':
            #check towards left and right if any block is there. If yes count=count+1
            for slab_left in slabs[0:k]:
                if slab_left[i]=='*':
                    break
            else:
                break

            for slab_right in slabs[k+1:len(slabs)]:
                if slab_right[i]=='*':
                    count+=1
                    break
                
                    

            
