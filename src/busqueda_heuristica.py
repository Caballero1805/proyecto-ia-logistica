import heapq
import time
import os
from src.escenario import EscenarioLogistico

def greedy_best_first(escenario, inicio, objetivo):
    """Búsqueda Voraz: Solo usa h(n). Rápida pero no garantiza optimalidad."""
    # Cola de prioridad: (heuristica, posicion, ruta)
    frontera = [(escenario.distancia_manhattan(inicio, objetivo), inicio, [inicio])]
    visitados = set()
    nodos_expandidos = 0
    
    while frontera:
        h, actual, ruta = heapq.heappop(frontera)
        
        if actual in visitados:
            continue
        visitados.add(actual)
        nodos_expandidos += 1
        
        if actual == objetivo:
            return ruta, len(ruta) - 1, nodos_expandidos
            
        for vecino, costo in escenario.obtener_vecinos(actual):
            if vecino not in visitados:
                h_vecino = escenario.distancia_manhattan(vecino, objetivo)
                heapq.heappush(frontera, (h_vecino, vecino, ruta + [vecino]))
                
    return None, float('inf'), nodos_expandidos

def a_estrella(escenario, inicio, objetivo):
    """A*: Usa f(n) = g(n) + h(n). Garantiza la ruta óptima."""
    # Cola de prioridad: (f, g, posicion, ruta)
    frontera = [(escenario.distancia_manhattan(inicio, objetivo), 0, inicio, [inicio])]
    visitados = {} # Guarda el mejor g(n) para cada nodo
    nodos_expandidos = 0
    
    while frontera:
        f, g, actual, ruta = heapq.heappop(frontera)
        
        # Si ya visitamos este nodo con un costo menor, lo ignoramos
        if actual in visitados and visitados[actual] <= g:
            continue
        visitados[actual] = g
        nodos_expandidos += 1
        
        if actual == objetivo:
            return ruta, g, nodos_expandidos
            
        for vecino, costo in escenario.obtener_vecinos(actual):
            nuevo_g = g + costo
            if vecino not in visitados or visitados[vecino] > nuevo_g:
                h = escenario.distancia_manhattan(vecino, objetivo)
                f = nuevo_g + h
                heapq.heappush(frontera, (f, nuevo_g, vecino, ruta + [vecino]))
                
    return None, float('inf'), nodos_expandidos

def probar_modulo_a():
    """Función de prueba rápida para el Módulo A."""
    # Rutas relativas a la carpeta raíz del proyecto
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_esc = os.path.join(base_dir, 'config', 'escenario.json')
    ruta_par = os.path.join(base_dir, 'config', 'parametros.json')
    
    escenario = EscenarioLogistico(ruta_esc, ruta_par)
    
    print(f"\n--- PRUEBA MÓDULO A: Búsqueda Heurística ---")
    print(f"Inicio: {escenario.inicio} | Destino: {escenario.destino}\n")
    
    # Probar Greedy
    t_inicio = time.time()
    ruta_g, costo_g, nodos_g = greedy_best_first(escenario, escenario.inicio, escenario.destino)
    t_greedy = time.time() - t_inicio
    
    # Probar A*
    t_inicio = time.time()
    ruta_a, costo_a, nodos_a = a_estrella(escenario, escenario.inicio, escenario.destino)
    t_a = time.time() - t_inicio
    
    print(f"{'Algoritmo':<10} | {'Costo':<10} | {'Nodos':<10} | {'Tiempo (s)':<10}")
    print("-" * 45)
    print(f"{'Greedy':<10} | {costo_g:<10} | {nodos_g:<10} | {t_greedy:<10.4f}")
    print(f"{'A*':<10} | {costo_a:<10} | {nodos_a:<10} | {t_a:<10.4f}")

if __name__ == "__main__":
    probar_modulo_a()