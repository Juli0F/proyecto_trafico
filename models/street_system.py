import json
from enum import Enum

from models.Type import Type


class StreetSystem:
    def __init__(self):
        self.nodes = []
        self.edges = []

    def save(self, file_path):
        data = {
            'nodes': [{**node, 'node_type': node.get('node_type', None)} for node in self.nodes],
            'edges': self.edges
        }
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2, cls=MyEncoder)

    def load(self, file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
            self.nodes = [{**node, 'node_type': Type(node['node_type']) if 'node_type' in node else None} for node in
                          data['nodes']]
            self.edges = data['edges']

            # self.nodes = [{**node, 'node_type': node.get('node_type', None)} for node in data['nodes']]
            # self.edges = data['edges']

    def remove_node(self, node_id):
        node = next((node for node in self.nodes if node['node_id'] == node_id), None)
        if node:
            self.nodes = [n for n in self.nodes if n['node_id'] != node_id]

            self.edges = [edge for edge in self.edges if
                          edge['source_node'] != node_id and edge['target_node'] != node_id]
            print(f"Nodo {node_id} eliminado")
        else:
            print(f"No se encontró el nodo con ID {node_id}")

    def add_node(self, node):
        existing_node = next((n for n in self.nodes if n['node_id'] == node['node_id']), None)
        if existing_node is None:
            self.nodes.append(node)
            print(f"Nodo {node['node_id']} agregado")
        else:
            print(f"El nodo con ID {node['node_id']} ya existe")
            node['node_id'] = node['node_id'] + 1
            self.add_node(node)
        if 'node_type' not in node:
            node['node_type'] = Type.NORMAL

    def update_node_type(self, node_id, node_type):
        for node in self.nodes:
            if node['node_id'] == int(node_id):
                node['node_type'] = node_type
                break

    def add_edge(self, edge):
        self.edges.append(edge)


    def remove_edge(self, edge):
        self.edges.remove(edge)

    def get_nodes(self):
        return self.nodes

    def get_edges(self):
        return self.edges

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        return json.JSONEncoder.default(self, obj)