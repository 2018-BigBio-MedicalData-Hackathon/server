from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask_restful import reqparse, Resource, Api
from flask import request, Flask
import dbconnect
import datetime
import hashlib
app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)
cursor = dbconnect.cursor
conn = dbconnect.conn


# salt+passwd로 passwd 만들기
def makepasswd(passwd, salt):
    _data = str.encode(passwd + salt)
    _hash = hashlib.sha256()
    _hash.update(_data)
    return _hash.hexdigest()


# /auth 구현
class Auth(Resource):
    def post(self):
        try:
            # 지역변수로 POST 받기 설정
            _parser = reqparse.RequestParser()
            _parser.add_argument('username', type=str)
            _parser.add_argument('password', type=str)
            _args = _parser.parse_args()

            _usernamet = _args['username']  # 토큰 용도
            _username = conn.escape_string(_args['username'])
            _password = conn.escape_string(_args['password'])
            _query = "select salt from user where username='%s'" % (_username)
            cursor.execute(_query)
            _data = cursor.fetchone()
            _salt = _data[0]

            # 회원 verify
            _password = makepasswd(_password, _salt)
            print(_username, _password)
            _query = "select username from user where passwd='%s'" \
            % (_password)
            cursor.execute(_query)
            _data = cursor.fetchone()

            print(_data[0])
            if _data[0] != _username:
                return {"id and password are wrong": 401}

            else:
                # 토큰발급
                _time = datetime.timedelta(hours=1)
                _access_token = create_access_token({'username': _usernamet}, expires_delta =_time)
                print(0)                                    
                _query = "UPDATE user SET token=%s WHERE username=%s"
                print(1)
                _access_token = conn.escape_string(_access_token)
                _value = (_access_token, _username)
                cursor.execute(_query, _value)
                conn.commit()         
                return {"Token": _access_token,
                        "Status": 200}

        except Exception:
            return {'error': 500}

    @jwt_required
    def delete(self):
        try:
            # username 알아내는 token 복호화
            _current_user = get_jwt_identity()
            _username = conn.escape_string(_current_user['username'])
            # header에서 token 추출
            _rawtoken = request.headers.get('Authorization').split()[1]
            _query = "select token from user where username='%s'" % (_username)
            cursor.execute(_query)
            _data = cursor.fetchone()
            _token = _data[0]
            if (_token != _rawtoken):
                return {"Not Validate Token": 401}
            # token 삭제
            else:
                _query = "UPDATE user SET token = null WHERE username = '%s'"\
                                                                 % (_username)
                cursor.execute(_query)
                conn.commit()
                return {"Token Deleted": 200}

        except Exception as e:
            return {'error': 500}


# /auth/verify 구현
class Authverify(Resource):
    @jwt_required
    def post(self):
        try:
            # username 알아내는 token 복호화
            _current_user = get_jwt_identity()
            _username = conn.escape_string(_current_user['username'])
            # header에서 token 추출
            _rawtoken = request.headers.get('Authorization').split()[1]
            _query = "select token from user where username='%s'" % (_username)
            cursor.execute(_query)
            _data = cursor.fetchone()
            _token = _data[0]
            if (_token != _rawtoken):
                return {"Not Validate Token": 404}
            # token 삭제
            else:
                return {"Validate Token": 200, "username": _username}

        except Exception:
            return {'error': 500}
