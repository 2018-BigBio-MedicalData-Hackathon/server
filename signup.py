from flask import Flask, render_template, Response, request, session
from flask_restful import Resource, Api
from flask_restful import reqparse
import config
import random
import hashlib
import dbconnect

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
            # 지역변수로 로그인 폼 데이터 POST 받기 설정
            _parser = reqparse.RequestParser()
            _parser.add_argument('userid', type=str)
            _parser.add_argument('password', type=str)
            _parser.add_argument('username', type=str)
            _parser.add_argument('reginum', type=int)
            _parser.add_argument('phonenum', type=int)
            _parser.add_argument('email', type=str)
            _args = _parser.parse_args()

            # 변수에 할당
            _userid = conn.escape_string(_args['userid'])
            _password = conn.escape_string(_args['password'])
            _username = conn.escape_string(_args['username'])
            _reginum = conn.escape_string(_args['reginum'])
            _phonenum = conn.escape_string(_args['phonenum'])
            _email = conn.escape_string(_args['email'])

            # salt 데이터베이스에서 가져오기
            _query = "select salt from user where username='%s'" % (_username)
            cursor.execute(_query)
            _data = cursor.fetchone()
            _salt = _data[0]

            # 회원 id verify
            _password = makepasswd(_password, _salt)
            print(_username, _password)
            _query = "select username from user where passwd='%s'" % (_password)
            cursor.execute(_query)
            _data = cursor.fetchone()
            print(_data[0])
            if _data[0] != _username:
                return {"id and password are wrong": 401}

            # 회원 password verify 
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
