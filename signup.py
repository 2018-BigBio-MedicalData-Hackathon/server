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
            _parser.add_argument('user_id', type=str)
            _parser.add_argument('user_pw', type=str)
            _parser.add_argument('username', type=str)
            _parser.add_argument('user_reginum', type=str)
            _parser.add_argument('phonenum', type=int)
            _parser.add_argument('email', type=str)
            _args = _parser.parse_args()

            # 변수에 할당
            _userid = conn.escape_string(_args['user_id'])
            _password = conn.escape_string(_args['user_pw'])
            _username = conn.escape_string(_args['username'])
            _reginum = conn.escape_string(_args['user_reginum'])
            _phonenum = conn.escape_string(_args['phonenum'])
            _email = conn.escape_string(_args['email'])
            _salt = salt()
            _newpassword = makepasswd(_password, _salt)

            # gender 구하기
            if _reginum[6] == "1" or _reginum[6] == "3":
                _gender = "male"
            elif _reginum[6] == "2" or _reginum[6] == "4":
                _gender = "female"
            else:
                return {"Register number Not valid": 404}        

            _query = "INSERT INTO user(user_id, user_pw, salt, username, user_reginum, phonenum, email, gender) values(%s, %s, %s, %s, %d, %d, %s, %s)"
            _value = (_userid, _newpassword, _username, int(_reginum), _phonenum, _email, _gender)
            cursor.execute(_query, _value)
            _data = cursor.fetchall()
            print(_data)
            if not _data:
                conn.commit()
                return {"Register Success": 200}
            else:
                conn.rollback()
                return {"Register Failed": 404}

        except Exception:
            return {'error': 500}
