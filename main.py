from flask import Flask
from flask_restful import Api
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)
import auth
import account
import license

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'super-secret'


Auth = auth.Auth
Authverify = auth.Authverify
Account = account.Account
License = license.License


# api 라우팅 부분
api.add_resource(Auth, '/auth')
api.add_resource(Authverify, '/auth/verify')
api.add_resource(Account, '/account')
api.add_resource(License, '/license')

if __name__ == '__main__':
    app.run(debug=True)
