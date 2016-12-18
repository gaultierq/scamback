# scamback

<h4>Database:</h4>
<p>MySQL: samback</p>
<p>user: samback</p>
<p>password: samback</p>
<p>config.py ->> SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://samback:samback@localhost/samback’</p>



<h4>Database migrations:</h4>
<p>python manage.py db init</p>
<p>python manage.py db migrate</p>
<p>python manage.py db upgrade</p>


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


