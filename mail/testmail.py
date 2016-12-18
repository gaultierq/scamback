# MAIL_SERVER = "pop.gmail.com"
import datetime

MAIL_USER = "jacob.carlsenis@gmail.com"
MAIL_PASSWORD = "lEEDVBQw9INa"

import email.header
import imaplib

from testsql import Mail

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(MAIL_USER, MAIL_PASSWORD)
mail.list()

# Out: list of "folders" aka labels in gmail.
mail.select("inbox")  # connect to inbox.

result, data = mail.search(None, "ALL")

ids = data[0]  # data is a list.
print "ids=", ids

id_list = ids.split()  # ids is a space separated string


def readBody():
    if email_message.is_multipart():
        for payload in email_message.get_payload():
            # if payload.is_multipart(): ...
            body = payload.get_payload()
    else:
        body = email_message.get_payload()

    return body


for num in id_list:
    result, data = mail.fetch(num, "(RFC822)")  # fetch the email body (RFC822) for the given ID

    raw_email = data[0][1]  # here's the body, which is raw text of the whole email
    # including headers and alternate payloads
    # print "email", raw_email

    email_message = email.message_from_string(raw_email)

    # print "all headers=", email_message.items()  # print all headers

    date_str = email_message['Date']
    date = None
    if date_str:
        date_tuple = email.utils.parsedate_tz(date_str)
        if date_tuple:
            date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))

    m = Mail(
        uuid=(email_message['Message-ID']),
        subject=(email_message['Subject']),
        from_=(email_message['From']),
        to=(email_message['To']),
        in_reply_to=(email_message['In-Reply-To']),
        references=email_message['References'], # probably gmail specific
        date=date,
        body = readBody()
    )
    # print m
    # print "\n"

    from testsql import insert_mail
    insert_mail(m)

# note that if you want to get text content (body) and the email contains
# multiple payloads (plaintext/ html), you must parse each message separately.
# # use something like the following: (taken from a stackoverflow post)
# def get_first_text_block(self, email_message_instance):
#     maintype = email_message_instance.get_content_maintype()
#     if maintype == 'multipart':
#         for part in email_message_instance.get_payload():
#             if part.get_content_maintype() == 'text':
#                 return part.get_payload()
#     elif maintype == 'text':
#         return email_message_instance.get_payload()



print "finished"
