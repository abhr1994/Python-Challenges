import sys
#l = raw_input("Enter the list: ")
l=['1', '3', '5', '4', '3', '4', '6', '7', '6', '8', '9']
count = 0
jump = int(l[0])
reached = l.index(str(jump)) + 1
while not (reached >= len(l)):
    temp = []
    old=str(jump)
    for i in range(jump):
        try:
            temp.append(l[l.index(str(jump))+i+1])
        except IndexError:
            count = count + 1
            print count
            sys.exit()
    jump = int(max(temp))
    reached = l.index(str(jump)) + 1
    count = count+1
    print old,':',str(jump)
print count
