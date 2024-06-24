# import pandas as pd
#
# # Leer panel_errors.csv y extraer todos los elementos de la columna Panel en una lista.Imprimir su tamanio
# panel_errors = pd.read_csv('panel_errors.csv')
# panel_errors_list = panel_errors['Panel'].tolist()
# print(len(panel_errors_list))
#
# # Leer todos los .txt de extraccion/ y extraccion2/ y concatenar una lista de lineas de esos archivos de texto sin duplicados
# import os
# lines = []
# # Evitar duplicados y repetidos
# for folder in ['extraccion', 'extraccion2']:
#     for file in os.listdir(folder):
#         with open(folder + '/' + file, 'r') as f:
#             lines += list(set(f.readlines()))
# print(len(lines))
#
# # Contabilizar que paneles de panel_errors_list no estan en lines
# missing_panels = [panel for panel in panel_errors_list if panel not in lines]
# print(len(missing_panels))

# contabilizar cuantas claves tiene el json:panelData.json
import json
with open('panelData.json', 'r') as f:
    panel_data = json.load(f)
print(len(panel_data.keys()))

# Leer missing_panels.txt y extraer todos los elementos en una lista
with open('missing_panels.txt', 'r') as f:
    missing_panels = f.readlines()
missing_panels = [panel.strip() for panel in missing_panels]


# Extraer las los registros de panelData.json que tengan la clave que este en missing_panels
missing_panels_data = {key: panel_data[key] for key in missing_panels}
print(len(missing_panels_data))

# Guardar los registros en un nuevo json
with open('missing_panels_data.json', 'w') as f:
    json.dump(missing_panels_data, f)

# Dividir ese json en 4 json con los siguientes numeros de registros: 600, 350, 300 y 479
missing_panels_data = list(missing_panels_data.items())
for i, size in enumerate([600, 350, 300, 479]):
    with open(f'missing_panels_data_{i}.json', 'w') as f:
        json.dump(dict(missing_panels_data[:size]), f)
        missing_panels_data = missing_panels_data[size:]
print(len(missing_panels_data))

