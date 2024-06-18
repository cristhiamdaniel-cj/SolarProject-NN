import os
import csv
import json

# Ruta a los archivos
panel_data_file = 'extraccion/panelData_part_4.json'
panel_errors_file = 'panel_errors.csv'

# Leer los modelos procesados de los archivos .txt
processed_models = set()
for filename in os.listdir('.'):
    if filename.startswith("processed_models") and filename.endswith(".txt"):
        with open(filename, 'r') as file:
            processed_models.update(line.strip() for line in file)

# Leer los datos de los paneles del archivo JSON
with open(panel_data_file, 'r') as file:
    panel_data = json.load(file)
    all_panels = set(panel_data.keys())

# Leer los paneles con errores del archivo CSV
errored_panels = set()
with open(panel_errors_file, 'r', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        errored_panels.add(row['Panel'])

# Determinar los paneles que faltan por procesar
remaining_panels = errored_panels - processed_models

# Mostrar el resultado
print(f"Total de paneles en {panel_data_file}: {len(all_panels)}")
print(f"Paneles procesados: {len(processed_models)}")
print(f"Paneles con errores en {panel_errors_file}: {len(errored_panels)}")
print(f"Paneles restantes por procesar: {len(remaining_panels)}")
# print("Paneles restantes por procesar:", remaining_panels)
