# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

# Proyecto: Sical Next

## 📋 Estado Actual del Proyecto

**Fase:** MVP Inicial - Frontend + Backend inicial
**Última actualización:** 2025-11-21

### ✅ Implementado

**Frontend:**
- **Framework**: Next.js 16 con App Router
- **TypeScript**: Configurado con paths aliases (`@/*`)
- **Styling**: Tailwind CSS v4
- **Estructura**:
  - `app/` - Páginas con App Router (dashboard, facturas, detalle de factura)
  - `components/` - Componentes organizados por dominio (facturas, layout)
  - `types/` - Tipos TypeScript del dominio SICAL
  - Layout base con Sidebar y Topbar
- **Componentes principales**:
  - `FacturasTable` - Tabla de listado de facturas
  - `FacturaFilters` - Filtros dinámicos
  - `EstadoBadge` - Badge de estados
  - `TramitesTimeline` - Timeline de trámites

**Backend (Inicial):**
- `backend/core/db.py` - Módulo de conexión a Oracle SICAL
  - Soporte para oracledb (modo thick)
  - Funciones de autenticación de usuarios
  - Consultas a tablas FACTURAS, FACTGAST, TER_GENERAL
  - Obtención de aplicaciones presupuestarias

### 🚧 Pendiente de Implementar
- Estructura completa Backend FastAPI (routers, services, etc.)
- Tests (Jest para frontend, pytest para backend)
- State management (Zustand)
- Validación de schemas (Zod)
- Integración frontend-backend real (actualmente usa mock data)
- Sistema de autenticación completo
- Migración a estructura Feature-First

## 🎯 Principios de Desarrollo

### Design Philosophy
- **KISS**: Keep It Simple, Stupid - Prefiere soluciones simples
- **YAGNI**: You Aren't Gonna Need It - Implementa solo lo necesario
- **DRY**: Don't Repeat Yourself - Evita duplicación de código
- **SOLID**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion

### Descripción del Proyecto
Tramitador de facturas integrado con la aplicación SICAL de la Diputación de Sevilla. El sistema conectará con la base de datos Oracle SICAL mediante servicios web (FastAPI) y presentará una interfaz de gestión con:
- Listado de facturas con filtros dinámicos
- Detalle de cada factura con información de trámites
- Gestión por áreas, unidades y servicios
- Seguimiento de estados de tramitación y contables

## 🏗️ Tech Stack

### 🟢 Stack Actual (Implementado)
**Frontend:**
- **Runtime**: Node.js + TypeScript 5
- **Framework**: Next.js 16.0.3 (App Router)
- **Styling**: Tailwind CSS v4
- **Utilities**: clsx para class composition
- **React**: v19.2.0

### 🔵 Stack Planificado (Futuro)
**Frontend Adicional:**
- **State Management**: Zustand
- **Testing**: Jest + React Testing Library
- **Schema Validation**: Zod
- **Data Fetching**: React Query / SWR

**Backend:**
- **Runtime**: Python 3.10+
- **Framework**: FastAPI
- **ORM**: SQLModel (Pydantic + SQLAlchemy)
- **Database**: Oracle SICAL (existente)
- **Testing**: pytest
- **Task Queue**: Celery (opcional)

## 📁 Estructura Actual del Proyecto

```
sical-next/
├── app/                      # Next.js App Router
│   ├── facturas/            # Gestión de facturas
│   │   ├── [id]/            # Detalle de factura (ruta dinámica)
│   │   │   └── page.tsx     # Página de detalle
│   │   └── page.tsx         # Listado de facturas
│   ├── layout.tsx           # Layout raíz con Sidebar y Topbar
│   ├── page.tsx             # Dashboard principal
│   └── globals.css          # Estilos globales
│
├── backend/                 # Backend Python (en desarrollo)
│   └── core/                # Módulos core
│       └── db.py            # Conexión y queries a Oracle SICAL
│
├── components/              # Componentes React organizados por dominio
│   ├── facturas/            # Componentes específicos de facturas
│   │   ├── EstadoBadge.tsx
│   │   ├── FacturaFilters.tsx
│   │   ├── FacturasTable.tsx
│   │   └── TramitesTimeline.tsx
│   └── layout/              # Componentes de layout
│       ├── Sidebar.tsx
│       └── Topbar.tsx
│
├── types/                   # Tipos TypeScript del dominio
│   └── sical.ts             # Tipos: Factura, Proveedor, Estados, etc.
│
├── public/                  # Assets estáticos
├── package.json             # Dependencias y scripts npm
└── tsconfig.json            # Configuración TypeScript (alias @/*)
```

## 🎯 Arquitectura Objetivo (Futuro)

### Enfoque: Arquitectura Híbrida optimizada para IA

**Feature-First (Frontend)** + **Clean Architecture (Backend)**

