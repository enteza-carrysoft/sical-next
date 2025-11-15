// src/components/facturas/FacturaFilters.tsx
"use client";

import { useState } from "react";

export default function FacturaFilters() {
  const [estado, setEstado] = useState<string>("TODOS");
  const [proveedor, setProveedor] = useState<string>("");

  // De momento solo UI; luego conectarás con búsqueda real (query params, etc.)
  return (
    <div className="bg-white rounded-xl shadow p-4 flex flex-wrap gap-4 items-end">
      <div className="flex flex-col">
        <label className="text-xs text-slate-500 mb-1">Estado tramitación</label>
        <select
          value={estado}
          onChange={(e) => setEstado(e.target.value)}
          className="border rounded-lg px-2 py-1 text-sm"
        >
          <option value="TODOS">Todos</option>
          <option value="REGISTRADA">Registrada</option>
          <option value="EN_SERVICIO">En servicio</option>
          <option value="EN_INTERVENCION">En intervención</option>
          <option value="LISTA_PARA_CONTABILIZAR">Lista para contabilizar</option>
          <option value="OBLIGADA">Obligada</option>
        </select>
      </div>

      <div className="flex flex-col">
        <label className="text-xs text-slate-500 mb-1">Proveedor</label>
        <input
          value={proveedor}
          onChange={(e) => setProveedor(e.target.value)}
          className="border rounded-lg px-2 py-1 text-sm"
          placeholder="Nombre o NIF"
        />
      </div>
    </div>
  );
}
