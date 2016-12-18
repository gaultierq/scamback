from sqlalchemy import Column, Integer, String,Unicode,UnicodeText, DateTime,ForeignKey
from sqlalchemy.orm import relationship
from database import DB
import datetime

class Thread(DB.db.Model):
    __tablename__ = 'threads'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode(255), unique=True, nullable=False)
    content = Column(UnicodeText, default=u'')
    created = Column(DateTime, default=datetime.datetime.utcnow)
    edited = Column(DateTime, default=datetime.datetime.utcnow)
    num_likes = Column(Integer,default=0,nullable=False)

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __repr__(self):
        return '<Thread %r>' % self.title

    def toJSON(self):
        return {'id':self.id,
                'title': self.title,
                'content': self.content,
                'num_likes':self.num_likes}


class ThreadLike(DB.db.Model):
    __tablename__ = 'thread_likes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    thread_id = Column(Integer, ForeignKey("threads.id"),nullable=False)
    user = relationship("User", foreign_keys=[user_id])
    thread = relationship("Thread", foreign_keys=[thread_id])

    def __init__(self, user_id, thread_id):
        self.user_id = user_id
        self.thread_id = thread_id
        if thread_id:
            thread = Thread.query.filter_by(id =thread_id).first()
            if thread:
                thread.num_likes += 1

    def toJSON(self):
        return {'thread': self.thread.toJSON() if self.thread else None ,
                 'user': self.user.toJSON() if self.user else None }
