// src/components/layout/Topbar.tsx
export default function Topbar() {
  return (
    <header className="h-16 border-b bg-white flex items-center justify-between px-6">
      <h1 className="text-lg font-semibold">Tramitación de facturas</h1>
      <div className="text-sm text-slate-500">
        Diputación · Área de Intervención
      </div>
    </header>
  );
}
