import random

from models.arista import Arista


datos_de_nodos = {
    1: [(2, 10, 100), (3, 5, 50)],  # Nodo 1 conecta con Nodo 2 y Nodo 3, con capacidades min y max
    2: [(3, 20, 200)],
    3: [(1, 0, 150)]  # Capacidad mínima no definida para esta conexión
}

def crear_poblacion_inicial(nodos, tamaño_poblacion):
    poblacion = []
    for _ in range(tamaño_poblacion):
        individuo = {}
        for nodo in nodos:
            # Asumiendo que cada nodo en nodos tiene un id_nodo que se puede usar para buscar en datos_de_nodos
            conexiones = datos_de_nodos.get(nodo.id_nodo, [])
            individuo[nodo.id_nodo] = [Arista(nodos[nodo_destino_id-1], capacidad_min, capacidad_max,10) for nodo_destino_id, capacidad_min, capacidad_max in conexiones]
        poblacion.append(individuo)
    return poblacion


def evaluar_fitness(individuo):
    total_puntaje = 0
    for nodo_id, aristas in individuo.items():
        for arista in aristas:
            if isinstance(arista, Arista):
                capacidad_maxima = arista.capacidad_maxima
                capacidad_minima = arista.capacidad_minima if arista.capacidad_minima else 0
                puntaje = capacidad_maxima / (1 + abs(capacidad_maxima - capacidad_minima))
                total_puntaje += puntaje
            else:
                raise TypeError("Expected Arista object, got int instead.")
    return total_puntaje



def seleccion_por_ruleta(poblacion):
    print("poblacion", poblacion)
    fitness_total = sum(1.0 / evaluar_fitness(individuo) for individuo in poblacion)
    pick = random.uniform(0, fitness_total)
    current = 0
    for individuo in poblacion:
        current += 1.0 / evaluar_fitness(individuo)
        if current > pick:
            return individuo


def crossover(padre1, padre2):
    hijo = {}
    for nodo_id in padre1:
        if len(padre1[nodo_id]) > 1:  # Solo realiza crossover si hay más de un elemento
            punto_corte = random.randint(1, len(padre1[nodo_id]) - 1)
            hijo[nodo_id] = padre1[nodo_id][:punto_corte] + padre2[nodo_id][punto_corte:]
        else:
            # Si no es posible hacer crossover, hereda de uno de los padres al azar
            hijo[nodo_id] = padre1[nodo_id] if random.random() < 0.5 else padre2[nodo_id]
    return hijo


def mutacion(individuo, tasa_mutacion=0.01):
    for nodo_id, aristas in individuo.items():
        for i, arista in enumerate(aristas):
            if random.random() < tasa_mutacion:
                nuevo_tiempo = random.randint(10, 60)
                if nuevo_tiempo >= arista.capacidad_minima and nuevo_tiempo <= arista.capacidad_maxima:
                    aristas[i].tiempo_semaforo = nuevo_tiempo

def imprimir_reporte(poblacion_optima, nodos):
    print("Reporte de Optimización de Tráfico")
    print("===================================")
    for individuo in poblacion_optima:
        print("\nConfiguración del Individuo:")
        for nodo_id, aristas in individuo.items():
            print(f"\nNodo {nodo_id}:")
            for arista in aristas:
                destino = arista.destino.id_nodo
                tiempo_semaforo = arista.tiempo_semaforo
                capacidad_max = arista.capacidad_maxima
                capacidad_min = arista.capacidad_minima if arista.capacidad_minima else "No definida"
                print(f"  Arista hacia Nodo {destino}:")
                print(f"    Tiempo Semaforo: {tiempo_semaforo} segundos")
                print(f"    Capacidad Máxima: {capacidad_max} vehículos")
                print(f"    Capacidad Mínima: {capacidad_min} vehículos")

            # Supongamos que también tienes datos simulados de flujo de vehículos:
            flujo_vehiculos = estimar_flujo_vehiculos(nodo_id, aristas)  # Esta función debería ser definida para simular o calcular el flujo basado en la configuración
            print(f"    Flujo Estimado de Vehículos: {flujo_vehiculos} vehículos por hora")

def estimar_flujo_vehiculos(nodo_id, aristas):
    # Esta es una función de ejemplo que necesitarías implementar basada en tu modelo de simulación
    # Por ahora, vamos a retornar un número simulado
    return sum(arista.capacidad_maxima for arista in aristas) / len(aristas)  # Simulación muy básica

def algoritmo_genetico(nodos, generaciones=100, tamaño_poblacion=50):
    poblacion = crear_poblacion_inicial(nodos, tamaño_poblacion)
    for _ in range(generaciones):
        nueva_poblacion = []
        while len(nueva_poblacion) < tamaño_poblacion:
            padre1 = seleccion_por_ruleta(poblacion)
            padre2 = seleccion_por_ruleta(poblacion)
            hijo = crossover(padre1, padre2)
            mutacion(hijo)
            nueva_poblacion.append(hijo)
        poblacion = nueva_poblacion
    return poblacion
