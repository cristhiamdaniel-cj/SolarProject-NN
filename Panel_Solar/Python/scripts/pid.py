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

    def predict_current(self, temperature, irradiance, voltage):
        current = super().predict_current(temperature, irradiance, voltage)
        return current

def closed_loop_simulation(target_current):
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

    # Inicializar variables
    temperature = 25  # Temperatura en grados Celsius
    irradiance = 1000  # Irradiancia en W/m^2
    voltage = 30  # Voltaje inicial en Voltios
    kp = 0.05  # Ganancia proporcional
    ki = 0.01  # Ganancia integral
    kd = 0.01  # Ganancia derivativa
    tolerance = 0.01  # Tolerancia de error
    max_voltage = 100  # Máximo voltaje permitido
    min_voltage = 0  # Mínimo voltaje permitido
    max_voltage_change = 1.0  # Máximo cambio de voltaje por iteración

    integral = 0
    previous_error = 0

    for _ in range(200):
        current = predictor.predict_current(temperature, irradiance, voltage)
        error = target_current - current

        if abs(error) < tolerance:
            break

        integral += error
        derivative = error - previous_error
        voltage_change = kp * error + ki * integral + kd * derivative
        voltage_change = max(-max_voltage_change, min(voltage_change, max_voltage_change))  # Limitar el cambio de voltaje
        voltage += voltage_change
        voltage = max(min_voltage, min(voltage, max_voltage))  # Limitar el voltaje dentro del rango permitido

        previous_error = error

    print(f"Condiciones: Temperatura={temperature}°C, Irradiancia={irradiance} W/m^2, Voltaje ajustado={voltage} V -> Corriente de salida={current} A")

if __name__ == '__main__':
    target_current = float(input('Ingrese la corriente de salida deseada en A: '))
    closed_loop_simulation(target_current)
