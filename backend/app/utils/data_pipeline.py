from app.utils.data_loader import DataLoader
from app.utils.preprocessing import Preprocessor

class DataPipeline:
    def __init__(self, train_dir, test_dir, test_labels_file, img_size=(32, 32)):
        # Instanciar el cargador de datos y el preprocesador
        self.data_loader = DataLoader(train_dir, test_dir, test_labels_file, img_size)
        self.preprocessor = Preprocessor(num_classes=self.data_loader.num_classes)
        self.img_size = img_size

    def load_and_preprocess_data(self):
        # Cargar datos de entrenamiento y prueba
        X_train, y_train = self.data_loader.load_training_data()
        X_test, y_test = self.data_loader.load_test_data()

        # Preprocesar imágenes y etiquetas
        X_train = self.preprocessor.normalize_images(X_train)
        X_test = self.preprocessor.normalize_images(X_test)
        y_train_encoded = self.preprocessor.encode_labels(y_train)
        y_test_encoded = self.preprocessor.encode_labels(y_test)

        return (X_train, y_train_encoded, y_train), (X_test, y_test_encoded, y_test)

    def get_cross_validation_splits(self, X, y, n_splits=2):
        # Obtener los índices para los splits de validación cruzada
        splits = self.preprocessor.split_data(X, y, n_splits)
        return splits