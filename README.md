# server
[![Meari](http://img.youtube.com/vi/-oMePyByb9A/0.jpg)](http://www.youtube.com/watch?v=-oMePyByb9A "Meari")
![poster](https://user-images.githubusercontent.com/19237348/50034937-bbcb1180-0042-11e9-9304-c45edb8785c4.jpg)





# API

----------------------------------------

### 기관 to 환자

1. `get` 처방전 발급 /send/prescription/

- REQUEST
  - insurance : string (의료보험 / 의료급여 / 산재보험 / 자동차보험 / 기타 )
  - nursing institution sign : string
  - grant number : string (2018년 12월 16일 ~ 제 01232호 )
  - patient : object
    - name : string
    - registration number : string
  - medical Institutions : object
    - name : string
    - phone number : string
    - Fax number : string
    - email address : string
  - disease classification codes : object
    - code : string
  - sign of prescription medical practitioner : string
  - license type : string
  - license number : string
  - prescription medicine : object 
    - name of medicines : string
    - one dose : string
    - number of daily doses : string
    - total dosing days :string
    - usage : string
    - inside : true / false
  - injection prescription : object
    - in_house_prescription : true / false
    - name_of_medicines : string
    - one_dose : string
    - number_of_daily doses : string
    - total_dosing_days :string
    - notes_on_preparation : string
  - period_of_use : string
  - preparation : object
    - name_of_dispenser : string
    - pharmacist : string
      - name : string
      - seal : string
    - preparation_amount : string
    - year_of_preparation : string
  - change_of_prescription : string

**example**
```markdown
{
  "insurance" : "1" , //1 - 의료보험, 2 - 의료급여, 3 - 산재보험, 4 - 자동차보험, 5 - 기타 )
  "nursing_institution_sign" : "346454",
  "grant_number" : "2018년 12월 16일 ~ 제 01232호",
  "patient" : {
    "name" : "박채현",
    "registration_number" : "930483-2285734"
  },
  "medical_Institutions" : {
    "name" : "서울대병원",
    "phone_number" : "010-8111-8888",
    "fax_number" : "02-853-4444",
    "email_address" : "snubi@snu.ac.kr"
  },
  "disease_classification_codes" : [{
    "code" : "H208"
  },{
    "code" : "A01"
  }],
  "sign_of_prescription_medical_practitioner" : "김의사",
  "license_type" : "의사",
  "license_number" : "AA45235TB2",
  "prescription_medicine" : [{
    "name_of_medicines" : "솔로젠정",
    "one_dose" : "2",
    "number_of_daily_doses" : "3",
    "total_dosing_days" :"2",
    "usage" : "식후30분",
    "inside" : true
  },  {
    "name_of_medicines" : "프레드포르테점안액",
    "one_dose" : "0.8333",
    "number_of_daily_doses" : "6",
    "total_dosing_days" :"1",
    "usage" : "2시간마다",
    "inside" : false
  }],
  "injection_prescription" :{
  
  "period_of_use" : "3",
  "preparation_amount" : "7",
  "year_of_preparation" : "2018년 12월 16일",
  "preparation" : {
    "name_of_dispenser" : "서울약국",
    "pharmacist" : {
      "name" : "김약사",
      "seal" : "/seal/kimStamp.img"
    }
    
  },
  "change_of_prescription" : ""
}
```
- RESPONSE
  - status : true / false
  - message : string

2. `get` 영상자료 발급 /send/file/

- REQUEST
  - patient : object
    - name : string
    - registration number : string
  - medical_Institutions : object
    - name : string
    - phone_number : string
    - fax_number : string
    - email_address : string
  - disease_classification codes : object
    - code : string
  - sign_of_prescription_medical practitioner : string
  - license_type : string
  - license_number : string
  - issue_date : date
  - filelink : string

- RESPONSE
  - status : true / false
  - message : string

**example**
```markdown
{
  status : false
  message : "전송이 실패하였습니다."
}
```
### 환자 to 기관
1. `post` 처방전 발급 /agency/prescription/

- REQUEST
  - insurance : string (의료보험 / 의료급여 / 산재보험 / 자동차보험 / 기타 )
  - nursing_institution sign : string
  - grant_number : string (2018년 12월 16일 ~ 제 01232호 )
  - patient : object
    - name : string
    - registration_number : string
  - medical_Institutions : object
    - name : string
    - phone_number : string
    - fax_number : string
    - email_address : string
  - disease_classification codes : object
    - code : string
  - sign_of_prescription medical practitioner : string
  - license_type : string
  - license_number : string
  - prescription_medicine : object 
    - name_of_medicines : string
    - one_dose : string
    - number_of_daily doses : string
    - total_dosing_days :string
    - usage : string
    - inside : true / false
  - injection_prescription : object
    - in_house_prescription : true / false
    - name of medicines : string
    - one dose : string
    - number of daily doses : string
    - total dosing days :string
    - notes on preparation : string
  - period of use : string
  - preparation : object
    - name of dispenser : string
    - pharmacist : string
      - name : string
      - seal : string
    - preparation amount : string
    - year of preparation : string
  - change of prescription : string

- RESPONSE
  - status : true / false
  - message : string

2. `post` 영상자료 발급 /agency/file/

- REQUEST
  - patient : object
    - name : string
    - registration_number : string
  - medical_Institutions : object
    - name : string
    - phone_number : string
    - Fax_number : string
    - email_address : string
  - disease_classification_codes : object
    - code : string
  - sign_of_prescription_medical_practitioner : string
  - license_type : string
  - license_number : string
  - issue_date : date
  - filelink : string

**example**
```markdown
{
  "patient" : [{
    "name" : "전가빈"
    "registration_number" : "990802-2123212"
  }]
  "medical_Institutions" : [{
    "name" : "서울대병원",
    "phone_number" : "010-8111-8888",
    "fax_number" : "02-853-4444",
    "email_address" : "snubi@snu.ac.kr"
  }]
  "disease_classification_codes" : [{
    "code" : "H208"
  },{
    "code" : "A01"
  }],
  "sign_of_prescription_medical_practitioner" : "김의사",
  "license_type" : "의사",
  "license_number" : "AA45235TB2",
  "issue_date" : "2018년 12월 16일"
  "filelink" : "http://mriVideo.com/jeonMri.mp4"
}
```

- RESPONSE
  - status : true / false
  - message : string

**example**
```markdown
{
  status : true
  message : "전송이 완료 되었습니다."
}
```



