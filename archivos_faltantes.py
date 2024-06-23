import json

# Rutas a los archivos
txt_file = 'processed_models_3.txt'
json_file = 'panelData_part_3.json'

# Contar las líneas en el archivo .txt
with open(txt_file, 'r') as file:
    num_lines_txt = sum(1 for line in file)

# Contar los registros en el archivo .json
with open(json_file, 'r') as file:
    json_data = json.load(file)
    num_records_json = len(json_data)

# Realizar la resta
difference = num_records_json - num_lines_txt

# Mostrar el resultado
print(f"Número de líneas en {txt_file}: {num_lines_txt}")
print(f"Número de registros en {json_file}: {num_records_json}")
print(f"Diferencia: {difference}")
