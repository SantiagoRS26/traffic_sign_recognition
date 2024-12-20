from app.utils.data_pipeline import DataPipeline
from app.utils.model_trainer import ModelTrainer
from app.models.cnn_models import create_cnn_model_1, create_cnn_model_2  # Asegúrate de importar ambas arquitecturas
from app.utils.model_evaluator import ModelEvaluator
import numpy as np
import matplotlib.pyplot as plt
import os
import json
import csv
from tensorflow.keras.models import load_model

class TrainingPipeline:
    def __init__(self):
        self.is_training = False
        self.model = None
        self.evaluation_results = None
        self.cross_validation_results = None  # Inicializar aquí
        self.correct_examples_path = None
        self.incorrect_examples_path = None

        # Intentar cargar el modelo entrenado si existe
        self.load_trained_model()

    def load_trained_model(self):
        if os.path.exists('trained_model.h5'):
            self.model = load_model('trained_model.h5')
            print("Modelo cargado desde 'trained_model.h5'")
            # Intentar cargar los resultados de validación cruzada
            if os.path.exists('cross_validation_results.json'):
                with open('cross_validation_results.json', 'r') as f:
                    self.cross_validation_results = json.load(f)
            else:
                self.cross_validation_results = None
            # Cargar datos necesarios para evaluaciones y predicciones
            self.load_data()
            # Evaluar el modelo para obtener métricas iniciales
            self.evaluate_model()
        else:
            print("No se encontró un modelo entrenado. Se requiere entrenar el modelo.")

    def load_data(self):
        # Cargar y preprocesar los datos (solo se hace una vez)
        train_dir = 'data/crop_dataset/crop_dataset'
        test_dir = 'data/test_data/test_data'
        test_labels_file = 'test_labels.csv'
        self.contar_imagenes_jpg(train_dir, "conteo_imagenes.csv")
        self.data_pipeline = DataPipeline(train_dir, test_dir, test_labels_file)
        (self.X_train, self.y_train_encoded, self.y_train), (self.X_test, self.y_test_encoded, self.y_test) = self.data_pipeline.load_and_preprocess_data()
        self.class_labels = self.data_pipeline.data_loader.classes

    def evaluate_model(self):
        # Evaluar el modelo en el conjunto de prueba
        evaluator = ModelEvaluator(self.model, self.X_test, self.y_test_encoded)
        evaluation_results = evaluator.evaluate()

        # Almacenar los resultados
        self.evaluation_results = {
            'accuracy': evaluation_results['accuracy'],
            'precision': evaluation_results['precision'],
            'recall': evaluation_results['recall'],
            'f1_score': evaluation_results['f1_score'],
            'classification_report': evaluation_results['classification_report'],
            'confusion_matrix': evaluation_results['confusion_matrix'].tolist(),  # Convertir a lista para JSON
            'data_quantity': evaluation_results['data_quantity'],
            'class_accuracies': evaluation_results['class_accuracies'],
        }

        # Generar y guardar imágenes de ejemplos
        self.save_example_images(evaluation_results)
    def contar_imagenes_jpg(self,ruta_relativa, nombre_archivo_salida):
        """
        Función que cuenta los archivos .jpg en cada subcarpeta de una ruta relativa y guarda los resultados en un archivo CSV.

        :param ruta_relativa: Ruta relativa donde buscar las carpetas.
        :param nombre_archivo_salida: Nombre del archivo CSV donde se guardarán los resultados.
        """
        # Crear una lista para almacenar los datos
        datos = [("clase", "cantidad")]

        # Recorrer cada carpeta en la ruta relativa
        for carpeta in os.listdir(ruta_relativa):
            ruta_carpeta = os.path.join(ruta_relativa, carpeta)
            if os.path.isdir(ruta_carpeta):
                # Contar los archivos .jpg en la carpeta actual
                cantidad_jpg = len([archivo for archivo in os.listdir(ruta_carpeta) if archivo.lower().endswith(".jpg")])
                # Agregar la carpeta y la cantidad al listado de datos
                datos.append((carpeta, cantidad_jpg))

        # Guardar los datos en un archivo CSV
        with open(nombre_archivo_salida, mode="w", newline="", encoding="utf-8") as archivo_csv:
            escritor = csv.writer(archivo_csv)
            escritor.writerows(datos)
        print(f"Conteo completado. Archivo generado: {nombre_archivo_salida}")

    def train_and_evaluate(self):
        self.is_training = True
        try:
            # Cargar datos si no se han cargado
            if not hasattr(self, 'X_train'):
                self.load_data()

            # Entrenar y evaluar los modelos con validación cruzada
            model_trainer = ModelTrainer(self.X_train, self.y_train_encoded, num_classes=self.data_pipeline.preprocessor.num_classes, n_splits=2)

            # CNN Modelo 1
            avg_accuracy_1, std_accuracy_1 = model_trainer.train_and_evaluate(create_cnn_model_1, "CNN Modelo 1")

            # CNN Modelo 2
            avg_accuracy_2, std_accuracy_2 = model_trainer.train_and_evaluate(create_cnn_model_2, "CNN Modelo 2")

            # Almacenar los resultados de validación cruzada
            self.cross_validation_results = [
                {
                    'model': 'CNN Modelo 1',
                    'average_accuracy': avg_accuracy_1,
                    'std_accuracy': std_accuracy_1,
                },
                {
                    'model': 'CNN Modelo 2',
                    'average_accuracy': avg_accuracy_2,
                    'std_accuracy': std_accuracy_2,
                }
            ]

            # Guardar los resultados de validación cruzada en un archivo JSON
            with open('cross_validation_results.json', 'w') as f:
                json.dump(self.cross_validation_results, f)

            # Seleccionar el mejor modelo
            if avg_accuracy_2 > avg_accuracy_1:
                best_model_creator = create_cnn_model_2
                best_model_name = "CNN Modelo 2"
            else:
                best_model_creator = create_cnn_model_1
                best_model_name = "CNN Modelo 1"

            # Entrenar el modelo seleccionado con el conjunto completo
            self.model = best_model_creator(input_shape=self.X_train.shape[1:], num_classes=self.data_pipeline.preprocessor.num_classes)
            self.model.fit(self.X_train, self.y_train_encoded,
                           epochs=10,
                           batch_size=64,
                           validation_data=(self.X_test, self.y_test_encoded),
                           verbose=1)

            # Guardar el modelo entrenado
            self.model.save('trained_model.h5')
            print("Modelo guardado en 'trained_model.h5'")

            # Evaluar el modelo
            self.evaluate_model()

        finally:
            self.is_training = False

    def save_example_images(self, evaluation_results):
        correct_indices = evaluation_results['correct_indices']
        incorrect_indices = evaluation_results['incorrect_indices']
        y_pred_classes = evaluation_results['y_pred_classes']
        y_true_classes = evaluation_results['y_true_classes']

        # Seleccionar 5 ejemplos correctos de clases diferentes
        correct_examples = []
        selected_classes_correct = set()
        for idx in correct_indices:
            true_class = y_true_classes[idx]
            if true_class not in selected_classes_correct:
                correct_examples.append(idx)
                selected_classes_correct.add(true_class)
            if len(correct_examples) == 5:
                break

        # Seleccionar 5 ejemplos incorrectos de clases diferentes
        incorrect_examples = []
        selected_classes_incorrect = set()
        for idx in incorrect_indices:
            true_class = y_true_classes[idx]
            if true_class not in selected_classes_incorrect:
                incorrect_examples.append(idx)
                selected_classes_incorrect.add(true_class)
            if len(incorrect_examples) == 5:
                break

        # Función para guardar imágenes
        def guardar_imagenes(indices, X_data, y_true, y_pred, titulo, filename):
            plt.figure(figsize=(15, 5))
            for i, idx in enumerate(indices):
                plt.subplot(1, 5, i+1)
                image = X_data[idx]
                image = image.reshape(32, 32, 3)
                plt.imshow(image)
                plt.axis('off')
                plt.title(f"V: {self.class_labels[y_true[idx]]}\nP: {self.class_labels[y_pred[idx]]}")
            plt.suptitle(titulo)
            plt.savefig(filename)
            plt.close()

        # Crear directorio para almacenar las imágenes si no existe
        if not os.path.exists('examples'):
            os.makedirs('examples')

        # Guardar imágenes
        self.correct_examples_path = 'examples/correct_examples.png'
        self.incorrect_examples_path = 'examples/incorrect_examples.png'

        guardar_imagenes(correct_examples, self.X_test, y_true_classes, y_pred_classes,
                         "Ejemplos Correctamente Clasificados", self.correct_examples_path)
        guardar_imagenes(incorrect_examples, self.X_test, y_true_classes, y_pred_classes,
                         "Ejemplos Incorrectamente Clasificados", self.incorrect_examples_path)
