
import time

import hashlib
import json

from sympy import true

from flask import Flask, render_template, request, redirect, url_for

print(time.time())

class block:
    
    def __init__(self, index, data, previousHash):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previousHash = previousHash
        self.hash = self.calculate_hash()
    def calculate_hash(self):
        blockString = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previousHash": self.previousHash
        }, sort_keys=True).encode()
        return hashlib.sha256(blockString).hexdigest()
    
def creategenisisBlock():
    return block(0, "genesisBlock", "0")

class blockChain():
    
    def __init__(self):
        self.chain = [creategenisisBlock()]
    def getlatestBlock(self):
        return self.chain[-1]
    def addBlock(self, data):
        latestBlock = self.getlatestBlock()
        newBlock = block(
            index=latestBlock.index + 1,
            data=data,
            previousHash=latestBlock.hash
        )
        self.chain.append(newBlock)

fincoin = blockChain()
balance = 0

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html", amount=balance, blockchain=fincoin.chain)

@app.route('/add', methods=['POST'])
def add_transaction():
    global balance
    amount = int(request.form['amount'])
    balance += amount
    fincoin.addBlock(balance)
    return redirect(url_for('index'))

@app.route('/reset', methods=['POST'])
def reset_balance():
    global balance
    global fincoin
    global chain
    for block in fincoin.chain:
        print(f"Index: {block.index}, Data: {block.data}, Hash: {block.hash}")
    fincoin.chain = [creategenisisBlock()]
    balance = 0
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)