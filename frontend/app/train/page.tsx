"use client";

import { useState } from "react";

export default function TrainPage() {
	const [message, setMessage] = useState("");

	const handleTrain = async () => {
		setMessage("Entrenando el modelo, por favor espera...");
		try {
			const response = await fetch("http://localhost:8000/train", {
				method: "POST",
			});
			const data = await response.json();
			setMessage(data.message || "Entrenamiento iniciado.");
		} catch (error) {
			setMessage("Error al iniciar el entrenamiento.");
		}
	};

	return (
		<main className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4">
			<h1 className="text-3xl font-bold mb-6">Entrenar Modelo</h1>
			<button
				onClick={handleTrain}
				className="btn mb-4">
				Iniciar Entrenamiento
			</button>
			<p>{message}</p>
		</main>
	);
}
