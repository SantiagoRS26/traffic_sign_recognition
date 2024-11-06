export default function CorrectExamplesPage() {
	return (
		<main className="min-h-screen p-8 bg-gray-100 flex flex-col items-center">
			<h1 className="text-3xl font-bold mb-6">
				Ejemplos Correctamente Clasificados
			</h1>
			<img
				src="http://localhost:8000/examples/correct"
				alt="Ejemplos Correctamente Clasificados"
				className="max-w-full h-auto"
			/>
		</main>
	);
}
