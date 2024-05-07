import random

from models.Type import Type
from models.config import POBLACION_SIZE, TASA_MUTACION, GENERACIONES


class GeneticAlgorithm:
    def __init__(self, nodos, aristas, poblacion_size, num_generaciones, tasa_mutacion):
        self.nodos = nodos
        self.aristas = aristas
        self.poblacion_size = poblacion_size
        self.num_generaciones = num_generaciones
        self.tasa_mutacion = tasa_mutacion
        print(f"Configuracion:\n Poblacion: {poblacion_size}\nGeneracion {num_generaciones}\nTasa Mutacion: {tasa_mutacion}")

    def initialize_population(self):
        poblacion = []
        for _ in range(self.poblacion_size):
            individual = {}
            for nodo in self.nodos.values():
                if nodo.type != Type.SALIDA:
                    tiempos = {arista.destino.nodo_id: random.random() for arista in nodo.aristas}
                    total_tiempo = sum(tiempos.values())
                    tiempos_normalizados = {destino_id: tiempo / total_tiempo for destino_id, tiempo in tiempos.items()}
                    individual[nodo.nodo_id] = tiempos_normalizados
            poblacion.append(individual)
            print("Poblacion generada", poblacion)
        return poblacion

    def fitness(self, individual, total_vehiculos):
        flujo_total = 0
        capacidad_total = sum(arista.max_vehiculos for nodo in self.nodos.values() for arista in nodo.aristas)
        subutilizacion_total = 0

        for nodo in self.nodos.values():
            if nodo.type == Type.ENTRADA:
                for arista in nodo.aristas:
                    tiempo_porcentaje = individual[nodo.nodo_id][arista.destino.nodo_id]
                    capacidad_porcentaje = (arista.max_vehiculos - arista.min_vehiculos) / capacidad_total

                    if tiempo_porcentaje >= capacidad_porcentaje:
                        flujo = arista.max_vehiculos
                    else:
                        flujo = arista.min_vehiculos + (tiempo_porcentaje / capacidad_porcentaje) * (
                                    arista.max_vehiculos - arista.min_vehiculos)

                    flujo = min(flujo, arista.max_vehiculos)
                    flujo_total += flujo

                    flujo_potencial = arista.min_vehiculos + (
                                capacidad_porcentaje * (arista.max_vehiculos - arista.min_vehiculos))
                    subutilizacion = max(0, flujo_potencial - flujo)
                    subutilizacion_total += subutilizacion

        fitness_score = flujo_total - 0.1 * subutilizacion_total
        print(f"Fitness : {fitness_score}")
        return fitness_score

    def roulette_selection(self, poblacion, total_vehiculos):
        fitness_total = sum(self.fitness(individual, total_vehiculos) for individual in poblacion)

        if fitness_total == 0:
            probabilidades = [1 / len(poblacion) for _ in poblacion]
        else:
            probabilidades = [self.fitness(individual, total_vehiculos) / fitness_total for individual in poblacion]

        indices = list(range(len(poblacion)))
        seleccionados = random.choices(indices, probabilidades, k=len(poblacion))
        return [poblacion[i] for i in seleccionados]

    def crossover(self, parent1, parent2):
        offspring = {}
        for nodo_id in parent1.keys():
            if random.random() < 0.5:
                offspring[nodo_id] = parent1[nodo_id]
            else:
                offspring[nodo_id] = parent2[nodo_id]
        return offspring

    def mutate(self, individual):
        for nodo_id, tiempos in individual.items():
            if random.random() < self.tasa_mutacion and len(tiempos) > 0:
                destino_id = random.choice(list(tiempos.keys()))
                tiempos[destino_id] = random.random()
                total_tiempo = sum(tiempos.values())
                tiempos_normalizados = {destino_id: tiempo / total_tiempo for destino_id, tiempo in tiempos.items()}
                individual[nodo_id] = tiempos_normalizados
        return individual

    def genetic_algorithm(self, total_vehiculos):
        poblacion = self.initialize_population()

        for generacion in range(self.num_generaciones):
            poblacion = self.roulette_selection(poblacion, total_vehiculos)
            nueva_poblacion = []

            for i in range(0, len(poblacion), 2):
                parent1 = poblacion[i]
                parent2 = poblacion[i + 1]
                offspring1 = self.crossover(parent1, parent2)
                offspring2 = self.crossover(parent1, parent2)
                offspring1 = self.mutate(offspring1)
                offspring2 = self.mutate(offspring2)
                nueva_poblacion.append(offspring1)
                nueva_poblacion.append(offspring2)

            poblacion = nueva_poblacion

        mejor_solucion = max(poblacion, key=lambda individual: self.fitness(individual, total_vehiculos))
        return mejor_solucion

    def presentar_solucion(self, mejor_solucion, total_vehiculos):
        resultados = []
        visto = set()
        flujo_acumulado = {nodo.nodo_id: 0 for nodo in self.nodos.values()}
        nodos_entrada = [nodo for nodo in self.nodos.values() if nodo.type == Type.ENTRADA]

        for nodo_entrada in nodos_entrada:
            flujo_acumulado[nodo_entrada.nodo_id] = total_vehiculos // len(nodos_entrada)

        visitados = set()
        cola = [nodo.nodo_id for nodo in nodos_entrada]

        while cola:
            nodo_id = cola.pop(0)
            if nodo_id in visitados:
                continue
            visitados.add(nodo_id)

            nodo = self.nodos[nodo_id]
            if nodo.type == Type.SALIDA:
                continue

            tiempos = mejor_solucion[nodo_id]

            total_tiempo = sum(tiempos.values())
            tiempos_normalizados = {destino_id: tiempo / total_tiempo for destino_id, tiempo in tiempos.items()}

            for arista in nodo.aristas:
                tiempo_porcentaje = tiempos_normalizados[arista.destino.nodo_id]
                flujo = min(flujo_acumulado[nodo_id], arista.max_vehiculos)
                flujo_arista = int(flujo * tiempo_porcentaje)
                flujo_acumulado[arista.destino.nodo_id] += flujo_arista

                print(
                    f"{nodo_id} -> {arista.destino.nodo_id}: [{{Porcentaje de tiempo: {tiempo_porcentaje:.2f}}}, {{Vehiculos: {flujo_arista}}}]")
                # resultado = {
                #     "desde": nodo_id,
                #     "hacia": arista.destino.nodo_id,
                #     "porcentaje_tiempo": f"{tiempo_porcentaje:.2f}",
                #     "vehiculos": flujo_arista
                # }
                resultado = (
                    nodo_id,
                    arista.destino.nodo_id,
                    f"{tiempo_porcentaje:.2f}",
                    flujo_arista
                )
                if resultado not in visto:
                    visto.add(resultado)
                    resultados.append({
                        "desde": nodo_id,
                        "hacia": arista.destino.nodo_id,
                        "porcentaje_tiempo": f"{tiempo_porcentaje:.2f}",
                        "vehiculos": flujo_arista
                    })
                    # resultados.append(resultado)

                if arista.destino.nodo_id not in visitados and arista.destino.type != Type.SALIDA:
                    cola.append(arista.destino.nodo_id)
        print("Fin")

        return resultados