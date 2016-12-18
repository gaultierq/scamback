import os
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from app import app
from database import DB
from users.models import User
from threads.models import Thread,ThreadLike
from answers.models import Answer,AnswerLike
from mail.models import Mail,MailAccount,MailAccountType

app.config.from_object(os.environ['APP_SETTINGS'])

migrate = Migrate(app, DB.db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()