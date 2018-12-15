from flask import Flask
from flask_restful import Api
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
from flask_cors import CORS
import agency
import signup
import login
# import license

app = Flask(__name__)
CORS(app)
api = Api(app)
jwt = JWTManager(app)


Agency = agency.Agency
# Auth = auth.Auth
# # Authverify = auth.Authverify
Signup = signup.Signup
Login = login.Login


# api 라우팅 부분
api.add_resource(Agency, '/agency')
# api.add_resource(Authverify, '/auth/verify')
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
