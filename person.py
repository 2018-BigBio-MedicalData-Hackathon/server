

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
            print()
        except Exception as e:
            return {'error': 500}
    
    #서버에 저장된 처방전 들고오기
    def get(self):
        try:
            username = request.args.get('username')
            print(username)
            # json 데이터 post로 받아서 변수 저장
            _query = "select * from prescription where patient_name=%s"%(username)
            print(_query)
            cursor.execute(_query)
            data = cursor.fetchall()
            print(data)
            data=data[0]
            _insurance = data[0]
            _nursesign = data[1]
            _grantnum = data[2]
            _patientname = data[3]
            _patientreginum = data[4]
            _insname = data[5]
            _insphonenum = data[6]
            _insfaxnum = data[7]
            _insemail = data[8]
            _diseasecode1 = data[9]
            _diseasecode2 = data[10]
            _doctorname = data[11]
            _doctortype = data[12]
            _doctornum = data[13]
            _mediname = data[14]
            _medidose = data[15]
            _medidailydose = data[16]
            _meditotalday = data[17]
            _mediusage = data[18]
            _mediinside = data[19]
            _usepreiod = data[20]
            _dispensename = data[21]
            _pharmacistname = data[22]
            _pharmacistseal = data[23]
            _preparationamount = data[24]
            _preparationyear = data[25]
            _changeprescription = data[26]
            result= { "insurance":_insurance ,"nursesgin": _nursesign, "patientname":_patientname ,"patientreginum" :_patientreginum ,"insname" : _insname ,"insphonenum": _insphonenum ,"insfaxnum": _insfaxnum , "insemail": _insemail ,"diseasecode1": _diseasecode1 ,"diseasecode2": _diseasecode2,"doctorname": _doctorname ,"doctortype": _doctortype ,"doctornum": _doctornum ,"mediname": _mediname ,"medidose": _medidose ,"medidailydose":_medidailydose ,"meditotalday" :_meditotalday , "mediusage":_mediusage ,"mediinside": _mediinside ,"usepreiod": _usepreiod ,"dispensename": _dispensename ,"pharmacistname": _pharmacistname , "pharmacistseal": _pharmacistseal ,"preparationamount": _preparationamount ,"preparationyear": _preparationyear , "changeprescription": _changeprescription }
                
            # resultjson = json.dumps(result)  
            return result
        except Exception as e:
            return {'error': e}