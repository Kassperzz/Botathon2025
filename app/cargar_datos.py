import pandas as pd
from sqlalchemy import create_engine, text # <-- Agregamos 'text' para comandos SQL

# --- CONFIGURACIÓN ---
# Tu conexión configurada
DB_URI = 'postgresql://postgres:root@127.0.0.1:5432/botathon'
ARCHIVO_CSV = 'Voluntarios_Botathon_2025_2(Voluntariado.csv'

def cargar_datos():
    print("1. Leyendo el archivo CSV...")
    try:
        # Usamos latin-1 para las tildes
        df = pd.read_csv(ARCHIVO_CSV, delimiter=';', encoding='latin-1')
    except FileNotFoundError:
        print(f"❌ Error: No encuentro el archivo '{ARCHIVO_CSV}'.")
        return
    except UnicodeDecodeError:
        print("   -> Probando codificación alternativa...")
        df = pd.read_csv(ARCHIVO_CSV, delimiter=';', encoding='cp1252')

    print(f"   -> Se encontraron {len(df)} registros.")

    # 2. RENOMBRAR COLUMNAS
    columnas_map = {
        'Id': 'id',
        'Nombres': 'nombres',
        'ApellidoP': 'apellido_paterno',
        'ApellidoM': 'apellido_materno',
        'Nacionalidad': 'nacionalidad_id',
        'FechaNacimiento': 'fecha_nacimiento',
        'Sexo': 'sexo_id',
        'RegionPostulante': 'region_id',
        'ComunaPostulante': 'comuna_id',
        'InstitutoId': 'instituto_id',
        'Enfermedad': 'enfermedad',
        'Salud': 'salud_id',
        'Ocupacion': 'ocupacion',
        'DetalleOcupacion': 'detalle_ocupacion',
        'Estado': 'estado_id',
        'Activo': 'activo'
    }
    
    # Filtramos columnas existentes
    cols_existentes = [c for c in columnas_map.keys() if c in df.columns]
    df = df[cols_existentes].rename(columns=columnas_map)

    print("3. Limpiando datos en memoria...")
    if 'fecha_nacimiento' in df.columns:
        df['fecha_nacimiento'] = pd.to_datetime(df['fecha_nacimiento'], format='%d/%m/%Y', errors='coerce')
    
    df = df.where(pd.notnull(df), None)

    print("4. Conectando a Base de Datos...")
    try:
        engine = create_engine(DB_URI)
        
        # --- NUEVO: BORRADO PREVIO ---
        # Abrimos conexión para borrar lo viejo
        with engine.connect() as conn:
            print("   -> 🧹 Limpiando tabla antigua (TRUNCATE)...")
            conn.execute(text("TRUNCATE TABLE voluntarios RESTART IDENTITY;"))
            conn.commit()
        # -----------------------------

        print("5. Insertando datos nuevos (esto puede tardar unos segundos)...")
        
        # if_exists='append': Agrega a la tabla (que ahora está vacía)
        df.to_sql('voluntarios', con=engine, if_exists='append', index=False, chunksize=1000)
        
        print(f"✅ ¡Éxito Total! {len(df)} registros insertados en la tabla 'voluntarios'.")
        
    except Exception as e:
        print(f"❌ Error al conectar o insertar en la BD:\n{e}")

if __name__ == '__main__':
    cargar_datos()