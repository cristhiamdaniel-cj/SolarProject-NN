# Documentación de Predicciones del Modelo de Red Neuronal y Simulink

## Descripción del Código

### `nn_predictor.py`

El script `nn_predictor.py` se utiliza para predecir la corriente de salida de un panel solar utilizando un modelo de red neuronal. El proceso seguido en este script es el siguiente:

1. **Importación de Librerías y Definiciones de Clase:**
   - Se importan las librerías necesarias (`pandas`, `numpy`, `joblib`, `json`, `os`, y métricas de `sklearn`).
   - Se define la clase `NeuralNetworkPredictor` que carga un modelo de red neuronal previamente entrenado y un escalador para las características de entrada.
   - Se crea la clase `SimpleNeuralNetworkPredictor` que hereda de `NeuralNetworkPredictor` y añade el método `show_current` para predecir y mostrar la corriente de salida.

2. **Función Principal:**
   - La función `main` se encarga de cargar el escalador y los parámetros del modelo.
   - Verifica la existencia de los archivos necesarios.
   - Solicita al usuario que ingrese los valores de temperatura, irradiancia y voltaje.
   - Predice y muestra la corriente de salida utilizando la clase `SimpleNeuralNetworkPredictor`.

### `simulink_runner.m`

El script `simulink_runner.m` se utiliza para predecir la corriente de salida de un panel solar utilizando un modelo de Simulink. El proceso seguido en este script es el siguiente:

1. **Definición y Carga del Modelo:**
   - Se define y carga el modelo de Simulink `sunset_pv`.

2. **Asignación de Valores de Entrada:**
   - Se asignan los valores de temperatura, irradiancia y voltaje a las variables de trabajo en el espacio base de MATLAB.

3. **Ejecución de la Simulación:**
   - Se ejecuta la simulación.
   - Se extraen y muestran los resultados de la corriente de salida del panel solar.
   - Se cierra el sistema de Simulink.

## Resultados Obtenidos

### Resultado en MATLAB
```plaintext
ki =

    0.0370

q =

   1.6022e-19

K =

   1.3807e-23

n =

     1

Eg0 =

    1.1000

Rs =

    0.3900

Rsh =

  545.8200

Tn =

   298

Voc =

   47.4000

Isc =

    9.3500

Ns =

    72

La corriente de salida del panel solar es: 9.283 A
```
- La corriente de salida del panel solar es de 9.283 A cuando se utilizan los parámetros especificados en MATLAB.

### Resultado en Python
```plaintext

Ingrese la temperatura en grados Celsius: 25
Ingrese la irradiancia en W/m^2: 1000
Ingrese el voltaje en V: 30
La corriente de salida para Temperatura=25.0, Irradiancia=1000.0, Voltaje=30.0 es: 9.27634 A

Process finished with exit code 0
```
- La corriente de salida para los mismos parámetros en Python es de 9.27634 A.

