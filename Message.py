from Crypto.PublicKey import RSA
from BlockchainUtils import BlockchainUtils
from Crypto.Signature import PKCS1_v1_5


class Message():
    def __init__(self, messageType, senderConnector, data):
        self.keyPair = RSA.generate(2048)
        self.payload = {}
        self.payload['senderConnector'] = senderConnector
        self.payload['messageType'] = messageType
        self.payload['data'] = data
        self.signature = self.sign()
        self.publicKeyString = self.publicKeyString()
        del self.keyPair

    def toJson(self):
        return self.__dict__

    def sign(self):
        data_hash = BlockchainUtils.hash(self.payload)
        signature = PKCS1_v1_5.new(self.keyPair).sign(data_hash)
        return signature.hex()

    @staticmethod
    def signatureValid(data):
        try:
            signature = bytes.fromhex(data.signature)
            data_hash = BlockchainUtils.hash(data.payload)
            public_key = RSA.importKey(data.publicKeyString)
            return PKCS1_v1_5.new(public_key).verify(data_hash, signature)
        except ValueError:
            return False

    def publicKeyString(self):
        return self.keyPair.publickey().exportKey('PEM').decode('utf-8')
