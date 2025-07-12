import os
import csv

CSV_DIR = 'datos_csv'

for fname in os.listdir(CSV_DIR):
    if not fname.lower().endswith('.csv'):
        continue

    path = os.path.join(CSV_DIR, fname)
    # Leer todo el fichero
    with open(path, 'r', encoding='utf-8-sig', newline='') as fin:
        lines = fin.readlines()

    if not lines:
        continue

    # Detectar y guardar la línea sep=, si existe
    idx = 0
    sep_directive = None
    if lines[0].startswith('sep='):
        sep_directive = lines[0].rstrip('\n')
        idx = 1

    # El encabezado es la línea idx
    header_line = lines[idx]
    reader = csv.reader([header_line], delimiter=',')
    header = next(reader)
    n_cols = len(header)

    # Procesar todas las filas siguientes
    fixed_rows = []
    for line in lines[idx+1:]:
        # saltar líneas vacías
        if not line.strip():
            continue
        reader = csv.reader([line], delimiter=',')
        row = next(reader)
        # ajustar longitud
        if len(row) < n_cols:
            row += [''] * (n_cols - len(row))
        elif len(row) > n_cols:
            row = row[:n_cols]
        fixed_rows.append(row)

    # Reescribir el CSV normalizado
    with open(path, 'w', encoding='utf-8-sig', newline='') as fout:
        # si había sep=, la ponemos de nuevo
        if sep_directive:
            fout.write(sep_directive + '\n')
        writer = csv.writer(fout, delimiter=',', quoting=csv.QUOTE_ALL)
        writer.writerow(header)
        writer.writerows(fixed_rows)

    print(f"Normalizado: {fname} ({n_cols} columnas)")  
