# Reconocimiento de Señales de Tráfico

Este proyecto implementa una API para el reconocimiento de señales de tráfico utilizando una red neuronal convolucional (CNN). La aplicación permite entrenar un modelo de reconocimiento de señales de tráfico con un conjunto de datos predefinido y ofrece endpoints para realizar predicciones sobre imágenes cargadas.

## **Contenido**

- [Requisitos](#requisitos)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Conjunto de Datos](#conjunto-de-datos)
- [Configuración](#configuración)
- [Iniciar la Aplicación](#iniciar-la-aplicación)
- [Uso de la API](#uso-de-la-api)
- [Endpoints Disponibles](#endpoints-disponibles)

---

## **Requisitos**

- Python 3.8 o superior
- [TensorFlow](https://www.tensorflow.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)

## **Estructura del Proyecto**

```
traffic_sign_recognition/
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

## **Conjunto de Datos**

Para entrenar el modelo, este proyecto utiliza un conjunto de datos de señales de tráfico recortadas. Puedes descargar el conjunto de datos desde Kaggle en el siguiente enlace:

**[Conjunto de Datos en Kaggle](https://www.kaggle.com/datasets/shanmukh05/traffic-sign-cropped)**

1. Descarga el conjunto de datos desde Kaggle.
2. Extrae el contenido descargado en la carpeta `data/` del proyecto, de modo que las subcarpetas `crop_dataset/` y `test_data/` se ubiquen en `data/`.

## **Configuración**

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/tu_usuario/traffic_sign_recognition.git
   cd traffic_sign_recognition
   ```

### **Crear y activar un entorno virtual**

1. **Crear el entorno virtual:**

   ```bash
   python -m venv env
   ```

2. **Activar el entorno virtual:**

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

## **Iniciar la Aplicación**

Para iniciar la aplicación, usa el siguiente comando en la raíz del proyecto:

```bash
uvicorn app.main:app --reload
```

La aplicación estará disponible en `http://127.0.0.1:8000`.

> **Nota**: La primera vez que se inicia la aplicación, es posible que sea necesario entrenar el modelo si no se encuentra el archivo `trained_model.h5`.

## **Uso de la API**

La API proporciona varios endpoints para interactuar con el modelo. Aquí se describen los endpoints principales:

### **Entrenar el Modelo**

- **Endpoint:** `POST /train`
- **Descripción:** Inicia el entrenamiento del modelo en segundo plano.
- **Ejemplo de uso (cURL):**
  ```bash
  curl -X POST http://127.0.0.1:8000/train
  ```

### **Obtener Métricas de Evaluación**

- **Endpoint:** `GET /metrics`
- **Descripción:** Devuelve las métricas de evaluación del modelo entrenado, como precisión, recall y matriz de confusión.
- **Ejemplo de uso (cURL):**
  ```bash
  curl http://127.0.0.1:8000/metrics
  ```

### **Ejemplos de Clasificaciones Correctas e Incorrectas**

- **Endpoint para ejemplos correctos:** `GET /examples/correct`
- **Endpoint para ejemplos incorrectos:** `GET /examples/incorrect`
- **Descripción:** Devuelve una imagen con ejemplos correctamente o incorrectamente clasificados por el modelo.
- **Ejemplo de uso (cURL):**
  ```bash
  curl http://127.0.0.1:8000/examples/correct
  ```

### **Realizar una Predicción**

- **Endpoint:** `POST /predict`
- **Descripción:** Permite cargar una imagen de señal de tráfico y devuelve la predicción del modelo.
- **Parámetros:** Se debe cargar la imagen como un archivo.
- **Ejemplo de uso (cURL):**
  ```bash
  curl -X POST -F "file=@ruta_de_la_imagen.jpg" http://127.0.0.1:8000/predict
  ```

---

## **Endpoints Disponibles**

| Método | Ruta               | Descripción                                           |
|--------|---------------------|-------------------------------------------------------|
| POST   | `/train`           | Inicia el entrenamiento del modelo                    |
| GET    | `/metrics`         | Devuelve las métricas de evaluación del modelo        |
| GET    | `/examples/correct`| Devuelve una imagen de ejemplos correctamente clasificados |
| GET    | `/examples/incorrect` | Devuelve una imagen de ejemplos incorrectamente clasificados |
| POST   | `/predict`         | Realiza una predicción de clase para una imagen cargada|

---

## **Notas Adicionales**

- **Persistencia del Modelo:** El modelo se guarda como `trained_model.h5` después del entrenamiento. Si este archivo está presente, la aplicación lo cargará automáticamente al iniciar, evitando la necesidad de volver a entrenarlo.
- **Manejo de Datos:** La carpeta `data/` debe contener las subcarpetas `crop_dataset/` y `test_data/` con los datos de entrenamiento y prueba, respectivamente.
- **Control de Entrenamiento Concurrente:** El endpoint `/train` no permite múltiples solicitudes de entrenamiento al mismo tiempo. Solo se puede entrenar un modelo a la vez.
- **Reentrenamiento:** Si deseas reentrenar el modelo, elimina el archivo `trained_model.h5` o llama al endpoint `/train`.

---

## **Contribuciones**

Si deseas contribuir al proyecto, por favor, abre un issue o envía un pull request. Cualquier mejora o sugerencia es bienvenida.

## **Licencia**

Este proyecto está licenciado bajo la [Licencia MIT](LICENSE).