import smtplib
smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
##smtpObj = smtplib.SMTP_SSL('smtp.gmail.com', 465) If above fails
smtpObj.ehlo()
smtpObj.starttls()   ##Skip this step if 465 port is used since it is SSL
smtpObj.login(' chokkadibhat@gmail.com ', ' abhI$hek15 ')
smtpObj.sendmail(' chokkadibhat@gmail.com ', ' abhishek.r@oracle.com ',
'Subject: So long.\nDear Alice, so long and thanks for all the fish. Sincerely, Bob')
smtpObj.quit()
