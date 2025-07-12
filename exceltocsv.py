import os
import csv
import pandas as pd

INPUT_DIR = 'datos'
OUTPUT_DIR = 'datos_csv'
os.makedirs(OUTPUT_DIR, exist_ok=True)

for filename in os.listdir(INPUT_DIR):
    if not filename.lower().endswith('.xls'):
        continue

    path_in = os.path.join(INPUT_DIR, filename)
    base, _ = os.path.splitext(filename)
    path_out = os.path.join(OUTPUT_DIR, f"{base}.csv")

    # 1) Lee todas las tablas del "HTML" en el .xls
    try:
        tables = pd.read_html(path_in, header=0, encoding='latin1')
    except Exception as e:
        print(f"[ERROR] {filename}: {e}")
        continue
    if not tables:
        print(f"[SKIP] {filename}: no se encontraron tablas")
        continue

    # 2) Selecciona sólo la última tabla
    df = tables[-1].dropna(how='all').reset_index(drop=True)

    # 3) Limpia cada celda de texto:
    #    - Sustituye NBSP por espacio.
    #    - Divide por cualquier whitespace (incluye \n,\r,\t, etc.) y vuelve a unir con un solo espacio.
    for col in df.select_dtypes(include=['object']):
        df[col] = (
            df[col]
            .fillna('')
            .astype(str)
            .str.replace('\xa0', ' ', regex=False)       # NBSP → espacio
            .apply(lambda x: ' '.join(x.split()))        # cualquier whitespace → un espacio
        )

    # 4) Escribe el CSV:
    #    - Línea sep=, para forzar coma como delimitador en Excel.
    #    - quoting=QUOTE_ALL para envolver **todos** los campos en comillas dobles.
    #    - utf-8-sig para que Excel reconozca UTF-8 correctamente.
    with open(path_out, 'w', encoding='utf-8-sig', newline='') as f:
        f.write('sep=,\n')
        df.to_csv(
            f,
            index=False,
            sep=',',
            quoting=csv.QUOTE_ALL,
            quotechar='"',
            doublequote=True
        )

    print(f"✔ {base}.csv generado con coma como separador y campos entre comillas.")
