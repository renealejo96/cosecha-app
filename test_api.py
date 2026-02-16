"""
Script de prueba para verificar los endpoints de la API de cosecha
Ejecutar: python test_api.py
"""

import requests
import json

# URL base (cambiar si estás en producción)
BASE_URL = "http://127.0.0.1:5000"

def test_api_resumen():
    """Prueba el endpoint /api/resumen"""
    print("\n" + "="*60)
    print("TEST 1: API Resumen (formato plano)")
    print("="*60)
    
    url = f"{BASE_URL}/api/resumen"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Respuesta exitosa!")
            print(f"   Semana: {data.get('semana', 'N/A')}")
            print(f"   Total registros: {data.get('total_registros', 0)}")
            
            if data.get('datos'):
                print(f"\n   Primeros 3 registros:")
                for i, registro in enumerate(data['datos'][:3], 1):
                    print(f"\n   Registro {i}:")
                    print(f"      - Variedad: {registro.get('variedad')}")
                    print(f"      - Bloque: {registro.get('modulo')}")
                    print(f"      - Total tallos: {registro.get('total_tallos')}")
                    print(f"      - Fecha: {registro.get('fecha')}")
            else:
                print("   ⚠️  No hay datos para mostrar")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_api_resumen_semana():
    """Prueba el endpoint /api/resumen con semana específica"""
    print("\n" + "="*60)
    print("TEST 2: API Resumen con semana específica")
    print("="*60)
    
    # Primero obtenemos las semanas disponibles
    semanas_url = f"{BASE_URL}/api/semanas"
    try:
        response = requests.get(semanas_url)
        if response.status_code == 200:
            semanas_data = response.json()
            if semanas_data.get('semanas'):
                semana = semanas_data['semanas'][0]  # Tomar la primera semana
                print(f"Probando con semana: {semana}")
                
                url = f"{BASE_URL}/api/resumen?semana={semana}"
                response = requests.get(url)
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ Respuesta exitosa!")
                    print(f"   Semana solicitada: {semana}")
                    print(f"   Total registros: {data.get('total_registros', 0)}")
                else:
                    print(f"❌ Error: {response.status_code}")
            else:
                print("⚠️  No hay semanas disponibles en la BD")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_api_resumen_jerarquico():
    """Prueba el endpoint /api/resumen con formato jerárquico"""
    print("\n" + "="*60)
    print("TEST 3: API Resumen (formato jerárquico)")
    print("="*60)
    
    url = f"{BASE_URL}/api/resumen?formato=jerarquico"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Respuesta exitosa!")
            print(f"   Semana: {data.get('semana', 'N/A')}")
            print(f"\n   Estructura de datos:")
            
            datos = data.get('datos', {})
            for producto_maestro, variedades in list(datos.items())[:2]:  # Mostrar solo 2 productos
                print(f"\n   📦 Producto: {producto_maestro}")
                for variedad, info in list(variedades.items())[:2]:  # Mostrar solo 2 variedades
                    print(f"      🌸 Variedad: {variedad}")
                    print(f"         Total tallos: {info.get('total_tallos', 0)}")
                    print(f"         Días: {list(info.get('dias', {}).keys())}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_api_semanas():
    """Prueba el endpoint /api/semanas"""
    print("\n" + "="*60)
    print("TEST 4: API Semanas disponibles")
    print("="*60)
    
    url = f"{BASE_URL}/api/semanas"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Respuesta exitosa!")
            print(f"   Total de semanas: {data.get('total', 0)}")
            semanas = data.get('semanas', [])
            if semanas:
                print(f"   Semanas disponibles (primeras 10):")
                for semana in semanas[:10]:
                    print(f"      - {semana}")
            else:
                print("   ⚠️  No hay semanas disponibles")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_api_excel():
    """Prueba el endpoint /api/resumen/excel"""
    print("\n" + "="*60)
    print("TEST 5: API Descargar Excel")
    print("="*60)
    
    # Primero obtenemos una semana disponible
    semanas_url = f"{BASE_URL}/api/semanas"
    try:
        response = requests.get(semanas_url)
        if response.status_code == 200:
            semanas_data = response.json()
            if semanas_data.get('semanas'):
                semana = semanas_data['semanas'][0]
                print(f"Descargando Excel de semana: {semana}")
                
                url = f"{BASE_URL}/api/resumen/excel?semana={semana}"
                response = requests.get(url)
                
                if response.status_code == 200:
                    filename = f"test_resumen_semana_{semana}.xlsx"
                    with open(filename, 'wb') as f:
                        f.write(response.content)
                    print(f"✅ Archivo descargado exitosamente!")
                    print(f"   Nombre: {filename}")
                    print(f"   Tamaño: {len(response.content)} bytes")
                else:
                    print(f"❌ Error: {response.status_code}")
            else:
                print("⚠️  No hay semanas disponibles para descargar")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_conexion():
    """Verifica que la aplicación esté corriendo"""
    print("\n" + "="*60)
    print("VERIFICANDO CONEXIÓN CON EL SERVIDOR")
    print("="*60)
    
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code in [200, 302, 404]:  # Cualquier respuesta válida
            print(f"✅ Servidor está corriendo en {BASE_URL}")
            return True
        else:
            print(f"⚠️  Servidor respondió con código: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ No se puede conectar a {BASE_URL}")
        print("   ¿Está corriendo el servidor Flask?")
        print("   Ejecuta: python app.py")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Ejecuta todas las pruebas"""
    print("\n" + "="*60)
    print("🧪 INICIANDO PRUEBAS DE LA API DE COSECHA")
    print("="*60)
    
    if not test_conexion():
        print("\n❌ No se puede continuar sin conexión al servidor")
        return
    
    # Ejecutar todas las pruebas
    test_api_semanas()
    test_api_resumen()
    test_api_resumen_semana()
    test_api_resumen_jerarquico()
    test_api_excel()
    
    print("\n" + "="*60)
    print("✅ PRUEBAS COMPLETADAS")
    print("="*60)
    print("\nPróximos pasos:")
    print("1. Importa los datos en Excel usando Power Query")
    print("   Consulta: EXCEL_POWER_QUERY_GUIDE.md")
    print("\n2. Lee la documentación completa:")
    print("   - API_DOCUMENTATION.md")
    print("   - TESTING_API.md")
    print("\n3. Para producción, actualiza BASE_URL a tu URL de Render")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
