d = {'1':'one','2':'two','3':'three','4':'four','5':'five','6':'six','7':'seven','8':'eight','9':'nine','10':'ten','11':'eleven','12':'twelve','13':'thirteen','14':'fourteen','15':'fifteen','16':'sixteen','17':'seventeen','18':'eighteen','19':'nineteen','20':'twenty','30':'thirty','40':'fourty','50':'fivety','60':'sixty','70':'seventy','80':'eighty','90':'ninety'}

l = ['thousand','hundred']
number = ""

while number != 'x':
    number = raw_input('\nEnter the number (press x to exit): ')
    if number == 'x':
        break
    output=""
    for i,j in enumerate(number[0:len(number)-2]):
        if j!='0':
            print d[j],l[i],
        

    count = 0
    for k in number[len(number)-2:len(number)]:
        if number[len(number)-2:len(number)] in d.keys():
            print d[number[len(number)-2:len(number)]],
            break
        if number[len(number)-2:len(number)]=='00':
            break

        if count == 0:
            if k!='0':
                print d[k+'0'],
            count+=1
        else:
            if k!='0':
                print d[k],
    
