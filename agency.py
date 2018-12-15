

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
            # json 데이터 post로 받아서 변수 저장
            _content = request.get_json()
            _insurance = _content['insurance']
            _nursesgin = _content['nursing_institution_sign']
            _patientname = _content['patient']['name']
            _patientreginum = _content['patient']['registration_number']
            _insname = _content["medical_Institutions"]["name"]
            _insphonenum = _content["medical_Institutions"]["phone_number"]
            _insfaxnum = _content["medical_Institutions"]["fax_number"]
            _insemail = _content["medical_Institutions"]["email_address"]
            _diseasecode1 = _content["disease_classification_codes"][0]
            _diseasecode2 = _content["disease_classification_codes"][1]
            _doctorname = _content["sign_of_prescription_medical_practitioner"]
            _doctortype = _content["license_type"]
            _doctornum = _content["license_number"]
            print(1)
            _mediname = []
            _medidose = []
            _medidailydose = []
            _meditotalday = []
            _mediusage = []
            _mediinside = []
            for data in _content["prescription_medicine"]:
                _mediname.append(data["name_of_medicines"])
                _medidose.append(data["one_dose"])
                _medidailydose.append(data["number_of_daily_doses"])
                _meditotalday.append(data["total_dosing_days"])
                _mediusage.append(data["usage"])
                _mediinside.append(data["inside"])
            # print(_content["injection_prescription"]["preparation_amount"])
            _usepreiod = _content["injection_prescription"]["period_of_use"]
            _dispensename = _content["injection_prescription"]["preparation"]["name_of_dispenser"]
            _pharmacistname = _content["injection_prescription"]["preparation"]["pharmacist"]["name"]
            _pharmacistseal = _content["injection_prescription"]["preparation"]["pharmacist"]["seal"]
            _preparationamount = _content["injection_prescription"]["preparation_amount"]
            _preparationyear = _content["injection_prescription"]["year_of_preparation"]
            _changeprescription = _content["injection_prescription"]["change_of_prescription"]
            # print(3)
            # print(_pharmacistname)
            return {'su': 200}

        except Exception as e:
            return {'error': e}