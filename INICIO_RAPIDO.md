# 🚀 INICIO RÁPIDO - API de Cosecha para Excel

## ⚡ En 3 Pasos

### 1️⃣ Iniciar el servidor
```bash
python app.py
```
Espera a ver: `Running on http://127.0.0.1:5000`

### 2️⃣ Probar en el navegador
Abre en tu navegador:
```
http://localhost:5000/api/resumen
```
Deberías ver datos en formato JSON.

### 3️⃣ Importar en Excel

#### Opción A: Descarga directa (10 segundos)
1. Abre en el navegador: `http://localhost:5000/api/resumen/excel`
2. Se descarga el Excel automáticamente
3. Abre el archivo
4. ¡Listo!

#### Opción B: Power Query (para actualizar con un click)
1. Abre Excel
2. **Datos** → **Obtener datos** → **Desde web**
3. Pega: `http://localhost:5000/api/resumen`
4. Click en las **dos flechas** junto a "datos"
5. Marca todas las casillas
6. **Cerrar y cargar**
7. Para actualizar: Click derecho → **Actualizar**

---

## 📋 URLs Útiles

```
Ver datos JSON:              http://localhost:5000/api/resumen
Descargar Excel:             http://localhost:5000/api/resumen/excel
Ver semanas disponibles:     http://localhost:5000/api/semanas
Resumen semana específica:   http://localhost:5000/api/resumen?semana=2546
```

---

## 🎯 Para cambiar de semana

Reemplaza `2546` por la semana que necesites:
```
http://localhost:5000/api/resumen/excel?semana=2546
```

---

## 📚 Más información

- **GUIA_RAPIDA_EXCEL.md** - 3 formas de usar en Excel
- **RESUMEN_API.md** - Resumen completo
- **API_DOCUMENTATION.md** - Documentación técnica
- **test_api.py** - Script de pruebas

---

## 🌐 Para Producción (Render.com)

Cuando despliegues, cambia:
```
http://localhost:5000
```
por:
```
https://tu-app.onrender.com
```

---

## ❓ Ayuda

### No veo datos en la API
- Verifica que tengas registros en la base de datos
- Visita la aplicación normal en `http://localhost:5000` y agrega registros

### Excel no se conecta
- Asegúrate de que `python app.py` esté corriendo
- Usa `http://localhost:5000` (con `localhost`, no con `127.0.0.1`)

### ¿Qué semanas están disponibles?
- Abre: `http://localhost:5000/api/semanas`

---

**¡Eso es todo! Ya puedes consumir tus datos de cosecha en Excel.** 🎉
