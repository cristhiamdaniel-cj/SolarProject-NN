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

def preprocess_data(val_data):
    # Renombrar las columnas para que coincidan con las utilizadas durante el entrenamiento del escalador
    if 'Voltage' in val_data.columns:
        val_data.rename(columns={
            'Voltage': 'Voltage (V)',
            'Current': 'Current (A)',
            'Power': 'Power (W)',
            'Temperature': 'Temperatura',
            'Irradiance': 'Irradiancia'
        }, inplace=True)
    
    val_data = val_data[val_data['Voltage (V)'] != 0]
    val_data = val_data[val_data['Current (A)'] >= 0]

    return val_data

def sample_data(val_data, sample_size):
    return val_data.sample(n=sample_size, random_state=42)

def evaluate_model(predictor, val_data):
    val_data['Predicted Current (A)'] = val_data.apply(
        lambda row: predictor.predict_current(row['Temperatura'], row['Irradiancia'], row['Voltage (V)']), axis=1
    )

    mse = mean_squared_error(val_data['Current (A)'], val_data['Predicted Current (A)'])
    mae = mean_absolute_error(val_data['Current (A)'], val_data['Predicted Current (A)'])
    r2 = r2_score(val_data['Current (A)'], val_data['Predicted Current (A)'])

    return mse, mae, r2

def main():
    base_path = os.path.dirname(os.path.abspath(__file__))

    predictor = NeuralNetworkPredictor(
        os.path.join(base_path, '../../model_results/relu_adam_scaler.joblib'),
        os.path.join(base_path, '../../model_results/relu_adam_params.json')
    )

    val_data_path = os.path.join(base_path, '../../data/val_data.csv')
    sim_data_path = os.path.join(base_path, '../../../Simulink/data/simulation_results.csv')

    val_data = preprocess_data(pd.read_csv(val_data_path))
    sim_data = preprocess_data(pd.read_csv(sim_data_path))

    sample_size = min(len(val_data), len(sim_data))
    val_data_sampled = sample_data(val_data, sample_size)
    sim_data_sampled = sample_data(sim_data, sample_size)

    avg_mse_val, avg_mae_val, avg_r2_val = evaluate_model(predictor, val_data_sampled)
    avg_mse_sim, avg_mae_sim, avg_r2_sim = evaluate_model(predictor, sim_data_sampled)

    print(f"Validation Data Metrics - MSE: {avg_mse_val:.5f}, MAE: {avg_mae_val:.5f}, R²: {avg_r2_val:.5f}")
    print(f"Simulation Data Metrics - MSE: {avg_mse_sim:.5f}, MAE: {avg_mae_sim:.5f}, R²: {avg_r2_sim:.5f}")

if __name__ == '__main__':
    main()
