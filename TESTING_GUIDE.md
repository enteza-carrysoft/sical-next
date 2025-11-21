# 🧪 Guía de Prueba - SICAL Next

Guía paso a paso para probar la integración frontend-backend.

## 📋 Prerrequisitos

Antes de empezar, asegúrate de tener:

- ✅ Python 3.10+ instalado
- ✅ Node.js 18+ instalado
- ✅ Oracle Instant Client instalado (si vas a conectar a Oracle)
- ✅ Acceso a la base de datos Oracle SICAL (opcional para pruebas iniciales)

## 🎯 Opción 1: Prueba Rápida (Sin Oracle)

**Ideal para:** Verificar que todo funciona sin necesitar la base de datos.

### Paso 1: Verificar Frontend (Mock Data)

```bash
# Asegurarse de estar en la raíz del proyecto
cd C:\Users\Usuario\Documents\Proyectos\facturas\sical-next

# Instalar dependencias si no lo has hecho
npm install

# Ejecutar servidor de desarrollo
npm run dev
```

**Resultado esperado:**
```
✓ Ready in 2.5s
○ Local:   http://localhost:3000
```

**Verificar en navegador:**
1. Abrir http://localhost:3000
2. Ir a "Ver facturas" o http://localhost:3000/facturas
3. Deberías ver 2 facturas de ejemplo (mock data)
4. Clic en una factura para ver el detalle

✅ **Si ves esto, el frontend funciona correctamente**

---

## 🔌 Opción 2: Prueba Completa (Con Backend Real)

**Ideal para:** Probar la integración completa con Oracle.

### Paso 1: Configurar Variables de Entorno

```bash
# Crear archivo .env en la raíz del proyecto
cp .env.example .env
```

**Editar `.env` con tus credenciales reales:**

```env
# IMPORTANTE: Reemplazar con tus valores reales
ORACLE_HOST=tu_servidor_oracle.com
ORACLE_PORT=1521
ORACLE_USER=tu_usuario
ORACLE_PASSWORD=tu_password
ORACLE_SERVICE=ORCL
ORACLE_CLIENT_DIR=C:\oracle\instantclient_19_23

# Configuración de autenticación (opcional)
AUTH_TABLE=USUARIO
AUTH_USER_COL=USUARIO
AUTH_PASS_COL=PASSWORD
```

### Paso 2: Instalar Dependencias del Backend

```bash
# Opción A: Crear entorno virtual (recomendado)
python -m venv venv
venv\Scripts\activate

# Opción B: Instalar directamente
pip install -r backend/requirements.txt
```

**Resultado esperado:**
```
Successfully installed fastapi-0.109.0 uvicorn-0.27.0 oracledb-2.0.1 ...
```

### Paso 3: Verificar Conexión a Oracle (Opcional)

```bash
# Test rápido de conexión
python -c "from backend.core.db import get_connection_for_sid; conn = get_connection_for_sid(); print('✓ Conexión exitosa'); conn.close()"
```

**Si falla:**
- Verificar credenciales en `.env`
- Verificar que Oracle Instant Client está instalado
- Verificar conectividad al servidor Oracle

### Paso 4: Ejecutar Backend

```bash
# Desde la raíz del proyecto
python backend/main.py
```

**Resultado esperado:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

✅ **Backend corriendo en:** http://localhost:8000

### Paso 5: Probar Backend (Nuevo Terminal)

```bash
# Abrir NUEVO terminal (dejar el backend corriendo)

# Test 1: Health check
curl http://localhost:8000/health

# Resultado esperado:
# {"status":"healthy","service":"sical-next-api"}

# Test 2: Listar facturas
curl http://localhost:8000/api/facturas

# Resultado esperado:
# [{"id":"1","numeroFactura":"F123",...}]

# Test 3: Documentación API
# Abrir en navegador: http://localhost:8000/api/docs
```

### Paso 6: Configurar Frontend para Usar Backend

```bash
# Crear archivo .env.local (opcional, ya usa localhost:8000 por defecto)
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

### Paso 7: Ejecutar Frontend

```bash
# Nuevo terminal (o el mismo si cerraste el anterior)
npm run dev
```

**Resultado esperado:**
```
✓ Ready in 2.5s
○ Local:   http://localhost:3000
```

### Paso 8: Verificar Integración Completa

**En el navegador:**

1. **Abrir:** http://localhost:3000

2. **Dashboard:** Deberías ver el panel de control

3. **Lista de facturas:**
   - Ir a http://localhost:3000/facturas
   - **Si backend funciona:** Verás facturas reales de Oracle
   - **Si backend falla:** Verás 2 facturas de ejemplo (fallback automático)

4. **Detalle de factura:**
   - Clic en una factura
   - Verás todos los detalles

5. **Verificar consola del navegador (F12):**
   - Si NO hay errores → ✅ Backend funciona
   - Si hay "Error fetching facturas" → ⚠️ Backend no responde (usando fallback)

---

## 🔍 Verificaciones Detalladas

### Backend Funcionando Correctamente

**Terminal del backend debe mostrar:**
```
INFO:     127.0.0.1:xxxxx - "GET /api/facturas HTTP/1.1" 200 OK
```

**Navegador debe mostrar:**
- Facturas con datos reales de Oracle
- Sin mensajes de error en consola (F12)

### Backend NO Funcionando

**Navegador mostrará:**
- 2 facturas de ejemplo (mock data)
- Mensaje en consola: "Error fetching facturas" (F12)
- La app sigue funcionando normalmente con datos de prueba

---

## 🐛 Solución de Problemas

### Problema: "DPI-1047: Cannot locate Oracle Client library"

**Solución:**
```bash
# Verificar que Oracle Instant Client está instalado
dir C:\oracle\instantclient_19_23

