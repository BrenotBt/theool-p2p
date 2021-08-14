import socket
from SocketCommunication import SocketCommunication


class Node():

    def __init__(self, key=None):
        self.p2p = None
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = 8866

    def startP2P(self):
        self.p2p = SocketCommunication(self.ip, self.port)
        self.p2p.startSocketCommunication(self)
