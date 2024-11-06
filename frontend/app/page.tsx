import Link from 'next/link';

export default function Home() {
  return (
    <main className="min-h-screen bg-cover bg-center" style={{ backgroundImage: 'url(/traffic-signs.jpg)' }}>
      <div className="bg-black bg-opacity-50 min-h-screen flex flex-col items-center justify-center">
        <h1 className="text-5xl font-bold text-white mb-8">Reconocimiento de Señales de Tráfico</h1>
        <div className="space-y-4">
          <Link href="/train" className="btn">
            Entrenar Modelo
          </Link>
          <Link href="/metrics" className="btn">
            Ver Métricas
          </Link>
          <Link href="/examples/correct" className="btn">
            Ejemplos Correctos
          </Link>
          <Link href="/examples/incorrect" className="btn">
            Ejemplos Incorrectos
          </Link>
          <Link href="/predict" className="btn">
            Realizar Predicción
          </Link>
        </div>
      </div>
    </main>
  );
}
