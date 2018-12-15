

"""
1) 제3자 (보험사, 제약사 등)에게 정보(처방전, 영상 등)을 전송과 응답을 위한 API
2) 제출하기 위한 API(약국 등에서 환자가 처방전을 직접(바코드 혹은 큐알) 보여주어 간편하게 정보를 전송및 응답가능하도록)
"""

from flask import Flask, request
from flask_restful import reqparse, Api, Resource
import config
import dbconnect

app = Flask(__name__)
api = Api(app)

# MySQL 연결
cursor = dbconnect.cursor
conn = dbconnect.conn


# /Agency 구현
class Agency(Resource):
    #병원이 보내는 처방전 서버에 저장하기
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