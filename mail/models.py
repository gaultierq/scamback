from enum import Enum

from sqlalchemy import Column, Integer, UnicodeText, String, DateTime, ForeignKey
from sqlalchemy_utils import EncryptedType
from database import DB
import datetime

from datetime import datetime
from sqlalchemy.orm import relationship

# MAIL_STATUS
CREATED=0
PROCESSED_OK=0

class MailStatus:
    CREATED = 0
    PROCESSING = 1
    PROCESSED_OK = 2
    PROCESSED_KO = 3
    FAIL_PARSE_EMAIL = 4
    FAIL_ATTACH = 5


class Mail(DB.db.Model):
    __tablename__ = 'mail'
    id = Column(Integer, primary_key=True)
    # uuid will be true eventually
    uuid = Column(String(255), unique=False, nullable=False)
    subject = Column(String(2000))
    from_ = Column(String(255))
    to = Column(String(255))
    delivered_to = Column(String(255))
    in_reply_to = Column(String(255))
    date = Column(DateTime)
    body = Column(UnicodeText)
    references = Column(UnicodeText)
    created_at = Column(DateTime, default=datetime.utcnow)
    account_id = Column(Integer)
    thread_id = Column(Integer)
    status = Column(Integer, default=0)

    def __repr__(self):
        # str_created_at = self._created_at.strftime("%Y-%m-%d %H:%M:%S")
        return "<Mail (" \
               "id='%s', " \
               "uuid='%s', " \
               "subject='%s', " \
               "from=%s" \
               "to=%s, " \
               "delivered_to=%s, " \
               "date=%s, " \
               "created_at=%s, " \
               "account_id=%s, " \
               "thread_id=%s, " \
               ")>" % (
                   self.id,
                   self.uuid,
                   self.subject,
                   self.from_,
                   self.to,
                   self.delivered_to,
                   self.date,
                   self.created_at,
                   self.account_id,
                   self.thread_id
               )


class MailAccount(DB.db.Model):
    __tablename__ = 'mail_account'
    id = Column(Integer, primary_key=True)
    login = Column(String(255), unique=False, nullable=False)
    password = Column(EncryptedType(String, 'HtfghhTT5565sk!#'))
    account_type_id = Column(Integer, ForeignKey("mail_account_type.id"), nullable=False)
    mail_boxes = Column(String(255), nullable=False)
    account_type = relationship("MailAccountType", foreign_keys=[account_type_id])

    def __repr__(self):
        # str_created_at = self._created_at.strftime("%Y-%m-%d %H:%M:%S")
        return "<MailAccount (id='%s', " \
               "login='%s', " \
               "pass=%s, " \
               "type_id=%s" \
               ")>" % (
                   self.id
                   , self.login
                   , self.password
                   , self.account_type_id
               )


class MailAccountType(DB.db.Model):
    __tablename__ = 'mail_account_type'
    id = Column(Integer, primary_key=True)
    type = Column(Integer, unique=True, nullable=False)
    host = Column(String(255))
    smtp_host = Column(String(255))

    def __repr__(self):
        return "<MailAccountType " \
               "(" \
               "id='%s', " \
               "type=%s" \
               ")>" % (
                   self.id,
                   self.type
               )


def insert_mail(new_mail=None):
    DB.db.session.add(new_mail)
    DB.db.session.commit()






def initDB():
    GMAIL = 1
    account_type = MailAccountType(type=GMAIL, host='imap.gmail.com', smtp_host='smtp.gmail.com:587')

    ACCOUNTS = [
        # user_account
        MailAccount(
            id=1, login="scam.scammers.back@gmail.com", password="4wqPSyUIA3dB", mail_boxes="inbox",
            account_type=account_type),

        # scammer_account
        MailAccount(id=2, login="jacob.carlsenis@gmail.com", password="lEEDVBQw9INa", mail_boxes="inbox",
                    account_type=account_type
                    ),
        # scammer_account
        MailAccount(id=3, login="scam.scammers.tras@gmail.com", password="qpn9B!cP@&oQ", mail_boxes="inbox",
                    account_type=account_type
                    )
    ]

    DB.db.session.add(account_type)
    DB.db.session.commit()

    for account in ACCOUNTS:
        DB.db.session.add(account)
        DB.db.session.commit()
