from functools import wraps

from flask import Flask, render_template, session, request, redirect, url_for
import redis
import os

app = Flask(__name__)
#redis_i = redis.from_url("redis://localhost:6379")
redis_i = redis.StrictRedis(host='localhost', port=6379, db=0)
app.secret_key = os.urandom(24)

def check_redis(f):
    @wraps(f)
    def decorated_fun(*args, **kwargs):
        id = kwargs["id"]
        if id not in session and id in redis_i.lrange("user_list", 0, -1):
            redis_i.lrem("user_list", 0, id)


@app.route("/<id>")
@check_redis
def index(id):
    if 'user' not in session:
        session['user'] = id
        redis_i.lpush("user_list", id)
    return "Logged!"

@app.route("/users")
def users():
    l = b",".join(list(redis_i.lrange("user_list", 0, -1)))
    return l

if __name__ == "__main__":
    app.run()
    redis_i.set("user_list", [])
