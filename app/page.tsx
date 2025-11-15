// src/app/page.tsx
import Link from "next/link";

export default function DashboardPage() {
  // Aquí luego podrás hacer fetch a tu backend de KPIs
  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-semibold">Panel de control</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white rounded-xl shadow p-4">
          <div className="text-sm text-slate-500">Facturas pendientes</div>
          <div className="text-3xl font-bold mt-2">42</div>
        </div>
        <div className="bg-white rounded-xl shadow p-4">
          <div className="text-sm text-slate-500">En intervención</div>
          <div className="text-3xl font-bold mt-2">15</div>
        </div>
        <div className="bg-white rounded-xl shadow p-4">
          <div className="text-sm text-slate-500">Pago medio (días)</div>
          <div className="text-3xl font-bold mt-2">18</div>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow p-4">
        <h3 className="text-lg font-semibold mb-2">Accesos rápidos</h3>
        <div className="flex gap-4">
          <Link
            href="/facturas"
            className="px-4 py-2 rounded-lg border text-sm hover:bg-slate-50"
          >
            Ver facturas
          </Link>
          <Link
            href="/facturas/nueva"
            className="px-4 py-2 rounded-lg bg-slate-900 text-white text-sm"
          >
            Registrar nueva factura
          </Link>
        </div>
      </div>
    </div>
  );
}
