import pandas as pd
from sqlalchemy import create_engine

# 1. Configuración (La misma que ya te funciona)
DB_URI = 'postgresql://postgres:Enaxxion13!@127.0.0.1:5432/botathon2025'

def exportar_todo():
    print("⏳ Conectando a la base de datos...")
    engine = create_engine(DB_URI)
    
    # 2. La Query SQL para traer TODO
    query = "SELECT * FROM voluntarios"
    
    print("📥 Descargando datos (esto puede tardar un poco)...")
    try:
        # Pandas ejecuta la query y guarda todo en memoria
        df = pd.read_sql(query, engine)
        print(f"   -> Se descargaron {len(df)} registros.")
        
        # 3. Guardar en CSV (Excel universal)
        nombre_archivo = "Exportacion_Voluntarios_Completa.csv"
        
        # 'index=False' quita los números de fila automáticos (0,1,2...)
        # 'sep=';'' usa punto y coma para que Excel lo abra ordenado
        # 'encoding='utf-8-sig'' asegura que las tildes (ñ, á) se vean bien en Excel
        df.to_csv(nombre_archivo, index=False, sep=';', encoding='utf-8-sig')
        
        print(f"✅ ¡Listo! Archivo guardado como: {nombre_archivo}")
        
    except Exception as e:
        print(f"❌ Error al exportar: {e}")

if __name__ == '__main__':
    exportar_todo()