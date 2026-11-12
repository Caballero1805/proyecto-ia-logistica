"""
SISTEMA INTELIGENTE DE PLANIFICACIÓN LOGÍSTICA
Archivo principal que integra todos los módulos, genera CSV y gráficas.
"""

import os
import csv
import matplotlib.pyplot as plt
from src.escenario import EscenarioLogistico
from src.busqueda_heuristica import greedy_best_first, a_estrella
from src.busqueda_local import hill_climbing_reinicios
from src.metaheuristicas import ejecutar_recocido_multiples_veces, ejecutar_ag_multiples_veces
from src.teoria_juegos import JuegoLogistico
from src.minimax import comparar_minimax

def main():
    print("🚀 INICIANDO SISTEMA INTELIGENTE DE PLANIFICACIÓN LOGÍSTICA 🚀\n")
    
    # Rutas base
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_esc = os.path.join(base_dir, 'config', 'escenario.json')
    ruta_par = os.path.join(base_dir, 'config', 'parametros.json')
    
    # 1. Cargar Escenario
    print("1️⃣ Cargando escenario y parámetros...")
    escenario = EscenarioLogistico(ruta_esc, ruta_par)
    print(f"   Escenario {escenario.tamaño}x{escenario.tamaño} cargado.\n")
    
    # 2. Módulo A: Búsqueda Heurística
    print("2️⃣ MÓDULO A: Búsqueda Heurística (Greedy vs A*)")
    ruta_g, costo_g, nodos_g = greedy_best_first(escenario, escenario.inicio, escenario.destino)
    ruta_a, costo_a, nodos_a = a_estrella(escenario, escenario.inicio, escenario.destino)
    print(f"   Greedy -> Costo: {costo_g}, Nodos: {nodos_g}")
    print(f"   A*     -> Costo: {costo_a}, Nodos: {nodos_a}\n")
    
    # 3. Módulo B: Búsqueda Local
    print("3️⃣ MÓDULO B: Búsqueda Local (Hill Climbing)")
    num_reinicios = escenario.params["hill_climbing"]["num_reinicios"]
    mejor_ruta_hc, mejor_costo_hc = hill_climbing_reinicios(escenario, num_reinicios)
    print()
    
    # 4. Módulo C: Metaheurísticas
    print("4️⃣ MÓDULO C: Metaheurísticas (Recocido y AG)")
    # Usamos los parámetros del JSON (20 ejecuciones como pide el proyecto)
    veces = escenario.params["recocido_simulado"]["num_ejecuciones"]
    costos_rs = ejecutar_recocido_multiples_veces(escenario, veces=veces)
    costos_ag = ejecutar_ag_multiples_veces(escenario, veces=veces)
    print()
    
    # 5. Módulo D: Teoría de Juegos
    print("5️⃣ MÓDULO D: Teoría de Juegos")
    juego = JuegoLogistico()
    juego.mostrar_matriz()
    juego.encontrar_equilibrios_nash()
    juego.interpretar_resultados()
    print()
    
    # 6. Módulo E: Minimax
    print("6️⃣ MÓDULO E: Búsqueda Adversaria (Minimax vs Alfa-Beta)")
    comparar_minimax()
    print()
    
    # 7. Guardar Resultados en CSV
    print("7️⃣ Guardando resultados experimentales en CSV...")
    ruta_csv = os.path.join(base_dir, 'resultados', 'datos_experimentales.csv')
    os.makedirs(os.path.dirname(ruta_csv), exist_ok=True)
    
    with open(ruta_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Metodo', 'Mejor_Costo', 'Promedio', 'Desv_Estandar'])
        
        # Cálculos básicos para el CSV
        prom_rs = sum(costos_rs)/len(costos_rs)
        prom_ag = sum(costos_ag)/len(costos_ag)
        
        writer.writerow(['Hill_Climbing', mejor_costo_hc, mejor_costo_hc, 0.0])
        writer.writerow(['Recocido_Simulado', min(costos_rs), prom_rs, 0.0])
        writer.writerow(['Algoritmo_Genetico', min(costos_ag), prom_ag, 0.0])
    print(f"   ✅ CSV guardado en: {ruta_csv}\n")
    
    # 8. Generar Gráfica comparativa
    print("8️⃣ Generando gráfica comparativa...")
    metodos = ['Hill Climbing', 'Recocido Simulado', 'Algoritmo Genético']
    promedios = [mejor_costo_hc, prom_rs, prom_ag]
    
    plt.figure(figsize=(8, 5))
    plt.bar(metodos, promedios, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    plt.ylabel('Costo Promedio de la Ruta')
    plt.title('Comparación de Métodos de Optimización')
    plt.grid(axis='y', alpha=0.3)
    
    ruta_grafica = os.path.join(base_dir, 'resultados', 'graficas', 'comparacion.png')
    os.makedirs(os.path.dirname(ruta_grafica), exist_ok=True)
    plt.savefig(ruta_grafica)
    plt.close()
    print(f"   ✅ Gráfica guardada en: {ruta_grafica}\n")
    
    print("🎉 ¡SISTEMA EJECUTADO EXITOSAMENTE! REVISAR CARPETA 'resultados' 🎉")

if __name__ == "__main__":
    main()