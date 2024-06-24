import pandas as pd
import os
import glob
import logging

# Configurar el logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Función para leer y concatenar archivos CSV de una carpeta
def read_csv_files(folder_path):
    logging.info(f'Leyendo archivos en la carpeta: {folder_path}')
    all_files = glob.glob(os.path.join(folder_path, "*.csv"))
    df_list = []

    for file in all_files:
        logging.info(f'Leyendo archivo: {file}')
        df = pd.read_csv(file)
        df_list.append(df)

    logging.info(f'Concatenando {len(df_list)} archivos de la carpeta: {folder_path}')
    return pd.concat(df_list, ignore_index=True) if df_list else pd.DataFrame()


# Leer y concatenar archivos de las carpetas /extraccion y /extraccion2
logging.info('Iniciando la lectura de archivos de las carpetas /extraccion y /extraccion2')
df_extraccion = read_csv_files('extraccion')
df_extraccion2 = read_csv_files('extraccion2')

# Concatenar los DataFrames de ambas carpetas
logging.info('Concatenando los DataFrames de las carpetas /extraccion y /extraccion2')
combined_df = pd.concat([df_extraccion, df_extraccion2], ignore_index=True)

# Eliminar filas duplicadas según la columna 'nombre_panel'
logging.info('Eliminando filas duplicadas basadas en la columna nombre_panel')
unique_df = combined_df.drop_duplicates(subset='nombre_panel')

# Guardar el resultado en un archivo CSV para verificación
output_file = 'combined_unique_panels.csv'
unique_df.to_csv(output_file, index=False)
logging.info(f'Resultado guardado en: {output_file}')

# Mostrar el resultado (opcional)
print(unique_df)

# Leer panel_errors.csv en un dataframe y extraer una lista de la columna Panel. y una lista de la columna 'nombre_panel' de unique_df
logging.info('Leyendo el archivo panel_errors.csv')
panel_errors = pd.read_csv('panel_errors.csv')
panel_errors_list = panel_errors['Panel'].tolist()
unique_df_list = unique_df['nombre_panel'].tolist()

# Calcular paneles que están en panel_errors.csv pero no en unique_df
missing_panels = set(panel_errors_list) - set(unique_df_list)
logging.info(f'Numero de paneles faltantes: {len(missing_panels)}')

# Guardar los paneles faltantes en un archivo txt
output_file = 'missing_panels.txt'

with open(output_file, 'w') as file:
    for panel in missing_panels:
        file.write(f'{panel}\n')

logging.info(f'Paneles faltantes guardados en: {output_file}')