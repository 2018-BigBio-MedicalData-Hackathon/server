import hashlib
import json

from time import time
from uuid import uuid4

from flask import Flask, jsonify, request 

@app.route('/mine', methods = ['GET'])
def mine():
    #다음 블록의 proof 값을 얻어내기 위해 POW 알고리즘을 수행한다. 
    last_block = blockchain.last_block
    last_proof = last_block['proof']
    proof = blockchain.proof_of_work(last_proof)
    
    #proof 값을 찾으면(채굴에 성공하면) 보상을 준다.
    #sender의 주소를 0으로 한다. (원래 거래는 송신자, 수신자가 있어야 하는데 챌굴에 대한 보상으로 얻은 코인은 sender 가 없다.)
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1,
    )
    
    #
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)
    
    response = {
        'message' : "New Block Forged",
        'index' : block['index'],
        'transactions' : block['transactions'],
        'proof' : block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), 200