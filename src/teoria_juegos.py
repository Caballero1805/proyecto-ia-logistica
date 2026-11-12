"""
Módulo D: Teoría de Juegos
Análisis de estrategias competitivas en el mercado logístico.
"""

import numpy as np

class JuegoLogistico:
    """
    Juego de dos jugadores: Empresa Logística (MAX) vs Competidor (MIN).
    Estrategias: 0=Agresivo, 1=Moderado, 2=Pasivo.
    """
    
    def __init__(self):
        self.jugadores = ["Empresa", "Competidor"]
        self.estrategias = ["Agresivo", "Moderado", "Pasivo"]
        
        # Matriz de pagos (Empresa, Competidor)
        # Filas: Empresa | Columnas: Competidor
        # Ejemplo: Si ambos son agresivos (guerra de precios), ganan poco (2,2).
        # Si uno es moderado y el otro pasivo, el moderado gana más mercado.
        self.matriz_pagos = np.array([
            [[2, 2], [5, 1], [6, 0]],   # Empresa: Agresivo
            [[1, 5], [4, 4], [5, 2]],   # Empresa: Moderado
            [[0, 6], [2, 5], [3, 3]]    # Empresa: Pasivo
        ])

    def mostrar_matriz(self):
        """Imprime la matriz de pagos de forma legible."""
        print("\n" + "="*60)
        print("MATRIZ DE PAGOS (Empresa, Competidor)")
        print("="*60)
        print(f"{'':<12}", end="")
        for estr in self.estrategias:
            print(f"Comp:{estr:<8}", end="")
        print()
        
        for i, estr_emp in enumerate(self.estrategias):
            print(f"Emp:{estr_emp:<8}", end="")
            for j in range(len(self.estrategias)):
                pago = self.matriz_pagos[i][j]
                print(f"({pago[0]},{pago[1]}){'':<6}", end="")
            print()

    def mejor_respuesta_empresa(self, estrategia_competidor):
        """Encuentra la mejor estrategia de la Empresa dada la acción del Competidor."""
        pagos = self.matriz_pagos[:, estrategia_competidor, 0]
        return int(np.argmax(pagos))

    def mejor_respuesta_competidor(self, estrategia_empresa):
        """Encuentra la mejor estrategia del Competidor dada la acción de la Empresa."""
        pagos = self.matriz_pagos[estrategia_empresa, :, 1]
        return int(np.argmax(pagos))

    def encontrar_equilibrios_nash(self):
        """Busca equilibrios de Nash puros."""
        print("\n" + "="*60)
        print("ANÁLISIS DE EQUILIBRIO DE NASH")
        print("="*60)
        
        equilibrios = []
        for i in range(len(self.estrategias)):
            for j in range(len(self.estrategias)):
                # Verificar si (i, j) es equilibrio de Nash
                if self.mejor_respuesta_empresa(j) == i and self.mejor_respuesta_competidor(i) == j:
                    equilibrios.append((i, j))
                    pago = self.matriz_pagos[i][j]
                    print(f"✅ Equilibrio encontrado: Empresa={self.estrategias[i]}, "
                          f"Competidor={self.estrategias[j]} -> Pago: {pago}")
        
        if not equilibrios:
            print("No se encontraron equilibrios de Nash puros.")
        return equilibrios

    def interpretar_resultados(self):
        """Interpreta los resultados en el contexto logístico."""
        print("\n" + "="*60)
        print("INTERPRETACIÓN LOGÍSTICA")
        print("="*60)
        print("""
En nuestro escenario logístico:
- 'Agresivo': Reducir drásticamente las tarifas de envío para ganar mercado.
- 'Moderado': Mantener tarifas competitivas pero estables.
- 'Pasivo': Mantener tarifas altas, enfocándose en nichos de lujo.

Si el equilibrio de Nash es (Agresivo, Agresivo), ambas empresas 
entran en una 'guerra de precios' que reduce sus ganancias (2,2), 
aunque cooperar en (Moderado, Moderado) les daría (4,4). Esto 
demuestra cómo la competencia individual puede perjudicar al mercado.
        """)

if __name__ == "__main__":
    juego = JuegoLogistico()
    juego.mostrar_matriz()
    juego.encontrar_equilibrios_nash()
    juego.interpretar_resultados()