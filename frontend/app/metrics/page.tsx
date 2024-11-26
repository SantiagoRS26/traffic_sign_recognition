'use client';

import { useEffect, useState } from 'react';

interface Metrics {
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  confusion_matrix: number[][];
  classification_report: any;
}

interface CrossValidationResult {
  model: string;
  average_accuracy: number;
  std_accuracy: number;
}

export default function MetricsPage() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [crossValidationResults, setCrossValidationResults] = useState<CrossValidationResult[] | null>(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchMetrics = async () => {
      try {
        const response = await fetch('http://localhost:8000/metrics');
        if (!response.ok) {
          throw new Error('El modelo no ha sido entrenado aún.');
        }
        const data = await response.json();
        setMetrics(data.evaluation_results);
        setCrossValidationResults(data.cross_validation_results);
      } catch (error: any) {
        setError(error.message);
      }
    };
    fetchMetrics();
  }, []);

  if (error) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-gray-100">
        <p className="text-red-500">{error}</p>
      </main>
    );
  }

  if (!metrics || !crossValidationResults) {
    return (
      <main className="min-h-screen flex items-center justify-center bg-gray-100">
        <p>Cargando métricas...</p>
      </main>
    );
  }

  const getCellColor = (value: number, maxValue: number) => {
    const intensity = Math.floor((value / maxValue) * 255);
    return `rgba(33, 150, 243, ${intensity / 255})`; // Usamos un color azul con opacidad según el valor
  };

  const maxConfusionValue = Math.max(...metrics.confusion_matrix.flat());

  return (
    <div className="min-h-screen p-8 bg-gray-100">
      <h1 className="text-3xl font-bold mb-6 text-center">Resultados del Modelo</h1>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">Resultados de Validación Cruzada (2-fold)</h2>
        <table className="min-w-full bg-white rounded-lg shadow-md border border-gray-200">
          <thead>
            <tr>
              <th className="py-3 px-4 bg-blue-600 text-white border">Modelo</th>
              <th className="py-3 px-4 bg-blue-600 text-white border">Exactitud Promedio</th>
            </tr>
          </thead>
          <tbody>
            {crossValidationResults.map((result, index) => (
              <tr key={index} className="text-center border-b last:border-b-0">
                <td className="py-3 px-4 border">{result.model}</td>
                <td className="py-3 px-4 border">
                  {result.average_accuracy.toFixed(4)} ± {result.std_accuracy.toFixed(4)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section>
        <h2 className="text-2xl font-semibold mb-4">Métricas de Evaluación del Mejor Modelo</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
            <h3 className="text-xl font-semibold mb-4">Métricas Generales</h3>
            <div className="space-y-2 text-lg">
              <p><strong>Exactitud:</strong> {metrics.accuracy.toFixed(4)}</p>
              <p><strong>Precisión:</strong> {metrics.precision.toFixed(4)}</p>
              <p><strong>Exhaustividad (Recall):</strong> {metrics.recall.toFixed(4)}</p>
              <p><strong>Medida F1:</strong> {metrics.f1_score.toFixed(4)}</p>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
            <h3 className="text-xl font-semibold mb-4">Matriz de Confusión</h3>
            <div className="overflow-auto max-h-96 border rounded-lg">
              <table className="min-w-full text-xs border-collapse">
                <tbody>
                  {metrics.confusion_matrix.map((row, rowIndex) => (
                    <tr key={rowIndex}>
                      {row.map((value, colIndex) => (
                        <td
                          key={colIndex}
                          className="border text-center text-white font-semibold"
                          style={{
                            backgroundColor: getCellColor(value, maxConfusionValue),
                          }}
                        >
                          {value}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
