from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import os
import csv
import pandas as pd
from io import BytesIO
import pytz

app = Flask(__name__)

# Configuración de zona horaria (Ecuador UTC-5)
ZONA_HORARIA = pytz.timezone('America/Guayaquil')

# Configuración para producción usando variables de entorno
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'tu_clave_secreta_aqui')

# Configurar DATABASE_URL para psycopg2
database_url = os.environ.get('DATABASE_URL', 'postgresql://postgres:admin@localhost:5432/pyganflor')
# Forzar el uso de psycopg2 dialect
if database_url.startswith('postgresql://'):
    database_url = database_url.replace('postgresql://', 'postgresql+psycopg2://', 1)
elif database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql+psycopg2://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de base de datos
class RegistroCosecha(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date, nullable=False)
    viaje = db.Column(db.String(100), nullable=False)
    semana = db.Column(db.Integer, nullable=False)
    tallos = db.Column(db.Integer, nullable=False)  # Solo valores: 10, 15, 25, 30
    mallas = db.Column(db.Integer, nullable=False)
    modulo = db.Column(db.String(100), nullable=False)
    total_tallos = db.Column(db.Integer, nullable=False)  # tallos * mallas
    variedad = db.Column(db.String(100), nullable=False)
    hora = db.Column(db.Time, nullable=False)
    responsable = db.Column(db.String(100), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.now)

    def get_hora_local(self):
        """Convertir hora a zona horaria local"""
        # Combinar fecha y hora
        dt_utc = datetime.combine(self.fecha, self.hora)
        # Asumir que está en UTC
        dt_utc = pytz.utc.localize(dt_utc)
        # Convertir a zona horaria local
        dt_local = dt_utc.astimezone(ZONA_HORARIA)
        return dt_local.time()

    def __repr__(self):
        return f'<RegistroCosecha {self.id}>'

# Crear las tablas
with app.app_context():
    db.create_all()

# Funciones para cargar datos desde CSV
def cargar_variedades():
    """Cargar variedades desde CSV"""
    variedades = []
    csv_path = 'variedades.csv'
    try:
        if os.path.exists(csv_path):
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    variedades.append(row['variedad'])
        else:
            # Variedades por defecto si no existe el archivo
            variedades = ['Gold', 'Red Naomi', 'Explorer', 'Freedom', 'High & Magic']
    except Exception as e:
        print(f"Error cargando variedades: {e}")
        variedades = ['Gold', 'Red Naomi', 'Explorer', 'Freedom', 'High & Magic']
    
    return sorted(variedades)

def cargar_responsables():
    """Cargar responsables desde CSV"""
    responsables = []
    csv_path = 'responsables.csv'
    try:
        if os.path.exists(csv_path):
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    responsables.append(row['responsable'])
        else:
            # Responsables por defecto si no existe el archivo
            responsables = ['Kevin Martinez', 'Maria Rodriguez', 'Juan Perez', 'Ana Garcia']
    except Exception as e:
        print(f"Error cargando responsables: {e}")
        responsables = ['Kevin Martinez', 'Maria Rodriguez', 'Juan Perez', 'Ana Garcia']
    
    return sorted(responsables)

def cargar_modulos():
    """Cargar módulos desde CSV"""
    modulos = []
    csv_path = 'modulos.csv'
    try:
        if os.path.exists(csv_path):
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    modulos.append(row['modulo'])
        else:
            # Módulos por defecto si no existe el archivo
            modulos = ['Modulo A1', 'Modulo A2', 'Modulo B1', 'Modulo B2', 'Invernadero 1']
    except Exception as e:
        print(f"Error cargando módulos: {e}")
        modulos = ['Modulo A1', 'Modulo A2', 'Modulo B1', 'Modulo B2', 'Invernadero 1']
    
    return sorted(modulos)

def cargar_maestro_productos():
    """Cargar mapeo de variedades a productos maestros desde CSV"""
    mapeo = {}
    csv_path = 'MAESTRO_PROS.csv'
    try:
        if os.path.exists(csv_path):
            with open(csv_path, 'r', encoding='utf-8-sig') as file:  # utf-8-sig para manejar BOM
                content = file.read()
                lines = content.strip().split('\n')
                
                # Primera línea son los headers
                if len(lines) > 1:
                    for line in lines[1:]:  # Saltar header
                        if ';' in line:
                            partes = line.strip().split(';')
                            if len(partes) >= 2:
                                variedad = partes[0].strip()
                                prod_maestro = partes[1].strip()
                                if variedad and prod_maestro:
                                    mapeo[variedad] = prod_maestro
                
                print(f"Maestro productos cargados: {len(mapeo)} variedades")
    except Exception as e:
        print(f"Error cargando maestro productos: {e}")
        import traceback
        traceback.print_exc()
    
    return mapeo

