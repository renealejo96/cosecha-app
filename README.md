# 🌱 Sistema de Registro de Cosecha

Una aplicación web profesional desarrollada en Flask para el registro y gestión de datos de cosecha agrícola.

## ✨ Características

- **📋 Registro completo de cosecha** con todos los campos requeridos
- **🔢 Cálculo automático** del total de tallos (tallos × mallas)
- **⏰ Hora automática** que se registra al momento de guardar
- **📝 Selectores CSV** para variedades, responsables y módulos
- **📊 Sistema de reportes** con estadísticas y análisis por variedad
- **🔒 Confirmación de eliminación** para mayor seguridad
- **🗄️ Base de datos PostgreSQL** para producción
- **🌐 Interfaz moderna** con Bootstrap 5 y Font Awesome
- **📱 Diseño responsivo** para escritorio y móvil
- **⚡ Operaciones CRUD** completas con validación

## 📋 Campos del Registro

- **📅 Fecha**: Fecha de la cosecha
- **🚛 Viaje**: Número o nombre del viaje
- **📆 Semana**: Semana del año (1-53)
- **🌿 Tallos**: Cantidad de tallos por malla (10, 15, 25, 30)
- **📦 Mallas**: Número de mallas
- **🏭 Módulo**: Selector desde `modulos.csv`
- **📊 Total Tallos**: Cálculo automático (tallos × mallas)
- **🌱 Variedad**: Selector desde `variedades.csv`
- **⏰ Hora**: Automática al guardar
- **👤 Responsable**: Selector desde `responsables.csv`

## 🚀 Instalación y Configuración
### **📋 Requisitos Previos**

1. **Python 3.7+** instalado
2. **PostgreSQL** instalado y ejecutándose
3. **Base de datos PostgreSQL** creada (ej: `pyganflor`)

### **⚙️ Configuración**

1. **Crear entorno virtual**:
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Instalar dependencias**:
   ```cmd
   pip install -r requirements.txt
   ```

3. **Configurar base de datos**:
   - Edita `app.py` línea 9 con tus credenciales de PostgreSQL:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://usuario:contraseña@localhost:5432/nombre_bd'
   ```

4. **Ejecutar aplicación**:
   ```cmd
   python app.py
   ```

5. **Acceder**: `http://localhost:5000`

## 📊 Gestión de Datos CSV

### **Archivos de Configuración**
- **`variedades.csv`**: Variedades de cosecha disponibles
- **`responsables.csv`**: Lista de responsables  
- **`modulos.csv`**: Módulos/sectores disponibles

### **Edición de Datos**
Edita los archivos CSV directamente:
1. Abre el archivo CSV en Excel o editor de texto
2. Agrega o elimina líneas según necesites  
3. Guarda el archivo
4. Los cambios se reflejan automáticamente

**Formato requerido:**
```csv
variedad
Gold
Red Naomi
Explorer
```

```csv
responsable
Kevin Martinez
Maria Rodriguez
Juan Perez
```

```csv
modulo
Modulo A1
Invernadero 1
Sector Norte
```

Para más detalles, consulta `GESTION_CSV.md`.

## Uso

### Crear un Nuevo Registro
1. Hacer clic en "Nuevo Registro" en la barra de navegación
2. Llenar todos los campos obligatorios
3. El total de tallos se calcula automáticamente
4. La hora se registra automáticamente al guardar
5. Hacer clic en "Guardar Registro"

### Ver Registros
- La página principal muestra todos los registros en una tabla
- Incluye estadísticas básicas (total de registros y total de tallos)
- Los registros se ordenan por fecha de creación (más recientes primero)

### Editar un Registro
1. Hacer clic en el botón de editar (ícono de lápiz) en la tabla
2. Modificar los campos necesarios
3. El total de tallos se recalcula automáticamente
4. La hora original se mantiene sin cambios
5. Hacer clic en "Actualizar Registro"

### Eliminar un Registro
1. Hacer clic en el botón de eliminar (ícono de basura) en la tabla
2. Confirmar la eliminación en el diálogo

## Estructura del Proyecto

```
d:\APP\
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias de Python
├── cosecha.db            # Base de datos SQLite (se crea automáticamente)
├── variedades.csv        # Lista de variedades disponibles
├── responsables.csv      # Lista de responsables disponibles
├── modulos.csv           # Lista de módulos/sectores disponibles
├── gestionar_csv.py      # Herramienta para gestionar archivos CSV
├── consultar_bd.py       # Consultor avanzado de base de datos
├── ver_datos.py          # Visualizador simple de registros
├── templates/
│   ├── base.html         # Plantilla base
│   ├── index.html        # Página principal con lista de registros
│   ├── nuevo.html        # Formulario para nuevo registro
│   └── editar.html       # Formulario para editar registro
├── GESTION_CSV.md        # Documentación de gestión CSV
└── README.md             # Este archivo
```

## Validaciones Incluidas

- **Campos obligatorios**: Todos los campos son requeridos
- **Tallos**: Solo permite valores 10, 15, 25, 30
- **Semana**: Rango válido de 1 a 53
- **Mallas**: Debe ser un número mayor que 0
- **Fecha**: Formato de fecha válido
- **Cálculo automático**: Total tallos = tallos × mallas

## Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **Base de datos**: SQLite con SQLAlchemy
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Iconos**: Font Awesome 6
- **JavaScript**: Vanilla JS para interactividad

## Personalización

Para personalizar la aplicación, puedes modificar:

- **Estilos**: Editar el CSS en `templates/base.html`
- **Opciones de tallos**: Modificar las opciones en los formularios
- **Campos adicionales**: Agregar columnas al modelo en `app.py`
- **Validaciones**: Modificar las reglas de validación en JavaScript y Python

## Notas Importantes

- La aplicación usa SQLite como base de datos por simplicidad
- Los datos se guardan en el archivo `cosecha.db`
- Para producción, se recomienda cambiar la clave secreta en `app.py`
- La hora se registra en el timezone local del servidor

## Solución de Problemas

**Error al instalar dependencias**:
- Asegúrate de tener Python 3.7 o superior
- Usa un entorno virtual para evitar conflictos

**La aplicación no inicia**:
- Verifica que todas las dependencias estén instaladas
- Revisa que no haya otro proceso usando el puerto 5000

**No se crean registros**:
- Verifica que todos los campos obligatorios estén llenos
- Revisa la consola para errores de validación