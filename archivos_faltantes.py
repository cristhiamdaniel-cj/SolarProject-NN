import json

# Rutas a los archivos
txt_file = 'processed_models_1.txt'
json_file = 'panelData_part_1.json'

# Leer y obtener nombres de los paneles del archivo JSON
with open(json_file, 'r') as file:
    json_data = json.load(file)
    panel_names_json = set(json_data.keys())

# Leer y obtener las líneas del archivo TXT
with open(txt_file, 'r') as file:
    lines_txt = [line.strip() for line in file]

# Verificar duplicados en el archivo TXT
unique_lines_txt = set(lines_txt)
duplicates_txt = [line for line in lines_txt if lines_txt.count(line) > 1]

# Comparar nombres de paneles en JSON y TXT
missing_in_json = unique_lines_txt - panel_names_json
missing_in_txt = panel_names_json - unique_lines_txt

# Mostrar resultados
print(f"Total de paneles en JSON: {len(panel_names_json)}")
print(f"Total de líneas en TXT: {len(lines_txt)}")
print(f"Total de líneas únicas en TXT: {len(unique_lines_txt)}")
print(f"Total de duplicados en TXT: {len(duplicates_txt)}")

print(f"Paneles en TXT que no están en JSON: {missing_in_json}")
print(f"Paneles en JSON que no están en TXT: {missing_in_txt}")
print(f"Número de paneles en TXT que no están en JSON: {len(missing_in_json)}")
print(f"Número de paneles en JSON que no están en TXT: {len(missing_in_txt)}")

if duplicates_txt:
    print(f"Líneas duplicadas en TXT: {duplicates_txt}")
else:
    print("No hay líneas duplicadas en TXT.")
