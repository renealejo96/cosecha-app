# 🚀 CONFIGURACIÓN PARA PRODUCCIÓN

## 📋 Lista de Verificación Pre-Producción

### ✅ **Seguridad**
- [ ] Cambiar `SECRET_KEY` en `app.py` por una clave segura única
- [ ] Configurar variables de entorno para credenciales de BD
- [ ] Deshabilitar modo debug (`debug=False`)
- [ ] Configurar HTTPS en el servidor web

### ✅ **Base de Datos**
- [ ] Verificar conexión a PostgreSQL de producción
- [ ] Configurar backup automático de PostgreSQL
- [ ] Verificar permisos de usuario de BD
- [ ] Probar restauración desde backup

### ✅ **Servidor Web**
- [ ] Instalar servidor WSGI (Gunicorn, uWSGI)
- [ ] Configurar proxy reverso (Nginx, Apache)
- [ ] Configurar SSL/TLS
- [ ] Configurar logs de aplicación

### ✅ **Archivos CSV**
- [ ] Verificar que existen: `variedades.csv`, `responsables.csv`, `modulos.csv`
- [ ] Establecer permisos de escritura apropiados
- [ ] Configurar backup de archivos CSV

## 🔧 **Configuración Recomendada**

### **1. Variables de Entorno**
Crear archivo `.env`:
```bash
SECRET_KEY=tu_clave_secreta_super_segura_aqui
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/pyganflor
FLASK_ENV=production
```

### **2. Modificar app.py**
```python
import os
from dotenv import load_dotenv

load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
```

### **3. Servidor WSGI con Gunicorn**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### **4. Nginx (Ejemplo)**
```nginx
server {
    listen 80;
    server_name tu-dominio.com;
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 🔒 **Seguridad Adicional**

### **Generar SECRET_KEY Segura**
```python
import secrets
print(secrets.token_hex(32))
```

### **Configuración PostgreSQL Segura**
- Crear usuario específico para la aplicación
- Otorgar solo permisos necesarios
- Configurar conexiones SSL
- Restricgir acceso por IP

## 📊 **Monitoreo**

### **Logs de Aplicación**
```python
import logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
```

### **Salud de la Aplicación**
Agregar endpoint de salud:
```python
@app.route('/health')
def health_check():
    return {'status': 'OK', 'timestamp': datetime.utcnow()}
```

## 🔄 **Backup y Recuperación**

### **PostgreSQL Backup**
```bash
# Backup diario
pg_dump -h localhost -U usuario -d pyganflor > backup_$(date +%Y%m%d).sql

# Restauración
psql -h localhost -U usuario -d pyganflor < backup_20251011.sql
```

### **Archivos CSV Backup**
```bash
# Copiar archivos CSV a ubicación segura
cp *.csv /ruta/backup/csv/$(date +%Y%m%d)/
```

## 🚨 **Consideraciones Importantes**

- **No usar Flask dev server en producción**
- **Configurar límites de rate limiting**
- **Implementar autenticación si es necesario**
- **Monitorear uso de recursos**
- **Configurar alertas para errores**