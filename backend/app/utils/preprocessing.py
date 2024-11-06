import numpy as np
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import StratifiedKFold

class Preprocessor:
    def __init__(self, num_classes):
        self.num_classes = num_classes

    def normalize_images(self, X):
        X = X.astype('float32') / 255.0  # Normalización al rango [0, 1]
        return X

    def encode_labels(self, y):
        y_encoded = to_categorical(y, num_classes=self.num_classes)
        return y_encoded

    def resize_images(self, X, img_size):
        # Si es necesario redimensionar las imágenes, implementamos esta función
        from tensorflow.image import resize
        X_resized = resize(X, img_size)
        return X_resized

    def split_data(self, X, y, n_splits=2):
        # Utilizamos StratifiedKFold para mantener la proporción de clases
        skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
        splits = list(skf.split(X, y))
        return splits