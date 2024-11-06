import os
import numpy as np
import pandas as pd
from PIL import Image
from tqdm import tqdm

class DataLoader:
    def __init__(self, train_dir, test_dir, test_labels_file, img_size=(32, 32)):
        self.train_dir = train_dir
        self.test_dir = test_dir
        self.test_labels_file = test_labels_file
        self.img_size = img_size
        self.classes = sorted(os.listdir(train_dir))
        self.num_classes = len(self.classes)
    
    def load_training_data(self):
        X = []
        y = []
        for label in tqdm(self.classes, desc='Cargando imágenes de entrenamiento'):
            class_dir = os.path.join(self.train_dir, label)
            image_files = os.listdir(class_dir)
            for image_file in image_files:
                image_path = os.path.join(class_dir, image_file)
                try:
                    image = Image.open(image_path)
                    image = image.resize(self.img_size)
                    image = np.array(image)
                    X.append(image)
                    y.append(int(label))
                except Exception as e:
                    print(f'Error al cargar la imagen {image_path}: {e}')
        X = np.array(X)
        y = np.array(y)
        return X, y
    
    def load_test_data(self):
        X_test = []
        y_test = []
        test_labels = pd.read_csv(self.test_labels_file)
        for index, row in tqdm(test_labels.iterrows(), total=test_labels.shape[0], desc='Cargando imágenes de prueba'):
            image_file = row['image']
            label = row['label']
            image_path = os.path.join(self.test_dir, image_file)
            try:
                image = Image.open(image_path)
                image = image.resize(self.img_size)
                image = np.array(image)
                X_test.append(image)
                y_test.append(label)
            except Exception as e:
                print(f'Error al cargar la imagen {image_path}: {e}')
        X_test = np.array(X_test)
        y_test = np.array(y_test)
        return X_test, y_test