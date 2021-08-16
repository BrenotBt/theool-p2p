import threading
import time
from Message import Message
from BlockchainUtils import BlockchainUtils


class PeerDiscoveryHandler():

    def __init__(self, node):
        self.socketCommunication = node

    def start(self):
        statusThread = threading.Thread(target=self.status, args=())
        statusThread.start()
        if not (self.socketCommunication.seedDiscovery.is_seed(self.socketCommunication.ip)):
            seedThread = threading.Thread(target=self.connect_to_seed, args=())
            seedThread.start()
        #discoveryThread = threading.Thread(target=self.discovery, args=())
        #discoveryThread.start()

    def status(self):
        while True:
            print('Current Connections:')
            for peer in self.socketCommunication.peers:
                print(str(peer.ip) + ':' + str(peer.port))
            time.sleep(5)

    def connect_to_seed(self):
        while True:
            print('PEERREGISTER')
            self.socketCommunication.connect_with_node(
                self.socketCommunication.seedDiscovery.seed_ip(),
                self.socketCommunication.port
            )
            time.sleep(60)

    def handshake(self, connected_node, refresh_seed=False):
        if refresh_seed or (not (self.socketCommunication.seedDiscovery.is_seed(self.socketCommunication.ip)) and not self.socketCommunication.peers):
            handshake_message = self.connect_to_seed_message()
        else:
            handshake_message = self.handshakeMessage()
        self.socketCommunication.send(connected_node, handshake_message)

    def discovery(self):
        while True:
            handshakeMessage = self.handshakeMessage()
            self.socketCommunication.broadcast(handshakeMessage)
            time.sleep(10)

    def connect_to_seed_message(self):
        messageType = 'PEERREGISTER'
        senderConnector = {"ip": self.socketCommunication.ip, "port": self.socketCommunication.port}
        data = self.socketCommunication.peers
        message = Message(messageType, senderConnector, data)
        encodedMessage = BlockchainUtils.encode(message)
        return encodedMessage

    def handshakeMessage(self):
        ownConnector = self.socketCommunication.socketConnector
        ownPeers = self.socketCommunication.peers
        data = ownPeers
        messageType = 'DISCOVERY'
        message = Message(ownConnector, messageType, data)
        encodedMessage = BlockchainUtils.encode(message)
        return encodedMessage
    """
    
    def handleMessage(self, message):
        peersSocketConnector = message.senderConnector
        peersPeerList = message.data
        newPeer = True
        for peer in self.socketCommunication.peers:
            if peer.equals(peersSocketConnector):
                newPeer = False
        if newPeer:
            self.socketCommunication.peers.append(peersSocketConnector)

        for peersPeer in peersPeerList:
            peerKnown = False
            for peer in self.socketCommunication.peers:
                if peer.equals(peersPeer):
                    peerKnown = True
            if not peerKnown and not peersPeer.equals(self.socketCommunication.socketConnector):
                self.socketCommunication.connect_with_node(
                    peersPeer.ip, peersPeer.port)
    """
