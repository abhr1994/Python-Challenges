##Given an odd number in the form of string, the task is to make largest even number possible
##from the given number provided one is allowed to do only one swap operation,
##if no such number is possible then print the input string itself.

for _ in range(int(input())):
    out = []
    even_index = []
    inp = input().strip()
    for j,i in enumerate(inp):
        if int(i)%2==0:
            even_index.append(j)
            
    if len(even_index)==0:
        print(inp)
        continue
    for i in even_index:
        out.append(int(inp[:i]+inp[-1]+inp[i+1:-1]+inp[i]))
    
    out.sort()
    print(out[-1])


##################Other solutions##################
##
##def oddToEven(n):
##    #Finding the even number
##    even = 10
##    index = 7
##    t = list(n)
##    for i in range(len(n)):
##        if int(t[i])%2 == 0:
##            even = int(t[i])
##            index = i
##        if even <= int(t[-1]):
##            break
##    if even == 10:
##        return n
##    try:
##        t[index], t[-1] = t[-1], t[index]
##    except IndexError:
##        return n
##    return ''.join(t)
##            
##            
##        
##n = int(input().strip())
##for i in range(n):
##    even = oddToEven(input().strip())
##    print(even)
