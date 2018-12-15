import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4
from flask import Flask


class Blockchain(object):
    # Instantiate our Node
    # 우리의 노드를 인스턴스 화
    app = Flask(__name__)

    # Generate a globally unique address for this node
    # 우리 노드의 이름을 임의로 설정
    node_identifier = str(uuid4()).replace('-', '')

    # Instantiate the Blockchain
    # Blockchain 클래스를 인스턴스화
    blockchain = Blockchain()

    # /mine의 endPint를 만든다(get 요청 하는 곳)
    @app.route('/mine', methods=['GET'])
    def mine():
        return "We'll mine a new Block"

    # /transactions/new의 endPoint를 만든다.
    # 우리가 데이터를 보내고 요청을 post하는 곳
    @app.route('/transactions/new', methods=['POST'])
    def new_transactions():
        return "We'll add a new transaction"

    # /chain의 endPoint를 만든다
    # 전체 블록체인을 반환하는 곳
    @app.route('/chain', methods=['GET'])
    def full_chain():
        response = {
            'chain':blockchain.chain,
            'length':len(blockchain.chain),
        }
        return jsonify(response), 200
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port= 5001)