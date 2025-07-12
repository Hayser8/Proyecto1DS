import os
import csv

CSV_DIR = 'datos_csv'

for fname in os.listdir(CSV_DIR):
    if not fname.lower().endswith('.csv'):
        continue

    path = os.path.join(CSV_DIR, fname)
    with open(path, 'r', encoding='utf-8-sig', newline='') as f:
        # Leer la primera línea
        first = f.readline().rstrip('\n')
        # Si es la directiva sep=, la saltamos y leemos la siguiente
        if first.startswith('sep='):
            header_line = f.readline().rstrip('\n')
        else:
            header_line = first

    # Parsear la línea de encabezado
    reader = csv.reader([header_line], delimiter=',')
    header = next(reader)

    # Imprimir nombre de archivo y lista de columnas
    print(f"{fname}:")
    for col in header:
        print(f"  - {col}")
    print("-" * 40)
