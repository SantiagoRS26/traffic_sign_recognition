from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import numpy as np
import csv
class ModelEvaluator:
    def __init__(self, model, X_test, y_test_encoded):
        self.model = model
        self.X_test = X_test
        self.y_test_encoded = y_test_encoded

    def evaluate(self):
        # Realizar predicciones
        y_pred_probs = self.model.predict(self.X_test)
        y_pred_classes = np.argmax(y_pred_probs, axis=1)
        y_true_classes = np.argmax(self.y_test_encoded, axis=1)

        # Calcular métricas
        accuracy = accuracy_score(y_true_classes, y_pred_classes)
        precision = precision_score(y_true_classes, y_pred_classes, average='weighted')
        recall = recall_score(y_true_classes, y_pred_classes, average='weighted')
        f1 = f1_score(y_true_classes, y_pred_classes, average='weighted')
        conf_matrix = confusion_matrix(y_true_classes, y_pred_classes, normalize='true')
        class_report = classification_report(y_true_classes, y_pred_classes, output_dict=True)
        per_class_metrics = {
            class_label: {
                'precision': metrics['precision'],
                'recall': metrics['recall'],
                'f1-score': metrics['f1-score'],
                'support': metrics['support']
            }
            for class_label, metrics in class_report.items() if class_label.isdigit()  # Solo clases numéricas
        }
        conf_mat = confusion_matrix(y_true_classes, y_pred_classes)  # Matriz de confusión sin normalizar
        class_accuracies = {}
        for i, class_name in enumerate(per_class_metrics.keys()):  # Usar claves del reporte por clase
            correct_predictions = conf_mat[i, i]
            total_samples = conf_mat[i, :].sum()  # Total de ejemplos reales de la clase i
            accuracy_per_class = correct_predictions / total_samples if total_samples > 0 else 0
            class_accuracies[class_name] = accuracy_per_class

        # Obtener índices de predicciones correctas e incorrectas
        correct_indices = np.nonzero(y_pred_classes == y_true_classes)[0]
        incorrect_indices = np.nonzero(y_pred_classes != y_true_classes)[0]
        
        # Obtener índices de predicciones correctas e incorrectas
        correct_indices = np.nonzero(y_pred_classes == y_true_classes)[0]
        incorrect_indices = np.nonzero(y_pred_classes != y_true_classes)[0]
        data_quantity = []
        with open('conteo_imagenes.csv', mode='r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Saltar la cabecera
            for row in csv_reader:
                data_quantity.append({"class": row[0], "quantity": int(row[1])})
        # Retornar resultados
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'confusion_matrix': conf_matrix,
            'classification_report': per_class_metrics,
            'correct_indices': correct_indices,
            'incorrect_indices': incorrect_indices,
            'y_pred_classes': y_pred_classes,
            'y_true_classes': y_true_classes,
            'data_quantity': data_quantity,
            'class_accuracies': class_accuracies
        }
