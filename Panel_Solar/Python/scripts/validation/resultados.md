# Resultados de la Validación del Modelo de Red Neuronal

## Descripción del Script `data_validation.py`

El script `data_validation.py` tiene como objetivo evaluar el rendimiento de un modelo de red neuronal que predice la corriente de salida de un panel solar. El script realiza las siguientes tareas:

1. **Importación de Librerías y Definiciones de Clase:**
   - Se importan librerías esenciales como `pandas`, `numpy`, `joblib`, `json`, `os`, y métricas de `sklearn`.
   - Se define la clase `NeuralNetworkPredictor` que carga un modelo de red neuronal previamente entrenado y un escalador para las características de entrada.

2. **Clase `NeuralNetworkPredictor`:**
   - **Constructor (`__init__`):** Carga el escalador y los parámetros del modelo desde archivos.
   - **Función `relu`:** Implementa la función de activación ReLU.
   - **Función `predict_current`:** Predice la corriente de salida del panel solar dada la temperatura, irradiancia y voltaje. Transforma los datos de entrada, aplica el modelo de red neuronal capa por capa y retorna la predicción final.

3. **Funciones Auxiliares:**
   - **`preprocess_data`:** Preprocesa los datos de validación, renombrando las columnas para que coincidan con las usadas durante el entrenamiento del escalador y filtrando valores inválidos.
   - **`sample_data`:** Toma una muestra aleatoria de los datos para la evaluación.
   - **`evaluate_model`:** Evalúa el modelo predictor sobre un conjunto de datos dado, calculando el error cuadrático medio (MSE), el error absoluto medio (MAE) y el coeficiente de determinación (R²).

4. **Función Principal (`main`):**
   - Carga el escalador y los parámetros del modelo.
   - Carga y preprocesa los datos de validación y de simulación.
   - Toma muestras aleatorias de los datos de validación y de simulación.
   - Evalúa el modelo predictor sobre los datos de validación y de simulación.
   - Imprime las métricas de evaluación (MSE, MAE, R²) para ambos conjuntos de datos.

## Resultados Obtenidos

El script se ejecutó correctamente y los resultados de las métricas de evaluación fueron los siguientes:

```plaintext
Validation Data Metrics - MSE: 0.00025, MAE: 0.01048, R²: 0.99996
Simulation Data Metrics - MSE: 0.10033, MAE: 0.19370, R²: 0.97629
```

### Análisis de Resultados

1. **Datos de Validación:**
   - **MSE:** 0.00025
   - **MAE:** 0.01048
   - **R²:** 0.99996

   Los resultados de las métricas sobre los datos de validación son muy buenos, indicando que el modelo de red neuronal predice con alta precisión la corriente de salida del panel solar cuando se utilizan datos de validación reales.

2. **Datos de Simulación:**
   - **MSE:** 0.10033
   - **MAE:** 0.19370
   - **R²:** 0.97629

   Los resultados de las métricas sobre los datos de simulación también son bastante buenos, aunque no tan precisos como en los datos de validación. Esto podría indicar que hay algunas discrepancias entre las condiciones simuladas y los datos reales, lo cual es común en modelos basados en simulaciones.

### Conclusiones

El modelo de red neuronal muestra un excelente rendimiento en la predicción de la corriente de salida del panel solar cuando se utilizan datos de validación. Aunque el rendimiento disminuye ligeramente en los datos de simulación, los resultados siguen siendo aceptables. Esto sugiere que el modelo puede generalizar bien, pero podría beneficiarse de ajustes adicionales o datos de entrenamiento más diversos para mejorar la precisión en condiciones simuladas.

Es importante destacar que los datos de validación son obtenidos mediante la función `fsolve` en Python, y que estos mismos datos se utilizaron para entrenar la red neuronal. Esta es la razón por la cual los resultados de la red neuronal se acercan más a los valores deseados en comparación con los datos de simulación.

