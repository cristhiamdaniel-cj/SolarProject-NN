import json

# Ruta a los archivos
processed_models_file = 'processed_models_4.txt'
panel_data_file = 'panelData_part_4.json'

# Leer los modelos procesados
with open(processed_models_file, 'r') as file:
    processed_models = set(line.strip() for line in file)

# Leer los datos de los paneles
with open(panel_data_file, 'r') as file:
    panel_data = json.load(file)
    all_panels = set(panel_data.keys())

# Determinar los paneles que faltan por procesar
remaining_panels = all_panels - processed_models

# Mostrar el resultado
print(f"Total de paneles en {panel_data_file}: {len(all_panels)}")
print(f"Paneles procesados en {processed_models_file}: {len(processed_models)}")
print(f"Paneles restantes por procesar: {len(remaining_panels)}")
