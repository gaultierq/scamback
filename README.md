# scamback

Database:
MySQL: samback
user: samback
password: samback
 config.py ->> SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://samback:samback@localhost/samback’



Database migrations:
python manage.py db init
python manage.py db migrate
python manage.py db upgrade


1. POST
http://127.0.0.1:5000/api/v1/auth/register?username=atanas&email=atanasster@gmail.com&password=xxxxxx

2. POST
http://127.0.0.1:5000/api/v1/auth/login?username=atanas&password=nasso

3. POST
http://127.0.0.1:5000/api/v1/thread/add?title=new thread 2333&content=big content ffsdfdsfsd

4. GET
http://127.0.0.1:5000/api/v1/thread/list

5. GET
http://127.0.0.1:5000/api/v1/thread/popular

6. POST
http://127.0.0.1:5000/api/v1/thread/like?thread_id=1&user_id=5

7. POST
http://127.0.0.1:5000/api/v1/answer/add?content=This is a funny answer&thread_id=1&user_id=5

8. POST
http://127.0.0.1:5000/api/v1/answer/like?assnswer_id=1&user_id=5


