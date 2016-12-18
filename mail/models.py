from sqlalchemy import Column, Integer, UnicodeText,String, DateTime,ForeignKey
from sqlalchemy_utils import EncryptedType
from database import DB
import datetime

from datetime import datetime

MYSQL_HOST = "localhost"
MYSQL_DATABASENAME = "spamback"
MYSQL_USERNAME = "spamback"
MYSQL_PASSWORD = "spamback"


class Mail(DB.db.Model):
    __tablename__ = 'mail'
    id = Column(Integer, primary_key=True)
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
               "created_at=%s" \
               ")>" % (
                   self.id,
                   self.uuid,
                   self.subject,
                   self.from_,
                   self.to,
                   self.delivered_to,
                   self.date,
                   self.created_at
               )

class MailAccount(DB.db.Model):
    __tablename__ = 'mail_account'
    id = Column(Integer, primary_key=True)
    login = Column(String(255), unique=False, nullable=False)
    password = Column(EncryptedType(String, 'HtfghhTT5565sk!#'))
    account_type_id = Column(Integer, ForeignKey("mail_account_type.id"), nullable=False)
    mail_boxes = Column(String(255), nullable=False)


    def __repr__(self):
        # str_created_at = self._created_at.strftime("%Y-%m-%d %H:%M:%S")
        return "<MailAccount (id='%s', " \
               "login='%s', " \
               "pass=%s" \
               "type=%s" \
               ")>" % (
                   self._id
                   , self.login
                   , self.password
                   , self.account_type
               )

class MailAccountType(DB.db.Model):

    __tablename__ = 'mail_account_type'
    id = Column(Integer, primary_key=True)
    type = Column(Integer, nullable=False)
    host = Column(String(255))
    account_type = Column(Integer)

    def __repr__(self):
        return "<MailAccountType " \
               "(" \
               "id='%s', " \
               "login='%s', " \
               "password=%s" \
               "type=%s" \
               ")>" % (
                   self._id,
                   self.login,
                   self.password,
                   self.account_type
               )
def insert_mail(new_mail=None):
    DB.db.session.add(new_mail)
    DB.db.session.commit()

