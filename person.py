

"병원 등에게서 처방전, 영수증을 받기 위한 API"

from flask import Flask, request
from flask_restful import reqparse, Api, Resource
import config
import dbconnect

app = Flask(__name__)
api = Api(app)

# MySQL 연결
cursor = dbconnect.cursor
conn = dbconnect.conn


# /Person 구현
class Person(Resource):
    #보험사 or 타 병원에 서류보내기
    def post(self):
        try:
            # 지역변수로 POST 받기 설정
            _parser = reqparse.RequestParser()
            _parser.add_argument('username', type=str)
            _parser.add_argument('password', type=str)
            _args = _parser.parse_args()

            _username = _args['username']
            _password = _args['password']

            # 아이디 중복확인
            _query = "SELECT 1 FROM user WHERE username='%s'" % (_username)
            cursor.execute(_query)
            _data = cursor.fetchall()
            if _data:
                return {"Duplicated id": 404}
            else:
                # 회원가입
                _query = "INSERT INTO user(username,passwd,permission,salt) values(%s,%s,%s,%s)"
                _salt = salt()  # salt 생성

                _password = makepasswd(_password, _salt)  # 암호화
                _value = (_username, _password, 0, _salt)
                cursor.execute(_query, _value)
                _data = cursor.fetchall()
                if not _data:
                    conn.commit()
                    return {"Register Success": 200}
                else:
                    conn.rollback()
                    return {"Register Failed": 404}

        except Exception as e:
            return {'error': 500}
    
    #서버에 저장된 처방전 들고오기
    def get(self):
        try:
            # 지역변수로 POST 받기 설정
            _parser = reqparse.RequestParser()
            _parser.add_argument('username', type=str)
            _parser.add_argument('password', type=str)
            _args = _parser.parse_args()

            _username = _args['username']
            _password = _args['password']

            # 아이디 중복확인
            _query = "SELECT 1 FROM user WHERE username='%s'" % (_username)
            cursor.execute(_query)
            _data = cursor.fetchall()
            if _data:
                return {"Duplicated id": 404}
            else:
                # 회원가입
                _query = "INSERT INTO user(username,passwd,permission,salt) values(%s,%s,%s,%s)"
                _salt = salt()  # salt 생성

                _password = makepasswd(_password, _salt)  # 암호화
                _value = (_username, _password, 0, _salt)
                cursor.execute(_query, _value)
                _data = cursor.fetchall()
                if not _data:
                    conn.commit()
                    return {"Register Success": 200}
                else:
                    conn.rollback()
                    return {"Register Failed": 404}

        except Exception as e:
            return {'error': 500}