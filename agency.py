

"""
1) 제3자 (보험사, 제약사 등)에게 정보(처방전, 영상 등)을 전송과 응답을 위한 API
2) 제출하기 위한 API(약국 등에서 환자가 처방전을 직접(바코드 혹은 큐알) 보여주어 간편하게 정보를 전송및 응답가능하도록)
"""

from flask import Flask, request, jsonify, json
from flask_restful import reqparse, Api, Resource
import config
# import dbconnect

app = Flask(__name__)
api = Api(app)

# MySQL 연결
# cursor = dbconnect.cursor
# conn = dbconnect.conn


# /Agency 구현
class Agency(Resource):
    #병원이 보내는 처방전 서버에 저장하기
    def post(self):
        try:
            # json 데이터 post로 받기
            _content = request.get_json()
            _insurance = _content['insurance']
            _nursesgin = _content['nursing_institution_sign']
            print(_nursesgin)
            return {'su': 200}

        except Exception as e:
            return {'error': e}