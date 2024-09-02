import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

import base64
class Criptor():
    def __init__(self):     
        key = os.getenv('ENCRYPTION_KEY')
        if key is None:
            raise ValueError("No encryption key found in environment variables.")
        self.key = key.encode()[:32]  # Asegurarse de que la llave tenga 32 bytes para AES-256

    def encrypt(self, data):
        key = self.key
        cipher = AES.new(key, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
        iv = base64.b64encode(cipher.iv).decode('utf-8')
        ct = base64.b64encode(ct_bytes).decode('utf-8')
        return iv + ct

    def decrypt(self, enc_data):
        key = self.key
        iv = base64.b64decode(enc_data[:24])
        ct = base64.b64decode(enc_data[24:])
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode('utf-8')
