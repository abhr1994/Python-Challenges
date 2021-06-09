##Given a dictionary, a method to do lookup in dictionary and a M x N board where every cell has one character. Find all possible words that can be formed by a sequence of adjacent characters. Note that we can move to any of 8 adjacent characters, but a word should not have multiple instances of same cell.
##
##Example:
##
##Input: dictionary[] = {"GEEKS", "FOR", "QUIZ", "GO"};
##       boggle[][]   = {{'G','I','Z'},
##                       {'U','E','K'},
##                       {'Q','S','E'}};
##
##Output:  Following words of dictionary are present
##         GEEKS, QUIZ

l=["GO","GEEKS", "FOR", "QUIZ"]
d={'G':1,'E':2,'K':1,'S':1,'Q':1,'U':1,'I':1,'Z':1,'O':1}

for element in l:
    string = ""
    d1 = d.copy()
    for i in element:
        try:
            if d1[i]>0:
                string = string + i
                d1[i]=d1.get(i) - 1
        except KeyError:
            break
    if string == element:
        print element," can be formed!!!"
        d = d1.copy()
