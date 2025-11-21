# 🔗 Guía de Integración Frontend-Backend

## ✅ Integración Completada

La aplicación SICAL Next ya está integrada con el backend FastAPI que conecta con la base de datos Oracle SICAL.

## 📋 Cambios Realizados

### 1. Estructura del Proyecto

**Antes:**
```
sical-next/
├── app/
├── components/
│   ├── core/db.py          ❌ Archivo Python mal ubicado
│   └── facturas/id/page.tsx ❌ Página mal ubicada
└── types/
```

**Después:**
```
sical-next/
├── app/
│   └── facturas/[id]/page.tsx  ✅ Página en lugar correcto
├── backend/                     ✅ Backend FastAPI completo
│   ├── api/
│   ├── application/
│   ├── domain/
│   └── core/db.py              ✅ Módulo Oracle en backend
├── components/                  ✅ Solo componentes React
├── lib/api.ts                  ✅ Cliente API frontend
└── types/
```

### 2. Backend FastAPI

**Archivos creados:**
- `backend/main.py` - Aplicación FastAPI con CORS
- `backend/api/facturas_router.py` - Endpoints de facturas
- `backend/application/services/factura_service.py` - Lógica de negocio
- `backend/domain/models/factura.py` - Modelos Pydantic
- `backend/core/config.py` - Configuración Oracle
- `backend/core/db.py` - Conexión Oracle (movido y mejorado)
- `backend/requirements.txt` - Dependencias Python
- `backend/README.md` - Documentación del backend

**Endpoints disponibles:**
- `GET /api/facturas` - Lista facturas
- `GET /api/facturas/{id}` - Detalle de factura
- `GET /health` - Health check
- `GET /api/docs` - Documentación Swagger

### 3. Cliente API Frontend

**Archivo creado:** `lib/api.ts`

Funciones disponibles:
- `fetchFacturas(limit, offset)` - Obtiene lista de facturas
- `fetchFactura(id)` - Obtiene detalle de factura
- `checkApiHealth()` - Verifica estado de la API

**Características:**
- ✅ Fallback automático a mock data si la API falla
- ✅ Error handling robusto
- ✅ TypeScript completamente tipado
- ✅ Cache desactivado para datos frescos

### 4. Páginas Actualizadas

**app/facturas/page.tsx** (`app/facturas/page.tsx:4`)
```typescript
import { fetchFacturas } from "@/lib/api";

export default async function FacturasPage() {
  const facturas = await fetchFacturas(100, 0);
  // ... resto del código
}
```

**app/facturas/[id]/page.tsx** (`app/facturas/[id]/page.tsx:4`)
```typescript
import { fetchFactura } from "@/lib/api";

export default async function FacturaDetailPage({ params }: Props) {
  const factura = await fetchFactura(params.id);
  // ... resto del código
}
```

### 5. Archivos de Configuración

**`.env.example`** - Configuración backend Oracle:
- Credenciales Oracle (host, user, password)
- Service name o SID
- Directorio Oracle Instant Client
- Configuración de autenticación

**`.env.local.example`** - Configuración frontend:
- `NEXT_PUBLIC_API_URL` - URL del backend API

## 🚀 Puesta en Marcha

### Backend

1. **Instalar Oracle Instant Client:**
   - Descargar desde [Oracle](https://www.oracle.com/database/technologies/instant-client/downloads.html)
   - Extraer en `C:\oracle\instantclient_19_23\`

2. **Configurar variables de entorno:**
```bash
cp .env.example .env
# Editar .env con tus credenciales Oracle
```

3. **Instalar dependencias:**
```bash
cd backend
pip install -r requirements.txt
```

4. **Ejecutar servidor:**
```bash
# Desde la raíz del proyecto
python backend/main.py

# La API estará en http://localhost:8000
# Docs: http://localhost:8000/api/docs
```

### Frontend

1. **Configurar URL de la API (opcional):**
```bash
cp .env.local.example .env.local
# Editar si necesitas cambiar la URL del backend
```

2. **Instalar dependencias (si no lo has hecho):**
```bash
npm install
```

3. **Ejecutar servidor de desarrollo:**
```bash
npm run dev
# La app estará en http://localhost:3000
```

## 🧪 Verificación

### 1. Verificar Backend
```bash
# Health check
curl http://localhost:8000/health

# Listar facturas
curl http://localhost:8000/api/facturas

# Ver documentación
# Abrir en navegador: http://localhost:8000/api/docs
```

### 2. Verificar Frontend
```bash
# Abrir en navegador: http://localhost:3000
# Navegar a: http://localhost:3000/facturas
```

### 3. Verificar Integración
- Frontend → Backend: Las facturas mostradas deben venir de la BD Oracle
- Si el backend no está disponible, se mostrará mock data con fallback automático

## 🔄 Flujo de Datos

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│   Next.js   │ HTTP    │   FastAPI    │  SQL    │   Oracle    │
│  (Frontend) │ ──────> │  (Backend)   │ ──────> │   SICAL     │
│             │ <────── │              │ <────── │   Database  │
└─────────────┘  JSON   └──────────────┘  Rows   └─────────────┘
     ↓ Si falla
     ↓
┌─────────────┐
│  Mock Data  │
│  (Fallback) │
└─────────────┘
```

## 📝 TODOs Pendientes

### Backend
- [ ] Implementar autenticación JWT
- [ ] Añadir tests (pytest)
- [ ] Obtener trámites reales desde BD
- [ ] Calcular estados de tramitación reales
- [ ] Implementar filtros y búsqueda
- [ ] Añadir paginación completa
- [ ] Implementar logging estructurado
- [ ] Añadir caché (Redis)

### Frontend
- [ ] Implementar state management (Zustand)
- [ ] Añadir loading states
- [ ] Implementar error boundaries
- [ ] Añadir tests (Jest + RTL)
- [ ] Implementar filtros dinámicos funcionales
- [ ] Añadir paginación en UI
- [ ] Implementar búsqueda
- [ ] Migrar a arquitectura Feature-First

### General
- [ ] Configurar CI/CD
- [ ] Documentación de API completa
- [ ] Configurar Docker para desarrollo
- [ ] Setup de staging/production
- [ ] Monitoring y observability

## 🐛 Troubleshooting

### Backend no arranca
**Error:** `DPI-1047: Cannot locate a 64-bit Oracle Client library`
- ✅ Verificar que Oracle Instant Client está instalado
- ✅ Verificar `ORACLE_CLIENT_DIR` en `.env`

**Error:** `ORA-12154: TNS:could not resolve the connect identifier`
- ✅ Verificar `ORACLE_SERVICE` o `ORACLE_SID` en `.env`
- ✅ Verificar conectividad con servidor Oracle

### Frontend muestra mock data
- ✅ Verificar que el backend está corriendo en puerto 8000
- ✅ Verificar `NEXT_PUBLIC_API_URL` en `.env.local`
- ✅ Verificar CORS en backend (debería permitir localhost:3000)

### Error CORS
- ✅ Backend debe incluir URL del frontend en ALLOWED_ORIGINS
- ✅ Verificar que frontend usa puerto 3000-3006

## 📚 Referencias

- **Backend API Docs:** http://localhost:8000/api/docs
- **Backend README:** `backend/README.md`
- **CLAUDE.md:** Principios y arquitectura del proyecto
- **Types:** `types/sical.ts` - Tipos del dominio SICAL

---

*Integración completada el 2025-11-21*
