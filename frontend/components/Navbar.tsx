import Link from 'next/link';

export default function Navbar() {
  return (
    <nav className="bg-blue-600 text-white">
      <div className="container mx-auto flex items-center justify-between p-4">
        <Link href="/" className="text-2xl font-bold">
          Reconocimiento de Señales
        </Link>
        <div className="space-x-4">
          <Link href="/train" className="hover:underline">
            Entrenar Modelo
          </Link>
          <Link href="/metrics" className="hover:underline">
            Ver Métricas
          </Link>
          <Link href="/examples/correct" className="hover:underline">
            Ejemplos Correctos
          </Link>
          <Link href="/examples/incorrect" className="hover:underline">
            Ejemplos Incorrectos
          </Link>
          <Link href="/predict" className="hover:underline">
            Realizar Predicción
          </Link>
        </div>
      </div>
    </nav>
  );
}
