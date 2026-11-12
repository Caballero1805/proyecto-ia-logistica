"""
Módulo E: Búsqueda Adversaria (Minimax y Poda Alfa-Beta)
Subproblema: Negociación de Capacidad de Carga (Reparto de Recursos).
"""

def minimax_basico(recursos, turno_max, profundidad_max, profundidad_actual=0):
    """
    Algoritmo Minimax básico.
    MAX quiere maximizar su puntuación, MIN quiere minimizarla.
    """
    # Condición terminal
    if recursos == 0 or profundidad_actual >= profundidad_max:
        return 0  # No hay más recursos que repartir

    if turno_max:
        mejor_valor = float('-inf')
        # Acciones legales: tomar 1 o 2 recursos
        for accion in [1, 2]:
            if accion <= recursos:
                # MAX toma 'accion' recursos y suma a su puntuación
                valor = accion + minimax_basico(recursos - accion, False, profundidad_max, profundidad_actual + 1)
                mejor_valor = max(mejor_valor, valor)
        return mejor_valor
    else:
        mejor_valor = float('inf')
        for accion in [1, 2]:
            if accion <= recursos:
                # MIN toma 'accion' recursos (no suman a MAX, por eso es + 0)
                valor = 0 + minimax_basico(recursos - accion, True, profundidad_max, profundidad_actual + 1)
                mejor_valor = min(mejor_valor, valor)
        return mejor_valor


def minimax_alfa_beta(recursos, turno_max, profundidad_max, alfa, beta, profundidad_actual, stats):
    """
    Minimax con Poda Alfa-Beta.
    stats: diccionario para contar nodos visitados y podados.
    """
    stats["visitados"] += 1

    # Condición terminal
    if recursos == 0 or profundidad_actual >= profundidad_max:
        return 0

    if turno_max:
        mejor_valor = float('-inf')
        for accion in [1, 2]:
            if accion <= recursos:
                valor = accion + minimax_alfa_beta(recursos - accion, False, profundidad_max, alfa, beta, profundidad_actual + 1, stats)
                mejor_valor = max(mejor_valor, valor)
                alfa = max(alfa, mejor_valor)
                # Poda Beta
                if beta <= alfa:
                    stats["podados"] += 1
                    break 
        return mejor_valor
    else:
        mejor_valor = float('inf')
        for accion in [1, 2]:
            if accion <= recursos:
                valor = 0 + minimax_alfa_beta(recursos - accion, True, profundidad_max, alfa, beta, profundidad_actual + 1, stats)
                mejor_valor = min(mejor_valor, valor)
                beta = min(beta, mejor_valor)
                # Poda Alfa
                if beta <= alfa:
                    stats["podados"] += 1
                    break
        return mejor_valor


def comparar_minimax():
    """Ejecuta ambos algoritmos y compara sus resultados."""
    print("\n" + "="*60)
    print("MÓDULO E: MINIMAX VS PODA ALFA-BETA")
    print("="*60)
    
    recursos_totales = 6
    profundidad = 6
    
    # 1. Minimax Básico
    valor_basico = minimax_basico(recursos_totales, True, profundidad)
    
    # 2. Minimax con Alfa-Beta
    stats = {"visitados": 0, "podados": 0}
    valor_alfa_beta = minimax_alfa_beta(recursos_totales, True, profundidad, float('-inf'), float('inf'), 0, stats)
    
    print(f"\nRecursos a repartir: {recursos_totales} | Profundidad máxima: {profundidad}")
    print(f"{'Algoritmo':<20} | {'Valor Óptimo (MAX)':<20} | {'Nodos Visitados':<20} | {'Nodos Podados':<20}")
    print("-" * 85)
    print(f"{'Minimax Básico':<20} | {valor_basico:<20} | {'N/A':<20} | {'N/A':<20}")
    print(f"{'Alfa-Beta':<20} | {valor_alfa_beta:<20} | {stats['visitados']:<20} | {stats['podados']:<20}")
    
    if valor_basico == valor_alfa_beta:
        print("\n✅ ÉXITO: Ambos algoritmos encontraron el mismo valor óptimo.")
        print(f"   La poda Alfa-Beta evitó evaluar {stats['podados']} nodos innecesarios.")
    else:
        print("\n❌ ERROR: Los valores no coinciden.")

if __name__ == "__main__":
    comparar_minimax()