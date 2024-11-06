
# Reconocimiento de Señales de Tráfico - Backend

Este proyecto implementa una API para el reconocimiento de señales de tráfico utilizando redes neuronales convolucionales (CNN). La API permite entrenar el modelo, evaluar su rendimiento y realizar predicciones sobre imágenes cargadas.

## Contenido

- [Requisitos](#requisitos)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Conjunto de Datos](#conjunto-de-datos)
- [Configuración](#configuración)
- [Iniciar la Aplicación](#iniciar-la-aplicación)
- [Uso de la API](#uso-de-la-api)
- [Endpoints Disponibles](#endpoints-disponibles)
- [Notas Adicionales](#notas-adicionales)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

---

## Requisitos

- Python 3.8 o superior
- [TensorFlow](https://www.tensorflow.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)

## Estructura del Proyecto

```
backend/
├── app/
│   ├── main.py                # Archivo principal para iniciar la aplicación
│   ├── api/
│   │   └── routes.py          # Definición de endpoints de la API
│   ├── models/
│   │   └── cnn_models.py      # Definición de arquitecturas CNN
│   ├── utils/
│   │   ├── data_pipeline.py   # Manejo de datos y preprocesamiento
│   │   ├── model_trainer.py   # Entrenamiento y validación del modelo
│   │   ├── model_evaluator.py # Evaluación del modelo
│   │   └── training_pipeline.py # Orquestador de entrenamiento y evaluación
├── data/
│   ├── crop_dataset/          # Carpeta con datos de entrenamiento
│   └── test_data/             # Carpeta con datos de prueba
├── test_labels.csv            # Archivo de etiquetas para los datos de prueba
├── requirements.txt           # Dependencias del proyecto
└── README.md                  # Este archivo
```

## Conjunto de Datos

El modelo utiliza un conjunto de datos de señales de tráfico recortadas, disponible en Kaggle:

- [Conjunto de Datos en Kaggle](https://www.kaggle.com/datasets/shanmukh05/traffic-sign-cropped)

### Instrucciones para la Configuración de Datos

1. **Descargar el Conjunto de Datos**: Descarga y extrae los datos en la carpeta `data/`.
2. **Estructura de la Carpeta de Datos**: El contenido extraído debe organizarse de la siguiente forma en `backend/data/`:
   ```
   backend/
   └── data/
       ├── crop_dataset/       # Carpeta con datos de entrenamiento
       └── test_data/          # Carpeta con datos de prueba
   ```

## Configuración

### Clonar el Repositorio

Desde la raíz del proyecto, clona el repositorio y navega a la carpeta `backend`:

```bash
git clone https://github.com/SantiagoRS26/traffic_sign_recognition.git
cd traffic_sign_recognition/backend
```

### Crear y Activar un Entorno Virtual

1. **Crear el entorno virtual**:
   ```bash
   python -m venv env
   ```

2. **Activar el entorno virtual**:
   - En **Linux o Mac**:
     ```bash
     source env/bin/activate
     ```
   - En **Windows (CMD)**:
     ```bash
     .\env\Scripts\activate
     ```
   - En **Windows (PowerShell)**:
     ```bash
     .\env\Scripts\Activate.ps1
     ```
   - En **Windows (Git Bash)**:
     ```bash
     source env/Scripts/activate
     ```

3. **Instalar las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

## Iniciar la Aplicación

Para iniciar la aplicación y levantar el servidor de FastAPI, ejecuta el siguiente comando desde la carpeta `backend`:

```bash
uvicorn app.main:app --reload
```

El servidor estará disponible en `http://127.0.0.1:8000`.

> **Nota**: La primera vez que se inicia la aplicación, será necesario entrenar el modelo si no se encuentra el archivo `trained_model.h5`.

## Uso de la API

Esta API ofrece varios endpoints para interactuar con el modelo, permitiendo entrenar, evaluar y realizar predicciones. A continuación, se describen los principales endpoints.

### Entrenar el Modelo

- **Endpoint:** `POST /train`
- **Descripción:** Inicia el entrenamiento del modelo en segundo plano.
- **Ejemplo de uso (cURL):**
  ```bash
  curl -X POST http://127.0.0.1:8000/train
  ```

### Obtener Métricas de Evaluación

- **Endpoint:** `GET /metrics`
- **Descripción:** Devuelve las métricas de evaluación del modelo entrenado, incluyendo precisión, recall y matriz de confusión.
- **Ejemplo de uso (cURL):**
  ```bash
  curl http://127.0.0.1:8000/metrics
  ```

### Ejemplos de Clasificaciones Correctas e Incorrectas

- **Endpoint para ejemplos correctos:** `GET /examples/correct`
- **Endpoint para ejemplos incorrectos:** `GET /examples/incorrect`
- **Descripción:** Devuelve una imagen con ejemplos correctamente o incorrectamente clasificados por el modelo.
- **Ejemplo de uso (cURL):**
  ```bash
  curl http://127.0.0.1:8000/examples/correct
  ```

### Realizar una Predicción

- **Endpoint:** `POST /predict`
- **Descripción:** Permite cargar una imagen de señal de tráfico y devuelve la predicción del modelo.
- **Parámetros:** La imagen se debe cargar como un archivo.
- **Ejemplo de uso (cURL):**
  ```bash
  curl -X POST -F "file=@ruta_de_la_imagen.jpg" http://127.0.0.1:8000/predict
  ```

---

## Endpoints Disponibles

| Método | Ruta                   | Descripción                                           |
|--------|-------------------------|-------------------------------------------------------|
| POST   | `/train`               | Inicia el entrenamiento del modelo                    |
| GET    | `/metrics`             | Devuelve las métricas de evaluación del modelo        |
| GET    | `/examples/correct`    | Devuelve una imagen de ejemplos correctamente clasificados |
| GET    | `/examples/incorrect`  | Devuelve una imagen de ejemplos incorrectamente clasificados |
| POST   | `/predict`             | Realiza una predicción de clase para una imagen cargada|

---

## Notas Adicionales

- **Persistencia del Modelo**: Después de entrenar el modelo, se guarda como `trained_model.h5`. Si este archivo existe, la aplicación lo cargará automáticamente al iniciar, evitando la necesidad de reentrenar.
- **Control de Entrenamiento Concurrente**: Solo se permite una solicitud de entrenamiento a la vez. Si deseas reentrenar el modelo, elimina `trained_model.h5` o vuelve a llamar al endpoint `/train`.
- **Manejo de Datos**: La carpeta `data/` debe contener las subcarpetas `crop_dataset/` y `test_data/` con los datos de entrenamiento y prueba.

---

## Contribuciones

Para contribuir a este proyecto:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -m 'Descripción de los cambios'`).
4. Realiza un push a tu rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un pull request para revisión.

## Licencia

Este proyecto está licenciado bajo la [Licencia MIT](../LICENSE).