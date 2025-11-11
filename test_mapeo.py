import csv
import os

def cargar_maestro_productos():
    """Cargar mapeo de variedades a productos maestros desde CSV"""
    mapeo = {}
    csv_path = 'MAESTRO_PROS.csv'
    try:
        if os.path.exists(csv_path):
            with open(csv_path, 'r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file, delimiter=';')
                for row in reader:
                    variedad = row['variedad'].strip()
                    prod_maestro = row['prod_maestro'].strip()
                    mapeo[variedad] = prod_maestro
                    print(f"'{variedad}' -> '{prod_maestro}'")
    except Exception as e:
        print(f"Error cargando maestro productos: {e}")
    
    return mapeo

# Probar
print("=== CARGANDO MAESTRO_PROS.csv ===\n")
mapeo = cargar_maestro_productos()
print(f"\n=== TOTAL: {len(mapeo)} variedades ===\n")

# Buscar GOLDEN GLORY YELLOW específicamente
print("=== BUSCANDO 'GOLDEN GLORY YELLOW' ===")
if 'GOLDEN GLORY YELLOW' in mapeo:
    print(f"✅ Encontrada: GOLDEN GLORY YELLOW -> {mapeo['GOLDEN GLORY YELLOW']}")
else:
    print("❌ NO encontrada en el mapeo")
    print("\nVariedades que contienen 'GOLDEN':")
    for var in mapeo.keys():
        if 'GOLDEN' in var:
            print(f"  - '{var}'")
