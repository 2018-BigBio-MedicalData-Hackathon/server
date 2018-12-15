

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


# /account 구현
class Agency(Resource):
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

    @jwt_required
    def put(self):
        try:
            # 지역변수로 POST 받기 설정
            _parser = reqparse.RequestParser()
            _parser.add_argument('username', type=str)
            _parser.add_argument('new_password', type=str)
            _args = _parser.parse_args()
            _username = _args['username']
            _new_password = _args['new_password']

            # username 알아내는 token 복호화
            _current_user = get_jwt_identity()
            _rawusername = _current_user['username']

            # header에서 token 추출
            _rawtoken = request.headers.get('Authorization').split()[1]
            _query = "select token from user where username='%s'" % (_username)
            cursor.execute(_query)
            _data = cursor.fetchone()
            _token = _data[0]

            if (_username != _rawusername):
                return {"Not Validate Token": 404}
            elif (_token != _rawtoken):
                return {"Token has expired": 404}
            else:
                _query = "UPDATE user SET passwd = %s WHERE username = '%s'" % (_new_password, _username)
                cursor.execute(_query)
                conn.commit()
                return {"Password Updated": 200}

        except Exception as e:
            return {'error': 500}

    @jwt_required
    def patch(self):
        try:
            # 지역변수로 POST 받기 설정
            _parser = reqparse.RequestParser()
            _parser.add_argument('username', type=str)
            _parser.add_argument('permission', type=str)
            _args = _parser.parse_args()
            _username = _args['username']
            _permission = _args['permission']

            # username 알아내는 token 복호화
            _current_user = get_jwt_identity()
            _rawusername = _current_user['username']

            # header에서 token 추출
            _rawtoken = request.headers.get('Authorization').split()[1]
            _query = "select token,permission,username from user where username='%s'" % (_rawusername)
            cursor.execute(_query)
            _data = cursor.fetchone()
            _token = _data[0]
            _rootpermission = _data[1]
            _rootusername = _data[2]

            if (_rootpermission != 99):
                return {"Not Admin Token": 404}
            if (_rootusername != _rawusername):
                return {"Not Validate Token": 404}
            elif (_token != _rawtoken):
                return {"Token has expired": 404}
            else:
                _query = "UPDATE user SET permission = %s WHERE username = %s"
                _value = (_permission, _username)
                cursor.execute(_query, _value)
                conn.commit()
                return {"Permission Updated": 200}

        except Exception as e:
            return {'error': 500}

    @jwt_required
    def delete(self):
        try:
            # 지역변수로 POST 받기 설정
            _parser = reqparse.RequestParser()
            _parser.add_argument('password', type=str)
            _args = _parser.parse_args()
            _password = _args['password']

            # username 알아내는 token 복호화
            _current_user = get_jwt_identity()
            _rawusername = _current_user['username']

            # header에서 token 추출
            _rawtoken = request.headers.get('Authorization').split()[1]
            _query = "select token,passwd,salt from user where username='%s'" % (_rawusername)
            cursor.execute(_query)
            _data = cursor.fetchone()
            _token = _data[0]
            _rawpassword = _data[1]
            _salt = _data[2]
            _password = makepasswd(_password, _salt)

            if (_password != _rawpassword):
                return {"Not Validate Password": 404}
            elif (_token != _rawtoken):
                return {"Token has expired": 404}
            else:
                _query = "Delete from user WHERE username = %s"
                _value = (_rawusername)
                cursor.execute(_query, _value)
                conn.commit()
                return {"Delete Successed": 200}

        except Exception as e:
            return {'error': 500}


# /auth 구현
class Auth(Resource):
    def post(self):
        try:
            # 지역변수로 POST 받기 설정
            _parser = reqparse.RequestParser()
            _parser.add_argument('username', type=str)
            _parser.add_argument('password', type=str)
            _args = _parser.parse_args()

            _username = _args['username']
            _password = _args['password']
            _query = "select salt from user where username='%s'" % (_username)
            cursor.execute(_query)
            _data = cursor.fetchone()
            _salt = _data[0]

            # 회원 verify
            _password = makepasswd(_password, _salt)
            print(_username, _password)
            _query = "select username,permission from user where passwd='%s'" % (_password)
            cursor.execute(_query)
            _data = cursor.fetchone()
            _permission = _data[1]
            print(_data[1])
            if _data[0] != _username:
                return {"id and password are wrong": 404}

            else:
                # 토큰발급
                _access_token = create_access_token({'username': _username},
                                                    expires_delta=datetime.timedelta(hours=1 if not app.debug else 24))
                _query = "UPDATE user SET token=%s WHERE username=%s"
                _value = (_access_token, _username)
                cursor.execute(_query, _value)
                conn.commit()
                return {"Token": _access_token, "Permission": _permission, "Status": 200}

        except Exception as e:
            return {'error': 500}

    @jwt_required
    def delete(self):
        try:
            # username 알아내는 token 복호화
            _current_user = get_jwt_identity()
            _username = _current_user['username']
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
                _query = "UPDATE user SET token = null WHERE username = '%s'" % (_username)
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
            _username = _current_user['username']
            # header에서 token 추출
            _rawtoken = request.headers.get('Authorization').split()[1]
            _query = "select token from user where username='%s'" % (_username)
            cursor.execute(_query)
            _data = cursor.fetchone()
            _token = _data[0]
            if (_token != _rawtoken):
                return {"Not Validate Token : 404"}
            # token 삭제
            else:
                return {"Validate Token": 200}

        except Exception as e:
            return {'error': 404}


