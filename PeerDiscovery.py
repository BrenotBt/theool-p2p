import json
import os.path
import random


seeds_path = os.path.abspath(os.curdir)+'\\peers.json'

class PeerDiscovery:

    def __init__(self, node):
        self.socketCommunication = node
        self.peers = []
        self.load_peers()

    def load_peers(self):
        if os.path.isfile(seeds_path):
            with open(seeds_path) as f:
                self.peers = json.load(f)

    def peer_ip(self):
        return random.choice(self.peers)

    def add_peer(self, data):
        self.peers.append(data)
        with open(seeds_path) as f:
            json.dump(self.peers, f)

    def peer_register(self, message):
        payload = message.payload
        ip = payload['senderConnector']['ip']
        if ip not in self.peers:
            self.add_peer(ip)