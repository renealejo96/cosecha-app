# Guía Paso a Paso: Importar Datos de la API en Excel con Power Query

## ¿Por qué usar Power Query?

Power Query es la forma más fácil y eficiente de conectar Excel con tu API. No requiere programación y permite actualizar los datos con un solo clic.

---

## Método 1: Power Query - Importar datos JSON (Recomendado)

### Paso 1: Preparar Excel

1. Abre un nuevo libro de Excel
2. Ve a la pestaña **Datos**

### Paso 2: Conectar con la API

1. Haz clic en **Obtener datos** (o **Nueva consulta**)
2. Selecciona **Desde otras fuentes** > **Desde web**
3. En el cuadro de diálogo, ingresa la URL:
   ```
   http://localhost:5000/api/resumen?semana=2546
   ```
   (Reemplaza `2546` con la semana que desees, o quita `?semana=2546` para la semana actual)

4. Haz clic en **Aceptar**

### Paso 3: Transformar los Datos

1. Se abrirá el **Editor de Power Query**
2. Verás una vista previa con columnas como `semana`, `total_registros`, y `datos`
3. Haz clic en la columna **datos** y selecciona **Expandir** (ícono con dos flechas)
4. Marca todas las casillas para incluir todos los campos:
   - semana
   - producto_maestro
   - variedad
   - fecha
   - dia_semana
   - modulo
   - hora_cosecha
   - tallos_por_malla
   - mallas
   - total_tallos
   - responsable
   - viaje
5. Desmarca "Usar el nombre de la columna original como prefijo"
6. Haz clic en **Aceptar**

### Paso 4: Configurar Tipos de Datos

1. Power Query detectará automáticamente los tipos
2. Si es necesario, ajusta los tipos de columna:
   - `fecha`: Fecha
   - `hora_cosecha`: Hora
   - `tallos_por_malla`, `mallas`, `total_tallos`: Número entero
   - Resto: Texto

### Paso 5: Cargar los Datos

1. Haz clic en **Cerrar y cargar** (esquina superior izquierda)
2. Los datos se cargarán en una nueva hoja de Excel
3. Se creará una tabla automáticamente

### Paso 6: Actualizar los Datos

Para actualizar los datos en cualquier momento:
1. Haz clic derecho en la tabla
2. Selecciona **Actualizar**

O simplemente:
- Ve a la pestaña **Datos** > **Actualizar todo**

---

## Método 2: Descargar Excel Directamente (Más Rápido)

### Opción A: Desde el Navegador

1. Abre tu navegador web
2. Ingresa la URL:
   ```
   http://localhost:5000/api/resumen/excel?semana=2546
   ```
3. El archivo Excel se descargará automáticamente
4. Abre el archivo descargado

### Opción B: Crear un Hipervínculo en Excel

1. En una celda de Excel, escribe:
   ```
   =HYPERLINK("http://localhost:5000/api/resumen/excel?semana=2546", "Descargar Resumen Semana 2546")
   ```
2. Haz clic en el hipervínculo para descargar el archivo

---

## Método 3: Crear Consulta Dinámica con Parámetros

### Configurar Parámetro de Semana

1. Crea una celda para ingresar la semana (ej: celda B1)
2. En B1, escribe: `2546`
3. En la pestaña **Datos**, haz clic en **Obtener datos** > **Desde otras fuentes** > **Desde web**
4. En el cuadro de URL, NO ingreses la URL todavía, haz clic en **Avanzado**
5. En **Partes de la URL**, ingresa:
   - Parte 1: `http://localhost:5000/api/resumen?semana=`
   - Haz clic en **Agregar parte**
   - Parte 2: Selecciona **Archivo de trabajo** > busca tu hoja > selecciona celda B1
6. Haz clic en **Aceptar**

Ahora, cada vez que cambies el valor en B1 y actualices la consulta, obtendrás los datos de esa semana.

---

## Método 4: Crear un Dashboard Interactivo

### Paso 1: Importar Múltiples Semanas

