####Given a linked list, the task is to complete the function maxPalindrome
##which returns an integer denoting  the length of the longest palindrome
##list that exist in the given linked list.
####
####Examples:
####
####Input  : List = 2->3->7->3->2->12->24
####Output : 5
####The longest palindrome list is 2->3->7->3->2
####
####Input  : List = 12->4->4->3->14
####Output : 2
####The longest palindrome list is 4->4
##
output=[]
def palindrome(l):
    count = 0
    for i in range(len(l)/2):
        if l[i] == l[-(i+1)]:
            count+=1
    if count == len(l)/2:
        output.append(l)

##list = [2,3,7,3,2,12,24]
list=[12,4,4,3,14]
for i in range(len(list)):
    for j in range(i+1,len(list)+1):
        if len(list[i:j])>1:
            palindrome(list[i:j])

print sorted(output,key=lambda x:len(x),reverse=True)
