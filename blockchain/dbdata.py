'''
db 연결 설정 코드입니다
'''
from flask_restful import reqparse, Resource, Api
from flask import request, Flask
from flaskext.mysql import MySQL
import config

app = Flask(__name__)
api = Api(app)

# MySQL 연결 세팅
app.config['MYSQL_DATABASE_USER'] = config._DB_CONF['user']
app.config['MYSQL_DATABASE_PASSWORD'] = config._DB_CONF['passwd']
app.config['MYSQL_DATABASE_DB'] = config._DB_CONF['db']
app.config['MYSQL_DATABASE_HOST'] = config._DB_CONF['host']
app.config['MYSQL_DATABASE_PORT'] = config._DB_CONF['port']

# MySQL 연결
mysql = MySQL()
mysql.init_app(app)
conn = mysql.connect()
cursor = conn.cursor()
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