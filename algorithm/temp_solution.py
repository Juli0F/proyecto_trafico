from models.Type import Type
from models.arista import Arista
from models.nodo import Nodo
import random

class SolutionAG:

    def __init__(self, nodos, aristas):
        self.poblacion_size = 500
        self.num_generaciones = 100
        self.tasa_mutacion = 0.1
        self.nodos = nodos
        print("Nodos generados",self.nodos)
        self.aristas = aristas
        for arista in self.aristas:
            arista.origen.aristas.append(arista)

    def __fitness(self, solucion, total_vehiculos):
        flujo_total = 0
        capacidad_total = sum(arista.max_vehiculos for nodo in self.nodos.values() for arista in nodo.aristas)

        for nodo_id, tiempos in solucion.items():
            nodo = self.nodos[nodo_id]

            for i, arista in enumerate(nodo.aristas):
                tiempo_porcentaje = tiempos[i]
                capacidad_porcentaje = (arista.max_vehiculos - arista.min_vehiculos) / capacidad_total

                if tiempo_porcentaje >= capacidad_porcentaje:
                    flujo = arista.max_vehiculos
                else:
                    flujo = arista.min_vehiculos + (tiempo_porcentaje / capacidad_porcentaje) * (
                                arista.max_vehiculos - arista.min_vehiculos)

                flujo = min(flujo, arista.max_vehiculos)
                flujo_total += flujo

        flujo_total = min(flujo_total, total_vehiculos)

        return flujo_total

    def __crear_solucion(self):
        solucion = {}
        for nodo in self.nodos.values():
            tiempos = [random.random() for _ in range(len(nodo.aristas))]
            total = sum(tiempos)
            tiempos = [tiempo / total for tiempo in tiempos]
            solucion[nodo.nodo_id] = tiempos
        return solucion

    def __seleccion_ruleta(self, poblacion, total_vehiculos):
        fitness_total = sum(self.__fitness(solucion, total_vehiculos) for solucion in poblacion)

        if fitness_total == 0:
            probabilidades = [1 / len(poblacion) for _ in poblacion]
        else:
            probabilidades = [self.__fitness(solucion, total_vehiculos) / fitness_total for solucion in poblacion]

        indices = list(range(len(poblacion)))
        seleccionados = random.choices(indices, probabilidades, k=len(poblacion))
        return [poblacion[i] for i in seleccionados]

    def __cruzar(self, solucion1, solucion2):
        nueva_solucion = {}
        for nodo_id in solucion1.keys():
            if random.random() < 0.5:
                nueva_solucion[nodo_id] = solucion1[nodo_id]
            else:
                nueva_solucion[nodo_id] = solucion2[nodo_id]
        return nueva_solucion

    def __mutar(self, solucion):
        for nodo_id, tiempos in solucion.items():
            if random.random() < self.tasa_mutacion and len(tiempos) > 0:
                indice = random.randint(0, len(tiempos) - 1)
                tiempos[indice] = random.random()
                total = sum(tiempos)
                tiempos = [tiempo / total for tiempo in tiempos]
                solucion[nodo_id] = tiempos
        return solucion

    def __algoritmo_genetico(self, total_vehiculos):
        poblacion = [self.__crear_solucion() for _ in range(self.poblacion_size)]

        for generacion in range(self.num_generaciones):
            poblacion = self.__seleccion_ruleta(poblacion, total_vehiculos)
            nueva_poblacion = []

            for i in range(0, len(poblacion), 2):
                padre1 = poblacion[i]
                padre2 = poblacion[i + 1]
                hijo1 = self.__cruzar(padre1, padre2)
                hijo2 = self.__cruzar(padre1, padre2)
                hijo1 = self.__mutar(hijo1)
                hijo2 = self.__mutar(hijo2)
                nueva_poblacion.append(hijo1)
                nueva_poblacion.append(hijo2)

            poblacion = nueva_poblacion

        mejor_solucion = max(poblacion, key=lambda  solucion: self.__fitness(solucion, total_vehiculos))
        return mejor_solucion

    def __presentar_solucion(self, mejor_solucion, total_vehiculos):
        flujo_acumulado = {nodo_id: 0 for nodo_id in self.nodos.keys()}
        nodo_entrada = next(iter(self.nodos))
        flujo_acumulado[nodo_entrada] = total_vehiculos

        visitados = set()
        cola = [nodo_entrada]

        while cola:
            nodo_id = cola.pop(0)
            if nodo_id in visitados:
                continue
            visitados.add(nodo_id)

            nodo = self.nodos[nodo_id]
            tiempos = mejor_solucion[nodo_id]

            total_tiempo = sum(tiempos)
            tiempos_normalizados = [tiempo / total_tiempo for tiempo in tiempos]

            for i, arista in enumerate(nodo.aristas):
                tiempo_porcentaje = tiempos_normalizados[i]
                flujo = min(flujo_acumulado[nodo_id], arista.max_vehiculos)
                flujo_arista = int(flujo * tiempo_porcentaje)
                flujo_acumulado[arista.destino.id] += flujo_arista

                print(
                    f"{nodo_id} -> {arista.destino.id}: [{{Porcentaje de tiempo: {tiempo_porcentaje:.2f}}}, {{Vehiculos: {flujo_arista}}}]")

                if arista.destino.id not in visitados:
                    cola.append(arista.destino.id)

    def exec(self):
        mejor_solucion = self.__algoritmo_genetico(300)
        print("Mejor solución encontrada:")
        print(self.__presentar_solucion(mejor_solucion,300))