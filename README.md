# server

![poster](https://user-images.githubusercontent.com/19237348/50034937-bbcb1180-0042-11e9-9304-c45edb8785c4.jpg)





# API

----------------------------------------

### 기관 to 환자

1. `get` 처방전 발급 /send/prescription/

 - REQUEST

  - 보험 여부 (의료보험 / 의료보험 / 산재보험 / 자동차보험 / 기타 )
    - 요양기관기호
    - 교부번호 (2018년 12월 16일 ~ 제 01232호 )
    - 환자
      - 성명
      - 주민등록번호
    - 의료기관
      - 명칭
      - 전화번호
      - 팩스번호
      - email 주소
    - 질병분류기호
    - 처방 의료인의 성명(디지털 날인)
    - 면허 종별 (의사)
    - 면허번호(제 53253 호)
    - 처방의약품
      - 의약품 명칭
      - 1회 투여량
      - 1일 투여횟수
      - 총 투약일수
      - 용법
    - 주사제 처방 냬역 (원내조제, 원외처방)
    - 조제시 참고 사항
    - 사용기간
    - 조제내역
      - 조제기관의 명칭
      - 조제약사
        - 성명
        - 날인
      - 조제량
      - 조제년원일
    - 처방의 변경 수정 확인 대체시 그 내용 등
  - RESPONSE
    - status : true / false
    - message : string

2. `get` MRI 발급 /send/mri/

- REQUEST
  - patient : object
    - name : string
    - registration number : string
  - Medical Institutions : object
    - name : string
    - phone number : string
    - Fax number : string
    - email address : string
  - disease classification code : string
  - sign of prescription medical practitioner : string
  - License type : string
  - License number : string
  - Issue date : date
- RESPONSE
  - status : true / false
  - message : string

### 환자 to 환자
  


