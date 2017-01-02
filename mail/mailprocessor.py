# MAIL_SERVER = "pop.gmail.com"
import datetime
import os
import email.header
import imaplib

from app import app
from database import DB
from mail.models import Mail, MailAccount, MailAccountType, insert_mail, MailStatus
from threads.models import Thread
from mail import utils

GMAIL = 1
persist = True

if __name__ == '__main__':
    app.config.from_object(os.environ['APP_SETTINGS'])
    DB.init_db(app)
    persist=False


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

# user --->  mail1
# processing
# mail2 --> scammer
# scammer --> mail2
# etc

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
            process_it(m)

            empty = False
        except Exception as e:
            m.status = MailStatus.PROCESSED_KO
            print("uncaught exception for ", m.id, ":", e)
            session.rollback()
            raise
        finally:
            session.commit()

    return not empty


def parse_scammer_mail(m):
    sender, message = utils.parse_forwarded_message(m.body)
    scammer_name, scammer_email = utils.parse_email_address(sender)
    return scammer_name, scammer_email, m.subject, message


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
#                   think of the mail thread as a tree, not a chain
#                   except: -> NO_PARENT , giving a chance to re-process them later on

def retrieve_thread_id(email: Mail):
    if email.thread_id:
        return

    inreplyto = email.in_reply_to

    if not inreplyto:
        email.status = MailStatus.FAIL_ATTACH
        return

    mails = Mail.query.filter_by(uuid=inreplyto).order_by(Mail.created_at.desc()).all()

    for m in mails:
        if m is not None and m.thread_id is not None:
            email.thread_id = m.thread_id
            break
    if not m.thread_id:
        email.status = MailStatus.FAIL_ATTACH


def process_it(m: Mail):
    m.status = MailStatus.PROCESSING
    DB.db.session.commit()

    try:

        if m.account_id == 1:

            name, em, title, content = parse_scammer_mail(m)

            if em is None or content is None:
                m.status = MailStatus.FAIL_PARSE_EMAIL
                return

            thread = Thread(title=title, content=content)
            DB.db.session.add(thread)
            DB.db.session.commit()

            m.thread_id = thread.id
            m.status = MailStatus.PROCESSED_OK

        elif m.account_id == 2:

            if not m.thread_id:
                m.thread_id = retrieve_thread_id(m)
                if m.thread_id is None:
                    m.status = MailStatus.FAIL_ATTACH
                    return

            m.status = MailStatus.PROCESSED_OK
        else:
            raise Exception("unknown account id", m.account_id)
    finally:
        if m.status == MailStatus.PROCESSING:
            m.status = MailStatus.PROCESSED_KO

        DB.db.session.commit()


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
            email_message = email.message_from_bytes(raw_email)

            body = read_body(email_message)
            if body is None:
                print("not supoprted")
                return


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
                body=body,
                account_id=account.id
            )

            insert_mail(m)

            # TODO: move email to other mailbox
        except:
            print("error while fetching message")


def read_body(email_message):
    body = None
    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(
                    decode=True)  # to control automatic email-style MIME decoding (e.g., Base64, uuencode, quoted-printable)
                body = body.decode()
                break

            elif part.get_content_type() == "text/html":
                continue
    return body


if __name__ == '__main__':
    # run()
    # fetch()

    process()
