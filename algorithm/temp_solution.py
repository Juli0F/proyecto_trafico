from models.Type import Type
from models.arista import Arista
from models.nodo import Nodo
import random

class SolutionAG:

    def __init__(self, nodos, aristas):
        self.population_size = 100
        self.mutation_rate = 0.01
        self.crossover_rate = 0.7
        self.generations = 100
        self.nodos = nodos
        print("Nodos generados",self.nodos)
        self.aristas = aristas
        for arista in self.aristas:
            arista.origen.aristas.append(arista)

    # def initialize_population(self):
    #     for _ in range(self.population_size):
    #         individual = {}
    #         for nodo in self.nodos:
    #             if nodo.type != Type.SALIDA:
    #                 total_aristas = len(nodo.aristas)
    #                 individual[nodo.nodo_id] = [1 / total_aristas] * total_aristas
    #         self.population.append(individual)
    def initialize_population(self):
        self.population = []  # Asegúrate de que la población está vacía antes de inicializar
        for _ in range(self.population_size):
            individual = {}
            for nodo_id, nodo in self.nodos.items():
                total_aristas = len(nodo.aristas)
                # Si no hay aristas, establecemos una distribución de tiempo de cero para mantener la estructura del individuo
                if total_aristas == 0:
                    individual[nodo_id] = [0]  # Puedes ajustar esto según sea necesario para nodos sin aristas
                else:
                    # Para nodos con aristas, distribuimos el tiempo de manera equitativa
                    individual[nodo_id] = [1 / total_aristas] * total_aristas

            self.population.append(individual)

    def fitness(self, individual):
        total_vehiculos_salida = 0
        for nodo_id, nodo in self.nodos.items():
            if nodo.type == Type.SALIDA:
                if nodo_id not in individual:
                    # Si el nodo de salida no está en el individuo, entonces no podemos calcular el flujo para ese nodo.
                    print(f"El nodo de salida {nodo_id} no está presente en el individuo.")
                    continue

                # Calcular el flujo de salida basado en la distribución del tiempo y las capacidades de las aristas
                for i, arista in enumerate(nodo.aristas):
                    flujo = individual[nodo_id][i] * arista.max_vehiculos
                    total_vehiculos_salida += flujo
                    print(f"Flujo del nodo {nodo_id}, arista {i}: {flujo}")

        if total_vehiculos_salida == 0:
            print("Advertencia: el total de vehículos de salida calculado es 0.")
        return total_vehiculos_salida

    # def fitness(self, individual):
    #     # Simular el flujo de tráfico basado en la distribución de tiempo del individuo
    #     # Para simplificar, asumiremos que la aptitud es el total de vehículos que salen de la red
    #     total_vehiculos_salida = 0
    #     for nodo_id, nodo in self.nodos.items():
    #         if nodo.type == Type.SALIDA:
    #
    #             # Calcular el flujo de salida basado en la distribución del tiempo y las capacidades de las aristas
    #             for i, arista in enumerate(nodo.aristas):
    #                 flujo = individual[nodo.nodo_id][i] * arista.max_vehiculos
    #                 total_vehiculos_salida += flujo
    #     # La aptitud podría ser simplemente el flujo total de salida, ya que queremos maximizarlo
    #     return total_vehiculos_salida

    # def roulette_selection(self):
    #     total_fitness = sum(self.fitness(individual) for individual in self.population)
    #     selection_probabilities = [self.fitness(individual) / total_fitness for individual in self.population]
    #     selected_indices = random.choices(range(self.population_size), weights=selection_probabilities,
    #                                       k=self.population_size)
    #     parents = [self.population[i] for i in selected_indices]
    #     return parents

    def roulette_selection(self):
        total_fitness = sum(self.fitness(individual) for individual in self.population)
        if total_fitness == 0:
            raise ValueError("La aptitud total de la población es cero, la selección por ruleta no puede proceder.")

        selection_probabilities = [self.fitness(individual) / total_fitness for individual in self.population]
        selected_indices = random.choices(range(self.population_size), weights=selection_probabilities,
                                          k=self.population_size)
        parents = [self.population[i] for i in selected_indices]
        return parents

    def crossover(self, parent1, parent2):
        child = {}
        for nodo_id in parent1.keys():
            child[nodo_id] = []
            for i in range(len(parent1[nodo_id])):
                if random.random() < self.crossover_rate:
                    child[nodo_id].append(parent1[nodo_id][i])
                else:
                    child[nodo_id].append(parent2[nodo_id][i])
        return child

    def mutate(self, individual):
        for nodo_id, tiempos in individual.items():
            if random.random() < self.mutation_rate:
                semaforo_idx = random.randrange(len(tiempos))
                mutation_amount = random.uniform(-0.1, 0.1)
                individual[nodo_id][semaforo_idx] = max(0, min(1, individual[nodo_id][semaforo_idx] + mutation_amount))
        return individual


    def exec(self):
        print("Executando Solution")
        self.initialize_population()

        for generation in range(self.generations):

            fitness_results = [self.fitness(individual) for individual in self.population]

            parents = self.roulette_selection()

            children = self.crossover(parents)

            mutated_children = [self.mutate(child) for child in children]

            self.population = mutated_children

            print(f"Generación {generation}: Mejor resultado {max(fitness_results)}")

        return max(self.population, key=self.fitness)
