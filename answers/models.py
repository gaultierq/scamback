from sqlalchemy import Column, Integer, UnicodeText, DateTime,ForeignKey
from sqlalchemy.orm import relationship
from database import DB
import datetime

class Answer(DB.db.Model):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    thread_id = Column(Integer, ForeignKey("threads.id"),nullable=False)
    content = Column(UnicodeText, default=u'')
    created = Column(DateTime, default=datetime.datetime.utcnow)
    edited = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship("User", foreign_keys=[user_id])
    thread = relationship("Thread", foreign_keys=[thread_id])
    num_likes = Column(Integer, default=0, nullable=False)

    def __init__(self, content,thread_id, user_id):
        self.thread_id = thread_id
        self.user_id = user_id
        self.content = content

    def __repr__(self):
        return '<Answer for %r>' % self.thread.title

    def toJSON(self):
        return {'id':self.id,
                'content': self.content,
                'num_likes':self.num_likes,
                'created': self.created,
                'edited': self.edited,
                'thread_id': self.thread_id,
                 'user': self.user.toJSON() if self.user else None}


class AnswerLike(DB.db.Model):
    __tablename__ = 'answer_likes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    answer_id = Column(Integer, ForeignKey("answers.id"),nullable=False)
    user = relationship("User", foreign_keys=[user_id])
    answer = relationship("Answer", foreign_keys=[answer_id])

    def __init__(self, user_id, answer_id):
        self.user_id = user_id
        self.answer_id = answer_id
        if answer_id:
            answer = Answer.query.filter_by(id =answer_id).first()
            if answer:
                answer.num_likes += 1

    def toJSON(self):
        return {'answer': self.answer.toJSON() if self.answer else None ,
                 'user': self.user.toJSON() if self.user else None }
