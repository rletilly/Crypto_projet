from spake2 import SPAKE2_B
from pwn import *
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import threading
from cryptography.fernet import Fernet
import base64
import json
import os
from ImportAccounts import writeAccounts,readAccounts
os.system('clear')
# some constants
InfoBank = b"confirm_Bank"
host = 'localhost'
port = 9999

class Client(threading.Thread):
    def __init__(self, connection, username, password, accounts):
        threading.Thread.__init__(self)
        self.username = username
        self.password = password
        self.accounts = accounts
        self.connection = connection
    
    def __str__(self):
        return str(self.username)

    def send(self, msg):
        self.connection.sendline(msg)
    
    def recv(self):
        return self.connection.recvline().rstrip()

    def handshake(self):
        backend = default_backend()
        infoA = self.username
        infoB = InfoBank
        hkdfA = HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=infoA,backend=backend)
        hkdfB = HKDF(algorithm=hashes.SHA256(),length=32,salt=None,info=infoB,backend=backend)

        q = SPAKE2_B(self.password)
        print(self.password)
        msg_out = q.start()
        self.send(msg_out)
        msg_in = self.recv() # this is message A->B
        key = q.finish(msg_in)
        expected_confirm_A = hkdfA.derive(key)
        confirm_B = hkdfB.derive(key)
        self.send(confirm_B)
        confirm_A = self.recv()
        assert confirm_A == expected_confirm_A
        return key

    def transfer(self):
        status = b'OK'
        secretKey = self.handshake()
        print(secretKey.hex())
        # TODO: do your jobs here
        _secretKey =base64.b64encode(secretKey)
        cipher = Fernet(_secretKey)

        msg_in = self.recv()
        msg_in = cipher.decrypt(msg_in)
        msg_in = msg_in.decode().split(':')
        _from = msg_in[1].encode()
        _accountNumber = int(msg_in[3])
        _to = msg_in[5].encode()
        _amount = int(msg_in[7])

        Accounts = readAccounts()
        print(self.username)
        if _from == self.username :
            for account in Accounts[self.username]['accounts'] :
                if account['accountNumber']== _accountNumber:
                    if account['balance'] < _amount :
                        status = b'Not enough money'
                    else:
                        account['balance'] = int(account['balance']) - int(_amount)
                        Accounts[_to]['accounts'][0]['balance'] =+ _amount
                        status = b'Transfer done'

        else:
            status = b'You are not the owner of the account'

        writeAccounts(Accounts)

        print(msg_in)

        self.send(status)
        return status

def new_request(r):
    username = r.recvline().rstrip()
    print(str(username))
    # TODO: read from the database the corresponding accounts info
    accounts = []
    with open('database.txt','rb') as file :
        lines = file.readlines()

    for line in lines:
        registerLine = line.decode().split(',')
        if registerLine[0].encode() == username :
            account = {'accountNumber': int(registerLine[2][3]), 'balance': int(registerLine[3])}
            accounts.append(account)
            password = registerLine[1].encode()


    client = Client(r, username, password, accounts)
    client.transfer()
    r.close()

if __name__ == "__main__":
    l = listen(port)
    c = l.wait_for_connection()
    new_request(c)
    c.close()
