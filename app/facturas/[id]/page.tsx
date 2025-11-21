// app/facturas/[id]/page.tsx
import TramitesTimeline from "@/components/facturas/TramitesTimeline";
import EstadoBadge from "@/components/facturas/EstadoBadge";
import { fetchFactura } from "@/lib/api";

interface Props {
  params: { id: string };
}

export default async function FacturaDetailPage({ params }: Props) {
  const factura = await fetchFactura(params.id);

  if (!factura) {
    return <div>No se ha encontrado la factura.</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-semibold">
            Factura {factura.numeroFactura}
          </h2>
          <p className="text-sm text-slate-500">
            {factura.proveedor.nombre} · {factura.proveedor.nif}
          </p>
        </div>
        <div className="text-right space-y-1">
          <EstadoBadge estado={factura.estadoTramitacion} />
          <div className="text-xs text-slate-500">
            Contable: {factura.estadoContable}
          </div>
        </div>
      </div>

      {/* Datos básicos */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white rounded-xl shadow p-4">
          <h3 className="text-sm font-semibold mb-2">Fechas</h3>
          <div className="text-xs text-slate-600 space-y-1">
            <div>
              Fecha factura:{" "}
              {new Date(factura.fechaFactura).toLocaleDateString("es-ES")}
            </div>
            <div>
              Fecha registro:{" "}
              {new Date(factura.fechaRegistro).toLocaleDateString("es-ES")}
            </div>
            <div>Canal: {factura.canal}</div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow p-4">
          <h3 className="text-sm font-semibold mb-2">Importes</h3>
          <div className="text-xs text-slate-600 space-y-1">
            <div>Base: {factura.baseImponible} €</div>
            <div>IVA: {factura.iva} €</div>
            <div className="font-semibold">
              Total:{" "}
              {factura.total.toLocaleString("es-ES", {
                style: "currency",
                currency: "EUR",
              })}
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow p-4">
          <h3 className="text-sm font-semibold mb-2">Situación</h3>
          <div className="text-xs text-slate-600 space-y-1">
            <div>Afecta 413: {factura.afecta413 ? "Sí" : "No"}</div>
            {factura.fechaInicioPMP && (
              <div>
                Inicio PMP:{" "}
                {new Date(factura.fechaInicioPMP).toLocaleDateString("es-ES")}
              </div>
            )}
            {factura.numeroObligacion && (
              <div>Obligación: {factura.numeroObligacion}</div>
            )}
          </div>
        </div>
      </div>

      {/* Timeline de tramitación */}
      <div className="bg-white rounded-xl shadow p-4">
        <h3 className="text-sm font-semibold mb-4">Tramitación</h3>
        <TramitesTimeline tramites={factura.tramites} />
      </div>
    </div>
  );
}
