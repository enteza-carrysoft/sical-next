// src/components/facturas/TramitesTimeline.tsx
import { TramiteFactura } from "@/types/sical";

interface Props {
  tramites: TramiteFactura[];
}

export default function TramitesTimeline({ tramites }: Props) {
  if (!tramites.length) {
    return <div className="text-xs text-slate-500">Sin trámites registrados.</div>;
  }

  return (
    <ol className="relative border-s border-slate-200">
      {tramites.map((t, idx) => (
        <li key={t.id} className="mb-6 ms-4">
          <div className="absolute w-3 h-3 bg-slate-200 rounded-full mt-1.5 -start-1.5 border border-white"></div>
          <time className="mb-1 text-xs font-normal leading-none text-slate-500">
            {new Date(t.fecha).toLocaleString("es-ES")}
          </time>
          <h4 className="text-sm font-semibold text-slate-900">{t.tipo}</h4>
          <p className="text-xs text-slate-600">
            Usuario: {t.usuario}
            {t.observaciones && ` · ${t.observaciones}`}
          </p>
        </li>
      ))}
    </ol>
  );
}