#### Migración Planificada: Frontend Feature-First
```
src/
├── app/                      # Next.js App Router (rutas)
├── features/                 # 🎯 Organizadas por funcionalidad
│   ├── facturas/            # Feature: Gestión de facturas
│   │   ├── components/      # FacturasTable, FacturaFilters, etc.
│   │   ├── hooks/           # useFacturas, useFacturaFilters
│   │   ├── services/        # facturasService.ts (API calls)
│   │   ├── types/           # Tipos específicos
│   │   └── store/           # facturasStore.ts (Zustand)
│   └── [feature]/           # Otras features...
│
└── shared/                   # Código reutilizable
    ├── components/          # Button, Card, Badge, etc.
    ├── hooks/               # useDebounce, useLocalStorage
    ├── types/               # Tipos compartidos
    └── utils/               # Funciones utilitarias
```

#### Backend: Clean Architecture
```
backend/
├── main.py                   # FastAPI entry point
├── api/                      # 🌐 Capa de presentación (routers)
├── application/              # 🎯 Casos de uso
├── domain/                   # 💎 Lógica de negocio
└── infrastructure/           # 🔧 DB, APIs externas
```

> **💡 Ventaja para desarrollo asistido por IA:**
> - Código relacionado agrupado → contexto más claro
> - Separación de responsabilidades → cambios aislados
> - Escalabilidad → nuevas features sin afectar existentes

## 🛠️ Comandos Disponibles

### Desarrollo (Estado Actual)
```bash
# Instalar dependencias
npm install

# Servidor de desarrollo (puerto 3000 por defecto)
npm run dev

# Build para producción
npm run build

# Iniciar servidor de producción
npm start

# Linter
npm run lint
```

### Git Workflow
```bash
# Ver estado del repositorio
git status

# Crear commit (usar Conventional Commits)
git commit -m "feat(facturas): añadir filtro por proveedor"
git commit -m "fix(ui): corregir espaciado en tabla"

# Tipos de commits:
# - feat: Nueva funcionalidad
# - fix: Corrección de bug
# - docs: Cambios en documentación
# - style: Cambios de formato (no afectan lógica)
# - refactor: Refactorización de código
# - test: Añadir o modificar tests
# - chore: Tareas de mantenimiento
```

### Comandos Futuros (Cuando se implementen)
```bash
# Tests (pendiente de configurar)
npm test
npm run test:watch
npm run test:coverage

# Backend (pendiente de crear)
cd backend && python dev_server.py
cd backend && python -m pytest
```

## 📝 Convenciones de Código

### File & Function Limits
- **Archivos**: Máximo 500 líneas
- **Funciones**: Máximo 50 líneas
- **Componentes**: Una responsabilidad clara

### Naming Conventions
- **Variables/Functions**: `camelCase`
- **Components**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Files**: `kebab-case.extension`
- **Folders**: `kebab-case`

### TypeScript Guidelines
- **Siempre usar type hints** para function signatures
- **Interfaces** para object shapes
- **Types** para unions y primitives
- **Evitar `any`** - usar `unknown` si es necesario

### Component Patterns
```typescript
// ✅ GOOD: Proper component structure
interface Props {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary';
  onClick: () => void;
}

export function Button({ children, variant = 'primary', onClick }: Props) {
  return (
    <button 
      onClick={onClick}
      className={`btn btn-${variant}`}
    >
      {children}
    </button>
  );
}
```

## 🧪 Testing Strategy (Pendiente)

### Objetivo: Test-Driven Development (TDD)
1. **Red**: Escribe el test que falla
2. **Green**: Implementa código mínimo para pasar
3. **Refactor**: Mejora el código manteniendo tests verdes

### Patrón AAA (Arrange-Act-Assert)
```typescript
test('should calculate total with tax', () => {
  // Arrange - Preparar datos
  const items = [{ price: 100 }, { price: 200 }];
  const taxRate = 0.1;

  // Act - Ejecutar función
  const result = calculateTotal(items, taxRate);

  // Assert - Verificar resultado
  expect(result).toBe(330);
});
```

### Metas de Cobertura
- **Unit Tests**: 80%+ coverage
- **Integration Tests**: Paths críticos
- **E2E Tests**: User journeys principales

## 🔒 Security Best Practices

### Input Validation
- Validate all user inputs
- Sanitize data before processing
- Use schema validation (Zod, Yup, etc.)

### Authentication & Authorization
- JWT tokens con expiración
- Role-based access control
- Secure session management

### Data Protection
- Never log sensitive data
- Encrypt data at rest
- Use HTTPS everywhere

## ⚡ Performance Guidelines

### Code Splitting
- Route-based splitting
- Component lazy loading
- Dynamic imports

### State Management
- Local state first
- Global state only when needed
- Memoization for expensive computations

### Database Optimization
- Index frequently queried columns
- Use pagination for large datasets
- Cache repeated queries

## 🔄 Git Workflow & Repository Rules

### Branch Strategy
- `main` - Production ready code
- `develop` - Integration branch
- `feature/TICKET-123-description` - Feature branches
- `hotfix/TICKET-456-description` - Hotfixes

