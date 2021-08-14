from Node import Node


if __name__ == '__main__':
    node = Node()
    node.startP2P()

    if not (node.p2p.seedDiscovery.is_seed(node.ip)):
        node.p2p.connect_with_node()