# /license 구현
class License(Resource):
    @jwt_required
    def post(self):
        try:
            # 지역변수로 POST 받기 설정
            _parser = reqparse.RequestParser()
            _parser.add_argument('username', type=str)
            _parser.add_argument('license', type=str)
            _parser.add_argument('serial', type=str)
            _parser.add_argument('available_pc_num', type=str)
            _parser.add_argument('expire_date', type=str)
            _args = _parser.parse_args()

            _username = _args['username']
            _license = _args['license']
            _serial = _args['serial']
            _available_pc_num = _args['available_pc_num']
            _expire_date = _args['expire_date']

            # username 알아내는 token 복호화
            _current_user = get_jwt_identity()
            _rawusername = _current_user['username']
            print(_rawusername, _license, _serial, _available_pc_num, _expire_date)

            # header에서 token 추출
            _rawtoken = request.headers.get('Authorization').split()[1]
            _query = "select token,permission from user where username='%s'" % (_rawusername)
            cursor.execute(_query)
            _data = cursor.fetchone()
            _token = _data[0]
            _permission = _data[1]
            print(_token, _permission)
            _query = "select id from user where username='%s'" % (_username)
            cursor.execute(_query)
            _data = cursor.fetchone()
            _user_id = _data[0]
            print(_user_id)
            if (_token != _rawtoken):
                return {"Not Validate Token": 404}
            if (_permission != 99):
                return {"Not Admin Token": 404}

            # license 등록
            else:
                _query = "INSERT INTO license(user_id,product_id,pc_num,serial_num,date) values(%s,%s,%s,%s,%s)"
                _value = (_user_id, _license, _available_pc_num, _serial, _expire_date)
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
            return {'error': str(e)}

    @jwt_required
    def patch(self):
        try:
            # 지역변수로 POST 받기 설정
            _parser = reqparse.RequestParser()
            _parser.add_argument('username', type=str)
            _parser.add_argument('license', type=str)
            _parser.add_argument('serial', type=str)
            _parser.add_argument('available_pc_num', type=str)
            _parser.add_argument('expire_date', type=str)
            _args = _parser.parse_args()

            _username = _args['username']
            _license = _args['license']
            _serial = _args['serial']
            _available_pc_num = _args['available_pc_num']
            _expire_date = _args['expire_date']
            # username 알아내는 token 복호화
            _current_user = get_jwt_identity()
            _rawusername = _current_user['username']
            print(_rawusername, _license, _serial, _available_pc_num, _expire_date)

            # header에서 token 추출
            _rawtoken = request.headers.get('Authorization').split()[1]
            _query = "select token,permission from user where username='%s'" % (_rawusername)
            cursor.execute(_query)
            _data = cursor.fetchone()
            _token = _data[0]
            _permission = _data[1]
            print(_token, _permission)
            _query = "select id from user where username='%s'" % (_username)
            cursor.execute(_query)
            _data = cursor.fetchone()
            _user_id = _data[0]
            print(_user_id)
            if (_token != _rawtoken):
                return {"Not Validate Token": 404}
            if (_permission != 99):
                return {"Not Admin Token": 404}

            # license 업데이트
            else:
                _query = "UPDATE license SET product_id=%s , serial_num=%s , pc_num=%s, date=%s WHERE user_id=%s"
                _value = (_license, _serial, _available_pc_num, _expire_date, _user_id)
                cursor.execute(_query, _value)
                _data = cursor.fetchall()
                conn.commit()
                return {"Updated Success": 200}

        except Exception as e:
            return {'error': str(e)}

    @jwt_required
    def delete(self):
        try:
            # 지역변수로 POST 받기 설정
            _parser = reqparse.RequestParser()
            _parser.add_argument('username', type=str)
            _parser.add_argument('license', type=str)
            _parser.add_argument('serial', type=str)
            _args = _parser.parse_args()

            _username = _args['username']
            _license = _args['license']
            _serial = _args['serial']
            # username 알아내는 token 복호화
            _current_user = get_jwt_identity()
            _rawusername = _current_user['username']

            # header에서 token 추출
            _rawtoken = request.headers.get('Authorization').split()[1]
            _query = "select token,permission from user where username='%s'" % (_rawusername)
            cursor.execute(_query)
            _data = cursor.fetchone()
            _token = _data[0]
            _permission = _data[1]
            print(_token, _permission)
            _query = "select id from user where username='%s'" % (_username)
            cursor.execute(_query)
            _data = cursor.fetchone()
            _user_id = _data[0]
            print(_user_id)
            if (_token != _rawtoken):
                return {"Not Validate Token": 404}
            if (_permission != 99):
                return {"Not Admin Token": 404}
            # license 삭제
            else:
                _query = "DELETE from license WHERE user_id=%s AND product_id=%s AND serial_num=%s"
                _value = (_user_id, _license, _serial)
                cursor.execute(_query, _value)
                _data = cursor.fetchall()
                print(_data)
                if not _data:
                    conn.commit()
                    return {"Deleted Success": 200}
                else:
                    conn.rollback()
                    return {"Deleted Failed": 404}

        except Exception as e:
            return {'error': str(e)}


# api 라우팅 부분


api.add_resource(Auth, '/auth')
api.add_resource(Authverify, '/auth/verify')
api.add_resource(Account, '/account')
api.add_resource(License, '/license')

if __name__ == '__main__':
    app.run(debug=True)