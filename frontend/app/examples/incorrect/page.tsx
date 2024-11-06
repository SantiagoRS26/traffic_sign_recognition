export default function IncorrectExamplesPage() {
	return (
		<main className="min-h-screen p-8 bg-gray-100 flex flex-col items-center">
			<h1 className="text-3xl font-bold mb-6">
				Ejemplos Incorrectamente Clasificados
			</h1>
			<img
				src="http://localhost:8000/examples/incorrect"
				alt="Ejemplos Incorrectamente Clasificados"
				className="max-w-full h-auto"
			/>
		</main>
	);
}
