# MAIL_SERVER = "pop.gmail.com"
import datetime
import os
import email.header
import imaplib
from app import app
from database import DB
from mail.models import Mail, MailAccount, MailAccountType, insert_mail


ACCOUNTS = None

GMAIL = 1

if __name__ == '__main__':
    app.config.from_object(os.environ['APP_SETTINGS'])
    DB.init_db(app)

    # TODO: store it in db
    account_type = MailAccountType(type=GMAIL, host = 'imap.gmail.com')
    account1 = MailAccount(id = 1, login = "jacob.carlsenis@gmail.com", password = "lEEDVBQw9INa", mail_boxes = "inbox")
    account1.account_type = account_type
    account2 = MailAccount(id = 2, login = "scam.scammers.back@gmail.com", password = "4wqPSyUIA3dB", mail_boxes = "inbox")
    account2.account_type = account_type
    ACCOUNTS = [account1, account2]


def run():
    # accounts = MailAccount.query.all()

    for account in ACCOUNTS:
        try:
            fetch_account(account)
        except:
            print("failed to fetch", account)


def fetch_account(account):
    print("fetching", account)
    mail = imaplib.IMAP4_SSL(account.account_type.host)
    mail.login(account.login, account.password)
    mail.list()
    # Out: list of "folders" aka labels in gmail.
    mail.select(account.mail_boxes)  # connect to inbox.
    result, data = mail.search(None, "ALL")
    ids = data[0]  # data is a list.
    # print("ids=", ids)
    id_list = ids.split()  # ids is a space separated string
    for num in id_list:
        result, data = mail.fetch(num, "(RFC822)")  # fetch the email body (RFC822) for the given ID

        raw_email = data[0][1]  # here's the body, which is raw text of the whole email
        # including headers and alternate payloads
        # print "email", raw_email
        print(raw_email)
        email_message = email.message_from_bytes(raw_email)

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
            references=email_message['References'],  # probably gmail specific
            date=date,
            body=readBody(email_message)
        )
        # print m
        # print "\n"

        insert_mail(m)


def readBody(email_message):
    body = None
    if email_message.is_multipart():
        for payload in email_message.get_payload():
            # if payload.is_multipart(): ...
            body = payload.get_payload()
    else:
        body = email_message.get_payload()

    return body


if __name__ == '__main__':
    run()
