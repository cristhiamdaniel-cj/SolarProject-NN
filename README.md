# SolarProject-NN

## Descripción del Proyecto

El objetivo de este proyecto es desarrollar una solución integral para la simulación y control de sistemas fotovoltaicos utilizando técnicas de aprendizaje automático y control avanzado. Este proyecto incluye la modelización de paneles solares, la implementación de controladores, convertidores, inversores y su integración con la red eléctrica. También se desarrollará una aplicación web para facilitar el acceso y la visualización de los resultados. Se demostrará la capacidad de realizar estas simulaciones tanto con Simulink como con herramientas de código abierto en Python.

## Estructura del Repositorio

```plaintext
SolarProject-NN/
├── Panel_Solar/
│   ├── Simulink/
│   │   ├── screenshots/
│   │   ├── data/
│   │   ├── sunset_pv.slx
│   │   ├── README.md
│   │   └── data_pv.m
│   ├── Python/
│   │   ├── scripts/
│   │   │   ├── validation/
│   │   │   ├── mppt/
│   │   ├── models/
│   │   ├── data/
│   │   └── README.md
│   └── README.md
├── Controller/
│   ├── scripts/
│   │   ├── mppt_perturb_and_observe.py
│   │   ├── sliding_mode_controller.py
│   └── README.md
├── Converter/
│   ├── scripts/
│   │   ├── dc_dc_converter.py
│   └── README.md
├── Inverter/
│   ├── scripts/
│   │   ├── csi_inverter.py
│   └── README.md
├── Filter/
│   ├── scripts/
│   │   ├── lc_filter.py
│   └── README.md
├── WebApp/
│   ├── app/
│   │   ├── static/
│   │   │   ├── css/
│   │   │   ├── js/
│   │   │   └── images/
│   │   ├── templates/
│   │   │   ├── index.html
│   │   ├── views.py
│   ├── tests/
│   └── README.md
├── CloudDeployment/
│   ├── scripts/
│   │   ├── deploy_to_aws.py
│   └── README.md
├── data/
│   ├── panel_data/
│   ├── training_data/
├── docs/
│   ├── thesis/
│   ├── presentations/
├── results/
│   ├── validation_results/
│   ├── simulation_results/
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE
```

## Contenidos

### Panel_Solar

Contiene todo lo relacionado con el modelado de paneles solares:
- **Simulink/**: Modelos y simulaciones en Simulink.
- **Python/**: Scripts para validación y simulación utilizando Python.
- **README.md**: Explicaciones detalladas y uso.

### Controller

Implementaciones de controladores avanzados:
- **scripts/**: Algoritmos de control como MPPT y modos deslizantes.
- **README.md**: Explicaciones detalladas y uso.

### Converter

Implementaciones de convertidores DC-DC:
- **scripts/**: Código relacionado con convertidores.
- **README.md**: Explicaciones detalladas y uso.

### Inverter

Implementaciones de inversores de corriente:
- **scripts/**: Código relacionado con inversores.
- **README.md**: Explicaciones detalladas y uso.

### Filter

Implementaciones de filtros LC:
- **scripts/**: Código relacionado con filtros.
- **README.md**: Explicaciones detalladas y uso.

### WebApp

Desarrollo de la aplicación web:
- **app/**: Código fuente de la aplicación web.
- **tests/**: Pruebas de la aplicación.
- **README.md**: Explicaciones detalladas y uso.

### CloudDeployment

Scripts y documentación para despliegue en la nube:
- **scripts/**: Scripts de despliegue.
- **README.md**: Explicaciones detalladas y uso.

### data

Datos utilizados en el proyecto:
- **panel_data/**: Datos de paneles solares.
- **training_data/**: Datos de entrenamiento.

### docs

Documentación del proyecto:
- **thesis/**: Capítulos de la tesis.
- **presentations/**: Presentaciones relacionadas.

### results

Resultados de validaciones y simulaciones:
- **validation_results/**: Resultados de validaciones.
- **simulation_results/**: Resultados de simulaciones.

## Instalación

1. Clonar el repositorio:
    ```sh
    git clone https://github.com/cristhiamdaniel-cj/SolarProject-NN.git
    ```

2. Crear y activar un entorno virtual:
    ```sh
    cd SolarProject-NN
    python -m venv .venv
    source .venv/bin/activate  # En Windows: .venv\Scripts\activate
    ```

3. Instalar las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

## Uso

Para ejecutar los scripts, primero asegúrate de que el entorno virtual esté activado.

### Validar Datos

```sh
python Panel_Solar/Python/scripts/validation/data_validation.py
```

### Simulación MPPT

```sh
python Panel_Solar/Python/scripts/mppt/mppt_simulation.py
```

### Despliegue en la Nube

```sh
python CloudDeployment/scripts/deploy_to_aws.py
```

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir los cambios que te gustaría hacer.

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](LICENSE) para más detalles.

## Contacto

Para preguntas o sugerencias, por favor contacta a Cristhiam Daniel en [danielcampos.ingenieria@gmail.com](mailto:tu-email@example.com).

