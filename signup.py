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


class Signup(Resource):
    def post(self):
        try:
            print(1)
            # 지역변수로 로그인 폼 데이터 POST 받기 설정
            _parser = reqparse.RequestParser()
            _parser.add_argument('user_id', type=str)
            _parser.add_argument('user_pw', type=str)
            _parser.add_argument('user_pwconfirm', type=str)
            _parser.add_argument('username', type=str)
            _parser.add_argument('user_reginum', type=str)
            _parser.add_argument('phonenum', type=int)
            _parser.add_argument('emailfirst', type=str)
            _parser.add_argument('emailsecond', type=str)
            _args = _parser.parse_args()
            print(2)
            # 변수에 할당
            print(_args)
            _userid = _args['user_id']
            _password = _args['user_pw']
            _passwordconfirm = _args['user_pwconfirm']
            _username = _args['username']
            _reginum = _args['user_reginum']
            _phonenum = _args['phonenum']
            _emailfirst = _args['emailfirst']
            _emailsecond = _args['emailsecond']
            _email = _emailfirst+ "@" + _emailsecond
            _salt = salt()
            _newpassword = makepasswd(_password, _salt)
            print(3)
            print(_email)

            # # user 중복체크
            # _query = "select 1 from user where user_pw=%s" % (_password)
            # cursor.execute(_query)
            # _data = cursor.fetchall()
            # print(_data)
            # if _data:
            #     return {"duplicate": 401}


            # 비밀번호 체크
            if _password != _passwordconfirm:
                return {"not match password": 404}

            # gender 구하기
            if _reginum[6] == "1" or _reginum[6] == "3":
                _gender = "male"
            elif _reginum[6] == "2" or _reginum[6] == "4":
                _gender = "female"
            else:
                return {"Register number Not valid": 404}        

            _query = "INSERT INTO user(user_id, user_pw, salt, username, user_reginum, phonenum, email, gender) values(%s, %s, %s, %s, %s, %s, %s, %s)"
            print(_query)
            _value = (_userid, _newpassword, _salt, _username, _reginum, str(_phonenum), _email, _gender)
            print(_value)
            cursor.execute(_query, _value)
            _data = cursor.fetchall()
            print(_data)
            if not _data:
                conn.commit()
                return {"Register Success": 200}
            else:
                conn.rollback()
                return {"Register Failed": 404}

        except Exception as e:
            return {'error': "e"}
