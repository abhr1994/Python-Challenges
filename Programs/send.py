#!/usr/bin/python

def sendmail(day):
    l_empl=[]
    l_shift=[]
    f = open('rota','r')
    for line in f:
        if 'Name' not in line and 'Days' not in line :
            l_empl.append(line.split()[0])
            l_shift.append(line.split()[int(day)+1])

    fromaddr = 'donotreply@oracle.com'
    bcc = ['abhishek.r@oracle.com']
    message_text = "Hi,\n Your tommorrow's shift is mentioned in the subject line.\n \n\n\tNote: This is an Auto-Generated mail, DO NOT reply"
    for emp,shift in zip(l_empl,l_shift):
        toaddr = 'abhishek.r@oracle.com'
        message_subject = shift+' shift tomorrow'
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


