// src/app/facturas/page.tsx
import FacturasTable from "@/components/facturas/FacturasTable";
import FacturaFilters from "@/components/facturas/FacturaFilters";
import { Factura } from "@/types/sical";

// TODO: sustituir por fetch real a tu backend (Python, SICAL, etc.)
async function fetchFacturas(): Promise<Factura[]> {
  // Simulación
  return [
    {
      id: "1",
      numeroFactura: "F2024/001",
      fechaFactura: "2024-03-01",
      fechaRegistro: "2024-03-03",
      canal: "FACE",
      proveedor: { id: "p1", nif: "B12345678", nombre: "Proveedor Demo SL" },
      baseImponible: 1000,
      iva: 210,
      total: 1210,
      afecta413: true,
      fechaInicioPMP: "2024-03-03",
      estadoTramitacion: "EN_SERVICIO",
      estadoContable: "NO_OBLIGADA",
      aplicaciones: [],
      tramites: [],
      esAbono: false,
    },
  ];
}

export default async function FacturasPage() {
  const facturas = await fetchFacturas();

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-semibold">Facturas</h2>
      </div>

      <FacturaFilters />

      <div className="bg-white rounded-xl shadow">
        <FacturasTable facturas={facturas} />
      </div>
    </div>
  );
}
