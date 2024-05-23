% Definir Voc (tensión en circuito abierto)
Voc = 47.4;  % Este valor debería ser definido según tu caso

% Crear un vector de voltaje con 100 valores desde 0 hasta Voc
voltage_values = linspace(0, Voc, 100)';

% Definir el tiempo de simulación (puede ser ajustado según la necesidad)
t = linspace(0, 100, 100)';  % Ajustamos el tiempo para que tenga 100 puntos

% Definir los rangos de entrada
temperatures = 15:5:55;  % Temperatura de 15 a 55 grados Celsius, en pasos de 5
irradiances = 100:100:1000;  % Irradiancia de 100 a 1000 W/m^2, en pasos de 100

% Cargar el modelo
model = 'sunset_pv';
load_system(model);

% Dividir las temperaturas en bloques
num_blocks = length(temperatures);  % Número de bloques basado en el tamaño del rango de temperatura
temp_blocks = arrayfun(@(i) temperatures(i), 1:num_blocks, 'UniformOutput', false);

parfor block_idx = 1:num_blocks
    results = [];  % Inicializar una matriz para almacenar los resultados por bloque
    temp = temp_blocks{block_idx};
    for irr = irradiances
        % Definir las señales de entrada para temperatura e irradiancia
        T = [t, temp * ones(size(t))];
        G = [t, irr * ones(size(t))];

        % Asignar las variables al espacio de trabajo base
        assignin('base', 'T', double(T));
        assignin('base', 'G', double(G));
        assignin('base', 'voltage_values', double([t, voltage_values]));  % Asignar el vector de voltaje

        % Mostrar la combinación actual de temperatura e irradiancia
        fprintf('Ejecutando simulación para temperatura = %d °C, irradiancia = %d W/m^2\n', temp, irr);

        % Ejecutar la simulación
        simOut = sim(model);

        % Verificar si 'simOut' contiene 'V' y 'I' como campos válidos
        if isfield(simOut, 'V') && isfield(simOut, 'I') && ~isempty(simOut.V) && ~isempty(simOut.I)
            % Obtener los resultados de la simulación
            voltage_data = simOut.V;
            current_data = simOut.I;

            % Verificar si las dimensiones son compatibles
            if length(voltage_data) == length(current_data)
                % Calcular la potencia
                power_data = voltage_data .* current_data;  

                % Crear una matriz temporal con los datos actuales
                temp_results = [voltage_data, current_data, power_data, temp * ones(size(voltage_data)), irr * ones(size(voltage_data))];

                % Concatenar los resultados actuales a la matriz de resultados
                results = [results; temp_results];
            else
                fprintf('Dimensiones incompatibles para temperatura = %d °C, irradiancia = %d W/m^2. No se pueden calcular los resultados.\n', temp, irr);
            end
        else
            fprintf('Simulink output does not contain expected fields for temperatura = %d °C, irradiancia = %d W/m^2.\n', temp, irr);
        end
    end
    if ~isempty(results)
        % Convertir la matriz de resultados a una tabla
        results_table = array2table(results, 'VariableNames', {'Voltage', 'Current', 'Power', 'Temperature', 'Irradiance'});

        % Guardar la tabla de resultados en un archivo CSV
        writetable(results_table, sprintf('simulation_results_block_%d.csv', block_idx));
    end
end

% Cerrar el modelo
close_system(model, 0);
