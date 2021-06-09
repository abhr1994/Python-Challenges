##
##Given a array of n strings, find the longest common prefix among all strings present in the array.
##
##Input:
##The first line of the input contains an integer T which denotes the number of test cases to follow. Each test case contains an integer n. Next line has space separated n strings. 
##
##Output:
##Print the longest common prefix as a string in the given array. If no such prefix exists print "-1"(without quotes).

T = input()
for i in range(int(T)):
    N = int(input())
    arr = input().strip().split()
    arr.sort(key=lambda x:len(x))
    ref=arr[0]
    if len(ref)==1:
        start = 1
        end = 0
    else:
        start = len(ref)
        end = 1

    for i in range(start,end,-1):
        for element in arr[1:]:
            if not element.startswith(ref[:i]):
                break
        else:
            print(ref[:i])
            break
    else:
        print("-1")
