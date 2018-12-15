

"""
1) 제3자 (보험사, 제약사 등)에게 정보(처방전, 영상 등)을 전송과 응답을 위한 API
2) 제출하기 위한 API(약국 등에서 환자가 처방전을 직접(바코드 혹은 큐알) 보여주어 간편하게 정보를 전송및 응답가능하도록)
"""

from flask import Flask, request, jsonify, json
from flask_restful import reqparse, Api, Resource
import config
import dbconnect
import json

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
            # json 데이터 post로 받아서 변수 저장
            _content = request.get_json()
            _insurance = _content['insurance']
            _nursesign = _content['nursing_institution_sign']
            _grantnum = _content['grant_number']
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
            _usepreiod = _content["injection_prescription"]["period_of_use"]
            _dispensename = _content["injection_prescription"]["preparation"]["name_of_dispenser"]
            _pharmacistname = _content["injection_prescription"]["preparation"]["pharmacist"]["name"]
            _pharmacistseal = _content["injection_prescription"]["preparation"]["pharmacist"]["seal"]
            _preparationamount = _content["injection_prescription"]["preparation_amount"]
            _preparationyear = _content["injection_prescription"]["year_of_preparation"]
            _changeprescription = _content["injection_prescription"]["change_of_prescription"]
            
            _query = "INSERT INTO prescription(insurance, nurse_sign, grant_num, patient_name, patient_reginum, ins_name, ins_phonenum, ins_fax, ins_email, diseasecode_1, diseasecode_2, doctor_name, doctor_type, doctor_num, medi_name, medi_dose, medi_dailydose, medi_totalday, medi_usage, medi_inside, period_use, dispenser_name, pharmacist_name, pharmacist_seal, preparation_amount, year_preparation, change_prescription) values( %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)"
            print(_query)
            _value = (_insurance ,_nursesign, _grantnum, _patientname ,_patientreginum ,_insname , _insphonenum , _insfaxnum , _insemail ,str(_diseasecode1) ,str(_diseasecode2),_doctorname , _doctortype , _doctornum ,str(_mediname) ,str(_medidose) ,str(_medidailydose) ,str(_meditotalday) , str(_mediusage) ,str(_mediinside) ,_usepreiod ,_dispensename ,_pharmacistname , _pharmacistseal , _preparationamount ,_preparationyear , _changeprescription )
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
            return {'error': e}
        
    def get(self):
        try:
            # json 데이터 post로 받아서 변수 저장
            _query = "select * from prescription"
            cursor.execute(_query)
            _data = cursor.fetchall()
            result= []
            for data in _data:
                _insurance = data[1]
                _nursesign = data[2]
                _grantnum = data[3]
                _patientname = data[4]
                _patientreginum = data[5]
                _insname = data[6]
                _insphonenum = data[7]
                _insfaxnum = data[8]
                _insemail = data[9]
                _diseasecode1 = data[10]
                _diseasecode2 = data[11]
                _doctorname = data[12]
                _doctortype = data[13]
                _doctornum = data[14]
                _mediname = data[15]
                _medidose = data[16]
                _medidailydose = data[17]
                _meditotalday = data[18]
                _mediusage = data[19]
                _mediinside = data[20]
                _usepreiod = data[21]
                _dispensename = data[22]
                _pharmacistname = data[23]
                _pharmacistseal = data[24]
                _preparationamount = data[25]
                _preparationyear = data[26]
                _changeprescription = data[27]
                tempjson= { "insurance":_insurance ,"nursesign": _nursesign,"grantnum": _grantnum , "patientname":_patientname ,"patientreginum" :_patientreginum ,"insname" : _insname ,"insphonenum": _insphonenum ,"insfaxnum": _insfaxnum , "insemail": _insemail ,"diseasecode1": _diseasecode1 ,"diseasecode2": _diseasecode2,"doctorname": _doctorname ,"doctortype": _doctortype ,"doctornum": _doctornum ,"mediname": _mediname ,"medidose": _medidose ,"medidailydose":_medidailydose ,"meditotalday" :_meditotalday , "mediusage":_mediusage ,"mediinside": _mediinside ,"usepreiod": _usepreiod ,"dispensename": _dispensename ,"pharmacistname": _pharmacistname , "pharmacistseal": _pharmacistseal ,"preparationamount": _preparationamount ,"preparationyear": _preparationyear , "changeprescription": _changeprescription }
                result.append(tempjson)
            # resultjson = json.dumps(result)  
            return result
        except Exception as e:
            return {'error': e}