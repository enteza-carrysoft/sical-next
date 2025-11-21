// app/facturas/page.tsx
import FacturasTable from "@/components/facturas/FacturasTable";
import FacturaFilters from "@/components/facturas/FacturaFilters";
import { fetchFacturas } from "@/lib/api";

export default async function FacturasPage() {
  // Obtener facturas desde la API (con fallback a mock data)
  const facturas = await fetchFacturas(100, 0);

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold">Facturas</h2>
        <div className="text-xs text-slate-500">
          {facturas.length} facturas
        </div>
      </div>

      <FacturaFilters />

      <div className="bg-white rounded-xl shadow">
        <FacturasTable facturas={facturas} />
      </div>
    </div>
  );
}
