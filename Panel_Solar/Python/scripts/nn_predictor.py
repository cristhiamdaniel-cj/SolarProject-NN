import os
import joblib
import json
import numpy as np
import pandas as pd
from validation.data_validation import NeuralNetworkPredictor

class SimpleNeuralNetworkPredictor(NeuralNetworkPredictor):
    def __init__(self, scaler_path, model_params_path):
        super().__init__(scaler_path, model_params_path)

    def show_current(self, temperature, irradiance, voltage):
        current = self.predict_current(temperature, irradiance, voltage)
        print(f'La corriente de salida para Temperatura={temperature}, Irradiancia={irradiance}, Voltaje={voltage} es: {current:.5f} A')

def main():
    base_path = os.path.dirname(os.path.abspath(__file__))
    scaler_path = os.path.join(base_path, '../model_results/relu_adam_scaler.joblib')
    model_params_path = os.path.join(base_path, '../model_results/relu_adam_params.json')

    # Verificar que los archivos existen
    if not os.path.exists(scaler_path):
        print(f"Error: No se encontró el archivo del escalador en {scaler_path}")
        return

    if not os.path.exists(model_params_path):
        print(f"Error: No se encontró el archivo de parámetros del modelo en {model_params_path}")
        return

    predictor = SimpleNeuralNetworkPredictor(scaler_path, model_params_path)

    # Ejemplo de uso
    temperature = float(input('Ingrese la temperatura en grados Celsius: '))
    irradiance = float(input('Ingrese la irradiancia en W/m^2: '))
    voltage = float(input('Ingrese el voltaje en V: '))

    predictor.show_current(temperature, irradiance, voltage)

if __name__ == '__main__':
    main()


