from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report
import numpy as np

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
        conf_matrix = confusion_matrix(y_true_classes, y_pred_classes)
        class_report = classification_report(y_true_classes, y_pred_classes, output_dict=True)

        # Obtener índices de predicciones correctas e incorrectas
        correct_indices = np.nonzero(y_pred_classes == y_true_classes)[0]
        incorrect_indices = np.nonzero(y_pred_classes != y_true_classes)[0]

        # Retornar resultados
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'confusion_matrix': conf_matrix,
            'classification_report': class_report,
            'correct_indices': correct_indices,
            'incorrect_indices': incorrect_indices,
            'y_pred_classes': y_pred_classes,
            'y_true_classes': y_true_classes
        }
