import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuración del logger para que guarde los logs en un archivo
logging.basicConfig(filename='simulation_1.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def safe_exp(x):
    x_clipped = np.clip(x, None, 700)
    return np.exp(x_clipped)

class PVModel:
    def __init__(self, pmax, isc, voc, vmpp, impp, num_cells, series_resistance, shunt_resistance, temp_coefficient_isc, temp_coefficient_voc, nI, I0, IL):
        self.pmax = pmax
        self.isc = isc
        self.voc = voc
        self.vmpp = vmpp
        self.impp = impp
        self.num_cells = num_cells
        self.series_resistance = series_resistance
        self.shunt_resistance = shunt_resistance
        self.temp_coefficient_isc = temp_coefficient_isc
        self.temp_coefficient_voc = temp_coefficient_voc
        self.nI = nI
        self.I0 = I0
        self.IL = IL

    def pv_model(self, temperature, irradiance):
        temperature_k = temperature + 273.15
        CHARGE = 1.602176634e-19
        BOLTZMANN_CONST = 1.380649e-23
        NOMINAL_TEMP = 298.15
        BANDGAP_ENERGY = 1.12

        i_ph = (self.IL + self.temp_coefficient_isc * (temperature_k - NOMINAL_TEMP)) * (irradiance / 1000)

        def current_voltage_relation(volt, i):
            ish = (volt + i * self.series_resistance) / self.shunt_resistance
            return i_ph - self.I0 * (safe_exp((CHARGE * (volt + i * self.series_resistance)) / (
                    self.nI * BOLTZMANN_CONST * self.num_cells * temperature_k)) - 1) - ish - i

        voltage_values = np.linspace(0, self.voc, 2000)
        current_values = []

        for v in voltage_values:
            try:
                i_solution = fsolve(lambda i: current_voltage_relation(v, i), self.isc)[0]
                current_values.append(i_solution)
            except RuntimeError as e:
                logging.warning(f'Error de convergencia para V={v} V: {e}')
                current_values.append(np.nan)

        power_values = voltage_values * np.array(current_values)
        results = pd.DataFrame(
            {'Voltage (V)': voltage_values, 'Current (A)': current_values, 'Power (W)': power_values})

        max_power_idx = results['Power (W)'].idxmax()
        vmpp = results.iloc[max_power_idx]['Voltage (V)']
        impp = results.iloc[max_power_idx]['Current (A)']
        pmax = results.iloc[max_power_idx]['Power (W)']

        return results, vmpp, impp, pmax

def get_model_names(json_file):
    with open(json_file) as f:
        panel_data = json.load(f)
    return list(panel_data.keys())

def read_processed_models(file_path):
    if not os.path.exists(file_path):
        return set()
    with open(file_path, 'r') as f:
        processed_models = set(line.strip() for line in f)
    return processed_models

def write_processed_models(file_path, processed_models):
    with open(file_path, 'w') as f:
        for model in processed_models:
            f.write(f"{model}\n")

def process_panel(panel_name, panel_specs, irradiance_values, temperature_values):
    logging.info(f'Procesando panel: {panel_name}')

    pmax = float(panel_specs.get("Pmax", 0))
    isc = float(panel_specs.get("Isc", 0))
    voc = float(panel_specs.get("Voc", 0))
    vmpp = float(panel_specs.get("Vmpp", 0))
    impp = float(panel_specs.get("Impp", 0))
    num_cells = int(panel_specs.get("Ncell", 0))
    series_resistance = float(panel_specs.get("Rs", 0))
    shunt_resistance = float(panel_specs.get("Rsh", 0))
    temp_coefficient_isc = float(panel_specs.get("alpha_Isc", 0))
    temp_coefficient_voc = float(panel_specs.get("beta_Voc", 0))
    nI = float(panel_specs.get("nI", 0))
    I0 = float(panel_specs.get("I0", 0))
    IL = float(panel_specs.get("IL", 0))

    model = PVModel(pmax, isc, voc, vmpp, impp, num_cells, series_resistance, shunt_resistance, temp_coefficient_isc, temp_coefficient_voc, nI, I0, IL)

    panel_data = []
    for irradiance in irradiance_values:
        for temperature in temperature_values:
            logging.debug(f'Simulando con irradiancia {irradiance} y temperatura {temperature}')
            _, vmpp, impp, pmax_calc = model.pv_model(temperature, irradiance)
            panel_data.append({
                "nombre_panel": panel_name,
                "Irradiancia": irradiance,
                "Temperatura": temperature,
                "Voc": voc,
                "Isc": isc,
                "Ns": num_cells,
                "alpha_Isc": temp_coefficient_isc,
                "beta_Voc": temp_coefficient_voc,
                "Rs": series_resistance,
                "Rsh": shunt_resistance,
                "Vmpp": vmpp,
                "Impp": impp,
                "Pmax": pmax_calc
            })
    return panel_data

def main():
    logger = logging.getLogger()
    logger.info('Leyendo datos del archivo JSON...')

    json_file = 'panelData_part_1.json'
    processed_file = 'processed_models_1.txt'
    processed_models = read_processed_models(processed_file)

    model_names = get_model_names(json_file)
    unprocessed_models = [model for model in model_names if model not in processed_models]

    if not unprocessed_models:
        logger.info('Todos los modelos han sido procesados.')
        return

    models_to_process = unprocessed_models[:600]
    logger.info(f'Modelos a procesar en esta ejecución: {models_to_process}')

    with open(json_file) as f:
        panel_data = json.load(f)

    irradiance_values = np.arange(100, 1050, 100)  # Valores de irradiancia de 200 a 1000 W/m²
    temperature_values = np.arange(10, 56,5)  # Valores de temperatura de 10 a 50 °C

    all_data = []

    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:  # Utiliza todos los núcleos disponibles
        future_to_panel = {executor.submit(process_panel, panel_name, panel_data[panel_name], irradiance_values,
                                           temperature_values): panel_name for panel_name in models_to_process}
        for future in as_completed(future_to_panel):
            panel_name = future_to_panel[future]
            try:
                panel_data_results = future.result()
                all_data.extend(panel_data_results)
                processed_models.add(panel_name)
            except Exception as e:
                logger.error(f'Error procesando el panel {panel_name}: {e}')

    # Especificar las columnas del DataFrame
    columns = ["nombre_panel", "Irradiancia", "Temperatura", "Voc", "Isc", "Ns", "alpha_Isc", "beta_Voc", "Rs", "Rsh", "Vmpp", "Impp", "Pmax"]
    data_df = pd.DataFrame(all_data, columns=columns)

    # Guardar los datos en el archivo CSV
    header = not os.path.exists('panel_simulation_data_1.csv')
    data_df.to_csv('panel_simulation_data_1.csv', index=False, mode='a', header=header)
    logger.info('Datos de simulación almacenados en panel_simulation_data_1.csv')

    # Actualizar el archivo de modelos procesados
    write_processed_models(processed_file, processed_models)

if __name__ == "__main__":
    main()
