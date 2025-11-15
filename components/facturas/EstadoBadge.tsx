// src/components/facturas/EstadoBadge.tsx
import { EstadoTramitacion } from "@/types/sical";
import clsx from "clsx";

interface Props {
  estado: EstadoTramitacion;
}

export default function EstadoBadge({ estado }: Props) {
  const base =
    "inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium";

  const color = clsx({
    "bg-yellow-100 text-yellow-800":
      estado === "REGISTRADA" || estado === "EN_SERVICIO",
    "bg-blue-100 text-blue-800": estado === "EN_INTERVENCION",
    "bg-green-100 text-green-800":
      estado === "LISTA_PARA_CONTABILIZAR" || estado === "OBLIGADA",
    "bg-red-100 text-red-800": estado === "REPARO" || estado === "SUBSANACION",
    "bg-slate-100 text-slate-700":
      estado === "PAGADA" || estado === "ANULADA",
  });

  return <span className={`${base} ${color}`}>{estado}</span>;
}
