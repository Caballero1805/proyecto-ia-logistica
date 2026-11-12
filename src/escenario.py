"""
Módulo de Escenario Logístico
Define la cuadrícula 12x12, carga configuración desde JSON,
valida movimientos y calcula costos.
"""

import json
import os


class EscenarioLogistico:
    """Representa el entorno logístico de 12x12 y sus reglas."""

    def __init__(self, ruta_escenario, ruta_parametros):
        """Carga los archivos JSON de configuración."""
        # CAMBIO CLAVE: usar 'utf-8-sig' en lugar de 'utf-8' para ignorar el BOM de Windows
        with open(ruta_escenario, 'r', encoding='utf-8-sig') as f:
            self.config = json.load(f)
        
        with open(ruta_parametros, 'r', encoding='utf-8-sig') as f:
            self.params = json.load(f)

        # Configuración del mapa
        self.tamaño = self.config["tamaño_cuadricula"]
        self.inicio = tuple(self.config["inicio"])
        self.destino = tuple(self.config["destino"])
        self.entregas = [tuple(p) for p in self.config["puntos_entrega"]]
        self.obstaculos = set(tuple(o) for o in self.config["obstaculos"])
        
        # Costos especiales
        self.costos_especiales = {}
        for k, v in self.config["costos_especiales"].items():
            coords = json.loads(k)
            self.costos_especiales[tuple(coords)] = v

    def es_valido(self, posicion):
        """Verifica si una posición está dentro de la cuadrícula y no es obstáculo."""
        x, y = posicion
        if x < 0 or x >= self.tamaño or y < 0 or y >= self.tamaño:
            return False
        if posicion in self.obstaculos:
            return False
        return True

    def obtener_vecinos(self, posicion):
        """Obtiene los movimientos válidos y sus costos."""
        movimientos = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        vecinos = []
        
        for dx, dy in movimientos:
            nueva_pos = (posicion[0] + dx, posicion[1] + dy)
            if self.es_valido(nueva_pos):
                costo = self.costos_especiales.get(nueva_pos, 1.0)
                vecinos.append((nueva_pos, costo))
        
        return vecinos

    def distancia_manhattan(self, a, b):
        """Calcula la distancia Manhattan (heurística admisible)."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])


# ============================================================
# BLOQUE DE PRUEBA
# ============================================================
if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ruta_esc = os.path.join(base_dir, 'config', 'escenario.json')
    ruta_par = os.path.join(base_dir, 'config', 'parametros.json')
    
    print("Cargando escenario...")
    escenario = EscenarioLogistico(ruta_esc, ruta_par)
    
    print(f"\n✅ Escenario cargado correctamente")
    print(f"   Tamaño: {escenario.tamaño}x{escenario.tamaño}")
    print(f"   Inicio: {escenario.inicio}")
    print(f"   Destino: {escenario.destino}")
    print(f"   Entregas: {escenario.entregas}")
    print(f"   Obstáculos: {len(escenario.obstaculos)}")
    print(f"   Costos especiales: {escenario.costos_especiales}")
    
    print(f"\n   ¿(5,5) es válido? {escenario.es_valido((5,5))}")
    print(f"   ¿(1,1) es válido? {escenario.es_valido((1,1))}  (debe ser False, es obstáculo)")
    
    print(f"\n   Vecinos de (0,0): {escenario.obtener_vecinos((0,0))}")
    
    print(f"\n   Distancia Manhattan de (0,0) a (11,11): {escenario.distancia_manhattan((0,0), (11,11))}")
    
    print("\n✅ Todas las pruebas del módulo escenario pasaron correctamente")