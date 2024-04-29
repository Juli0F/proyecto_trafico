from algorithm.temp_solution import  SolutionAG
from models.arista import Arista
from models.nodo import Nodo


class AlgorithmController:
    def __init__(self):
        pass

    def convert(self, street_system):

        print("-------------")
        nodos = {}
        for nodoIterator in street_system.nodes:
            nodos[nodoIterator['node_id']] =Nodo(nodoIterator['node_id'], nodoIterator['node_type'],nodoIterator['init'])# nodoTemp


        aristas = []
        for arista in street_system.edges:
            print("Arista:", arista)
            print("Atributos disponibles:")
            for key, value in arista.items():
                print(f"{key}: {value}")
            print()

        print("nodos, ",nodos)
        print("Aristas: ", street_system.edges)

        temp_solution = SolutionAG(nodos,aristas);
        temp_solution.exec();

        print("-------------")

