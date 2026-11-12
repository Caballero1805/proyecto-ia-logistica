
"""
Módulo B: Búsqueda Local
Implementa Hill Climbing con reinicios aleatorios para optimizar el orden de entregas.
"""

import random
import time
from src.escenario import EscenarioLogistico

def calcular_costo_ruta(ruta, escenario):
    """Calcula el costo total de una ruta usando distancia Manhattan."""
    costo_total = 0
    actual = escenario.inicio
    
    for entrega in ruta:
        costo_total += escenario.distancia_manhattan(actual, entrega)
        actual = entrega
        
    # Sumar el costo de regresar al destino final
    costo_total += escenario.distancia_manhattan(actual, escenario.destino)
    return costo_total

def generar_vecino(ruta):
    """Genera un vecino intercambiando dos entregas aleatorias (vecindad por intercambio)."""
    vecino = ruta[:] # Copia de la ruta
    i, j = random.sample(range(len(vecino)), 2)
    vecino[i], vecino[j] = vecino[j], vecino[i]
    return vecino

def hill_climbing(escenario, ruta_inicial, max_iter=100):
    """Hill Climbing básico: se detiene cuando no encuentra un vecino mejor (óptimo local)."""
    ruta_actual = ruta_inicial[:]
    costo_actual = calcular_costo_ruta(ruta_actual, escenario)
    
    for _ in range(max_iter):
        vecino = generar_vecino(ruta_actual)
        costo_vecino = calcular_costo_ruta(vecino, escenario)
        
        # Minimización: aceptamos si el vecino tiene MENOR costo
        if costo_vecino < costo_actual:
            ruta_actual = vecino
            costo_actual = costo_vecino
        else:
            break # Nos quedamos en un óptimo local
            
    return ruta_actual, costo_actual

def hill_climbing_reinicios(escenario, num_reinicios=10):
    """Hill Climbing con múltiples reinicios aleatorios para escapar de óptimos locales."""
    print(f"\n--- MÓDULO B: Hill Climbing con {num_reinicios} reinicios ---")
    mejor_ruta_global = None
    mejor_costo_global = float('inf')
    
    for i in range(num_reinicios):
        # Generar solución inicial aleatoria
        ruta_inicial = escenario.entregas[:]
        random.shuffle(ruta_inicial)
        
        # Ejecutar Hill Climbing
        ruta_final, costo_final = hill_climbing(escenario, ruta_inicial)
        print(f"Reinicio {i+1:2d}: Costo = {costo_final} | Ruta: {ruta_final}")
        
        # Guardar el mejor resultado global
        if costo_final < mejor_costo_global:
            mejor_costo_global = costo_final
            mejor_ruta_global = ruta_final[:]
            
    print(f"\n🏆 Mejor costo global encontrado: {mejor_costo_global}")
    print(f"🏆 Mejor ruta: {mejor_ruta_global}")
    return mejor_ruta_global, mejor_costo_global

# Bloque de prueba (lo usaremos al final cuando arreglemos los JSON)
if __name__ == "__main__":
    print("Módulo de Búsqueda Local cargado correctamente. (Falta configurar los JSON para ejecutar)")