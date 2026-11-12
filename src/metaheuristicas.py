"""
Módulo C: Metaheurísticas
Implementa Recocido Simulado y Algoritmo Genético.
"""

import random
import math
import time
from src.escenario import EscenarioLogistico
from src.busqueda_local import calcular_costo_ruta, generar_vecino

# ==========================================
# 1. RECOCIDO SIMULADO (Simulated Annealing)
# ==========================================
def recocido_simulado(escenario, temp_inicial=100.0, temp_final=0.1, alfa=0.95):
    """
    Recocido Simulado: Acepta soluciones peores con cierta probabilidad para escapar de óptimos locales.
    """
    # Solución inicial aleatoria
    ruta_actual = escenario.entregas[:]
    random.shuffle(ruta_actual)
    costo_actual = calcular_costo_ruta(ruta_actual, escenario)
    
    mejor_ruta = ruta_actual[:]
    mejor_costo = costo_actual
    
    temperatura = temp_inicial
    
    while temperatura > temp_final:
        vecino = generar_vecino(ruta_actual)
        costo_vecino = calcular_costo_ruta(vecino, escenario)
        delta = costo_vecino - costo_actual
        
        # Si es mejor, la aceptamos. Si es peor, la aceptamos con probabilidad
        if delta < 0:
            ruta_actual = vecino
            costo_actual = costo_vecino
        else:
            probabilidad = math.exp(-delta / temperatura)
            if random.random() < probabilidad:
                ruta_actual = vecino
                costo_actual = costo_vecino
                
        # Actualizar el mejor histórico
        if costo_actual < mejor_costo:
            mejor_costo = costo_actual
            mejor_ruta = ruta_actual[:]
            
        # Enfriar el sistema
        temperatura *= alfa
        
    return mejor_ruta, mejor_costo

def ejecutar_recocido_multiples_veces(escenario, veces=20):
    print(f"\n--- MÓDULO C.1: Recocido Simulado ({veces} ejecuciones) ---")
    costos = []
    for i in range(veces):
        ruta, costo = recocido_simulado(escenario)
        costos.append(costo)
        print(f"Ejecución {i+1:2d}: Costo = {costo}")
        
    print(f"\n📊 Estadísticas Recocido Simulado:")
    print(f"   Mejor costo: {min(costos)}")
    print(f"   Promedio:    {sum(costos)/len(costos):.2f}")
    return costos

# ==========================================
# 2. ALGORITMO GENÉTICO
# ==========================================
class AlgoritmoGenetico:
    def __init__(self, escenario, tam_poblacion=50, generaciones=100, prob_cruza=0.8, prob_mutacion=0.1):
        self.escenario = escenario
        self.tam_poblacion = tam_poblacion
        self.generaciones = generaciones
        self.prob_cruza = prob_cruza
        self.prob_mutacion = prob_mutacion
        
    def crear_poblacion(self):
        poblacion = []
        for _ in range(self.tam_poblacion):
            ind = self.escenario.entregas[:]
            random.shuffle(ind)
            poblacion.append(ind)
        return poblacion
        
    def calcular_fitness(self, ruta):
        # En AG queremos maximizar, así que usamos el inverso del costo
        costo = calcular_costo_ruta(ruta, self.escenario)
        return 1.0 / (1.0 + costo)
        
    def seleccionar_padre(self, poblacion):
        # Selección por torneo simple (elegimos 3 al azar y nos quedamos con el mejor)
        torneo = random.sample(poblacion, 3)
        return max(torneo, key=self.calcular_fitness)
        
    def cruzar(self, p1, p2):
        if random.random() > self.prob_cruza:
            return p1[:], p2[:]
        # Cruza de un solo punto
        punto = random.randint(1, len(p1)-1)
        h1 = p1[:punto] + [x for x in p2 if x not in p1[:punto]]
        h2 = p2[:punto] + [x for x in p1 if x not in p2[:punto]]
        return h1, h2
        
    def mutar(self, ruta):
        if random.random() < self.prob_mutacion:
            return generar_vecino(ruta)
        return ruta
        
    def ejecutar(self):
        poblacion = self.crear_poblacion()
        mejor_individuo = None
        mejor_fitness = -1
        
        for gen in range(self.generaciones):
            nueva_poblacion = []
            while len(nueva_poblacion) < self.tam_poblacion:
                p1 = self.seleccionar_padre(poblacion)
                p2 = self.seleccionar_padre(poblacion)
                h1, h2 = self.cruzar(p1, p2)
                nueva_poblacion.append(self.mutar(h1))
                nueva_poblacion.append(self.mutar(h2))
            poblacion = nueva_poblacion[:self.tam_poblacion]
            
            # Evaluar mejor de la generación
            actual_mejor = max(poblacion, key=self.calcular_fitness)
            actual_fitness = self.calcular_fitness(actual_mejor)
            if actual_fitness > mejor_fitness:
                mejor_fitness = actual_fitness
                mejor_individuo = actual_mejor[:]
                
        mejor_costo = calcular_costo_ruta(mejor_individuo, self.escenario)
        return mejor_individuo, mejor_costo

def ejecutar_ag_multiples_veces(escenario, veces=20):
    print(f"\n--- MÓDULO C.2: Algoritmo Genético ({veces} ejecuciones) ---")
    costos = []
    for i in range(veces):
        ag = AlgoritmoGenetico(escenario)
        ruta, costo = ag.ejecutar()
        costos.append(costo)
        print(f"Ejecución {i+1:2d}: Costo = {costo}")
        
    print(f"\n📊 Estadísticas Algoritmo Genético:")
    print(f"   Mejor costo: {min(costos)}")
    print(f"   Promedio:    {sum(costos)/len(costos):.2f}")
    return costos

if __name__ == "__main__":
    print("Módulo de Metaheurísticas cargado correctamente.")