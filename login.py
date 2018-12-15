from flask import Flask, render_template, Response, request, session
from flask_restful import Resource, Api
from flask_restful import reqparse
import config
import random
import hashlib

app = Flask(__name__)
api = Api(app)

# MySQL 연결
cursor = dbconnect.cursor
conn = dbconnect.conn


# salt 생성
def salt():
    alphabet = "0123456789abcdefghijklmnopqrstuvwxyz" + \
               "ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%()"
    chars = []
    for i in range(32):
        chars.append(random.choice(alphabet))

    return "".join(chars)


# salt+passwd로 passwd 만들기
def makepasswd(passwd, salt):
    _data = str.encode(passwd + salt)
    _hash = hashlib.sha256()
    _hash.update(_data)
    return _hash.hexdigest()


class Login(Resource):
    def post(self):
        try:
            # 지역변수로 POST 받기 설정
            _parser = reqparse.RequestParser()
            _parser.add_argument('username', type=str)
            _parser.add_argument('password', type=str)
            _args = _parser.parse_args()

            _username = conn.escape_string(_args['username'])
            _password = conn.escape_string(_args['password'])
            _salt = salt()  # salt 생성
            _password = makepasswd(_password, _salt)  # 암호화
            _query = "select password from user where id='%s'" % (_username)
            cursor.execute(_query)
            newpassword = cursor.fetchone()[0]
            if(_password == newpassword):
                print("login success")
                return {"login Success": 200}
            else:
                return {"login fail": 401}
            return Response("login success")
        except Exception:
            return {'error': 500}
