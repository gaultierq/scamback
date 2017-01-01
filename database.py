from flask_sqlalchemy import SQLAlchemy
class DB():
    db = None
    @classmethod
    def init_db(self,app):
        self.db = SQLAlchemy(app)

