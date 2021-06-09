##100 people are standing in a circle with gun in their hands.
##1 kills 2, 3 kills 4, 5 kills 6 and so on till we are
##left with only one person. Who will be the last person alive?
##Write code to implement this ##efficiently.## <-[ Python is not efficient]

def kill(n):
    persons = list(range(1,n+1))
    while (len(persons)>1):
        if len(persons)%2==0:
            persons=persons[::2]
        else:
            persons = persons[2::2]
        
    return persons[0]

print kill(100)
