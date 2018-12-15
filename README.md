# server

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
    - in-house prescription : true / false
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

  example
  ```markdown
  {
    "insurance" : "1" ,//1 - 의료보험, 2 - 의료급여, 3 - 산재보험, 4 - 자동차보험, 5 - 기타 )
    "nursing institution sign" : "346454",
    "grant number" : "2018년 12월 16일 ~ 제 01232호",
    "patient" : {
      "name" : "박채현",
      "registration number" : "930483-2285734"
    },
    "medical Institutions" : {
      "name" : "서울대병원",
      "phone number" : "010-8111-8888",
      "Fax number" : "02-853-4444",
      "email address" : "snubi@snu.ac.kr"
    },
    "disease classification codes" : [{
      "code" : "H208"
    },{
      "code" : "A01"
    }],
    "sign of prescription medical practitioner" : "김의사",
    "license type" : "의사",
    "license number" : "AA45235TB2",
    "prescription medicine" : [{
      "name of medicines" : "솔로젠정",
      "one dose" : "2",
      "number of daily doses" : "3",
      "total dosing days" :"2",
      "usage" : "식후30분",
      "inside" : true
    },  {
      "name of medicines" : "프레드포르테점안액",
      "one dose" : "0.8333",
      "number of daily doses" : "6",
      "total dosing days" :"1",
      "usage" : "2시간마다",
      "inside" : false
    }],
    "injection prescription" :[{
    
    "period of use" : "3",
    "preparation" : {
      "name of dispenser" : "서울약국",
      "pharmacist" : {
        "name" : "김약사",
        "seal" : "/seal/kimStamp.img"
      },
      "preparation amount" : "7",
      "year of preparation" : "2018년 12월 16일"
    },
    "change of prescription" : ""
  }]
}
  ```
- RESPONSE
  - status : true / false
  - message : string

2. `get` MRI 발급 /send/mri/

- REQUEST
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
  - issue date : date
- RESPONSE
  - status : true / false
  - message : string

### 환자 to 환자
  


