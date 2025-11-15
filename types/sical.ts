// src/types/sical.ts
export type CanalFactura = "MANUAL" | "FACE" | "OTRO";

export type EstadoTramitacion =
  | "REGISTRADA"
  | "EN_SERVICIO"
  | "CONFORME_SERVICIO"
  | "EN_INTERVENCION"
  | "REPARO"
  | "SUBSANACION"
  | "LISTA_PARA_CONTABILIZAR"
  | "OBLIGADA"
  | "PAGADA"
  | "ANULADA";

export type EstadoContable = "NO_OBLIGADA" | "OBLIGADA" | "ORDENADA" | "PAGADA" | "ANULADA";

export interface Proveedor {
  id: string;
  nif: string;
  nombre: string;
}

export interface AplicacionPresupuestaria {
  ejercicio: string;      // "2024"
  organica: string;
  funcional: string;
  economica: string;
  importe: number;
}

export interface TramiteFactura {
  id: string;
  facturaId: string;
  tipo: EstadoTramitacion;
  fecha: string;          // ISO string
  usuario: string;
  observaciones?: string;
}

export interface Factura {
  id: string;
  numeroFactura: string;
  fechaFactura: string;       // ISO
  fechaRegistro: string;      // ISO
  canal: CanalFactura;
  proveedor: Proveedor;
  baseImponible: number;
  iva: number;
  total: number;

  // Info “413 / morosidad / PMP”
  afecta413: boolean;
  fechaInicioPMP?: string;    // Fecha que empieza a contar periodo medio de pago

  estadoTramitacion: EstadoTramitacion;
  estadoContable: EstadoContable;

  aplicaciones: AplicacionPresupuestaria[];
  tramites: TramiteFactura[];

  // Campos mínimos para obligación
  numeroObligacion?: string;
  ejercicioObligacion?: string;

  // Abonos
  esAbono: boolean;
  facturaAbonadaId?: string;
}
