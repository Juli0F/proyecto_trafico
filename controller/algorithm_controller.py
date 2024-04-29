from algorithm.temp_solution import Nodo, Arista, SolutionAG


class AlgorithmController:
    def __init__(self):
        pass

    def convert(self, street_system):

        print("-------------")
        #nodos = {nodo['node_id']: Nodo((nodo['node_id'])) for nodo in street_system.nodes}
    #print("nodos en la calle: ", nodos);

        nodos = {}
        for nodoIterator in street_system.nodes:
            # print(nodoIterator)
            # nodoTemp = Nodo(nodoIterator["node_id"])
            # nodoTemp.aristas = nodoIterator.aristas
            nodos[nodoIterator['node_id']] =Nodo(nodoIterator['node_id'])# nodoTemp

        print("nodos, ",nodos)
        aristas = [
            Arista(nodos[arista['source_node']], nodos[arista['target_node']], arista['capacity_min'], arista['capacity'])
            for arista in street_system.edges
        ]

        temp_solution = SolutionAG(nodos,aristas);
        temp_solution.exec();

        print("-------------")