def formato_semana(fecha):
    """Convertir fecha a formato AA-SS (año-semana ISO)"""
    year = fecha.year % 100  # Últimos 2 dígitos del año
    semana = fecha.isocalendar()[1]  # Semana ISO
    return f"{year:02d}{semana:02d}"

@app.route('/')
def index():
    # Obtener todos los registros ordenados desde el más reciente hasta el más antiguo
    # Primero por fecha_creacion, luego por fecha y hora como backup
    registros = RegistroCosecha.query.order_by(
        RegistroCosecha.fecha_creacion.desc(),
        RegistroCosecha.fecha.desc(), 
        RegistroCosecha.hora.desc()
    ).all()
    return render_template('index.html', registros=registros)

@app.route('/nuevo', methods=['GET', 'POST'])
def nuevo_registro():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d').date()
            viaje = request.form['viaje']
            semana = int(request.form['semana'])
            tallos = int(request.form['tallos'])
            mallas = int(request.form['mallas'])
            modulo = request.form['modulo']
            variedad = request.form['variedad']
            responsable = request.form['responsable']
            
            # La hora se toma automáticamente al momento del registro
            hora_actual = datetime.now().time()
            
            # Calcular total de tallos
            total_tallos = tallos * mallas
            
            # Crear nuevo registro
            nuevo_registro = RegistroCosecha(
                fecha=fecha,
                viaje=viaje,
                semana=semana,
                tallos=tallos,
                mallas=mallas,
                modulo=modulo,
                total_tallos=total_tallos,
                variedad=variedad,
                hora=hora_actual,
                responsable=responsable
            )
            
            db.session.add(nuevo_registro)
            db.session.commit()
            
            flash('¡Registro guardado exitosamente! Puedes ingresar un nuevo registro.', 'success')
            # Redirigir a la misma página para seguir ingresando registros
            return redirect(url_for('nuevo_registro'))
            
        except Exception as e:
            flash(f'Error al crear el registro: {str(e)}', 'error')
            return render_template('nuevo.html', 
                                 variedades=cargar_variedades(), 
                                 responsables=cargar_responsables(),
                                 modulos=cargar_modulos())
    
    return render_template('nuevo.html', 
                         variedades=cargar_variedades(), 
                         responsables=cargar_responsables(),
                         modulos=cargar_modulos())

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_registro(id):
    registro = RegistroCosecha.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            registro.fecha = datetime.strptime(request.form['fecha'], '%Y-%m-%d').date()
            registro.viaje = request.form['viaje']
            registro.semana = int(request.form['semana'])
            registro.tallos = int(request.form['tallos'])
            registro.mallas = int(request.form['mallas'])
            registro.modulo = request.form['modulo']
            registro.variedad = request.form['variedad']
            registro.responsable = request.form['responsable']
            
            # Recalcular total de tallos
            registro.total_tallos = registro.tallos * registro.mallas
            
            db.session.commit()
            flash('Registro actualizado exitosamente!', 'success')
            return redirect(url_for('index'))
            
        except Exception as e:
            flash(f'Error al actualizar el registro: {str(e)}', 'error')
    
    return render_template('editar.html', 
                         registro=registro,
                         variedades=cargar_variedades(), 
                         responsables=cargar_responsables(),
                         modulos=cargar_modulos())

@app.route('/eliminar/<int:id>')
def eliminar_registro(id):
    registro = RegistroCosecha.query.get_or_404(id)
    try:
        db.session.delete(registro)
        db.session.commit()
        flash('Registro eliminado exitosamente!', 'success')
    except Exception as e:
        flash(f'Error al eliminar el registro: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/reportes')
