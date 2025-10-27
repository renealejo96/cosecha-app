#!/usr/bin/env python3
"""
Script de verificación pre-producción
Verifica que todos los componentes estén listos para producción
"""

import os
import sys
import csv
import psycopg2
from urllib.parse import urlparse

def verificar_archivos_esenciales():
    """Verifica que todos los archivos necesarios existan"""
    print("🔍 Verificando archivos esenciales...")
    
    archivos_requeridos = [
        'app.py',
        'requirements.txt', 
        'variedades.csv',
        'responsables.csv',
        'modulos.csv',
        'templates/base.html',
        'templates/index.html',
        'templates/nuevo.html',
        'templates/editar.html',
        'templates/reportes.html'
    ]
    
    faltantes = []
    for archivo in archivos_requeridos:
        if not os.path.exists(archivo):
            faltantes.append(archivo)
        else:
            print(f"  ✅ {archivo}")
    
    if faltantes:
        print(f"  ❌ Archivos faltantes: {', '.join(faltantes)}")
        return False
    
    print("  ✅ Todos los archivos esenciales presentes")
    return True

def verificar_archivos_csv():
    """Verifica que los archivos CSV tengan contenido válido"""
    print("\n📋 Verificando archivos CSV...")
    
    archivos_csv = ['variedades.csv', 'responsables.csv', 'modulos.csv']
    
    for archivo in archivos_csv:
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                filas = list(reader)
                if len(filas) > 0:
                    print(f"  ✅ {archivo}: {len(filas)} elementos")
                else:
                    print(f"  ⚠️ {archivo}: archivo vacío")
        except Exception as e:
            print(f"  ❌ {archivo}: Error - {e}")
            return False
    
    return True

def verificar_configuracion_app():
    """Verifica la configuración de la aplicación"""
    print("\n⚙️ Verificando configuración...")
    
    try:
        # Importar app para verificar configuración
        sys.path.insert(0, '.')
        from app import app
        
        # Verificar SECRET_KEY
        if app.config.get('SECRET_KEY') == 'tu_clave_secreta_aqui':
            print("  ⚠️ SECRET_KEY usando valor por defecto (cambiar para producción)")
        else:
            print("  ✅ SECRET_KEY configurada")
        
        # Verificar DATABASE_URI
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
        if 'postgresql://' in db_uri:
            print("  ✅ Configurada para PostgreSQL")
        else:
            print("  ❌ No configurada para PostgreSQL")
            return False
            
        return True
        
    except Exception as e:
        print(f"  ❌ Error en configuración: {e}")
        return False

def verificar_conexion_bd():
    """Verifica la conexión a PostgreSQL"""
    print("\n🗄️ Verificando conexión a PostgreSQL...")
    
    try:
        sys.path.insert(0, '.')
        from app import app
        
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
        
        # Parsear URI de conexión
        parsed = urlparse(db_uri)
        
        conn = psycopg2.connect(
            host=parsed.hostname,
            port=parsed.port or 5432,
            user=parsed.username,
            password=parsed.password,
            database=parsed.path[1:]  # Remover '/' inicial
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        print(f"  ✅ Conexión exitosa: {version}")
        
        # Verificar tabla
        cursor.execute("""
            SELECT COUNT(*) FROM information_schema.tables 
            WHERE table_name = 'registro_cosecha'
        """)
        tabla_existe = cursor.fetchone()[0] > 0
        
        if tabla_existe:
            cursor.execute("SELECT COUNT(*) FROM registro_cosecha")
            registros = cursor.fetchone()[0]
            print(f"  ✅ Tabla existe con {registros} registros")
        else:
            print("  ⚠️ Tabla no existe (se creará al ejecutar app)")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"  ❌ Error de conexión: {e}")
        return False

def main():
    """Función principal de verificación"""
    print("🚀 VERIFICACIÓN PRE-PRODUCCIÓN")
    print("=" * 50)
    
    verificaciones = [
        verificar_archivos_esenciales(),
        verificar_archivos_csv(),
        verificar_configuracion_app(),
        verificar_conexion_bd()
    ]
    
    print(f"\n📊 RESULTADO:")
    exitosas = sum(verificaciones)
    total = len(verificaciones)
    
    if exitosas == total:
        print(f"✅ {exitosas}/{total} verificaciones exitosas")
        print("🎉 ¡Aplicación lista para producción!")
        return 0
    else:
        print(f"❌ {exitosas}/{total} verificaciones exitosas")
        print("⚠️ Revisa los errores antes de desplegar")
        return 1

if __name__ == "__main__":
    sys.exit(main())