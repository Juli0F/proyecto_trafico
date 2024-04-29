from models.arista import Arista


class Nodo:
    def __init__(self, id, type):
        self.nodo_id = id
        self.type = type
        #self.init = init
        self.aristas = []

    def conectar_a(self, nodo_destino, capacidad_maxima, capacidad_minima, tiempo_semaforo):
        self.aristas.append(Arista(nodo_destino, capacidad_maxima, capacidad_minima, tiempo_semaforo))

    def __repr__(self):
        return f"Nodo({self.nodo_id})"
