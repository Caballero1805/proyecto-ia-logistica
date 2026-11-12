import json
import os

print("🧹 Limpiando archivos JSON...")

# Rutas
ruta_esc = 'config/escenario.json'
ruta_par = 'config/parametros.json'

# Función para leer (ignorando BOM) y reescribir (UTF-8 puro)
def limpiar(ruta):
    if not os.path.exists(ruta):
        print(f"⚠️ No existe {ruta}")
        return
    
    # Leer con utf-8-sig para ignorar el BOM si existe
    with open(ruta, 'r', encoding='utf-8-sig') as f:
        data = json.load(f)
    
    # Reescribir con utf-8 puro (sin BOM)
    with open(ruta, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"   ✅ {ruta} limpiado.")

limpiar(ruta_esc)
limpiar(ruta_par)

print("\n🗑️  Ahora puedes borrar este archivo 'limpiar_json.py'. ¡Ya no lo necesitas!")