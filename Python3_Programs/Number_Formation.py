'''
Given three integers x,y and z you need to find the sum of all the numbers formed by 
having 4 atmost x times , having 5 atmost y times and having 6 atmost z times as a digit.

Note : Output the sum modulo 10^9+7.

Input
The first line of input contains of an integer 'T' denoting number of test cases. Then T test cases follow . The first line of each test case contains an three integers x , y and z .

Output:
For each test case print in a new line an integer corresponding to the answer.

Constraints:
1<=t<=50
0<=x,y,z<=100
'''

for _ in range(int(input())):
    out,l = [],[]
    num = [int(i)for i in input().split()]
    lis_four = num[0]*['4']
    lis_five = num[1]*['5']
    lis_six  = num[2]*['6']
    tot = len(lis_four)+len(lis_five)+len(lis_six)
    temp = []
    for i in range(1,tot+1):
        if i == 1:
            if len(lis_four) >=1:
                temp.append('4')
            if len(lis_five) >=1:
                temp.append('5')
            if len(lis_six) >=1:
                temp.append('6')
        else:
            temp1 = temp[:]
            temp = []
            for ele in temp1:
                if len(lis_four)-ele.count('4')-1 >= 0:
                    temp.append(ele+'4')
                if len(lis_five)-ele.count('5')-1 >= 0:
                    temp.append(ele+'5')
                if len(lis_six)-ele.count('6')-1 >= 0:
                    temp.append(ele+'6')
                
                

        for ele in temp:
            #print(ele)
            out.append(int(ele))
    
