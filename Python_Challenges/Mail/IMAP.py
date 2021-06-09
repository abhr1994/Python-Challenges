import imapclient
import pyzmail
imapObj = imapclient.IMAPClient('imap.gmail.com', ssl=True)
imapObj.login(' chokkadibhat@gmail.com ', ' abhI$hek15 ')
imapObj.select_folder('INBOX', readonly=True)
UIDs = imapObj.search(['SINCE 05-Jul-2014'])
#UIDs have list of message ID
rawMessages = imapObj.fetch([40041], ['BODY[]', 'FLAGS'])
message = pyzmail.PyzMessage.factory(rawMessages[40041]['BODY[]'])
message.get_subject()
message.text_part.get_payload().decode(message.text_part.charset)
imapObj.logout()
