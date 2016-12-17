# First create the Base class

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from datetime import datetime, timedelta
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref


class Mail(Base):
    __tablename__ = 'mail'

    _id = Column(Integer, primary_key=True)

    _subject = Column(String(255), unique=False, nullable=True)

    _from = Column(String(255), unique=False, nullable=True)

    _to = Column(String(255), unique=False, nullable=True)

    _message_id = Column(String(255), unique=False, nullable=True)

    _in_reply_to_id = Column(String(255), unique=False, nullable=True)

    _body = Column(String(2000), unique=False, nullable=True)

    _created_at = Column(DateTime, default=datetime.utcnow)

    # tags = relationship('Tag', secondary=tags,
    #                     backref=backref('images', lazy='dynamic'))

    # comments = relationship('Comment', backref='image', lazy='dynamic')

    def __repr__(self):
        str_created_at = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        return "<Mail (id='%s', " \
               "subject='%d', " \
               "created_at=%s)>" % (self._id, self._subject, self._created_at)


MYSQL_HOST = "localhost"
MYSQL_DATABASENAME = "spamback"
MYSQL_USERNAME = "spamback"
MYSQL_PASSWORD = "spamback"

from sqlalchemy import create_engine

# engine = create_engine('sqlite:///:memory:', echo=True)

engine_name = 'mysql://%s:%s@%s/%s' % (MYSQL_USERNAME, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DATABASENAME)

print "engine", engine_name

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
    print "inserting a new mail"
    session = Session()

    session.add(new_mail)

    session.commit()


def test_insert():
    m = Mail(
        _subject="test",
        _from="a@b.com"
    )
    insert_mail(m)



test_insert()
