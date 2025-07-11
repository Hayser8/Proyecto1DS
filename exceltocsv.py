import os
import pandas as pd

INPUT_DIR = 'Datos'
OUTPUT_DIR = 'datos_csv'

os.makedirs(OUTPUT_DIR, exist_ok=True)

for filename in os.listdir(INPUT_DIR):
    if not filename.lower().endswith('.xls'):
        continue

    input_path = os.path.join(INPUT_DIR, filename)
    base, _ = os.path.splitext(filename)

    try:
        # Lee todas las tablas; header=0 usa la primera fila como nombres de columna
        tables = pd.read_html(input_path, header=0, encoding='latin1')
    except Exception as e:
        print(f"[ERROR] {filename}: {e}")
        continue

    if not tables:
        print(f"[SKIP] {filename}: no se encontraron tablas")
        continue

    # Nos quedamos con la última tabla
    df = tables[-1]

    # Elimina filas completamente vacías (p. ej. la fila de &nbsp; al final)
    df = df.dropna(how='all').reset_index(drop=True)

    # Guarda a CSV
    output_path = os.path.join(OUTPUT_DIR, f"{base}.csv")
    df.to_csv(output_path, index=False)
    print(f"Guardado: {base}.csv")
