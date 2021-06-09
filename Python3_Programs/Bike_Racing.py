# -*- coding: utf-8 -*-
'''
A Bike race is to be organized. There will be N bikers. You are given initial Speed of the ith Biker by Hi and the Acceleration of ith biker as Ai KiloMeters per Hour.

The organizers want the safety of the bikers and the viewers.They monitor the Total Speed on the racing track after every Hour.
A biker whose Speed is 'L' or more, is considered a Fast Biker.
To Calculate the Total speed on the track- They Add the speed of each Fast biker ,at that Hour. 
As soon as The total speed on the track is 'M' KiloMeters per Hour or more, The safety Alarm buzzes.
You need to tell what is the minimum number of Hours after which the safety alarm will buzz.

Input:
The first Line contains T- denoting the number of test cases.
The first line of each test case contains three space-separated integers N, M and L denoting the number of bikers and speed limit of the track respectively, and A fast Biker's Minimum Speed. 
Each of next N lines contains two space-separated integers denoting Hi and Ai respectively.

Output:
For each test case-Output a single integer denoting the minimum number of Hours after which alarm buzzes.

Constraints:
1<=T<=100
1<=N<=1e5
1 ≤ M,L ≤ 1e10
1 ≤ Hi, Ai ≤ 1e9

Explanation:
Sample Input:
1
3 400 120
20 20
50 70
20 90

Sample Output:
3

Explanation:
Speeds of all the Bikers at ith Minute
Biker1= 20 40 60 80 100 120 
Biker2= 50 120 190 260 330
Biker3= 20 110 200 290 380 

Total Initial speeds = 0 (Because none of the biker's speed is fast enough)
total Speed at 1st Hour= 120
total Speed at 2nd Hour= 190+200=390
total Speed at 3rd Hour= 260+290=550
Alarm will buzz at 3rd Hour.

'''

#code
import math
def f(u_a,t):
    v = u_a[0] + u_a[1]*t
    return v

for _ in range(int(input())):
    N_M_L = list(map(int,input().split()))
    threshold = N_M_L[-1]
    i_a = []
    t = []
    for i in range(N_M_L[0]):
        i_a.append(list(map(int,input().split())))
        t.append(math.ceil((threshold - i_a[-1][0])/i_a[-1][1]))
    start_time = min(t)
    print(t)
    while True:
        stack = []
        if start_time >= max(t):
            print('here')
            print(math.ceil((N_M_L[1]-sum([i[0] for i in i_a]))/sum([i[1] for i in i_a])))
            break
        else:
            for i in range(N_M_L[0]):
                if start_time >= t[i]:
                    stack.append(f(i_a[i],start_time))
            
        #operation
        if sum(stack) >= N_M_L[1]:
            print(start_time)
            break
        start_time+=1
    
