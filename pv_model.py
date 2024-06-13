# # import numpy as np
# # import pandas as pd
# # import matplotlib.pyplot as plt
# # from scipy.optimize import fsolve
# #
# # def safe_exp(x):
# #     """
# #     Calcula el exponencial de x, evitando overflow en el cálculo.
# #     :param x: Valor a calcular el exponencial.
# #     :return: Exponencial de x.
# #     """
# #     x_clipped = np.clip(x, None, 700)  # 700 es un valor seguro para evitar overflow en np.exp
# #     return np.exp(x_clipped)
# #
# # class PVModel:
# #     """
# #     Modelo de un panel fotovoltaico usando el modelo de los 5 parámetros.
# #     """
# #
# #     def __init__(self, irradiance, temperature, isc, voc, num_cells, series_resistance, shunt_resistance,
# #                  temp_coefficient, nI, I0, IL):
# #         self.irradiance = irradiance  # Irradiancia en W/m^2
# #         self.temperature = temperature  # Temperatura en grados Celsius
# #         self.isc = isc  # Corriente de cortocircuito en A
# #         self.voc = voc  # Tensión de circuito abierto en V
# #         self.num_cells = num_cells  # Número de celdas en serie
# #         self.series_resistance = series_resistance  # Resistencia en serie en ohmios
# #         self.shunt_resistance = shunt_resistance  # Resistencia en paralelo en ohmios
# #         self.temp_coefficient = temp_coefficient  # Coeficiente de temperatura en A/°C
# #         self.nI = nI  # Factor de idealidad del diodo
# #         self.I0 = I0  # Corriente de saturación inversa
# #         self.IL = IL  # Foto corriente
# #
# #     def pv_model(self, temperature=None, irradiance=None):
# #         """
# #         Simula el comportamiento de un panel fotovoltaico bajo ciertas condiciones de temperatura e irradiancia.
# #         :param temperature: Temperatura en grados Celsius.
# #         :param irradiance: Irradiancia en W/m^2.
# #         :return: DataFrame con los valores de corriente, voltaje y potencia para el panel.
# #         """
# #         temperature_k = temperature + 273.15  # Convertir a Kelvin
# #
# #         # Constantes
# #         CHARGE = 1.602176634e-19
# #         BOLTZMANN_CONST = 1.380649e-23
# #         NOMINAL_TEMP = 298.15  # 25°C en Kelvin
# #         BANDGAP_ENERGY = 1.12  # Energía de banda prohibida del silicio en eV
# #
# #         # Foto corriente ajustada por temperatura y irradiancia
# #         i_ph = (self.IL + self.temp_coefficient * (temperature_k - NOMINAL_TEMP)) * (irradiance / 1000)
# #
# #         def current_voltage_relation(volt, i):
# #             """
# #             Relación I-V para el modelo de diodo del panel PV.
# #             :param volt: Tensión en el punto de operación.
# #             :param i: Corriente en el punto de operación.
# #             :return: Diferencia entre la corriente foto generada y la corriente de saturación.
# #             """
# #             # Corriente Shunt
# #             ish = (volt + i * self.series_resistance) / self.shunt_resistance
# #
# #             return i_ph - self.I0 * (safe_exp((CHARGE * (volt + i * self.series_resistance)) / (
# #                     self.nI * BOLTZMANN_CONST * self.num_cells * temperature_k)) - 1) - ish - i
# #
# #         voltage_values = np.linspace(0, self.voc, 2000)  # Valores de voltaje para evaluar (aumentar la precisión)
# #         current_values = []
# #
# #         for v in voltage_values:
# #             try:
# #                 # Se utiliza un valor inicial cercano a isc y se ajusta la función para que fsolve trabaje correctamente
# #                 i_solution = fsolve(lambda i: current_voltage_relation(v, i), self.isc)[0]
# #                 current_values.append(i_solution)
# #             except RuntimeError as e:
# #                 print(f'Error de convergencia para V={v} V: {e}')
# #                 current_values.append(np.nan)
# #
# #         power_values = voltage_values * np.array(current_values)
# #         results = pd.DataFrame(
# #             {'Voltage (V)': voltage_values, 'Current (A)': current_values, 'Power (W)': power_values})
# #
# #         # Encontrar el punto de máxima potencia
# #         max_power_idx = results['Power (W)'].idxmax()
# #         vmpp = results.iloc[max_power_idx]['Voltage (V)']
# #         impp = results.iloc[max_power_idx]['Current (A)']
# #         pmax = results.iloc[max_power_idx]['Power (W)']
# #
# #         return results, vmpp, impp, pmax
# #
# #     def single_graph(self, G, T, image_path='./img'):
# #         resultados, vmpp, impp, pmax = self.pv_model(T, G)
# #         # Gráficos
# #         fig, ax1 = plt.subplots()
# #
# #         color = 'tab:blue'
# #         ax1.set_xlabel('Voltage (V)')
# #         ax1.set_ylabel('Current (A)', color=color)
# #         ax1.plot(resultados['Voltage (V)'], resultados['Current (A)'], color=color)
# #         ax1.tick_params(axis='y', labelcolor=color)
# #         ax1.grid()
# #
# #         ax2 = ax1.twinx()
# #         color = 'tab:green'
# #         ax2.set_ylabel('Power (W)', color=color)
# #         ax2.plot(resultados['Voltage (V)'], resultados['Power (W)'], color=color)
# #         ax2.tick_params(axis='y', labelcolor=color)
# #
# #         plt.title('Curvas I-V y P-V')
# #
# #         # Guardar la figura
# #         plt.tight_layout()
# #         plt.savefig(f'{image_path}/curvas_pv_single.png', dpi=300)
# #         plt.show()
# #
# #         # Mostrar la potencia máxima
# #         print(f'Potencia máxima (Pmax): {pmax:.2f} W')
# #         print(f'Voltaje en Pmax (Vmpp): {vmpp:.2f} V')
# #         print(f'Corriente en Pmax (Impp): {impp:.2f} A')
# #
# # def main():
# #     # Datos del panel A10Green Technology A10J-S72-175 bajo condiciones STD
# #     irradiance = 1000  # W/m^2
# #     temperature = 25  # Grados Celsius
# #     isc = 5.17  # A
# #     voc = 43.99 # V
# #     num_cells = 72
# #     series_resistance = 0.38412  # Ohms
# #     shunt_resistance = 249.6758  # Ohms
# #     temp_coeff_isc = 0.002146  # A/K
# #     nI = 0.98852  # Factor de idealidad del diodo
# #     I0 = 1.7842e-10  # Corriente de saturación inversa
# #     IL = 5.178  # Foto corriente
# #
# #     model = PVModel(irradiance, temperature, isc, voc, num_cells, series_resistance, shunt_resistance, temp_coeff_isc, nI, I0, IL)
# #
# #     # Simulación para un conjunto específico de condiciones
# #     model.single_graph(irradiance, temperature)
# #
# # if __name__ == "__main__":
# #     main()
# #
# # # import numpy as np
# # # import pandas as pd
# # # import matplotlib.pyplot as plt
# # # from scipy.optimize import fsolve
# # #
# # # def safe_exp(x):
# # #     """
# # #     Calcula el exponencial de x, evitando overflow en el cálculo.
# # #     :param x: Valor a calcular el exponencial.
# # #     :return: Exponencial de x.
# # #     """
# # #     x_clipped = np.clip(x, None, 700)  # 700 es un valor seguro para evitar overflow en np.exp
# # #     return np.exp(x_clipped)
# # #
# # # class PVModel:
# # #     """
# # #     Modelo de un panel fotovoltaico usando el modelo de los 5 parámetros.
# # #     """
# # #
# # #     def __init__(self, irradiance, temperature, isc, voc, num_cells, series_resistance, shunt_resistance,
# # #                  temp_coefficient, nI, I0, IL):
# # #         self.irradiance = irradiance  # Irradiancia en W/m^2
# # #         self.temperature = temperature  # Temperatura en grados Celsius
# # #         self.isc = isc  # Corriente de cortocircuito en A
# # #         self.voc = voc  # Tensión de circuito abierto en V
# # #         self.num_cells = num_cells  # Número de celdas en serie
# # #         self.series_resistance = series_resistance  # Resistencia en serie en ohmios
# # #         self.shunt_resistance = shunt_resistance  # Resistencia en paralelo en ohmios
# # #         self.temp_coefficient = temp_coefficient  # Coeficiente de temperatura en A/°C
# # #         self.nI = nI  # Factor de idealidad del diodo
# # #         self.I0 = I0  # Corriente de saturación inversa
# # #         self.IL = IL  # Foto corriente
# # #
# # #     def pv_model(self, temperature=None, irradiance=None):
# # #         """
# # #         Simula el comportamiento de un panel fotovoltaico bajo ciertas condiciones de temperatura e irradiancia.
# # #         :param temperature: Temperatura en grados Celsius.
# # #         :param irradiance: Irradiancia en W/m^2.
# # #         :return: DataFrame con los valores de corriente, voltaje y potencia para el panel.
# # #         """
# # #         temperature_k = temperature + 273.15  # Convertir a Kelvin
# # #
# # #         # Constantes
# # #         CHARGE = 1.602176634e-19
# # #         BOLTZMANN_CONST = 1.380649e-23
# # #         NOMINAL_TEMP = 298.15  # 25°C en Kelvin
# # #         BANDGAP_ENERGY = 1.12  # Energía de banda prohibida del silicio en eV
# # #
# # #         # Foto corriente ajustada por temperatura y irradiancia
# # #         i_ph = (self.IL + self.temp_coefficient * (temperature_k - NOMINAL_TEMP)) * (irradiance / 1000)
# # #
# # #         def current_voltage_relation(volt, i):
# # #             """
# # #             Relación I-V para el modelo de diodo del panel PV.
# # #             :param volt: Tensión en el punto de operación.
# # #             :param i: Corriente en el punto de operación.
# # #             :return: Diferencia entre la corriente foto generada y la corriente de saturación.
# # #             """
# # #             # Corriente Shunt
# # #             ish = (volt + i * self.series_resistance) / self.shunt_resistance
# # #
# # #             return i_ph - self.I0 * (safe_exp((CHARGE * (volt + i * self.series_resistance)) / (
# # #                     self.nI * BOLTZMANN_CONST * self.num_cells * temperature_k)) - 1) - ish - i
# # #
# # #         voltage_values = np.linspace(0, self.voc, 2000)  # Valores de voltaje para evaluar (aumentar la precisión)
# # #         current_values = []
# # #
# # #         for v in voltage_values:
# # #             try:
# # #                 # Se utiliza un valor inicial cercano a isc y se ajusta la función para que fsolve trabaje correctamente
# # #                 i_solution = fsolve(lambda i: current_voltage_relation(v, i), self.isc)[0]
# # #                 current_values.append(i_solution)
# # #             except RuntimeError as e:
# # #                 print(f'Error de convergencia para V={v} V: {e}')
# # #                 current_values.append(np.nan)
# # #
# # #         power_values = voltage_values * np.array(current_values)
# # #         results = pd.DataFrame(
# # #             {'Voltage (V)': voltage_values, 'Current (A)': current_values, 'Power (W)': power_values})
# # #
# # #         # Encontrar el punto de máxima potencia
# # #         max_power_idx = results['Power (W)'].idxmax()
# # #         vmpp = results.iloc[max_power_idx]['Voltage (V)']
# # #         impp = results.iloc[max_power_idx]['Current (A)']
# # #         pmax = results.iloc[max_power_idx]['Power (W)']
# # #
# # #         return results, vmpp, impp, pmax
# # #
# # #     def single_graph(self, G, T, image_path='./img'):
# # #         resultados, vmpp, impp, pmax = self.pv_model(T, G)
# # #         # Gráficos
# # #         fig, ax1 = plt.subplots()
# # #
# # #         color = 'tab:blue'
# # #         ax1.set_xlabel('Voltage (V)')
# # #         ax1.set_ylabel('Current (A)', color=color)
# # #         ax1.plot(resultados['Voltage (V)'], resultados['Current (A)'], color=color)
# # #         ax1.tick_params(axis='y', labelcolor=color)
# # #         ax1.grid()
# # #
# # #         ax2 = ax1.twinx()
# # #         color = 'tab:green'
# # #         ax2.set_ylabel('Power (W)', color=color)
# # #         ax2.plot(resultados['Voltage (V)'], resultados['Power (W)'], color=color)
# # #         ax2.tick_params(axis='y', labelcolor=color)
# # #
# # #         plt.title(f'Curvas I-V y P-V para G={G} W/m² y T={T}°C')
# # #
# # #         # Guardar la figura
# # #         plt.tight_layout()
# # #         plt.savefig(f'{image_path}/curvas_pv_single_G{G}_T{T}.png', dpi=300)
# # #         plt.show()
# # #
# # #         # Mostrar la potencia máxima
# # #         print(f'Potencia máxima (Pmax) para G={G} W/m² y T={T}°C: {pmax:.2f} W')
# # #         print(f'Voltaje en Pmax (Vmpp): {vmpp:.2f} V')
# # #         print(f'Corriente en Pmax (Impp): {impp:.2f} A')
# # #
# # # def main():
# # #     # Datos del panel A10Green Technology A10J-S72-175 bajo condiciones STD
# # #     isc = 5.17  # A
# # #     voc = 43.99  # V
# # #     num_cells = 72
# # #     series_resistance = 0.38412  # Ohms
# # #     shunt_resistance = 249.6758  # Ohms
# # #     temp_coeff_isc = 0.002146  # A/K
# # #     nI = 0.98852  # Factor de idealidad del diodo
# # #     I0 = 1.7842e-10  # Corriente de saturación inversa
# # #     IL = 5.178  # Foto corriente
# # #
# # #     # Crear modelo PV
# # #     model = PVModel(irradiance=1000, temperature=25, isc=isc, voc=voc, num_cells=num_cells,
# # #                     series_resistance=series_resistance, shunt_resistance=shunt_resistance,
# # #                     temp_coefficient=temp_coeff_isc, nI=nI, I0=I0, IL=IL)
# # #
# # #     # Valores de irradiancia y temperatura para la simulación
# # #     # irradiances = [1000, 500, 100]
# # #     irradiances = [1000]
# # #     temperature = 25  # Temperatura fija
# # #
# # #     for G in irradiances:
# # #         model.single_graph(G, temperature)
# # #
# # # if __name__ == "__main__":
# # #     main()
#
# import json
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# from scipy.optimize import fsolve
# import logging
#
# # Configuración del logger
# logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
#
#
# def safe_exp(x):
#     x_clipped = np.clip(x, None, 700)
#     return np.exp(x_clipped)
#
#
# class PVModel:
#     def __init__(self, irradiance, temperature, isc, voc, num_cells, series_resistance, shunt_resistance,
#                  temp_coefficient, nI, I0, IL):
#         self.irradiance = irradiance
#         self.temperature = temperature
#         self.isc = isc
#         self.voc = voc
#         self.num_cells = num_cells
#         self.series_resistance = series_resistance
#         self.shunt_resistance = shunt_resistance
#         self.temp_coefficient = temp_coefficient
#         self.nI = nI
#         self.I0 = I0
#         self.IL = IL
#
#     def pv_model(self, temperature=None, irradiance=None):
#         temperature_k = temperature + 273.15
#         CHARGE = 1.602176634e-19
#         BOLTZMANN_CONST = 1.380649e-23
#         NOMINAL_TEMP = 298.15
#         BANDGAP_ENERGY = 1.12
#
#         i_ph = (self.IL + self.temp_coefficient * (temperature_k - NOMINAL_TEMP)) * (irradiance / 1000)
#
#         def current_voltage_relation(volt, i):
#             ish = (volt + i * self.series_resistance) / self.shunt_resistance
#             return i_ph - self.I0 * (safe_exp((CHARGE * (volt + i * self.series_resistance)) / (
#                         self.nI * BOLTZMANN_CONST * self.num_cells * temperature_k)) - 1) - ish - i
#
#         voltage_values = np.linspace(0, self.voc, 2000)
#         current_values = []
#
#         for v in voltage_values:
#             try:
#                 i_solution = fsolve(lambda i: current_voltage_relation(v, i), self.isc)[0]
#                 current_values.append(i_solution)
#             except RuntimeError as e:
#                 logging.warning(f'Error de convergencia para V={v} V: {e}')
#                 current_values.append(np.nan)
#
#         power_values = voltage_values * np.array(current_values)
#         results = pd.DataFrame(
#             {'Voltage (V)': voltage_values, 'Current (A)': current_values, 'Power (W)': power_values})
#
#         max_power_idx = results['Power (W)'].idxmax()
#         vmpp = results.iloc[max_power_idx]['Voltage (V)']
#         impp = results.iloc[max_power_idx]['Current (A)']
#         pmax = results.iloc[max_power_idx]['Power (W)']
#
#         return results, vmpp, impp, pmax
#
#
# def main():
#     logging.info('Leyendo datos del archivo JSON...')
#     with open('panelData.json') as f:
#         panel_data = json.load(f)
#
#     irradiance = 1000
#     temperature = 25
#
#     errors = []
#
#     for panel_name, panel_specs in panel_data.items():
#         logging.info(f'Procesando panel: {panel_name}')
#
#         isc = float(panel_specs["Isc"])
#         voc = float(panel_specs["Voc"])
#         num_cells = int(panel_specs["Ncell"])
#         series_resistance = float(panel_specs["Rs"])
#         shunt_resistance = float(panel_specs["Rsh"])
#         temp_coeff_isc = float(panel_specs["alpha_Isc"])
#         nI = float(panel_specs["nI"])
#         I0 = float(panel_specs["I0"])
#         IL = float(panel_specs["IL"])
#         pmax_spec = float(panel_specs["Pm"])
#
#         logging.info(f'Iniciando simulación para {panel_name}...')
#         model = PVModel(irradiance, temperature, isc, voc, num_cells, series_resistance, shunt_resistance,
#                         temp_coeff_isc, nI, I0, IL)
#         _, _, _, pmax_calc = model.pv_model(temperature, irradiance)
#
#         abs_error = abs(pmax_calc - pmax_spec)
#         rel_error = abs_error / pmax_spec
#
#         logging.info(
#             f'Panel {panel_name}: Pmax especificado = {pmax_spec}, Pmax calculado = {pmax_calc}, Error absoluto = {abs_error}, Error relativo = {rel_error}')
#         errors.append({"Panel": panel_name, "Pmax_Spec": pmax_spec, "Pmax_Calc": pmax_calc, "Abs_Error": abs_error,
#                        "Rel_Error": rel_error})
#
#     error_df = pd.DataFrame(errors)
#     error_df.to_csv('panel_errors.csv', index=False)
#     logging.info('Resultados almacenados en panel_errors.csv')
#
#     plt.hist(error_df['Rel_Error'], bins=20, edgecolor='black')
#     plt.title('Relative Error Histogram')
#     plt.xlabel('Relative Error')
#     plt.ylabel('Frequency')
#     plt.grid(True)
#     plt.savefig('relative_error_histogram.png', dpi=300)
#     logging.info('Histograma de errores relativos guardado como relative_error_histogram.png')
#     plt.show()
#
#
# if __name__ == "__main__":
#     main()


import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
import logging
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Configuración del logger para que guarde los logs en un archivo
logging.basicConfig(filename='simulation.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

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

    json_file = 'panelData.json'
    processed_file = 'processed_models.txt'
    processed_models = read_processed_models(processed_file)

    model_names = get_model_names(json_file)
    unprocessed_models = [model for model in model_names if model not in processed_models]

    if not unprocessed_models:
        logger.info('Todos los modelos han sido procesados.')
        return

    models_to_process = unprocessed_models[:30]
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
    header = not os.path.exists('panel_simulation_data.csv')
    data_df.to_csv('panel_simulation_data.csv', index=False, mode='a', header=header)
    logger.info('Datos de simulación almacenados en panel_simulation_data.csv')

    # Actualizar el archivo de modelos procesados
    write_processed_models(processed_file, processed_models)

if __name__ == "__main__":
    main()
