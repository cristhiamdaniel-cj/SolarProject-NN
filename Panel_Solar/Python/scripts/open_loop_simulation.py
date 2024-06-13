import os
import joblib
import json
import numpy as np
import pandas as pd
import sys

# Asegurarse de que el directorio padre esté en el path de búsqueda de módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))

from validation.data_validation import NeuralNetworkPredictor

class SimpleNeuralNetworkPredictor(NeuralNetworkPredictor):
    def __init__(self, scaler_path, model_params_path):
        super().__init__(scaler_path, model_params_path)

    def show_current(self, temperature, irradiance, voltage):
        current = super().predict_current(temperature, irradiance, voltage)
        print(f'La corriente de salida para Temperatura={temperature}, Irradiancia={irradiance}, Voltaje={voltage} es: {current:.5f} A')
        return current

def open_loop_simulation():
    base_path = os.path.dirname(os.path.abspath(__file__))
    scaler_path = os.path.join(base_path, '../model_results/relu_adam_scaler.joblib')
    model_params_path = os.path.join(base_path, '../model_results/relu_adam_params.json')

    if not os.path.exists(scaler_path):
        print(f"Error: No se encontró el archivo del escalador en {scaler_path}")
        return

    if not os.path.exists(model_params_path):
        print(f"Error: No se encontró el archivo de parámetros del modelo en {model_params_path}")
        return

    predictor = SimpleNeuralNetworkPredictor(scaler_path, model_params_path)

    # Definir diferentes condiciones ambientales para la simulación
    conditions = [
        {'temperature': 25, 'irradiance': 1000, 'voltage': 30},
        {'temperature': 35, 'irradiance': 800, 'voltage': 25},
        {'temperature': 20, 'irradiance': 900, 'voltage': 28},
        {'temperature': 30, 'irradiance': 600, 'voltage': 22},
    ]

    results = []
    for condition in conditions:
        current = predictor.show_current(condition['temperature'], condition['irradiance'], condition['voltage'])
        results.append({
            'temperature': condition['temperature'],
            'irradiance': condition['irradiance'],
            'voltage': condition['voltage'],
            'current': current
        })

    # Mostrar los resultados de la simulación
    for result in results:
        print(f"Condiciones: Temperatura={result['temperature']}°C, Irradiancia={result['irradiance']} W/m^2, Voltaje={result['voltage']} V -> Corriente de salida={result['current']} A")

if __name__ == '__main__':
    open_loop_simulation()
