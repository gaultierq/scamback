MAIL_SERVER = "pop.gmail.com"
MAIL_USER = "jacob.carlsenis@gmail.com"
MAIL_PASSWORD = "lEEDVBQw9INa"



import email.header
import imaplib

import MySQLdb

mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login(MAIL_USER, MAIL_PASSWORD)
mail.list()
# Out: list of "folders" aka labels in gmail.
mail.select("inbox") # connect to inbox.

result, data = mail.search(None, "ALL")

ids = data[0]  # data is a list.
print "ids=", ids

id_list = ids.split()  # ids is a space separated string

for num in id_list:

    result, data = mail.fetch(num, "(RFC822)")  # fetch the email body (RFC822) for the given ID

    raw_email = data[0][1]  # here's the body, which is raw text of the whole email
    # including headers and alternate payloads
    # print "email", raw_email

    email_message = email.message_from_string(raw_email)

    # result, data = mail.uid('fetch', uid, '(X-GM-THRID X-GM-MSGID)')

    print "to=", email_message['To']
    print "from=", email.utils.parseaddr(email_message['From'])  # for parsing "Yuji Tomita" <yuji@grovemade.com>
    hdr = email.header.make_header(email.header.decode_header(email_message['Subject']))
    subject = str(hdr)
    print "subject=", subject
    print "all headers=", email_message.items()  # print all headers
    print "\n"

    conn = MySQLdb.connect(host= MYSQL_HOST,
                      user=MYSQL_USERNAME,
                      passwd=MYSQL_PASSWORD,
                      db=MYSQL_DATABASENAME)

    cursor = conn.cursor()

    try:
       cursor.execute("""INSERT INTO mail VALUES (%s,%s)""", (188, 90))
       conn.commit()
    except:
       conn.rollback()

    conn.close()


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