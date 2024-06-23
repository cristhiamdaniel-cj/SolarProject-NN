# import json
# import os
#
#
# # Leer los modelos ya procesados
# def read_processed_models(file_path):
#     if not os.path.exists(file_path):
#         return set()
#     with open(file_path, 'r') as f:
#         processed_models = set(line.strip() for line in f)
#     return processed_models
#
# # Leer el archivo JSON original y filtrar los modelos ya procesados
# def filter_unprocessed_models(json_file, processed_models):
#     with open(json_file, 'r') as f:
#         panel_data = json.load(f)
#     unprocessed_data = {key: value for key, value in panel_data.items() if key not in processed_models}
#     return unprocessed_data
#
# # Dividir un diccionario en partes iguales
# def split_dict_equally(input_dict, chunks=3):
#     items = list(input_dict.items())
#     size = len(items) // chunks
#     return [dict(items[i * size:(i + 1) * size]) for i in range(chunks)]
#
# # Guardar las partes en archivos separados
# def save_splits(splits):
#     for i, part in enumerate(splits):
#         with open(f'panelData_part_{i+1}.json', 'w') as f:
#             json.dump(part, f, indent=4)
#
# def main():
#     processed_models_file = 'processed_models.txt'
#     json_file = 'panelData.json'
#
#     # Leer los modelos ya procesados
#     processed_models = read_processed_models(processed_models_file)
#
#     # Filtrar el archivo JSON para excluir los modelos ya procesados
#     unprocessed_data = filter_unprocessed_models(json_file, processed_models)
#
#     if not unprocessed_data:
#         print("Todos los paneles han sido procesados.")
#         return
#
#     # Dividir los datos en partes iguales
#     split_data = split_dict_equally(unprocessed_data, chunks=4)
#
#     # Guardar las partes en archivos separados
#     save_splits(split_data)
#
# if __name__ == "__main__":
#     main()

import os
import csv
import json


# Leer los modelos ya procesados de los archivos .txt
def read_processed_models(directory):
    processed_models = set()
    for filename in os.listdir(directory):
        if filename.startswith("processed_models") and filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r') as file:
                processed_models.update(line.strip() for line in file)
    return processed_models


# Leer los datos de los paneles del archivo JSON
def read_panel_data(json_file):
    if not os.path.exists(json_file):
        print(f"El archivo {json_file} no existe.")
        return {}
    with open(json_file, 'r') as file:
        panel_data = json.load(file)
    return panel_data


# Leer los paneles con errores del archivo CSV
def read_errored_panels(csv_file):
    errored_panels = set()
    if not os.path.exists(csv_file):
        print(f"El archivo {csv_file} no existe.")
        return errored_panels
    with open(csv_file, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            errored_panels.add(row['Panel'])
    return errored_panels


# Dividir un diccionario en partes según las proporciones indicadas
def split_dict_proportionally(input_dict, proportions):
    items = list(input_dict.items())
    total_items = len(items)
    split_sizes = [int(total_items * proportion) for proportion in proportions]

    splits = []
    current_index = 0
    for size in split_sizes:
        splits.append(dict(items[current_index:current_index + size]))
        current_index += size

    # Asegurarse de que cualquier elemento restante se añada al último split
    if current_index < total_items:
        splits[-1].update(dict(items[current_index:total_items]))

    return splits


# Guardar las partes en archivos separados e imprimir la cantidad de paneles
def save_splits(splits):
    total_panels = 0
    for i, part in enumerate(splits):
        with open(f'panelData_part_{i + 1}.json', 'w') as f:
            json.dump(part, f, indent=4)
        num_panels = len(part)
        total_panels += num_panels
        print(f'panelData_part_{i + 1}.json tiene {num_panels} paneles')
    print(f'El total de paneles en todos los archivos es: {total_panels}')


def main():
    processed_models_directory = '.'
    json_file = 'panelData.json'
    panel_errors_file = 'panel_errors.csv'

    # Leer los modelos ya procesados
    processed_models = read_processed_models(processed_models_directory)
    print(f"Modelos procesados leídos: {len(processed_models)}")

    # Leer los datos de los paneles del archivo JSON
    panel_data = read_panel_data(json_file)
    all_panels = set(panel_data.keys())
    print(f"Total de paneles en {json_file}: {len(all_panels)}")

    # Leer los paneles con errores del archivo CSV
    errored_panels = read_errored_panels(panel_errors_file)
    print(f"Paneles con errores en {panel_errors_file}: {len(errored_panels)}")

    # Determinar los paneles que faltan por procesar
    remaining_panels = errored_panels - processed_models
    print(f"Paneles restantes por procesar: {len(remaining_panels)}")

    if not remaining_panels:
        print("Todos los paneles han sido procesados.")
        return

    # Convertir remaining_panels a un diccionario basado en panel_data
    remaining_data = {panel: panel_data[panel] for panel in remaining_panels if panel in panel_data}
    print(f"Paneles restantes después de filtrar: {len(remaining_data)}")

    # # Definir las proporciones para dividir los datos
    # proportions = [0.5, 4 / 16, 3 / 16, 1 / 16]
    #
    # # Dividir los datos en partes según las proporciones definidas
    # split_data = split_dict_proportionally(remaining_data, proportions)
    #
    # # Guardar las partes en archivos separados e imprimir la cantidad de paneles
    # save_splits(split_data)


if __name__ == "__main__":
    main()
