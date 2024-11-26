"use client";

import { useEffect, useState } from "react";
import clasesDict from "../clasesDict";
interface Metrics {
  accuracy: number;
  precision: number;
  recall: number;
  f1_score: number;
  confusion_matrix: number[][];
  classification_report: any;
  data_quantity : any;
  class_accuracies: any;
}

interface CrossValidationResult {
  model: string;
  average_accuracy: number;
  std_accuracy: number;
}

export default function MetricsPage() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [crossValidationResults, setCrossValidationResults] = useState<
    CrossValidationResult[] | null
  >(null);
  const [error, setError] = useState("");
  const [clases, setClases] = useState(clasesDict);
  useEffect(() => {
    console.log(clases);

    const fetchMetrics = async () => {
      try {
        const response = await fetch("http://localhost:8000/metrics");
        if (!response.ok) {
          throw new Error("El modelo no ha sido entrenado aún.");
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
    const intensity = Math.max(0.2, value / maxValue); // Aseguramos un mínimo de intensidad del 20%
    return `rgba(33, 150, 243, ${intensity})`; // Azul con opacidad según el valor
  };

  const maxConfusionValue = Math.max(...metrics.confusion_matrix.flat());

  return (
    <div className="min-h-screen p-8 bg-gray-100">
      <h1 className="text-3xl font-bold mb-6 text-center">
        Resultados del Modelo
      </h1>

      <section className="mb-12">
        <h2 className="text-2xl font-semibold mb-4">
          Resultados de Validación Cruzada (2-fold)
        </h2>
        <table className="min-w-full bg-white rounded-lg shadow-md border border-gray-200">
          <thead>
            <tr>
              <th className="py-3 px-4 bg-blue-600 text-white border">
                Modelo
              </th>
              <th className="py-3 px-4 bg-blue-600 text-white border">
                Exactitud Promedio
              </th>
            </tr>
          </thead>
          <tbody>
            {crossValidationResults.map((result, index) => (
              <tr key={index} className="text-center border-b last:border-b-0">
                <td className="py-3 px-4 border">{result.model}</td>
                <td className="py-3 px-4 border">
                  {result.average_accuracy.toFixed(4)} ±{" "}
                  {result.std_accuracy.toFixed(4)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section>
        <h2 className="text-2xl font-semibold mb-4">
          Métricas de Evaluación del Mejor Modelo
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
            <h3 className="text-xl font-semibold mb-4">Métricas Generales</h3>
            <div className="space-y-2 text-lg">
              <p>
                <strong>Exactitud:</strong> {metrics.accuracy.toFixed(4)}
              </p>
              <p>
                <strong>Precisión:</strong> {metrics.precision.toFixed(4)}
              </p>
              <p>
                <strong>Exhaustividad (Recall):</strong>{" "}
                {metrics.recall.toFixed(4)}
              </p>
              <p>
                <strong>Medida F1:</strong> {metrics.f1_score.toFixed(4)}
              </p>
            </div>
          </div>

          <div className="bg-white p-6 rounded-lg shadow-md border border-gray-200">
            <h3 className="text-xl font-semibold mb-4">
              Matriz de Confusión normalizada
            </h3>
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
                            backgroundColor: getCellColor(
                              value,
                              maxConfusionValue
                            ),
                          }}
                        >
                          {value.toFixed(2)}
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
      <section className="mb-12">
  <h2 className="text-xl font-semibold mb-4 text-center">
    Reporte de Clasificación Detallado
  </h2>
  <div className="overflow-auto">
    <table className="min-w-full bg-white rounded-lg shadow-md border border-gray-200 text-sm">
      <thead>
        <tr>
          <th className="py-2 px-4 bg-blue-600 text-white border">Clase</th>
          <th className="py-2 px-4 bg-blue-600 text-white border">Precisión</th>
          <th className="py-2 px-4 bg-blue-600 text-white border">Recall</th>
          <th className="py-2 px-4 bg-blue-600 text-white border">F1-Score</th>
          <th className="py-2 px-4 bg-blue-600 text-white border">Support</th>
        </tr>
      </thead>
      <tbody>
        {Object.entries(metrics.classification_report).map(
          ([classId, values]: any) => {
            const classKey = classId.padStart(5, "0"); // Aseguramos que el ID tenga formato "00001"
            const className = clases[classKey] || `Clase ${classId}`; // Si no encuentra el nombre, usa "Clase X"

            return (
              <tr
                key={classId}
                className="text-center border-b last:border-b-0"
              >
                <td className="py-2 px-4 border">{className}</td>
                <td className="py-2 px-4 border">
                  {values.precision.toFixed(4)}
                </td>
                <td className="py-2 px-4 border">
                  {values.recall.toFixed(4)}
                </td>
                <td className="py-2 px-4 border">
                  {values["f1-score"].toFixed(4)}
                </td>
                <td className="py-2 px-4 border">{values.support}</td>
              </tr>
            );
          }
        )}
      </tbody>
    </table>
  </div>
</section>
<section className="mb-12">
  <h2 className="text-xl font-semibold mb-4 text-center">
    Precisión de clase (Class-Wise Accuracy)
  </h2>
  <div className="overflow-auto">
    <table className="min-w-full bg-white rounded-lg shadow-md border border-gray-200 text-sm">
      <thead>
        <tr>
          <th className="py-2 px-4 bg-blue-600 text-white border">Clase</th>
          <th className="py-2 px-4 bg-blue-600 text-white border">Precisión</th>
        </tr>
      </thead>
      <tbody>
        {Object.entries(metrics.class_accuracies).map(([classId, accuracy]: any) => {
          const classKey = classId.padStart(5, "0"); // Aseguramos que el ID tenga formato "00001"
          const className = clases[classKey] || `Clase ${classId}`; // Obtiene el nombre de la clase o muestra un nombre genérico
          return (
            <tr
              key={classId}
              className="text-center border-b last:border-b-0"
            >
              <td className="py-2 px-4 border">{className}</td>
              <td className="py-2 px-4 border">{(accuracy * 100).toFixed(2)}%</td>
            </tr>
          );
        })}
      </tbody>
    </table>
  </div>
</section>

<section className="mb-12">
  <h2 className="text-xl font-semibold mb-4 text-center">
    Cantidad de Datos por Clase
  </h2>
  <div className="overflow-auto">
    <table className="min-w-full bg-white rounded-lg shadow-md border border-gray-200 text-sm">
      <thead>
        <tr>
          <th className="py-2 px-4 bg-blue-600 text-white border">Clase</th>
          <th className="py-2 px-4 bg-blue-600 text-white border">Cantidad de imagenes</th>
        </tr>
      </thead>
      <tbody>
        {metrics.data_quantity.map(({ class: classId, quantity }: any) => {
          const className = clases[classId] || `Clase ${classId}`; // Obtiene el nombre de la clase o muestra un nombre genérico
          return (
            <tr
              key={classId}
              className="text-center border-b last:border-b-0"
            >
              <td className="py-2 px-4 border">{className}</td>
              <td className="py-2 px-4 border">{quantity}</td>
            </tr>
          );
        })}
      </tbody>
    </table>
  </div>
</section>

    </div>
  );
}
