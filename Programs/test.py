##You are given two arrays of numbers. You have to maximize the first array by using the elements from the second array such that the new array formed contains unique elements. For example, let the size of array be 'n'. Then the output should be n greatest but unique elements of both the arrays. The order of elements should be as explained in example below, i.e., giving the second array priority.
##
##Input:
##The first line of each input contains the number of test cases . The description of T test cases follows:
##The first line of each test case contains the size of the array (This is going to be the size of both the arrays).
##The second line of each test case contains the elements of the first array.
##The final line of each test case contains the elements of the second array.
##
##Output:
##Print the maximum elements giving second array higher priority. The order of appearance of elements is kept same in output as in input (See Example for better Understanding).
##
##Input:
##
##2
##5
##7 4 8 0 1
##9 7 2 3 6
##4
##6 7 5 3
##5 6 2 9
##
##Output:
##
##9 7 6 4 8
##5 6 9 7


l = [7, 4, 8, 0, 1]
l1 = [9, 7, 2, 3, 6]

l2 = l+l1

l2.sort(reverse=True)
l3 = list(set(l2))
l3.sort(reverse=True)
l4 = l3[0:len(l)]

for i in l1:
    if i in l4:
        print i,
        l4.remove(i)

for i in l:
    if i in l4:
        print i,
        l4.remove(i)
