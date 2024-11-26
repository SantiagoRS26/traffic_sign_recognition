from fastapi import APIRouter, BackgroundTasks, HTTPException, UploadFile, File
from app.utils.training_pipeline import TrainingPipeline
from fastapi.responses import JSONResponse, FileResponse
import numpy as np
from tensorflow.keras.preprocessing import image
import io

router = APIRouter()

# Instancia del pipeline de entrenamiento (almacena resultados)
training_pipeline = TrainingPipeline()

@router.get("/")
async def root():
    return {"message": "API de Reconocimiento de Señales de Tráfico"}

@router.post("/train")
async def train_model(background_tasks: BackgroundTasks):
    if training_pipeline.is_training:
        raise HTTPException(status_code=400, detail="El entrenamiento ya está en curso.")
    background_tasks.add_task(training_pipeline.train_and_evaluate)
    return {"message": "El entrenamiento ha comenzado."}

@router.get("/metrics")
async def get_metrics():
    if not training_pipeline.evaluation_results:
        raise HTTPException(status_code=400, detail="El modelo no ha sido entrenado aún.")
    response = {
        'evaluation_results': training_pipeline.evaluation_results,
        'cross_validation_results': training_pipeline.cross_validation_results
    }
    return response

@router.get("/examples/correct")
async def get_correct_examples():
    if not training_pipeline.correct_examples_path:
        raise HTTPException(status_code=400, detail="Los ejemplos no están disponibles.")
    return FileResponse(training_pipeline.correct_examples_path, media_type='image/png')

@router.get("/examples/incorrect")
async def get_incorrect_examples():
    if not training_pipeline.incorrect_examples_path:
        raise HTTPException(status_code=400, detail="Los ejemplos no están disponibles.")
    return FileResponse(training_pipeline.incorrect_examples_path, media_type='image/png')

# Nuevo endpoint para predecir una imagen
@router.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    if not training_pipeline.model:
        raise HTTPException(status_code=400, detail="El modelo no ha sido entrenado aún.")

    contents = await file.read()
    img = image.load_img(io.BytesIO(contents), target_size=(32, 32))
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0  # Normalizar la imagen
    img_array = np.expand_dims(img_array, axis=0)  # Añadir dimensión batch

    # Realizar la predicción
    predictions = training_pipeline.model.predict(img_array)
    predicted_class = np.argmax(predictions, axis=1)[0]
    class_label = training_pipeline.class_labels[predicted_class]

    return {"predicted_class": int(predicted_class), "class_label": class_label}
