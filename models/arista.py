class Arista:

    def __init__(self, origen, destino, min_vehiculos, max_vehiculos):
        self.origen = origen
        self.destino = destino
        self.min_vehiculos = min_vehiculos
        self.max_vehiculos = max_vehiculos

    def __repr__(self):
        return (f"Arista(destino={self.destino.id_nodo},"
                f" capacidad_min={self.capacidad_minima},"
                f" capacidad_max={self.capacidad_maxima},"
                f" tiempo_semaforo={self.tiempo_semaforo})")