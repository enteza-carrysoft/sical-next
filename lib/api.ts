// lib/api.ts
import { Factura } from "@/types/sical";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Cliente API para comunicación con backend FastAPI
 */

interface FacturaListItem {
  id: string;
  numeroFactura: string;
  fechaFactura: string;
  fechaRegistro: string;
  canal: string;
  proveedor: {
    id: string;
    nif: string;
    nombre: string;
  };
  total: number;
  estadoTramitacion: string;
  estadoContable: string;
}

/**
 * Obtiene lista de facturas desde la API
 */
export async function fetchFacturas(
  limit: number = 100,
  offset: number = 0
): Promise<FacturaListItem[]> {
  try {
    const response = await fetch(
      `${API_BASE_URL}/api/facturas?limit=${limit}&offset=${offset}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
        cache: "no-store", // Desactivar caché para obtener datos frescos
      }
    );

    if (!response.ok) {
      throw new Error(`Error HTTP: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Error fetching facturas:", error);

    // Fallback: retornar mock data si la API falla
    return getMockFacturas();
  }
}

/**
 * Obtiene detalle de una factura específica
 */
export async function fetchFactura(id: string): Promise<Factura | null> {
  try {
    const response = await fetch(`${API_BASE_URL}/api/facturas/${id}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
      cache: "no-store",
    });

    if (response.status === 404) {
      return null;
    }

    if (!response.ok) {
      throw new Error(`Error HTTP: ${response.status}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error(`Error fetching factura ${id}:`, error);

    // Fallback: retornar mock data si la API falla
    return getMockFactura(id);
  }
}

/**
 * Health check de la API
 */
export async function checkApiHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: "GET",
    });
    return response.ok;
  } catch (error) {
    console.error("API health check failed:", error);
    return false;
  }
}

// ============================================
// Mock Data (Fallbacks)
// ============================================

function getMockFacturas(): FacturaListItem[] {
  return [
    {
      id: "1",
      numeroFactura: "F2024/001",
      fechaFactura: "2024-03-01",
      fechaRegistro: "2024-03-03",
      canal: "FACE",
      proveedor: { id: "p1", nif: "B12345678", nombre: "Proveedor Demo SL" },
      total: 1210,
      estadoTramitacion: "EN_SERVICIO",
      estadoContable: "NO_OBLIGADA",
    },
    {
      id: "2",
      numeroFactura: "F2024/002",
      fechaFactura: "2024-03-05",
      fechaRegistro: "2024-03-06",
      canal: "MANUAL",
      proveedor: { id: "p2", nif: "B87654321", nombre: "Construcciones ABC" },
      total: 5420.5,
      estadoTramitacion: "EN_INTERVENCION",
      estadoContable: "NO_OBLIGADA",
    },
  ];
}

function getMockFactura(id: string): Factura {
  return {
    id,
    numeroFactura: `F2024/00${id}`,
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
    tramites: [
      {
        id: "t1",
        facturaId: id,
        tipo: "REGISTRADA",
        fecha: "2024-03-03T10:15:00Z",
        usuario: "Registro General",
        observaciones: "Factura recibida vía FACe (MOCK DATA)",
      },
      {
        id: "t2",
        facturaId: id,
        tipo: "EN_SERVICIO",
        fecha: "2024-03-04T09:00:00Z",
        usuario: "Servicio Obras",
        observaciones: "En revisión de conformidad (MOCK DATA)",
      },
    ],
    esAbono: false,
  };
}
