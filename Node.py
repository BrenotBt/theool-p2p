import socket
from SocketCommunication import SocketCommunication
from BlockchainUtils import BlockchainUtils


class Node():

    def __init__(self, key=None):
        self.p2p = None
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = 8866

    def startP2P(self):
        self.p2p = SocketCommunication(self.ip, self.port)
        self.p2p.start_socket_communication(self)
