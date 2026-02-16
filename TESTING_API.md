# Script de Prueba para los Endpoints de la API

## URLs de Prueba

### 1. Probar endpoint de resumen JSON (formato plano)
http://127.0.0.1:5000/api/resumen

### 2. Probar endpoint de resumen JSON con semana específica
http://127.0.0.1:5000/api/resumen?semana=2546

### 3. Probar endpoint de resumen JSON (formato jerárquico)
http://127.0.0.1:5000/api/resumen?formato=jerarquico

### 4. Descargar Excel directamente
http://127.0.0.1:5000/api/resumen/excel

### 5. Descargar Excel de semana específica
http://127.0.0.1:5000/api/resumen/excel?semana=2546

### 6. Obtener lista de semanas disponibles
http://127.0.0.1:5000/api/semanas

---

## Pruebas con cURL (desde PowerShell/CMD)

```powershell
# 1. Obtener resumen JSON
curl http://127.0.0.1:5000/api/resumen

# 2. Obtener resumen de semana específica
curl "http://127.0.0.1:5000/api/resumen?semana=2546"

# 3. Obtener formato jerárquico
curl "http://127.0.0.1:5000/api/resumen?formato=jerarquico"

# 4. Descargar archivo Excel
curl -o resumen.xlsx "http://127.0.0.1:5000/api/resumen/excel?semana=2546"

# 5. Obtener semanas disponibles
curl http://127.0.0.1:5000/api/semanas
```

---

## Pruebas con Python

```python
import requests
import json

# URL base
BASE_URL = "http://127.0.0.1:5000"

# 1. Obtener resumen en formato JSON
response = requests.get(f"{BASE_URL}/api/resumen")
data = response.json()
print("Resumen (formato plano):")
print(json.dumps(data, indent=2, ensure_ascii=False))

# 2. Obtener resumen de semana específica
response = requests.get(f"{BASE_URL}/api/resumen", params={"semana": "2546"})
data = response.json()
print(f"\nResumen semana 2546:")
print(f"Total registros: {data['total_registros']}")
if data['datos']:
    print(f"Primer registro: {data['datos'][0]}")

# 3. Obtener formato jerárquico
response = requests.get(f"{BASE_URL}/api/resumen", params={"formato": "jerarquico"})
data = response.json()
print("\nResumen (formato jerárquico):")
print(json.dumps(data, indent=2, ensure_ascii=False))

# 4. Descargar Excel
response = requests.get(f"{BASE_URL}/api/resumen/excel", params={"semana": "2546"})
with open("resumen_cosecha.xlsx", "wb") as f:
    f.write(response.content)
print("\nArchivo Excel descargado: resumen_cosecha.xlsx")

# 5. Obtener semanas disponibles
response = requests.get(f"{BASE_URL}/api/semanas")
data = response.json()
print(f"\nSemanas disponibles ({data['total']}):")
print(data['semanas'])
```

---

## Pruebas con PowerShell (para Windows)

```powershell
# 1. Obtener resumen JSON
$response = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/resumen" -Method Get
$response | ConvertTo-Json -Depth 10

# 2. Obtener semana específica
$response = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/resumen?semana=2546" -Method Get
Write-Host "Total de registros: $($response.total_registros)"
$response.datos | Format-Table

# 3. Descargar Excel
Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/resumen/excel?semana=2546" -OutFile "resumen.xlsx"
Write-Host "Archivo descargado: resumen.xlsx"

# 4. Obtener semanas disponibles
$response = Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/semanas" -Method Get
$response.semanas
```

---

## Verificación de los Endpoints

1. ✅ **Servidor corriendo**: http://127.0.0.1:5000
2. ✅ **Endpoint API resumen**: http://127.0.0.1:5000/api/resumen
3. ✅ **Endpoint API Excel**: http://127.0.0.1:5000/api/resumen/excel
4. ✅ **Endpoint API semanas**: http://127.0.0.1:5000/api/semanas

---

## Siguiente Paso: Importar en Excel

### Opción 1: Power Query (Recomendado)

1. Abre Excel
2. Datos > Obtener datos > Desde otras fuentes > Desde web
3. URL: `http://127.0.0.1:5000/api/resumen?semana=2546`
4. Expande la columna "datos"
5. Cerrar y cargar

### Opción 2: Descarga directa

Abre en el navegador:
http://127.0.0.1:5000/api/resumen/excel?semana=2546

---

## Notas Importantes

- La aplicación está corriendo en modo desarrollo en `http://127.0.0.1:5000`
- Para producción, usa la URL de Render.com cuando despliegues
- Los endpoints devuelven datos en tiempo real desde la base de datos
- El formato "plano" es ideal para Excel, el "jerárquico" para aplicaciones web

---

Consulta `API_DOCUMENTATION.md` y `EXCEL_POWER_QUERY_GUIDE.md` para más detalles.
