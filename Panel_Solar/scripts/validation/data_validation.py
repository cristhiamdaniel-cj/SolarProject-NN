import pandas as pd
import numpy as np
import joblib
import json
import os
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

class NeuralNetworkPredictor:
    def __init__(self, scaler_path, model_params_path):
        self.scaler = joblib.load(scaler_path)
        with open(model_params_path, 'r') as file:
            self.model_data = json.load(file)

    def relu(self, x):
        return np.maximum(0, x)

    def predict_current(self, temperature, irradiance, voltage):
        input_df = pd.DataFrame([[temperature, irradiance, voltage]], columns=['Temperatura', 'Irradiancia', 'Voltage (V)'])
        input_data_scaled = self.scaler.transform(input_df)

        output = input_data_scaled
        for layer in range(1, len(self.model_data) + 1):
            weights = np.array(self.model_data[f'Layer_{layer}']['weights'])
            biases = np.array(self.model_data[f'Layer_{layer}']['biases'])
            output = np.dot(output, weights) + biases
            if layer < len(self.model_data):
                output = self.relu(output)

        return output[0][0]

class DataValidator:
    def __init__(self, predictor, val_data_path, output_path):
        self.predictor = predictor
        self.val_data_path = val_data_path
        self.output_path = output_path

    def validate(self):
        # Cargar el dataset de validación
        print(f"Cargando el dataset desde {self.val_data_path}...")
        val_data = pd.read_csv(self.val_data_path)
        print(f"Dataset cargado con {val_data.shape[0]} registros.")

        # Preprocesar los datos
        val_data = self.preprocess_data(val_data)
        print(f"Dataset preprocesado con {val_data.shape[0]} registros.")

        # Predecir la corriente y calcular las métricas para cada registro
        print("Prediciendo la corriente y calculando métricas para cada registro...")
        val_data['Predicted Current (A)'] = val_data.apply(
            lambda row: self.predictor.predict_current(row['Temperatura'], row['Irradiancia'], row['Voltage (V)']), axis=1
        )
        print("Predicciones completadas.")

        # Calcular las métricas de desempeño
        print("Calculando métricas de desempeño...")
        val_data['MSE'] = val_data.apply(
            lambda row: mean_squared_error([row['Current (A)']], [row['Predicted Current (A)']]), axis=1
        )
        val_data['MAE'] = val_data.apply(
            lambda row: mean_absolute_error([row['Current (A)']], [row['Predicted Current (A)']]), axis=1
        )
        val_data['R2'] = val_data.apply(
            lambda row: r2_score([row['Current (A)']], [row['Predicted Current (A)']]) if len([row['Current (A)']]) > 1 else np.nan, axis=1
        )

        # Guardar el dataset con las nuevas columnas
        val_data.to_csv(self.output_path, index=False)
        print(f"Dataset con predicciones guardado en {self.output_path}.")

        # Calcular y mostrar los promedios de las métricas
        avg_mse = val_data['MSE'].mean()
        avg_mae = val_data['MAE'].mean()
        avg_r2 = val_data['R2'].mean()

        print(f'Average MSE: {avg_mse:.5f}')
        print(f'Average MAE: {avg_mae:.5f}')
        print(f'Average R²: {avg_r2:.5f if not np.isnan(avg_r2) else "undefined"}')

    def preprocess_data(self, val_data):
        # Eliminar registros inválidos
        val_data = val_data[val_data['Voltage (V)'] != 0]
        val_data = val_data[val_data['Current (A)'] >= 0]

        # Renombrar las columnas para que coincidan con las utilizadas durante el entrenamiento del escalador
        if 'Temperature' in val_data.columns and 'Irradiance' in val_data.columns:
            val_data.rename(columns={'Temperature': 'Temperatura', 'Irradiance': 'Irradiancia', 'Voltage': 'Voltage (V)', 'Current': 'Current (A)'}, inplace=True)
        
        return val_data

def main():
    # Obtener la ruta base del script actual
    base_path = os.path.dirname(os.path.abspath(__file__))

    # Inicializar el predictor
    predictor = NeuralNetworkPredictor(
        os.path.join(base_path, '../../../model_results/relu_adam_scaler.joblib'),
        os.path.join(base_path, '../../../model_results/relu_adam_params.json')
    )

    # Validar datos de val_data.csv
    val_data_validator = DataValidator(
        predictor,
        os.path.join(base_path, '../../data/val_data.csv'),
        os.path.join(base_path, '../../data/val_data_with_predictions.csv')
    )
    val_data_validator.validate()

    # Validar datos de simulation_results.csv
    sim_data_validator = DataValidator(
        predictor,
        os.path.join(base_path, '../../data/simulation_results.csv'),
        os.path.join(base_path, '../../data/simulation_results_with_predictions.csv')
    )
    sim_data_validator.validate()

if __name__ == '__main__':
    main()
