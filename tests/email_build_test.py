from email.message import EmailMessage
from pprint import pprint
import sys

subject_line = 'This is the subject line'
sent_to      = 'to@email.com'
sent_from    = 'from@email.com'
body         = 'This is the text of the email.'

msg = EmailMessage()
msg.set_content(body)
for k, v in zip(['Subject', 'To', 'From'], [subject_line, sent_to, sent_from]):
    msg[k] = v


'''
richest = msg.get_body()
partfiles = {}
if richest['content-type'].maintype == 'text':
    if richest['content-type'].subtype == 'plain':
        for line in richest.get_content().splitlines():
            print(line)
        print(msg.items())
        sys.exit()
    elif richest['content-type'].subtype == 'html':
        body = richest
    else:
        print("Don't know how to display {}".format(richest.get_content_type()))
        sys.exit()
else:
    print("Don't know how to display {}".format(richest.get_content_type()))
    sys.exit()
'''

for line in msg.walk():
    print(line)

print(msg['To'])
print(msg['From'])
print(msg['Subject'])
