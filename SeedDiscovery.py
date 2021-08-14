import json
import os.path
import random


class SeedDiscovery:

    def __init__(self):
        self.directory = os.path.abspath(os.curdir)
        self.seed = []
        self.load_seeds()

    def load_seeds(self):
        seeds_path = self.directory+'\\seeds.json'
        with open(seeds_path) as f:
            self.seed = json.load(f)

    def is_seed(self, ip):
        if (ip in self.seed):
            return True
        return False

    def seed_ip(self):
        return random.choice(self.seed)