1. Usa Power Query para importar datos de varias semanas
2. Crea una consulta para cada semana o usa el método de parámetros

### Paso 2: Crear Tablas Dinámicas

1. Selecciona los datos importados
2. Ve a **Insertar** > **Tabla dinámica**
3. Configura:
   - **Filas**: Producto Maestro, Variedad
   - **Valores**: Suma de Total Tallos
   - **Filtros**: Semana, Día Semana
   - **Columnas**: Bloque/Módulo

### Paso 3: Crear Gráficos

1. Con la tabla dinámica seleccionada, ve a **Insertar** > **Gráfico dinámico**
2. Selecciona el tipo de gráfico (barras, líneas, etc.)
3. Personaliza colores y formato

### Paso 4: Agregar Segmentadores

1. Selecciona la tabla dinámica
2. Ve a **Analizar** > **Insertar segmentador**
3. Selecciona: Semana, Producto Maestro, Día Semana
4. Los segmentadores permitirán filtrar dinámicamente

---

## Configuración para Producción

Cuando despliegues tu aplicación en producción (ej: Render), actualiza la URL:

1. Abre el Editor de Power Query
2. Haz clic en **Configuración de origen**
3. Reemplaza:
   ```
   http://localhost:5000
   ```
   por tu URL de producción:
   ```
   https://tu-app.onrender.com
   ```
4. Haz clic en **Aceptar** y luego **Cerrar y cargar**

---

## Automatización con Macros (Opcional)

### Crear Botón de Actualización

1. Ve a la pestaña **Programador** (si no está visible, habilítala en Opciones)
2. Haz clic en **Insertar** > **Botón** (Control de formulario)
3. Dibuja el botón en tu hoja
4. Asigna la siguiente macro:

```vba
Sub ActualizarDatos()
    ActiveWorkbook.RefreshAll
    MsgBox "Datos actualizados correctamente!", vbInformation
End Sub
```

5. Haz clic en **Aceptar**
6. Ahora puedes actualizar con un clic en el botón

---

## Solución de Problemas

### Error: "No se puede conectar al servidor"

- Verifica que tu aplicación Flask esté ejecutándose
- Comprueba que la URL sea correcta
- Si usas localhost, asegúrate de estar en la misma red

### Error: "Formato JSON inválido"

- Verifica que el endpoint `/api/resumen` esté funcionando en tu navegador
- Comprueba que haya datos en la base de datos para la semana solicitada

### Los datos no se actualizan

- Haz clic en **Datos** > **Actualizar todo**
- O haz clic derecho en la tabla > **Actualizar**
- Verifica que la conexión a la API esté activa

### Consulta muy lenta

- Filtra por semanas específicas en lugar de cargar todos los datos
- Usa el endpoint `/api/resumen/excel` para descargas grandes
- Considera crear índices en la base de datos

---

## Consejos Adicionales

1. **Formato de Fechas**: Power Query puede tener problemas con formatos de fecha. Si ves fechas incorrectas, cambia el tipo de columna a Texto primero, luego a Fecha.

2. **Actualización Automática**: Puedes configurar Excel para que actualice automáticamente al abrir el archivo:
   - Haz clic derecho en la consulta > **Propiedades**
   - Marca "Actualizar al abrir el archivo"

3. **Guardar Credenciales**: Si tu API requiere autenticación en el futuro, Power Query te permitirá guardar las credenciales de forma segura.

4. **Compartir el Libro**: Si compartes el archivo Excel con otros usuarios, asegúrate de que tengan acceso a la misma URL de la API.

---

## Recursos Adicionales

- [Documentación oficial de Power Query](https://support.microsoft.com/power-query)
- [Video tutoriales de Power Query](https://www.youtube.com/results?search_query=power+query+tutorial+español)
- Archivo de documentación: `API_DOCUMENTATION.md` en tu proyecto

---

¡Listo! Ahora puedes consumir los datos de tu aplicación de cosecha directamente en Excel.
