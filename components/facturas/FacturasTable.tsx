// src/components/facturas/FacturasTable.tsx
import Link from "next/link";
import { Factura } from "@/types/sical";
import EstadoBadge from "./EstadoBadge";

interface Props {
  facturas: Factura[];
}

export default function FacturasTable({ facturas }: Props) {
  return (
    <table className="min-w-full text-sm">
      <thead className="bg-slate-50 border-b">
        <tr>
          <th className="px-4 py-2 text-left">Nº factura</th>
          <th className="px-4 py-2 text-left">Proveedor</th>
          <th className="px-4 py-2 text-left">Fecha reg.</th>
          <th className="px-4 py-2 text-right">Total</th>
          <th className="px-4 py-2 text-left">Tramitación</th>
          <th className="px-4 py-2 text-left">Contable</th>
          <th className="px-4 py-2"></th>
        </tr>
      </thead>
      <tbody>
        {facturas.map((f) => (
          <tr key={f.id} className="border-b hover:bg-slate-50">
            <td className="px-4 py-2">
              <Link
                href={`/facturas/${f.id}`}
                className="text-slate-900 font-medium hover:underline"
              >
                {f.numeroFactura}
              </Link>
            </td>
            <td className="px-4 py-2">{f.proveedor.nombre}</td>
            <td className="px-4 py-2">
              {new Date(f.fechaRegistro).toLocaleDateString("es-ES")}
            </td>
            <td className="px-4 py-2 text-right">
              {f.total.toLocaleString("es-ES", {
                style: "currency",
                currency: "EUR",
              })}
            </td>
            <td className="px-4 py-2">
              <EstadoBadge estado={f.estadoTramitacion} />
            </td>
            <td className="px-4 py-2 text-xs text-slate-600">
              {f.estadoContable}
            </td>
            <td className="px-4 py-2 text-right text-xs text-slate-500">
              {f.canal}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
