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

    def start_socket_communication(self, node):
        self.node = node
        self.start()
        self.peerDiscoveryHandler.start()

    def inbound_node_connected(self, connected_node):
        self.peerDiscoveryHandler.handshake(connected_node)

    def outbound_node_connected(self, connected_node):
        self.peerDiscoveryHandler.handshake(connected_node)

    def node_message(self, connected_node, message):
        message = BlockchainUtils.decode(json.dumps(message))
        print('node_message = ', message.toJson())
        if message.payload['messageType'] == 'PEERREGISTER':
            self.peerDiscovery.peer_register(message)
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
        #print(receiver, message.toJson())
        self.send_to_node(receiver, message)

    def broadcast(self, message):
        self.send_to_nodes(message)
