import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request

""""""

@app.route('/transactions/new', methods =['POST'])
def new_transaction():
    values = request.get_json()
    
    # 요청된 필드가 POST 된 데이터인지 확인하는 
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400
    
    # 새로운 거래 생성
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
    
    response = {'message' : f'Transaction will be added to Block {index}'}
    return jsonify(response), 201