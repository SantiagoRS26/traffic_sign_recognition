from app.models.cnn_models import create_cnn_model_1, create_cnn_model_2
from sklearn.model_selection import StratifiedKFold
import numpy as np

class ModelTrainer:
    def __init__(self, X, y, num_classes, n_splits=2):
        self.X = X
        self.y = y
        self.num_classes = num_classes
        self.n_splits = n_splits
        self.input_shape = X.shape[1:]  # (altura, ancho, canales)
        self.splits = self.get_splits()
    
    def get_splits(self):
        skf = StratifiedKFold(n_splits=self.n_splits, shuffle=True, random_state=42)
        splits = list(skf.split(self.X, np.argmax(self.y, axis=1)))
        return splits
    
    def train_and_evaluate(self, model_creator, model_name):
        accuracies = []
        for fold, (train_idx, val_idx) in enumerate(self.splits):
            print(f"\nEntrenando fold {fold + 1}/{self.n_splits} para {model_name}")
            X_train_fold, X_val_fold = self.X[train_idx], self.X[val_idx]
            y_train_fold, y_val_fold = self.y[train_idx], self.y[val_idx]
            
            # Crear el modelo
            model = model_creator(self.input_shape, self.num_classes)
            
            # Entrenar el modelo
            history = model.fit(X_train_fold, y_train_fold,
                                epochs=10,
                                batch_size=64,
                                validation_data=(X_val_fold, y_val_fold),
                                verbose=1)
            
            # Evaluar el modelo en el conjunto de validación
            loss, accuracy = model.evaluate(X_val_fold, y_val_fold, verbose=0)
            print(f"Exactitud en fold {fold + 1}: {accuracy:.4f}")
            accuracies.append(accuracy)
        
        average_accuracy = np.mean(accuracies)
        std_accuracy = np.std(accuracies)
        print(f"\nExactitud promedio para {model_name}: {average_accuracy:.4f} +/- {std_accuracy:.4f}")
        return average_accuracy, std_accuracy