import test
import texttable as tt
string = ""
count = 0
row=[]
parser = test.MyHTMLParser()
f= open('C:/Users/abhr/Desktop/test.txt','r')
for line in f:
    string = string + line
#parser.feed('<p /><table width="1994" cellspacing="1" cellpadding="0" height="2809" border="1"> <tbody><tr><th>Server</th><th>ACSLS</th><th>Library</th><th>Data Centre</th><th>Quad/Zone</th><th>Environment Supported</th><th>Archive Server</th><th colspan="2">Media Server</th></tr> <tr><td><a href="https://" target="_top">adc07osbadm03</a></td><td>adc-acsls2</td><td>ADC-SL3K02</td><td>ADC</td><td>Zone07</td><td><p />On Demand- RMAN/NDMP (Netapp) adc07ntap05/06/07/08/09/10/11/12/13/14/15/16/<p />adc07ntap21/22/23/24/25/26/27/28/29/30/31/32/33/34/35/36/37/38</td><td>adc07osbmed304</td><td colspan="2">adc07osbmed301, adc07osbmed302 , adc07osbmed303, adc07osbmed304</td></tr> <tr>')
parser.feed(string)
l=test.l



s=' '.join(l)
m=s.split('td')
n=m[1:]
for i in n[:]:
   if (i.isspace()) or (i == ''):
      n.remove(i)


tab=tt.Texttable()
header=['Server','ACSL5','Library','Data Center','Quad/Zone','Environment Supported','Archive Server','Media Server']
tab.header(header)

for j in n:
    count = count + 1
    if count <= 8:
        row.append(j)
    else:
        print len(row)
        print row
        tab.add_row(row)
        row=[j]
        count=1

tab.set_cols_width([18,35,15])
tab.set_deco(tab.HEADER | tab.VLINES)
tab.set_chars(['-','|','+','#'])
tab.set_cols_align(['r','r','r'])
s=tab.draw()
print s


###U r removing blank spaces..Hence the problem of seperation by 8
