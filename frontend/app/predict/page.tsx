'use client';

import { useState } from 'react';

export default function PredictPage() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [prediction, setPrediction] = useState('');
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [error, setError] = useState('');

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setError('');
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setImagePreview(URL.createObjectURL(file));
    } else {
      setSelectedFile(null);
      setImagePreview(null);
    }
  };

  const handlePredict = async () => {
    if (!selectedFile) {
      setError('Por favor, selecciona una imagen.');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        body: formData,
      });
      if (!response.ok) {
        throw new Error('Error al realizar la predicción.');
      }
      const data = await response.json();
      setPrediction(`Clase Predicha: ${data.class_label} (ID: ${data.predicted_class})`);
    } catch (error: any) {
      setError(error.message);
    }
  };

  return (
    <main className="min-h-screen p-8 bg-gray-100 flex flex-col items-center">
      <h1 className="text-3xl font-bold mb-6">Realizar Predicción</h1>
      <div className="mb-4">
        <input type="file" accept="image/*" onChange={handleFileChange} />
      </div>
      {imagePreview && (
        <div className="mb-4">
          <img src={imagePreview} alt="Imagen seleccionada" className="max-w-xs" />
        </div>
      )}
      <button onClick={handlePredict} className="btn mb-4">
        Predecir
      </button>
      {prediction && <p className="text-green-600">{prediction}</p>}
      {error && <p className="text-red-600">{error}</p>}
    </main>
  );
}