import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request
import dbdata

DBdata = dbdata.result
class Blockchain(object):
    def __init__(self):
        self.current_transactions=[]
        self.chain=[]
        _content=[]
        #genesis block 생성
        for data in DBdata:
            self.new_block(previous_hash=1, _content=data, proof=100)
        
    def new_block(self, proof, _content, previous_hash=None):
        """
        블록체인에 새로운 블록 만들기 
        :param proof: <int> proof 는 Proof of Work 알고리즘에 의해서 제공된다. 
        :param previous_hash: (Optional) <str> 이전 블록의 해쉬값
        :return : <dict> 새로운 블록
        
        """
        print(_content)
        block = {
            # basic info of block
            'index' : len(self.chain) + 1,
            'timestamp' : time(),
            'transactions' : self.current_transactions,
            'proof' : proof,
            'previous_hash' : previous_hash or self.hash(self.chain[-1]),

            # info of prescription
            '_insurance' : _content['insurance'],
            '_nursesgin' : _content['nursesgin'],
            '_patientname' : _content['patientname'],
            '_patientreginum' : _content['patientreginum'],
            '_insname' : _content["insname"],
            '_insphonenum' : _content["insphonenum"],
            '_insfaxnum' : _content["insfaxnum"],
            '_insemail' : _content["insemail"],
            '_diseasecode1' : _content["diseasecode1"],
            '_diseasecode2' : _content["diseasecode2"],
            '_doctorname' : _content["doctorname"],
            '_doctortype' : _content["doctortype"],
            '_doctornum' : _content["doctornum"],
            '_mediname' : _content["mediname"],
            '_medidose' : _content["medidose"],
            '_medidailydose' : _content["medidailydose"],
            '_meditotalday' : _content["meditotalday"],
            '_mediusage' : _content["mediusage"],
            '_mediinside' : _content["mediinside"],
            '_usepreiod' : _content["usepreiod"],
            '_dispensename' : _content["dispensename"],
            '_pharmacistname' : _content["pharmacistname"],
            '_pharmacistseal' : _content["pharmacistseal"],
            '_preparationamount' : _content["preparationamount"],
            '_preparationyear' : _content["preparationyear"],
            '_changeprescription' : _content["changeprescription"]
        }
        
        #거래 내역 초기화
        self.current_transactions = []
        
        self.chain.append(block)
        return block
    
    def new_transaction(self, sender, recipient, amount):
        """
        다음에 채굴될 블록(새로운 블록)에 들어갈 거래내역 
        
        :param sender : <str> sender의 주소
        :param recipient : <str> recipient의 주소
        :param amount : <int> amount
        :return : <int> 이 거래내역들을 포함하는 블록의 index
        """
        self.current_transactions.append({
            'sender':sender,
            'recipient':recipient,
            'amount':amount,
        })
        
        return self.last_block['index'] + 1
    
    @property
    def last_block(self):
        return self.chain[-1]
    
    @staticmethod
    def hash(block):
        """
        Creates a SHA-256 hash of a Block
        
        :param block: <dict> Block
        :return : <str>
        """
        
        #We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(block_string).hexdigest()

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
    app.run(host='0.0.0.0', port= 5001, debug=True)