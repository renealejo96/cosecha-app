# Guía Rápida: 3 Formas de Usar la API en Excel

## 🚀 Forma 1: Power Query (La Más Fácil - NO REQUIERE CÓDIGO)

### Pasos:
1. Abre Excel
2. Click en pestaña **Datos**
3. Click en **Obtener datos** → **Desde otras fuentes** → **Desde web**
4. Pega esta URL:
   ```
   http://localhost:5000/api/resumen
   ```
5. Click **Aceptar**
6. En la ventana que aparece, click en las **dos flechas** al lado de "datos"
7. Marca todas las casillas
8. Click **Aceptar**
9. Click **Cerrar y cargar**

### ¡Listo! Los datos están en Excel

### Para actualizar los datos:
- Click derecho en cualquier celda de la tabla → **Actualizar**

---

## 📥 Forma 2: Descargar Excel Directamente (La Más Rápida)

### Pasos:
1. Abre tu navegador (Chrome, Firefox, Edge, etc.)
2. Copia y pega esta URL en la barra de direcciones:
   ```
   http://localhost:5000/api/resumen/excel
   ```
3. Presiona Enter
4. El archivo Excel se descarga automáticamente
5. Abre el archivo descargado

### Para una semana específica:
```
http://localhost:5000/api/resumen/excel?semana=2546
```
(Cambia 2546 por la semana que necesites)

---

## 🔗 Forma 3: Crear un Botón en Excel

### Pasos:

1. En una celda (ej: A1), escribe la semana: `2546`
2. En otra celda (ej: A3), crea un hipervínculo con esta fórmula:
   ```excel
   =HYPERLINK("http://localhost:5000/api/resumen/excel?semana="&A1, "📥 Descargar Resumen Semana "&A1)
   ```
3. Ahora al hacer click en esa celda, descargará el Excel de esa semana

### Mejorar con un botón:

1. Agrega un botón:
   - Pestaña **Programador** → **Insertar** → **Botón** (si no ves "Programador", habilítalo en Opciones de Excel)
2. Dibuja el botón
3. En la ventana que aparece, click **Nueva**
4. Pega este código:

```vba
Sub DescargarResumen()
    Dim semana As String
    semana = Range("A1").Value  ' Lee la semana de la celda A1
    
    ' Construir URL
    Dim url As String
    url = "http://localhost:5000/api/resumen/excel?semana=" & semana
    
    ' Abrir en navegador (descarga automática)
    ThisWorkbook.FollowHyperlink url
    
    MsgBox "Descargando resumen de semana " & semana, vbInformation
End Sub
```

5. Cierra el editor VBA
6. Ahora al hacer click en el botón, descargará el Excel

---

## 🎨 Crear Dashboard Automático

### Configuración única (hazlo una sola vez):

1. Importa los datos con Power Query (Forma 1)
2. Los datos aparecerán en una hoja (ej: "Hoja1")
3. Crea una **Tabla Dinámica**:
   - Selecciona cualquier celda de los datos
   - Click en **Insertar** → **Tabla dinámica**
   - Click **Aceptar**
4. Configura la tabla:
   - **Filas**: Producto Maestro, Variedad
   - **Valores**: Suma de Total Tallos
   - **Columnas**: Día Semana
   - **Filtros**: Semana

5. Inserta un gráfico:
   - Con la tabla dinámica seleccionada
   - Click en **Insertar** → **Gráfico dinámico**
   - Elige tipo de gráfico (barras, líneas, etc.)

### Cada vez que necesites actualizar:
1. Click derecho en la tabla → **Actualizar**
2. ¡El gráfico se actualiza automáticamente!

---

## 🔄 Cambiar de Semana en Power Query

Si quieres cambiar la semana sin recrear la consulta:

### Opción A: Editar manualmente
1. Click derecho en la consulta (panel derecho) → **Editar**
2. En la barra de fórmulas, cambia el número de semana en la URL
3. Click **Cerrar y cargar**

### Opción B: Usar parámetro (Avanzado)
1. En Power Query, click en **Administrar parámetros** → **Nuevo parámetro**
2. Nombre: `Semana`
3. Tipo: Texto
4. Valor actual: `2546`
5. En la consulta, reemplaza `2546` por el parámetro
6. Ahora puedes cambiar la semana desde el panel de parámetros

---

## 📊 Ejemplo de Fórmulas Útiles en Excel

Una vez que tengas los datos en Excel, puedes usar fórmulas:

### Contar total de tallos por variedad:
```excel
=SUMAR.SI(C:C,"Freedom",J:J)
```
(Asumiendo que C es Variedad y J es Total Tallos)

### Contar registros de un módulo:
```excel
=CONTAR.SI(F:F,"F6")
```
(Asumiendo que F es Módulo)

### Promedio de tallos por día:
```excel
=PROMEDIO.SI(E:E,"Lunes",J:J)
```
(Asumiendo que E es Día Semana y J es Total Tallos)

---

## 🌐 Para Producción

Cuando tu aplicación esté en internet (Render.com), solo cambia la URL:

**De:**
```
http://localhost:5000/api/resumen
```

**A:**
```
https://tu-app.onrender.com/api/resumen
```

Todo lo demás funciona exactamente igual.

---

## ❓ Preguntas Frecuentes

### ¿Cómo sé qué semanas están disponibles?
Abre en el navegador: `http://localhost:5000/api/semanas`

### ¿Puedo automatizar la actualización?
Sí, en Power Query:
1. Click derecho en la consulta → **Propiedades**
2. Marca "Actualizar al abrir el archivo"
3. Opcional: "Actualizar cada X minutos"

### ¿Funciona con Excel en Mac?
Sí, Power Query funciona igual en Mac (Excel 2016+)

### ¿Puedo usar esto en Google Sheets?
Sí, pero necesitas usar Apps Script. En Excel es más fácil.

### ¿Los datos se guardan en mi Excel?
Sí, los datos se guardan en tu archivo. Al actualizar, se reemplazan con los datos más recientes.

---

## 🎯 Recomendación

**Para empezar rápido**: Usa la **Forma 2** (descargar directamente)

**Para trabajo diario**: Usa la **Forma 1** (Power Query) porque puedes actualizar con un click

**Para automatización**: Usa la **Forma 3** (Botón con VBA)

---

## 📝 Resumen de URLs

```
Datos JSON:          http://localhost:5000/api/resumen
Datos semana 2546:   http://localhost:5000/api/resumen?semana=2546
Descargar Excel:     http://localhost:5000/api/resumen/excel
Excel semana 2546:   http://localhost:5000/api/resumen/excel?semana=2546
Ver semanas:         http://localhost:5000/api/semanas
```

---

¿Necesitas ayuda? Revisa los otros archivos de documentación:
- **API_DOCUMENTATION.md** - Detalles técnicos
- **EXCEL_POWER_QUERY_GUIDE.md** - Guía completa paso a paso
- **RESUMEN_API.md** - Resumen general
