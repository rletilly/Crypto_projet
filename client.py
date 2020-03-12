from spake2 import SPAKE2_A
from pwn import *
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import base64
import json
import os
os.system('clear')

# some constants
InfoBank = b"confirm_Bank"
host = 'localhost'
port = 9999


username = b'A'
password = b'123456'
receiver = b'B'


class Client:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.connection = None

    def connect(self, host, port):
        self.connection = remote(host, port)
        self.send(self.username)

    def send(self, msg):
        self.connection.sendline(msg)
    
    def recv(self):
        return self.connection.recvline().rstrip()

    def close(self):
        self.connection.close()

    def handshake(self):
        backend = default_backend()
        infoA = self.username
        hkdfA = HKDF(algorithm=hashes.SHA256(), length=32,
                     salt=None, info=infoA, backend=backend)
        hkdfB = HKDF(algorithm=hashes.SHA256(), length=32,
                     salt=None, info=InfoBank, backend=backend)
        hs = SPAKE2_A(self.password)
        msg_out = hs.start()
        self.send(msg_out)  # this is message A->B
        msg_in = self.recv()
        key = hs.finish(msg_in)
        confirm_A = hkdfA.derive(key)
        expected_confirm_B = hkdfB.derive(key)
        self.send(confirm_A)
        confirm_B = self.recv()
        assert confirm_B == expected_confirm_B
        return key

    def transfer(self,nb, to, amount):
        secretKey = self.handshake()
        #print(type(secretKey))
        #print(len(secretKey))
        # TODO: transfer `amount` of money from your balance to `to`.
        _secretKey =base64.b64encode(secretKey)
        cipher = Fernet(_secretKey)
        msg_out = str('sender:'+str(self.username.decode())+':accountNumber:'+str(nb)+':receiver:'+str(to.decode())+':amount:'+str(amount)).encode()
        msg_out = cipher.encrypt(msg_out)
        #print(msg_out)
        
        self.send(msg_out)
        
        status = self.recv()
        self.close()
        return status


if __name__ == "__main__":
    client = Client(username, password)
    client.connect(host, port)
    status = client.transfer(1,receiver, 999)
    print(status)