### Commit Convention (Conventional Commits)
```
type(scope): description

feat(auth): add OAuth2 integration
fix(api): handle null user response  
docs(readme): update installation steps
```

### Pull Request Rules
- **No direct commits** a `main` o `develop`
- **Require PR review** antes de merge
- **All tests must pass** antes de merge
- **Squash and merge** para mantener historia limpia

## ❌ No Hacer (Critical)

### Code Quality
- ❌ No usar `any` en TypeScript
- ❌ No hacer commits sin tests
- ❌ No omitir manejo de errores
- ❌ No hardcodear configuraciones

### Security  
- ❌ No exponer secrets en código
- ❌ No loggear información sensible
- ❌ No saltarse validación de entrada
- ❌ No usar HTTP en producción

### Architecture
- ❌ No editar archivos en `src/legacy/`
- ❌ No crear dependencias circulares
- ❌ No mezclar concerns en un componente
- ❌ No usar global state innecesariamente

## 📚 Dominio SICAL

### Entidades Principales

**Factura** (`types/sical.ts:41`)
- Información básica: número, fechas, proveedor, importes
- Estados: tramitación y contable
- Relaciones: aplicaciones presupuestarias, trámites
- Campos especiales: afecta413, PMP (Periodo Medio de Pago)

**Estados de Tramitación**
```typescript
"REGISTRADA" | "EN_SERVICIO" | "CONFORME_SERVICIO" |
"EN_INTERVENCION" | "REPARO" | "SUBSANACION" |
"LISTA_PARA_CONTABILIZAR" | "OBLIGADA" | "PAGADA" | "ANULADA"
```

**Estados Contables**
```typescript
"NO_OBLIGADA" | "OBLIGADA" | "ORDENADA" | "PAGADA" | "ANULADA"
```

**Canales de Entrada**
```typescript
"MANUAL" | "FACE" | "OTRO"
```

### Referencias del Proyecto
- `types/sical.ts` - Tipos del dominio SICAL
- `components/facturas/` - Componentes de gestión de facturas
- `app/facturas/page.tsx` - Página principal con mock data
- `package.json` - Scripts y dependencias disponibles

## 🤖 Guía para AI Assistants

### Al Sugerir Código
- **TypeScript estricto**: Siempre incluir tipos explícitos
- **Componentes funcionales**: Usar React function components con hooks
- **Error handling**: Incluir try-catch y fallbacks con mock data
- **Imports con alias**: Usar `@/*` para imports locales
- **Tailwind CSS**: Usar clases de utilidad, evitar CSS custom
- **Dominio SICAL**: Respetar tipos definidos en `types/sical.ts`

### Al Revisar Código
- Verificar tipos TypeScript correctos
- Validar uso de componentes Next.js (Link, Image, etc.)
- Revisar que componentes estén en la carpeta correcta
- Sugerir separación de concerns si es necesario
- Identificar código duplicado para refactorizar

### Contexto y Prioridades
1. **CLAUDE.md** (máxima prioridad) - Este archivo
2. **types/sical.ts** - Tipos del dominio de negocio
3. **Código existente** - Mantener consistencia con patterns actuales
4. **Best practices** de Next.js, React, TypeScript

### Estado del Proyecto
- 🟢 **Solo frontend** implementado actualmente
- 🔴 **No hay backend** todavía
- 🟡 **Mock data** en uso para desarrollo
- 🔵 **Feature-First** es arquitectura objetivo futura

## 🚀 Protocolos de Desarrollo

### Validación Pre-Desarrollo
**CRÍTICO**: Siempre verificar antes de asumir
- ✅ Verificar que las versiones de APIs/librerías existen
- ✅ Validar que endpoints externos funcionan
- ✅ Implementar fallbacks para dependencias externas

### Desarrollo Simplicity-First
- ✅ Empezar con versión simplificada
- ✅ Probar funcionalidad básica antes de añadir complejidad
- ✅ Mantener mock data para desarrollo sin backend
- ✅ Usar TodoWrite para tracking de progreso

### Manejo de Errores
```typescript
// ✅ GOOD: Siempre incluir error handling
try {
  const data = await fetchFacturas();
  return data;
} catch (error) {
  console.error('Error fetching facturas:', error);
  return mockFacturas; // Fallback data
}
```

## 🐛 Debugging

### Debugging Problemas de Puerto
```bash
# Ver qué proceso usa un puerto (Windows)
netstat -ano | findstr :3000

# Matar proceso por PID
taskkill /PID <PID> /F
```

### Logs de Desarrollo
```bash
# Ejecutar dev server con logs verbose
npm run dev -- --verbose

# Monitoring en tiempo real
npm run dev 2>&1 | tee dev.log
```

---

*Este archivo es la fuente de verdad para desarrollo en este proyecto. Todas las decisiones de código deben alinearse con estos principios.*