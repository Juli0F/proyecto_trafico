class Arista:

    def __init__(self, origen, destino, min_vehiculos, max_vehiculos):
        self.origen = origen
        self.destino = destino
        self.min_vehiculos = min_vehiculos
        self.max_vehiculos = max_vehiculos
        self.time = 0

    def __repr__(self):
        return (f"Arista(origen={self.origen},"
                f"destino={self.destino},"
                f" capacidad_min={self.min_vehiculos},"
                f" capacidad_max={self.max_vehiculos},"
                f" tiempo = {self.time})\n")
                # f" tiempo_semaforo={self.tiempo_semaforo})")