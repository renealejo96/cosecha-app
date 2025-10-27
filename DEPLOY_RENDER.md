# 🚀 INSTRUCCIONES DE DESPLIEGUE EN RENDER

## 📋 Pasos Completados

✅ **Aplicación preparada para producción**
✅ **Variables de entorno configuradas** 
✅ **Archivos de despliegue creados**
✅ **Repositorio Git inicializado**

## 🌐 Próximos Pasos en Render.com

### **1. Crear cuenta en Render**
- Ve a https://render.com
- Regístrate con tu cuenta de GitHub

### **2. Subir código a GitHub**
1. Crea un nuevo repositorio en GitHub llamado `cosecha-app`
2. Ejecuta estos comandos:
```bash
git remote add origin https://github.com/TU_USUARIO/cosecha-app.git
git branch -M main
git push -u origin main
```

### **3. Crear servicios en Render**

#### **A. Base de Datos PostgreSQL**
1. En el dashboard de Render, click **"New +"**
2. Selecciona **"PostgreSQL"**
3. Configuración:
   - **Name:** `cosecha-db`
   - **Database:** `cosecha`
   - **User:** `cosecha_user`
   - **Plan:** Free
4. Click **"Create Database"**
5. **¡IMPORTANTE!** Copia la **External Database URL** que aparecerá

#### **B. Aplicación Web**
1. Click **"New +"** → **"Web Service"**
2. Conecta tu repositorio de GitHub `cosecha-app`
3. Configuración:
   - **Name:** `cosecha-app`
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
4. **Variables de Entorno:**
   - `FLASK_ENV` = `production`
   - `SECRET_KEY` = (Render lo generará automáticamente)
   - `DATABASE_URL` = (Pega la URL de la base de datos del paso anterior)
5. Click **"Create Web Service"**

### **4. Verificar Despliegue**
- Render construirá y desplegará automáticamente
- Recibirás una URL como: `https://cosecha-app.onrender.com`
- El primer despliegue toma 5-10 minutos

### **5. Configuración Post-Despliegue**

#### **Subir Datos CSV**
Los archivos CSV se subirán automáticamente con el código:
- `variedades.csv` (48 variedades)
- `responsables.csv` (4 responsables)  
- `modulos.csv` (230 módulos)

#### **Migrar Datos (Opcional)**
Si quieres transferir tus 67 registros existentes:
1. Exporta desde PostgreSQL local
2. Usa la consola de Render para importar

## 🎯 **Configuración Automática**

### **Variables de Entorno**
```
FLASK_ENV=production
SECRET_KEY=(generado automáticamente)
DATABASE_URL=postgresql://usuario:pass@host:5432/cosecha
PORT=(asignado automáticamente)
```

### **Características en Producción**
- ✅ **HTTPS automático**
- ✅ **SSL certificado**
- ✅ **Dominio personalizable**
- ✅ **Logs en tiempo real**
- ✅ **Despliegue automático** con git push

## 🔧 **Comandos Git para Subir**

```bash
# Si aún no has creado el repositorio en GitHub
git remote add origin https://github.com/TU_USUARIO/cosecha-app.git
git branch -M main
git push -u origin main

# Para futuras actualizaciones
git add .
git commit -m "Actualización de la app"
git push
```

## 📞 **Soporte**

Si encuentras problemas:
1. Revisa los **logs** en el dashboard de Render
2. Verifica que las **variables de entorno** estén correctas
3. Confirma que la **base de datos** esté conectada

## 🎉 **¡Listo!**

Tu aplicación estará disponible en línea 24/7 con:
- Base de datos PostgreSQL gratuita
- SSL/HTTPS automático
- Dominio .onrender.com
- Despliegues automáticos