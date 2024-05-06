from algorithm.ga import GeneticAlgorithm
from models.arista import Arista
from models.nodo import Nodo


class AlgorithmController:
    def __init__(self, population, num_gen, mutation):
        self.population = population.get()
        self.num_gen = num_gen.get()
        self.mutation = mutation.get()

    def convert(self, street_system):

        print("-------------")
        nodos = {}
        for nodoIterator in street_system.nodes:
            nodos[nodoIterator['node_id']] =Nodo(nodoIterator['node_id'], nodoIterator['node_type'])# nodoTemp


        aristas = []
        for arista_data in street_system.edges:
            origen = nodos[arista_data['source_node']]
            destino = nodos[arista_data['target_node']]
            min_vehiculos = arista_data['capacity_min']
            max_vehiculos = arista_data['capacity']
            nueva_arista = Arista(origen, destino, min_vehiculos, max_vehiculos)
            aristas.append(nueva_arista)
            nodos[origen.nodo_id].aristas.append(nueva_arista)

        for arista in aristas:
            arista.origen.aristas.append(arista)

        print("nodos, ",nodos)
        print("aristas, ",aristas)
        print("___INIT_AG____")

        genetic_algorithm = GeneticAlgorithm(nodos, aristas, int(self.population), int(self.num_gen), float(self.mutation))
        solution = genetic_algorithm.genetic_algorithm(self.population)
        print("___Solucion__")
        return genetic_algorithm.presentar_solucion(solution,self.population)



