# Reconocimiento de Señales de Tráfico - Frontend

Este proyecto es la interfaz de usuario para una aplicación de reconocimiento de señales de tráfico. Utiliza una API proporcionada por el backend para interactuar con un modelo de aprendizaje automático, permitiendo a los usuarios cargar imágenes para predicciones, visualizar métricas de evaluación y analizar ejemplos de clasificaciones correctas e incorrectas.

## Contenido

- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Iniciar la Aplicación](#iniciar-la-aplicación)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Uso de la Aplicación](#uso-de-la-aplicación)
- [Dependencias](#dependencias)
- [Notas Adicionales](#notas-adicionales)
- [Contribuciones](#contribuciones)

---

## Requisitos

- Node.js 14 o superior
- npm o yarn como gestor de paquetes

## Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/tu_usuario/traffic_sign_recognition.git
   cd traffic_sign_recognition/frontend
   ```

2. **Instalar las dependencias**:
   ```bash
   npm install
   ```
   > Si encuentras problemas de dependencias, puedes usar `npm install --legacy-peer-deps`.

## Iniciar la Aplicación

Para iniciar la aplicación en modo de desarrollo:

```bash
npm run dev
```

La aplicación estará disponible en `http://localhost:3000`. 

> **Nota**: Asegúrate de que el backend esté en ejecución en `http://localhost:8000` para que el frontend pueda acceder a los endpoints de la API.

## Estructura del Proyecto

```plaintext
frontend/
├── app/
│   ├── layout.tsx            # Layout principal de la aplicación
│   ├── page.tsx              # Página de inicio
│   ├── metrics/
│   │   └── page.tsx          # Página para visualización de métricas del modelo
│   ├── examples/
│   │   ├── correct.tsx       # Página para mostrar ejemplos correctamente clasificados
│   │   └── incorrect.tsx     # Página para mostrar ejemplos incorrectamente clasificados
│   └── predict/
│       └── page.tsx          # Página para cargar imágenes y hacer predicciones
├── components/
│   ├── Navbar.tsx            # Barra de navegación principal
│   ├── MetricCard.tsx        # Componente para mostrar métricas individuales
│   └── ConfusionMatrix.tsx   # Visualización de la matriz de confusión
├── public/                   # Archivos públicos y recursos
├── styles/                   # Archivos de estilos personalizados
├── tailwind.config.js        # Configuración de Tailwind CSS
├── tsconfig.json             # Configuración de TypeScript
└── README.md                 # Este archivo
```

## Uso de la Aplicación

La interfaz del usuario tiene varias funcionalidades:

- **Ver Métricas del Modelo**: Accede a `/metrics` para visualizar los resultados de validación cruzada, la matriz de confusión y métricas generales de evaluación como exactitud, precisión y F1.
- **Ejemplos Correctos e Incorrectos**: En las páginas `/examples/correct` y `/examples/incorrect`, puedes ver ejemplos de imágenes que el modelo clasificó correctamente e incorrectamente.
- **Hacer Predicciones**: En `/predict`, puedes cargar una imagen de señal de tráfico para obtener la predicción de clase del modelo.

## Dependencias

- **Next.js**: Framework de React utilizado para construir la aplicación.
- **React**: Biblioteca de JavaScript para construir interfaces de usuario.
- **TypeScript**: Superconjunto de JavaScript que añade tipado estático.
- **Tailwind CSS**: Framework de utilidades de CSS para diseño rápido y responsivo.
- **@nivo/heatmap**: Librería de visualización para crear la matriz de confusión.
  - Si tienes problemas de instalación, puedes usar `npm install @nivo/heatmap --legacy-peer-deps`.

## Notas Adicionales

- **Configuración de la API**: Asegúrate de que la URL del backend esté configurada correctamente en los archivos de Next.js, apuntando a `http://localhost:8000`.
- **Visualización de la Matriz de Confusión**: La aplicación utiliza `@nivo/heatmap` para mostrar la matriz de confusión de forma visual e interactiva. 
- **Error de Dependencias**: Si encuentras errores de dependencia relacionados con la versión de React, prueba usar `--legacy-peer-deps` al instalar `@nivo/heatmap` o considera una versión alternativa de la biblioteca.

## Contribuciones

Las contribuciones a este proyecto son bienvenidas. Si deseas contribuir:

1. Haz un fork del proyecto.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza los cambios necesarios y haz commit (`git commit -m 'Añadir nueva funcionalidad'`).
4. Realiza un push a tu rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un pull request en este repositorio.