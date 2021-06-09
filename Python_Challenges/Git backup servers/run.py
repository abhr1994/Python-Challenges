import test
import texttable as tt
import sys
import urllib2
count = 0
row = []
string = ""
parser = test.MyHTMLParser()

for line in urllib2.urlopen('http://globaldc-git.oracle.com/perl/twiki/view/Operations/CITBkpSrvrs'):
    string = string + line

##f= open('test1.txt','r')
##for line in f:
##    string = string + line
parser.feed(string)
l=test.l
###############################################################
# List l contains all the tags 'td' and data in between tag 'td'
# From list l extract only data between start and end 'td' tag..List 's' has that
count_1=0
s=[]
flag=0
string=""
z=l[:]
for i in z:
    if i == 'td':
        count_1 = count_1+1
        if count_1 == 2:
            count_1 = 0
            flag = 0
            s.append(string)
            string=""
        else:
            flag = 1
    else:
        if flag==1:
            string=string+i

l1=s[:]

################Collect the indexes which has empty spaces#######################
n=[]
m=[]
flag=0
for j,i in enumerate(l1):
	if i.isspace():
		flag = 1
		m.append(j)
	else:
		if flag == 1:
			n.append(m)
			m=[]
		flag = 0

## n has index of empty spaces in list

# Replace all the consecutive empty spaces with character '-*-*-' and then remove those
for element in n:
	if len(element)>2:
		for i in element:
			l1[i]='-*-*-'

## Now remove those elements with '-*-*-'

##Count number of '-*-*-'and then use l.remove('-*-*-')
toremove=0
for k in l1:
    if k == '-*-*-':
        toremove=toremove+1

for i in range(toremove):
    l1.remove('-*-*-')

for i in l1[:]:
    if i == '\n\n\n\n':
        l1.remove(i)
#######################################

tab=tt.Texttable()
header=['Server','ACSL5','Library','Data Center','Quad/Zone','Environment Supported','Archive Server','Media Server']
tab.header(header)
count=0
enter=0
for j in l1:
    count = count + 1
    if count <= 8:
        row.append(j)
    else:
        #print len(row)
        #enter = enter + 1
        #print enter
        tab.add_row(row)
        row=[j]
        count=1
#tab.add_row(row)
try:
    tab.set_cols_width([18,35,15])
    tab.set_deco(tab.HEADER | tab.VLINES)
    tab.set_chars(['-','|','+','#'])
    tab.set_cols_align(['r','r','r'])
except tt.ArraySizeError:
    s=tab.draw()
print s

#####################################
storage = ""
while storage != 'n':
    storage = raw_input("Please enter the storage name: ")
    if storage == 'n':
        sys.exit()
    for i,element in enumerate(l1):
        if storage[:len(storage)-2] in element:
            if storage[len(storage)-2:len(storage)] in element:
                if (l1[i+1].isspace()) or (l1[i+1] == '---') or (l1[i+1] == 'All media servers'):
                    print "The media server is : ",l1[i+2]
                else:
                    print "The media server is : ",l1[i+1]
                break
    else:
        print "No details found"
        


