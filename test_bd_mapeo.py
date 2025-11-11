from app import app, db, RegistroCosecha, cargar_maestro_productos

with app.app_context():
    # Cargar mapeo
    maestro = cargar_maestro_productos()
    print(f"=== MAPEO CARGADO: {len(maestro)} variedades ===\n")
    
    # Obtener todas las variedades únicas en la BD
    variedades_bd = db.session.query(RegistroCosecha.variedad).distinct().all()
    
    print(f"=== VARIEDADES EN LA BASE DE DATOS: {len(variedades_bd)} ===\n")
    
    for (variedad,) in variedades_bd:
        prod_maestro = maestro.get(variedad, 'SIN CLASIFICAR')
        if prod_maestro == 'SIN CLASIFICAR':
            print(f"❌ '{variedad}' -> SIN CLASIFICAR")
        else:
            print(f"✅ '{variedad}' -> {prod_maestro}")
