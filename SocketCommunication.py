from Message import Message
from BlockchainUtils import BlockchainUtils
from SocketConnector import SocketConnector
from SeedDiscovery import SeedDiscovery
from PeerDiscovery import PeerDiscovery
from PeerDiscoveryHandler import PeerDiscoveryHandler
from p2pnetwork.node import Node
import json


class SocketCommunication(Node):

    def __init__(self, ip, port):
        self.ip = ip
        self.seed_ip = ''
        self.port = port
        super(SocketCommunication, self).__init__(ip, port, None)
        self.peers = []
        self.peerDiscovery = PeerDiscovery(self)
        self.seedDiscovery = SeedDiscovery(self)
        self.peerDiscoveryHandler = PeerDiscoveryHandler(self)
        self.socketConnector = SocketConnector(ip, port)


    def connectToSeed(self):
        if not (self.seedDiscovery.is_seed(self.ip)):
            self.seed_ip = self.seedDiscovery.seed_ip()
            self.connect_with_node(self.seed_ip, self.port)
            messageType = 'PEERREGISTER'
            senderConnector = {"ip": self.ip, "port": self.port}
            data = self.peers
            message = Message(messageType, senderConnector, data)
            self.seedDiscovery.handshake_message(message)

    def startSocketCommunication(self, node):
        self.node = node
        self.start()
        self.peerDiscoveryHandler.start()
        self.connectToSeed()

    def inbound_node_connected(self, connected_node):
        self.peerDiscoveryHandler.handshake(connected_node)

    def outbound_node_connected(self, connected_node):
        self.peerDiscoveryHandler.handshake(connected_node)

    def node_message(self, connected_node, message):
        message = BlockchainUtils.decode(json.dumps(message))
        if handshake_message.payload['messageType'] == 'PEERREGISTER':
            self.peerDiscovery.handle_message(message)
        """
        elif message.messageType == 'DISCOVERY':
            self.peerDiscoveryHandler.handleMessage(message)
        elif message.messageType == 'TRANSACTION':
            transaction = message.data
            self.node.handleTransaction(transaction)
        elif message.messageType == 'BLOCK':
            block = message.data
            self.node.handleBlock(block)
        elif message.messageType == 'BLOCKCHAINREQUEST':
            self.node.handleBlockchainRequest(connected_node)
        elif message.messageType == 'BLOCKCHAIN':
            blockchain = message.data
            self.node.handleBlockchain(blockchain)
        """

    def send(self, receiver, message):
        self.send_to_node(receiver, message)

    def broadcast(self, message):
        self.send_to_nodes(message)
