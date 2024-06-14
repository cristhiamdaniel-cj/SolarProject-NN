import json
import os


# Leer los modelos ya procesados
def read_processed_models(file_path):
    if not os.path.exists(file_path):
        return set()
    with open(file_path, 'r') as f:
        processed_models = set(line.strip() for line in f)
    return processed_models

# Leer el archivo JSON original y filtrar los modelos ya procesados
def filter_unprocessed_models(json_file, processed_models):
    with open(json_file, 'r') as f:
        panel_data = json.load(f)
    unprocessed_data = {key: value for key, value in panel_data.items() if key not in processed_models}
    return unprocessed_data

# Dividir un diccionario en partes iguales
def split_dict_equally(input_dict, chunks=3):
    items = list(input_dict.items())
    size = len(items) // chunks
    return [dict(items[i * size:(i + 1) * size]) for i in range(chunks)]

# Guardar las partes en archivos separados
def save_splits(splits):
    for i, part in enumerate(splits):
        with open(f'panelData_part_{i+1}.json', 'w') as f:
            json.dump(part, f, indent=4)

def main():
    processed_models_file = 'processed_models.txt'
    json_file = 'panelData.json'

    # Leer los modelos ya procesados
    processed_models = read_processed_models(processed_models_file)

    # Filtrar el archivo JSON para excluir los modelos ya procesados
    unprocessed_data = filter_unprocessed_models(json_file, processed_models)

    if not unprocessed_data:
        print("Todos los paneles han sido procesados.")
        return

    # Dividir los datos en partes iguales
    split_data = split_dict_equally(unprocessed_data, chunks=4)

    # Guardar las partes en archivos separados
    save_splits(split_data)

if __name__ == "__main__":
    main()
