% Nombre del archivo del modelo de Simulink
model = 'sunset_pv';

% Cargar el modelo de Simulink
load_system(model);

% Definir los parámetros de entrada: Temperatura (T), Irradiancia (G) y Tensión (V)
T = 25; % Temperatura en grados Celsius
G = 1000; % Irradiancia en W/m^2
V = 30; % Tensión en Voltios

% Asignar los valores a las variables de trabajo
assignin('base', 'T', T);
assignin('base', 'G', G);
assignin('base', 'V', V);

% Ejecutar la simulación
simOut = sim(model);

% Extraer los resultados de la simulación
% La corriente de salida se asume que está en 'simOut.I'
Iout = simOut.I.Data;

% Mostrar la corriente de salida
disp(['La corriente de salida del panel solar es: ', num2str(Iout(end)), ' A']); % Mostramos el último valor de la corriente

% Cerrar el modelo de Simulink
close_system(model, 0);