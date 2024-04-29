class Arista:
    def __init__(self,origen, destino, capacidad_minima, capacidad_maxima, tiempo_semaforo):
        self.origen = origen
        self.destino = destino
        self.capacidad_minima = capacidad_minima if capacidad_minima is not None else 0
        self.capacidad_maxima = capacidad_maxima
        self.tiempo_semaforo = tiempo_semaforo

    def __repr__(self):
        return (f"Arista(destino={self.destino.id_nodo},"
                f" capacidad_min={self.capacidad_minima},"
                f" capacidad_max={self.capacidad_maxima},"
                f" tiempo_semaforo={self.tiempo_semaforo})")