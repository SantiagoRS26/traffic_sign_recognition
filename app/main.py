from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Traffic Sign Recognition API")
app.include_router(router)

# Puntos de entrada para ejecutar Uvicorn si se ejecuta este archivo directamente
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)