def reportes():
    from sqlalchemy import func
    from datetime import datetime, timedelta
    
    # Obtener parámetros de filtro
    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')
    
    # Verificar si se enviaron parámetros (se hizo clic en Filtrar)
    mostrar_resultados = fecha_desde is not None and fecha_hasta is not None
    
    # Inicializar variables
    resumen_variedad = []
    total_registros = 0
    total_tallos = 0
    total_mallas = 0
    variedades_unicas = 0
    
    # Solo calcular si hay filtros aplicados
    if mostrar_resultados:
        fecha_desde_dt = datetime.strptime(fecha_desde, '%Y-%m-%d').date()
        fecha_hasta_dt = datetime.strptime(fecha_hasta, '%Y-%m-%d').date()
        
        # Para incluir TODO el día final, agregar un día y usar < en lugar de <=
        fecha_hasta_inclusiva = fecha_hasta_dt + timedelta(days=1)
        
        # Consulta base con filtro de fechas
        query_base = RegistroCosecha.query.filter(
            RegistroCosecha.fecha >= fecha_desde_dt,
            RegistroCosecha.fecha < fecha_hasta_inclusiva
        )
        
        # Resumen por variedad
        resumen_variedad = db.session.query(
            RegistroCosecha.variedad,
            func.count(RegistroCosecha.id).label('total_registros'),
            func.sum(RegistroCosecha.total_tallos).label('total_tallos'),
            func.sum(RegistroCosecha.mallas).label('total_mallas'),
            func.avg(RegistroCosecha.total_tallos).label('promedio_tallos')
        ).filter(
            RegistroCosecha.fecha >= fecha_desde_dt,
            RegistroCosecha.fecha < fecha_hasta_inclusiva
        ).group_by(RegistroCosecha.variedad).order_by(
            func.sum(RegistroCosecha.total_tallos).desc()
        ).all()
        
        # Estadísticas generales
        total_registros = query_base.count()
        total_tallos = db.session.query(func.sum(RegistroCosecha.total_tallos)).filter(
            RegistroCosecha.fecha >= fecha_desde_dt,
            RegistroCosecha.fecha < fecha_hasta_inclusiva
        ).scalar() or 0
        
        total_mallas = db.session.query(func.sum(RegistroCosecha.mallas)).filter(
            RegistroCosecha.fecha >= fecha_desde_dt,
            RegistroCosecha.fecha < fecha_hasta_inclusiva
        ).scalar() or 0
        
        variedades_unicas = db.session.query(func.count(func.distinct(RegistroCosecha.variedad))).filter(
            RegistroCosecha.fecha >= fecha_desde_dt,
            RegistroCosecha.fecha < fecha_hasta_inclusiva
        ).scalar() or 0
    else:
        # Valores por defecto para mostrar en el formulario
        fecha_desde = ''
        fecha_hasta = ''
    
    return render_template('reportes.html',
                         resumen_variedad=resumen_variedad,
                         fecha_desde=fecha_desde,
                         fecha_hasta=fecha_hasta,
                         total_registros=total_registros,
                         total_tallos=total_tallos,
                         total_mallas=total_mallas,
                         variedades_unicas=variedades_unicas,
                         mostrar_resultados=mostrar_resultados)