# Actualizar .env con la ruta correcta
ORACLE_CLIENT_DIR=C:\oracle\instantclient_19_23
```

### Problema: "ORA-12154: TNS could not resolve"

**Solución:**
```bash
# Verificar ORACLE_SERVICE o ORACLE_SID en .env
ORACLE_SERVICE=ORCL
# O
ORACLE_SID=ORCL
```

### Problema: Backend no arranca

**Revisar:**
```bash
# 1. Dependencias instaladas
pip list | findstr fastapi

# 2. Puerto 8000 no ocupado
netstat -ano | findstr :8000

# 3. Variables de entorno cargadas
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('ORACLE_HOST'))"
```

### Problema: Frontend muestra mock data siempre

**Verificar:**
1. Backend está corriendo en puerto 8000
2. No hay errores en consola del backend
3. Probar endpoint manualmente: http://localhost:8000/api/facturas
4. Verificar `.env.local` (si existe):
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

### Problema: Error CORS

**Síntoma:** Error en consola del navegador sobre CORS

**Solución:**
- Verificar que `backend/main.py` incluye `http://localhost:3000` en ALLOWED_ORIGINS
- El código ya lo incluye, debería funcionar automáticamente

---

## ✅ Checklist de Pruebas

### Backend
- [ ] Backend arranca sin errores
- [ ] http://localhost:8000/health responde
- [ ] http://localhost:8000/api/docs muestra documentación
- [ ] http://localhost:8000/api/facturas devuelve JSON
- [ ] Logs muestran consultas SQL exitosas

### Frontend
- [ ] Frontend arranca sin errores
- [ ] http://localhost:3000 carga el dashboard
- [ ] http://localhost:3000/facturas muestra lista
- [ ] Clic en factura muestra detalle
- [ ] No hay errores en consola del navegador (F12)

### Integración
- [ ] Frontend muestra datos del backend (no mock)
- [ ] Contador de facturas es correcto
- [ ] Datos coinciden con los de Oracle
- [ ] Al parar el backend, frontend usa mock data automáticamente

---

## 🎯 Comandos Rápidos de Prueba

### Test Backend (API directo)
```bash
# Health check
curl http://localhost:8000/health

# Listar facturas
curl http://localhost:8000/api/facturas?limit=5

# Obtener factura específica (reemplazar {id} con un ID real)
curl http://localhost:8000/api/facturas/123
```

### Test Frontend (desde navegador)
```javascript
// Abrir consola del navegador (F12) y pegar:

// Test 1: Verificar API
fetch('http://localhost:8000/health')
  .then(r => r.json())
  .then(d => console.log('✅ Backend:', d))
  .catch(e => console.log('❌ Backend no disponible:', e));

// Test 2: Obtener facturas
fetch('http://localhost:8000/api/facturas')
  .then(r => r.json())
  .then(d => console.log('✅ Facturas:', d.length, 'encontradas'))
  .catch(e => console.log('❌ Error:', e));
```

---

## 📊 Ejemplo de Flujo Completo

```
1. cd C:\Users\Usuario\Documents\Proyectos\facturas\sical-next
2. cp .env.example .env
3. [Editar .env con credenciales]
4. pip install -r backend/requirements.txt
5. python backend/main.py
   → Backend en http://localhost:8000 ✅

6. [Abrir NUEVO terminal]
7. npm run dev
   → Frontend en http://localhost:3000 ✅

8. [Abrir navegador]
9. http://localhost:3000/facturas
   → Ver facturas reales de Oracle ✅
```

---

## 🎉 ¡Éxito!

Si llegaste hasta aquí y todo funciona, la integración está completa:
- ✅ Frontend Next.js funcionando
- ✅ Backend FastAPI funcionando
- ✅ Conexión a Oracle SICAL funcionando
- ✅ Datos reales mostrados en la interfaz

**Próximos pasos:**
- Implementar filtros y búsqueda
- Añadir autenticación
- Implementar más funcionalidades de gestión de facturas
