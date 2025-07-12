import os
import pandas as pd

INPUT_DIR = 'datos_csv'
OUTPUT_FILE = 'todos_los_establecimientos.csv'

dfs = []

for fname in os.listdir(INPUT_DIR):
    if not fname.lower().endswith('.csv'):
        continue

    path = os.path.join(INPUT_DIR, fname)
    # Leer la primera línea para ver si es "sep=,"
    with open(path, 'r', encoding='utf-8-sig') as f:
        first = f.readline().strip()
    # Si es la directiva, saltamos la primera fila al leer
    skip = 1 if first == 'sep=,' else 0

    df = pd.read_csv(
        path,
        skiprows=skip,
        encoding='utf-8-sig'
    )
    dfs.append(df)

# Concatenamos todos los DataFrames
all_df = pd.concat(dfs, ignore_index=True)

# Guardamos el CSV combinado
all_df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
print(f"Hecho: generado {OUTPUT_FILE} con {len(all_df):,} filas y {len(all_df.columns)} columnas.")
