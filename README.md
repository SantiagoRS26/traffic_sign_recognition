# Proyecto de Reconocimiento de Señales de Tráfico

Este repositorio contiene la implementación completa de una aplicación para el reconocimiento de señales de tráfico, organizada en dos subproyectos: **backend** y **frontend**. El backend proporciona una API para la carga, entrenamiento, evaluación y predicción de señales de tráfico mediante redes neuronales, mientras que el frontend ofrece una interfaz visual para interactuar con esta API.

## Tabla de Contenidos

- [Estructura del Proyecto](#estructura-del-proyecto)
- [Configuración General](#configuración-general)
- [Iniciar la Aplicación Completa](#iniciar-la-aplicación-completa)
- [Verificación de Servicios](#verificación-de-servicios)
- [Detalles del Proyecto](#detalles-del-proyecto)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)

---

## Estructura del Proyecto

La estructura de este repositorio está organizada en dos directorios principales, cada uno con sus propios archivos de configuración y dependencias:

```
traffic_sign_recognition/
├── backend/                   # Código del backend con FastAPI y TensorFlow
│   ├── app/                   # Aplicación backend
│   ├── data/                  # Carpeta para datos de entrenamiento y prueba
│   ├── requirements.txt       # Dependencias del backend
│   └── README.md              # Instrucciones específicas del backend
├── frontend/                  # Código del frontend con Next.js y Tailwind CSS
│   ├── app/                   # Componentes y páginas de Next.js
│   ├── public/                # Archivos públicos
│   ├── tailwind.config.js     # Configuración de Tailwind CSS
│   ├── tsconfig.json          # Configuración de TypeScript
│   └── README.md              # Instrucciones específicas del frontend
├── .gitignore                 # Configuración global para ignorar archivos
└── README.md                  # Este archivo
```

## Configuración General

Cada subproyecto (backend y frontend) tiene su propio entorno de desarrollo, y es necesario configurarlos por separado. A continuación, se indican los pasos para preparar el entorno en cada carpeta.

1. **Clonar el Repositorio**:
   ```bash
   git clone https://github.com/SantiagoRS26/traffic_sign_recognition.git
   cd traffic_sign_recognition
   ```

2. **Configuración del Backend**:
   - Navega a la carpeta `backend` e instala las dependencias necesarias.
   - Los detalles específicos están disponibles en el archivo [`backend/README.md`](backend/README.md).

3. **Configuración del Frontend**:
   - Navega a la carpeta `frontend` y sigue las instrucciones para instalar las dependencias de Node.js y configurar el entorno.
   - Consulta el archivo [`frontend/README.md`](frontend/README.md) para detalles adicionales.

## Iniciar la Aplicación Completa

Para ejecutar el proyecto completo en desarrollo, es necesario iniciar tanto el backend como el frontend en terminales separadas.

1. **Iniciar el Backend**:
   - En una terminal, navega a `backend/` y ejecuta:
   ```bash
   uvicorn app.main:app --reload
   ```
   - Esto iniciará el servidor de FastAPI en `http://localhost:8000`.

2. **Iniciar el Frontend**:
   - En otra terminal, navega a `frontend/` y ejecuta:
   ```bash
   npm run dev
   ```
   - Esto iniciará la aplicación de Next.js en `http://localhost:3000`.

Con ambos servicios en funcionamiento, puedes acceder al frontend en `http://localhost:3000` y la interfaz interactuará automáticamente con el backend para realizar operaciones de entrenamiento, evaluación y predicción.

## Verificación de Servicios

### Backend

Puedes verificar que el backend está en funcionamiento accediendo a `http://localhost:8000/docs`. Esto abrirá la documentación generada automáticamente de la API con todos los endpoints disponibles.

### Frontend

El frontend debe estar disponible en `http://localhost:3000`, donde podrás interactuar con el modelo de reconocimiento de señales de tráfico a través de una interfaz de usuario.

## Detalles del Proyecto

- **Backend**: Proporciona los endpoints necesarios para entrenar el modelo de reconocimiento de señales de tráfico, ver métricas de rendimiento y realizar predicciones sobre imágenes.
- **Frontend**: Una interfaz de usuario que consume los endpoints del backend, mostrando métricas de validación, permitiendo la carga de imágenes para predicciones y visualizando ejemplos de clasificaciones correctas e incorrectas.

## Contribuciones

Las contribuciones a este proyecto son bienvenidas. Si deseas contribuir:

1. Realiza un fork de este repositorio.
2. Crea una nueva rama para tu funcionalidad (`git checkout -b feature/nueva-funcionalidad`).
3. Haz commit de tus cambios (`git commit -am 'Añadir nueva funcionalidad'`).
4. Realiza un push a tu rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un pull request en este repositorio.

Para más detalles sobre la configuración específica del backend o frontend, consulta los archivos `README.md` en sus respectivos directorios.

## Licencia

Este proyecto está licenciado bajo la [Licencia MIT](LICENSE).