# First create the Base class
from sqlalchemy import ForeignKey
from sqlalchemy import UnicodeText
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy import create_engine

MYSQL_HOST = "localhost"
MYSQL_DATABASENAME = "spamback"
MYSQL_USERNAME = "spamback"
MYSQL_PASSWORD = "spamback"


class Mail(Base):
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

class MailAccount(Base):

    __tablename__ = 'mail_account'

    id = Column(Integer, primary_key=True)

    login = Column(String(255), unique=False, nullable=False)

    password = Column(String(255), unique=False)

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

class MailAccountType(Base):

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


# engine = create_engine('sqlite:///:memory:', echo=True)

engine_name = 'mysql://%s:%s@%s/%s?%s' % (MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DATABASENAME, "charset=utf8")

print("engine", engine_name)

engine = create_engine(engine_name, echo=True)
engine.execute("CREATE DATABASE IF NOT EXISTS %s" % (MYSQL_DATABASENAME)) #create db
engine.execute("USE %s" % (MYSQL_DATABASENAME))


Mail.__table__.create(engine, checkfirst=True)


from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)

session = Session()

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)



def insert_mail(new_mail=None):
    print("inserting a new mail")
    session = Session()

    session.add(new_mail)

    session.commit()

#
# def test_insert():
#     m = Mail(
#         _subject="test",
#         _from="a@b.com"
#     )
#     insert_mail(m)
#
#
#
# test_insert()
