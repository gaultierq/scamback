# MAIL_SERVER = "pop.gmail.com"
import datetime
import os
import email.header
import imaplib

from app import app
from database import DB
from mail.models import Mail, MailAccount, MailAccountType, insert_mail, MailStatus
from threads.models import Thread

ACCOUNTS = None

GMAIL = 1

if __name__ == '__main__':
    app.config.from_object(os.environ['APP_SETTINGS'])
    DB.init_db(app)

    # TODO: store it in db
    account_type = MailAccountType(type=GMAIL, host='imap.gmail.com')

    ACCOUNTS = [
        # user_account
        MailAccount(
            id=1, login="scam.scammers.back@gmail.com", password="4wqPSyUIA3dB", mail_boxes="inbox",
            account_type=account_type),

        # scammer_account
        MailAccount(id=2, login="jacob.carlsenis@gmail.com", password="lEEDVBQw9INa", mail_boxes="inbox",
                    account_type=account_type
                    )
    ]


def fetch():
    print("feeding the email table")
    for account in ACCOUNTS:
        try:
            fetch_account(account)
        except:
            print("failed to fetch", account)


# process the new emails, and create the thread, messages
# 1. take next CREATED -> PROCESSING (order by email_sent_date asc)

#
# 2. (threadId, email)
#   a. parse latest message body, create a message, add it to the thread
#   b. setThreadId on email &  -> PROCESSED_OK
def process():
    print("processing created emails")

    session = DB.db.session

    empty = True
    new_emails = Mail.query.filter_by(status=MailStatus.CREATED).all()

    for m in new_emails:

        if m is None:
            break

        try:
            print("processing mail: ", m.id)
            processed, ok = process_it(m)

            empty &= not processed
        except Exception as e:
            m.status = MailStatus.PROCESSED_KO
            print("uncaught exception for ", m.id, ":", e)
        finally:
            session.commit()

    # if loop != 1000 - 1 and not empty:
    #     assert not process()

    return not empty


# A: if from user_email  accounts
#       a. parse the scammer email from the body
#               except: -> FAIL_READ_PARSE_EMAIL
#       b. parse the boddy message
#                     except: -> FAIL_READ_ORIGINAL_MESSAGE
#
#       c. create a new thread
#
# B: if from scam accounts
#       a. retrieve the threadID
#           use: in-reply-to field
#                 use-case: answering yourself (scammer, or user)
#                   trust the sent-date (and the ordering)
#                   nb: the mail thread is a tree, not a chain
#                   except: -> NO_PARENT , giving a chance to re-process them later on


def parse_scammer_mail(m):
    scammer_email = "placeholder@xyz.com"
    original_scammer_message = "placeholder body"
    title = "placeholder title"
    return scammer_email, title, original_scammer_message


def process_it(m: Mail):
    processed, ok = False, False
    if m.account_id == 1:
        processed = True

        m.status = MailStatus.PROCESSING
        DB.db.session.commit()

        email, title, content = parse_scammer_mail(m)
        if email is None or content is None:
            m.status = MailStatus.FAIL_PARSE_EMAIL
            return

        thread = Thread(title=title, content=content)
        DB.db.session.add(thread)
        DB.db.session.commit()
        ok = True

    elif m.account_id == 2:
        pass
    else:
        raise Exception("unknown account id", m.account_id)

    if processed:
        if ok:
            m.status = MailStatus.PROCESSED_OK
        else:
            m.status = MailStatus.PROCESSED_KO

    DB.db.session.commit()
    return processed, ok


# add last_processing date on email resource

# funcion2:
# process_no_parent: give a chance to retrieve the borken email chain
def process_no_parent():
    pass


# function3:
# create new emails to be sent
# source1: process the thread/message table, get the closed bid. create an email to be sent to scammer
# opt. source2: (later) user who create new threads.
# opt. source3: (uers who subscribed)
def prepare_emails():
    pass


# function4: add pending emails
# send emails marked as PENDING
# NB: obtain the messageId after the message is sent, and update the table
def send_pending_emails():
    pass


# take the emails into the database. save headers
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
        try:
            result, data = mail.fetch(num, "(RFC822)")  # fetch the email body (RFC822) for the given ID

            raw_email = data[0][1]  # here's the body, which is raw text of the whole email
            # including headers and alternate payloads
            # print "email", raw_email
            # print(raw_email)
            email_message = email.message_from_bytes(raw_email)

            print("all headers=", email_message.items())  # print all headers

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
                body=readBody(email_message),
                account_id=account.id
            )

            insert_mail(m)

            # TODO: move email to other mailbox
        except:
            print("error while fetching message")


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
    # run()
    # fetch()

    process()
