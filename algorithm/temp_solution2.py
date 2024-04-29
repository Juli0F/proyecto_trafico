import random


# Definir la estructura de datos para representar el diagrama de calles
class Nodo:
    def __init__(self, id):
        self.id = id
        self.aristas = []


class Arista:
    def __init__(self, origen, destino, min_vehiculos, max_vehiculos):
        self.origen = origen
        self.destino = destino
        self.min_vehiculos = min_vehiculos
        self.max_vehiculos = max_vehiculos


# Crear el diagrama de calles
nodos = {
    'A': Nodo('A'),
    'B': Nodo('B'),
    'C': Nodo('C'),
    'D': Nodo('D'),
    'X': Nodo('X')
}

aristas = [
    Arista(nodos['A'], nodos['B'], 5, 50),
    Arista(nodos['A'], nodos['C'], 0, 75),
    Arista(nodos['A'], nodos['D'], 5, 100),
    Arista(nodos['B'], nodos['D'], 0, 100),
    Arista(nodos['C'], nodos['D'], 0, 100),
    Arista(nodos['D'], nodos['X'], 0, 75)
]

for arista in aristas:
    arista.origen.aristas.append(arista)

# Parámetros del algoritmo genético
poblacion_size = 500
num_generaciones = 100
tasa_mutacion = 0.1

def fitness(solucion, total_vehiculos):
    flujo_total = 0
    penalizacion_congestion = 0
    capacidad_total = sum(arista.max_vehiculos for arista in aristas)

    for nodo_id, tiempos in solucion.items():
        nodo = nodos[nodo_id]
        for i, arista in enumerate(nodo.aristas):
            tiempo_porcentaje = tiempos[i]
            flujo_potencial = tiempo_porcentaje * total_vehiculos
            flujo_real = min(flujo_potencial, arista.max_vehiculos)
            flujo_total += flujo_real

            # Penalizar si el flujo excede la capacidad máxima
            if flujo_potencial > arista.max_vehiculos:
                penalizacion_congestion += (flujo_potencial - arista.max_vehiculos) ** 2

            # Penalizar si el flujo es menor que la capacidad mínima
            if flujo_potencial < arista.min_vehiculos:
                penalizacion_congestion += (arista.min_vehiculos - flujo_potencial) ** 2

    fitness_valor = flujo_total - penalizacion_congestion
    return fitness_valor

def crear_solucion():
    solucion = {}
    for nodo in nodos.values():
        tiempos = [random.random() for _ in range(len(nodo.aristas))]
        total = sum(tiempos)
        tiempos = [tiempo / total for tiempo in tiempos]
        solucion[nodo.id] = tiempos
    return solucion


# Función para seleccionar individuos mediante el método de la ruleta
# def seleccion_ruleta(poblacion, total_vehiculos):
#     fitness_total = sum(fitness(solucion) for solucion in poblacion)
#     probabilidades = [fitness(solucion) / fitness_total for solucion in poblacion]
#     indices = list(range(len(poblacion)))
#     seleccionados = random.choices(indices, probabilidades, k=len(poblacion))
#     return [poblacion[i] for i in seleccionados]
def seleccion_ruleta(poblacion, total_vehiculos):
    fitness_total = sum(fitness(solucion, total_vehiculos) for solucion in poblacion)
    probabilidades = [fitness(solucion, total_vehiculos) / fitness_total for solucion in poblacion]
    indices = list(range(len(poblacion)))
    seleccionados = random.choices(indices, probabilidades, k=len(poblacion))
    return [poblacion[i] for i in seleccionados]

# Función para cruzar dos soluciones
def cruzar(solucion1, solucion2):
    nueva_solucion = {}
    for nodo_id in solucion1.keys():
        if random.random() < 0.5:
            nueva_solucion[nodo_id] = solucion1[nodo_id]
        else:
            nueva_solucion[nodo_id] = solucion2[nodo_id]
    return nueva_solucion


def mutar(solucion):
    for nodo_id, tiempos in solucion.items():
        if random.random() < tasa_mutacion and len(tiempos) > 0:
            indice = random.randint(0, len(tiempos) - 1)
            tiempos[indice] = random.random()
            total = sum(tiempos)
            tiempos = [tiempo / total for tiempo in tiempos]
            solucion[nodo_id] = tiempos
    return solucion


# Algoritmo genético principal
def algoritmo_genetico(total_vehiculos):
    poblacion = [crear_solucion() for _ in range(poblacion_size)]

    for generacion in range(num_generaciones):
        poblacion = seleccion_ruleta(poblacion, total_vehiculos)
        nueva_poblacion = []

        for i in range(0, len(poblacion), 2):
            padre1 = poblacion[i]
            padre2 = poblacion[i + 1]
            hijo1 = cruzar(padre1, padre2)
            hijo2 = cruzar(padre1, padre2)
            hijo1 = mutar(hijo1)
            hijo2 = mutar(hijo2)
            nueva_poblacion.append(hijo1)
            nueva_poblacion.append(hijo2)

        poblacion = nueva_poblacion

    mejor_solucion = max(poblacion, key=lambda  solucion: fitness(solucion, total_vehiculos))
    return mejor_solucion

def presentar_solucion(mejor_solucion, total_vehiculos):
    print("Distribución del tiempo y flujo estimado de vehículos por arista:")
    for nodo_id, porcentajes in mejor_solucion.items():
        nodo = nodos[nodo_id]
        print(f"\nNodo {nodo_id}:")
        for i, arista in enumerate(nodo.aristas):
            tiempo_porcentaje = porcentajes[i]
            flujo_estimado = tiempo_porcentaje * total_vehiculos
            # Asegurarse de que el flujo no exceda la capacidad máxima
            flujo_estimado = min(flujo_estimado, arista.max_vehiculos)
            print(f"  Arista hacia {arista.destino.id}:")
            print(f"    Porcentaje de tiempo: {tiempo_porcentaje:.2%}")
            print(f"    Flujo estimado de vehículos: {flujo_estimado:.0f}/{arista.max_vehiculos}")

# Ejecutar el algoritmo genético
mejor_solucion = algoritmo_genetico(300)
print("Mejor solución encontrada:", mejor_solucion)
presentar_solucion(mejor_solucion, 300)
