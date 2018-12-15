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
  - disease classification code : string
  - sign of prescription medical practitioner : string
  - license type : string
  - license number : string
  - prescription medicine : object 
    - name of medicines : string
    - one dose : string
    - number of daily doses : string
    - total dosing days :string
    - usage : string
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
  - disease classification code : string
  - sign of prescription medical practitioner : string
  - license type : string
  - license number : string
  - issue date : date
- RESPONSE
  - status : true / false
  - message : string

### 환자 to 환자
  


