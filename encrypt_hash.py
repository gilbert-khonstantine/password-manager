import base64
from Crypto.Cipher import AES
from Crypto import Random
import hashlib
import os 
class Cipher:
    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

class Hash:
	def __init__(self, key):
		self.key = hashlib.sha256(key.encode()).digest()

	def hash(self, plain_text: str):
		return hashlib.blake2b(plain_text.encode(), key= self.key).hexdigest()

def encrypt_text(plain_text):
	key = os.getenv('SECRET_KEY')
	return Cipher(key).encrypt(plain_text)

def decrypt_text(cipher_text):
	key = os.getenv('SECRET_KEY')
	return Cipher(key).decrypt(cipher_text)

def hash_text(text):
	key = os.getenv('SECRET_KEY')
	return Hash(key).hash(text)

# runner
# print(Hash("SECRET_KEY").hash("master_password"))
# print(Cipher("SECRET_KEY").encrypt("password"))
# print(Cipher("SECRET_KEY").decrypt("R4Q98wrGSAZPnmHAdQn6ZIM7CftOp/JmR0LWl1W01mg="))