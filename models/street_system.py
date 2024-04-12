import json

class StreetSystem:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def save(self, file_path):
        data = {
            'nodes': self.nodes,
            'edges': self.edges
        }
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)

    def load(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            self.nodes = data['nodes']
            self.edges = data['edges']

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, edge):
        self.edges.append(edge)

    def remove_node(self, node):
        self.nodes.remove(node)

    def remove_edge(self, edge):
        self.edges.remove(edge)

    def get_nodes(self):
        return self.nodes

    def get_edges(self):
        return self.edges