@app.route('/resumen')
def resumen():
    """Resumen por semana con tabla: producto maestro → variedades → desglose de bloques"""
    from sqlalchemy import func
    from collections import defaultdict
    from datetime import datetime, timedelta
    
    # Obtener semana seleccionada (formato AASS como 2546)
    semana_filtro = request.args.get('semana', '')
    
    # Cargar mapeo de variedades a productos maestros
    maestro_productos = cargar_maestro_productos()
    
    # Obtener todos los registros
    if semana_filtro:
        # Filtrar por semana específica
        registros = RegistroCosecha.query.all()
        registros_filtrados = []
        for r in registros:
            semana_registro = formato_semana(r.fecha)
            if semana_registro == semana_filtro:
                registros_filtrados.append(r)
        registros = registros_filtrados
    else:
        # Mostrar semana actual por defecto
        fecha_hoy = datetime.now().date()
        # Obtener lunes de la semana actual
        dias_desde_lunes = fecha_hoy.weekday()
        fecha_lunes = fecha_hoy - timedelta(days=dias_desde_lunes)
        
        registros = RegistroCosecha.query.filter(
            RegistroCosecha.fecha >= fecha_lunes
        ).all()
        semana_filtro = formato_semana(fecha_hoy)
    
    # Estructura: {semana: {prod_maestro: {variedad: {dia_semana: total_tallos}}}}
    # Desglose: {semana: {prod_maestro: {variedad: {dia_semana: {modulo: total_tallos}}}}}
    datos_por_semana = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int))))
    desglose_modulos = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int)))))
    semanas_disponibles = set()
    
    # Obtener todas las semanas disponibles en la BD
    todos_registros = RegistroCosecha.query.all()
    for r in todos_registros:
        semanas_disponibles.add(formato_semana(r.fecha))
    
    # Procesar registros filtrados
    for registro in registros:
        semana = formato_semana(registro.fecha)
        prod_maestro = maestro_productos.get(registro.variedad, 'SIN CLASIFICAR')
        variedad = registro.variedad
        dia_semana = registro.fecha.weekday()  # 0=Lunes, 6=Domingo
        modulo = registro.modulo
        
        # Acumular totales por producto maestro, variedad y día
        datos_por_semana[semana][prod_maestro][variedad][dia_semana] += registro.total_tallos
        
        # Guardar desglose por módulo
        desglose_modulos[semana][prod_maestro][variedad][dia_semana][modulo] += registro.total_tallos
    
    # Ordenar semanas disponibles (más reciente primero)
    semanas_ordenadas = sorted(list(semanas_disponibles), reverse=True)
    
    # Convertir defaultdict a dict normal
    datos_finales = {}
    for semana in datos_por_semana:
        datos_finales[semana] = {}
        for prod_maestro in datos_por_semana[semana]:
            datos_finales[semana][prod_maestro] = {}
            for variedad in datos_por_semana[semana][prod_maestro]:
                datos_finales[semana][prod_maestro][variedad] = dict(datos_por_semana[semana][prod_maestro][variedad])
    
    desglose_finales = {}
    for semana in desglose_modulos:
        desglose_finales[semana] = {}
        for prod_maestro in desglose_modulos[semana]:
            desglose_finales[semana][prod_maestro] = {}
            for variedad in desglose_modulos[semana][prod_maestro]:
                desglose_finales[semana][prod_maestro][variedad] = {}
                for dia in desglose_modulos[semana][prod_maestro][variedad]:
                    desglose_finales[semana][prod_maestro][variedad][dia] = dict(desglose_modulos[semana][prod_maestro][variedad][dia])
    
    # Días de la semana
    dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    
    return render_template('resumen.html',
                         datos=datos_finales,
                         desglose=desglose_finales,
                         semanas_disponibles=semanas_ordenadas,
                         semana_seleccionada=semana_filtro,
                         dias_semana=dias_semana)

@app.route('/exportar_excel')
def exportar_excel():
    """Exportar todos los registros de cosecha a un archivo Excel"""
    try:
        # Obtener todos los registros ordenados por fecha (más recientes primero)
        registros = RegistroCosecha.query.order_by(RegistroCosecha.fecha.desc()).all()
        
        # Convertir a lista de diccionarios
        data = []
        for registro in registros:
            data.append({
                'ID': registro.id,
                'Fecha': registro.fecha.strftime('%Y-%m-%d'),
                'Hora': registro.hora.strftime('%H:%M:%S'),
                'Viaje': registro.viaje,
                'Semana': registro.semana,
                'Variedad': registro.variedad,
                'Módulo': registro.modulo,
                'Tallos por Malla': registro.tallos,
                'Cantidad Mallas': registro.mallas,
                'Total Tallos': registro.total_tallos,
                'Responsable': registro.responsable
            })
        
        # Crear DataFrame de pandas
        df = pd.DataFrame(data)
        
        # Crear archivo Excel en memoria
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Hoja con todos los datos
            df.to_excel(writer, sheet_name='Registros de Cosecha', index=False)
            
            # Hoja con resumen por variedad
            if not df.empty:
                resumen = df.groupby('Variedad').agg({
                    'Total Tallos': 'sum',
                    'Cantidad Mallas': 'sum',
                    'ID': 'count'
                }).rename(columns={'ID': 'Total Registros'})
                resumen.to_excel(writer, sheet_name='Resumen por Variedad')
                
                # Hoja con resumen por fecha
                resumen_fecha = df.groupby('Fecha').agg({
                    'Total Tallos': 'sum',
                    'Cantidad Mallas': 'sum',
                    'ID': 'count'
                }).rename(columns={'ID': 'Total Registros'})
                resumen_fecha.to_excel(writer, sheet_name='Resumen por Fecha')
        
        output.seek(0)
        
        # Nombre del archivo con fecha actual
        fecha_actual = datetime.now().strftime('%Y%m%d_%H%M%S')
        nombre_archivo = f'cosecha_registros_{fecha_actual}.xlsx'
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=nombre_archivo
        )
        
    except Exception as e:
        flash(f'Error al exportar: {str(e)}', 'error')
        return redirect(url_for('reportes'))

if __name__ == '__main__':
    # Crear las tablas si no existen
    with app.app_context():
        db.create_all()
    
    # Configuración para producción/desarrollo
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') != 'production'
    app.run(host='0.0.0.0', port=port, debug=debug)