# 🎉 API de Resumen de Cosecha - Implementación Completa

## ✅ Lo que hemos creado

He agregado **3 endpoints de API** a tu aplicación Flask para que puedas consumir los datos del resumen de cosecha desde Excel u otras aplicaciones.

---

## 📋 Endpoints Disponibles

### 1. **GET `/api/resumen`** - Obtener datos en formato JSON

**Descripción**: Devuelve los datos del resumen de cosecha en formato JSON.

**Parámetros opcionales**:
- `semana`: Semana en formato AASS (ej: `2546`). Si no se especifica, devuelve la semana actual.
- `formato`: `plano` (tabla, ideal para Excel) o `jerarquico` (agrupado)

**Ejemplos**:
```
http://localhost:5000/api/resumen
http://localhost:5000/api/resumen?semana=2546
http://localhost:5000/api/resumen?semana=2546&formato=jerarquico
```

**Respuesta (formato plano)**:
```json
{
  "semana": "2546",
  "total_registros": 150,
  "datos": [
    {
      "semana": "2546",
      "producto_maestro": "FREEDOM",
      "variedad": "Freedom",
      "fecha": "2025-11-10",
      "dia_semana": "Lunes",
      "modulo": "F6",
      "hora_cosecha": "08:30:00",
      "tallos_por_malla": 25,
      "mallas": 10,
      "total_tallos": 250,
      "responsable": "Juan Pérez",
      "viaje": "Viaje 1"
    }
  ]
}
```

---

### 2. **GET `/api/resumen/excel`** - Descargar archivo Excel

**Descripción**: Genera y descarga automáticamente un archivo Excel con los datos del resumen.

**Parámetros opcionales**:
- `semana`: Semana en formato AASS (ej: `2546`)

**Ejemplos**:
```
http://localhost:5000/api/resumen/excel
http://localhost:5000/api/resumen/excel?semana=2546
```

**Resultado**: Descarga un archivo Excel con el nombre `resumen_cosecha_semana_XXXX.xlsx`

---

### 3. **GET `/api/semanas`** - Obtener semanas disponibles

**Descripción**: Devuelve todas las semanas que tienen datos en la base de datos.

**Ejemplo**:
```
http://localhost:5000/api/semanas
```

**Respuesta**:
```json
{
  "total": 24,
  "semanas": ["2546", "2545", "2544", ...]
}
```

---

## 📊 Cómo consumir desde Excel

### **Método 1: Power Query (⭐ Recomendado)**

1. Abre Excel
2. Ve a **Datos** > **Obtener datos** > **Desde otras fuentes** > **Desde web**
3. Ingresa la URL: `http://localhost:5000/api/resumen?semana=2546`
4. En el Editor de Power Query:
   - Expande la columna `datos`
   - Selecciona todas las columnas
   - Desmarca "Usar nombre original como prefijo"
5. Click en **Cerrar y cargar**
6. ¡Listo! Los datos se importarán como tabla

**Para actualizar los datos**: Click derecho en la tabla > **Actualizar**

---

### **Método 2: Descarga directa de Excel**

1. Abre tu navegador
2. Ingresa: `http://localhost:5000/api/resumen/excel?semana=2546`
3. El archivo Excel se descarga automáticamente
4. Abre el archivo descargado

---

## 📁 Archivos Creados

He creado los siguientes archivos de documentación:

1. **API_DOCUMENTATION.md** - Documentación completa de la API
2. **EXCEL_POWER_QUERY_GUIDE.md** - Guía paso a paso para importar en Excel
3. **TESTING_API.md** - Instrucciones y URLs para probar la API
4. **test_api.py** - Script Python para probar todos los endpoints
5. **excel_vba_module.bas** - Código VBA para Excel (opcional)
6. **RESUMEN_API.md** - Este archivo

---

## 🚀 Cómo usar

### Paso 1: Iniciar el servidor

```bash
python app.py
```

El servidor se ejecutará en: `http://localhost:5000`

### Paso 2: Probar los endpoints

