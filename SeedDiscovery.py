from BlockchainUtils import BlockchainUtils
import json
import os.path
import random


class SeedDiscovery:

    def __init__(self, node):
        self.socketCommunication = node
        self.directory = os.path.abspath(os.curdir)
        self.seeds = []
        self.load_seeds()

    def load_seeds(self):
        seeds_path = self.directory+'/seeds.json'
        if os.path.exists(seeds_path):
            with open(seeds_path, "r") as f:
                self.seeds = json.load(f)
        else:
            with open(seeds_path, "w+") as f:
                self.seeds = json.load(f)

    def is_seed(self, ip):
        if (ip in self.seeds):
            return True
        return False

    def seed_ip(self):
        return random.choice(self.seeds)

    def handshake_message(self, handshake_message):
        self.socketCommunication.send(self.seed_ip, handshake_message)
