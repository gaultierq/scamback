import os
if not 'APP_SETTINGS' in os.environ:
    os.environ['APP_SETTINGS'] = 'config.ProductionConfig'

from flask import Flask,jsonify, abort, request
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
from database import DB
DB.init_db(app)
from users.models import User
from threads.models import Thread, ThreadLike
from answers.models import Answer,AnswerLike


@app.route('/api/v1/auth/register',methods=['POST'])
def register():
    if not 'username' in request.args:
        return jsonify({'error': 'username is required'}), 400
    user = User(username=request.args.get('username'),email= request.args.get('email', ''),password=request.args.get('password', ''))
    DB.db.session.add(user)
    DB.db.session.commit()
    return jsonify( { 'user': user.toJSON() } ), 201

@app.route('/api/v1/auth/login',methods=['POST'])
def login():
    if not 'username' in request.args:
        return jsonify({'error': 'username is required'}), 400
    if not 'password' in request.args:
        return jsonify({'error': 'passwords is required'}), 400

    user = User.query.filter_by(username=request.args.get('username')).first()
    if user is None:
        return jsonify({'error': 'username not found'}), 400
    if user.password != request.args.get('password'):
        return jsonify({'error': 'password does not match'}), 400

    return jsonify({'user': user.toJSON()}), 201


@app.route('/api/v1/thread/add',methods=['POST'])
def add_thread():
    if not 'title' in request.args:
        return jsonify({'error': 'title is required'}), 400
    thread = Thread(title=request.args.get('title'),content=request.args.get('content'))
    DB.db.session.add(thread)
    DB.db.session.commit()
    return jsonify( { 'thread': thread.toJSON() } ), 201


@app.route('/api/v1/thread/list',methods=['GET'])
def list_thread():
    threads = Thread.query.order_by(Thread.created.desc()).all()
    return jsonify([t.toJSON() for t in threads])


@app.route('/api/v1/thread/popular',methods=['GET'])
def popular_thread():
    threads = Thread.query.filter(Thread.content.contains('top')).limit(3).all()
    return jsonify([t.toJSON() for t in threads])

@app.route('/api/v1/thread/like',methods=['POST'])
def like_thread():
    if not 'thread_id' in request.args:
        return jsonify({'error': 'thread_id is required'}), 400
    like = ThreadLike(thread_id=request.args.get('thread_id'),user_id=request.args.get('user_id',None))
    DB.db.session.add(like)
    DB.db.session.commit()
    return jsonify(like.toJSON())


@app.route('/api/v1/answer/add',methods=['POST'])
def add_answer():
    if not 'thread_id' in request.args:
        return jsonify({'error': 'thread_id is required'}), 400
    if not 'content' in request.args:
        return jsonify({'error': 'content is required'}), 400

    answer = Answer(content=request.args.get('content'),thread_id=request.args.get('thread_id'),user_id=request.args.get('user_id',None))
    DB.db.session.add(answer)
    DB.db.session.commit()
    return jsonify( { 'answer': answer.toJSON() } ), 201


@app.route('/api/v1/answer/like',methods=['POST'])
def like_answer():
    if not 'answer_id' in request.args:
        return jsonify({'error': 'answer_id is required'}), 400
    like = AnswerLike(answer_id=request.args.get('answer_id'),user_id=request.args.get('user_id',None))
    DB.db.session.add(like)
    DB.db.session.commit()
    return jsonify(like.toJSON())

if __name__ == '__main__':
    app.run()
