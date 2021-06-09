import smtplib
d={}
f = open("file.txt","r")
for line in f:
    l = line.split('~~')
    d[l[0]]=l[1]


def f(mail,inc):
    toaddr = mail
    bcc = ['abhishek.r@oracle.com']
    fromaddr = 'donotreply@oracle.com'
    message_subject = "Please clear the incidents in your name"
    message_text = "Hi, Please solve the incidents which you have owned\n\n"+inc+"\n\nNote: This is an Auto-Generated mail, DO NOT reply. \nThanks,\nOMCS Team."
    message = "From: %s\r\n" % fromaddr + "To: %s\r\n" % toaddr + "Subject: %s\r\n" % message_subject + "\r\n" + message_text
    toaddrs = [toaddr] +  bcc
    try:    
        server = smtplib.SMTP('localhost')
        #server.set_debuglevel(1)
        server.sendmail(fromaddr, toaddrs, message)
        print "Successfully sent email"
    except smtplib.SMTPException:
        print "Error: unable to send email"
    
        server.quit()

key = d.keys()
value = d.values()
for i,j in zip(key,value):
    f(i,j)