**Opción A: Desde el navegador**
- Abre: `http://localhost:5000/api/resumen`
- Verás el JSON con los datos

**Opción B: Descargar Excel**
- Abre: `http://localhost:5000/api/resumen/excel`
- Se descargará el archivo automáticamente

**Opción C: Ejecutar script de prueba**
```bash
python test_api.py
```

### Paso 3: Importar en Excel

Sigue la guía en **EXCEL_POWER_QUERY_GUIDE.md**

---

## 🌐 Para Producción (Render.com)

Cuando despliegues tu aplicación en producción, simplemente reemplaza:

```
http://localhost:5000
```

por tu URL de producción:

```
https://tu-app.onrender.com
```

Los endpoints funcionarán exactamente igual:
- `https://tu-app.onrender.com/api/resumen`
- `https://tu-app.onrender.com/api/resumen/excel`
- `https://tu-app.onrender.com/api/semanas`

---

## 📦 Columnas Disponibles

Los datos incluyen las siguientes columnas:

| Columna | Descripción |
|---------|-------------|
| **semana** | Semana en formato AASS (ej: 2546) |
| **producto_maestro** | Categoría del producto (ej: FREEDOM, EXPLORER) |
| **variedad** | Variedad específica de flor |
| **fecha** | Fecha de cosecha (YYYY-MM-DD) |
| **dia_semana** | Día de la semana (Lunes, Martes, etc.) |
| **modulo** | Bloque o módulo de cosecha |
| **hora_cosecha** | Hora de cosecha (HH:MM:SS) |
| **tallos_por_malla** | Número de tallos por malla (10, 15, 25, 30) |
| **mallas** | Cantidad de mallas cosechadas |
| **total_tallos** | Total de tallos (tallos_por_malla × mallas) |
| **responsable** | Persona responsable de la cosecha |
| **viaje** | Identificador del viaje |

---

## 💡 Casos de Uso

### 1. **Dashboard en Excel**
- Importa datos con Power Query
- Crea tablas dinámicas
- Genera gráficos automáticos
- Actualiza con un click

### 2. **Reportes Automáticos**
- Descarga Excel diario/semanal
- Envía por correo automáticamente
- Integra con otras herramientas

### 3. **Integración con Power BI**
- Conecta Power BI a la API
- Crea dashboards interactivos
- Análisis en tiempo real

### 4. **Análisis de Datos**
- Exporta a Python/R
- Realiza análisis estadísticos
- Predicciones y forecasting

---

## 🔧 Solución de Problemas

### Error: "No se puede conectar"
✅ Verifica que el servidor esté corriendo: `python app.py`

### Error: "No hay datos"
✅ Verifica que haya registros en la base de datos para la semana solicitada

### Datos no se actualizan en Excel
✅ Click derecho en la tabla > **Actualizar**

### Consulta muy lenta
✅ Filtra por semanas específicas en lugar de cargar todo

---

## 📚 Documentación Completa

- **API_DOCUMENTATION.md** - Referencias técnicas de la API
- **EXCEL_POWER_QUERY_GUIDE.md** - Tutorial detallado de Excel
- **TESTING_API.md** - Guías de prueba

---

## ✨ Características

✅ **3 endpoints RESTful** listos para usar  
✅ **Formato JSON** para integración con cualquier aplicación  
✅ **Descarga directa de Excel** sin programación  
✅ **Compatibilidad con Power Query** de Excel  
✅ **Datos en tiempo real** desde la base de datos  
✅ **Filtrado por semana** flexible  
✅ **Documentación completa** y ejemplos  
✅ **Script de pruebas** incluido  

---

## 🎯 Siguiente Paso

1. **Iniciar el servidor**: `python app.py`
2. **Probar la API**: Abre `http://localhost:5000/api/resumen` en tu navegador
3. **Importar en Excel**: Sigue `EXCEL_POWER_QUERY_GUIDE.md`

---

¡Listo! Ahora puedes consumir tus datos de cosecha en Excel y cualquier otra aplicación que soporte HTTP/REST APIs. 🚀
