# 🔧 Instalación Oracle Instant Client para Windows

## 📥 Descarga

### Opción 1: Descarga Directa (Recomendada)

1. **Ir a:** https://www.oracle.com/database/technologies/instant-client/winx64-64-downloads.html

2. **Descargar:** "Basic Package" (instantclient-basic-windows.x64-XX.X.X.X.zip)
   - Versión recomendada: 19.x o superior
   - Tamaño: ~70-80 MB

3. **No requiere cuenta Oracle** para la versión Basic

### Opción 2: Archivo Local

Si ya tienes el archivo descargado, continúa con la instalación.

## 📦 Instalación

### Paso 1: Crear Directorio

```cmd
mkdir C:\oracle
```

### Paso 2: Extraer ZIP

1. Extraer el archivo descargado
2. Copiar la carpeta `instantclient_XX_X` a `C:\oracle\`
3. Renombrar (opcional) a `C:\oracle\instantclient_19_23\`

**Estructura final esperada:**
```
C:\oracle\instantclient_19_23\
├── adrci.exe
├── oci.dll
├── oraociei19.dll
├── ...y otros archivos
```

### Paso 3: Verificar Instalación

```cmd
# Listar archivos del directorio
dir C:\oracle\instantclient_19_23\

# Debería mostrar múltiples archivos .dll y .exe
```

### Paso 4 (Opcional): Añadir al PATH

No es necesario para este proyecto, pero si quieres:

```cmd
# Añadir a PATH del sistema
setx PATH "%PATH%;C:\oracle\instantclient_19_23"
```

## 🧪 Verificación

Una vez instalado, verificaremos la conexión con Python.

---

## 🔗 Links de Referencia

- **Oracle Instant Client Downloads:** https://www.oracle.com/database/technologies/instant-client/downloads.html
- **Documentación:** https://www.oracle.com/database/technologies/instant-client.html

---

## 🆘 Problemas Comunes

### "No se encuentra el archivo DLL especificado"
- Verificar que los archivos .dll están en el directorio
- Verificar la ruta en el .env: `ORACLE_CLIENT_DIR`

### "OCI.dll is not found"
- Descargar el "Basic Package", no el "Basic Light"
- Verificar que la versión es 64-bit

### "DPI-1047: Cannot locate Oracle Client library"
- Verificar que `ORACLE_CLIENT_DIR` apunta al directorio correcto
- Reiniciar el terminal después de cambiar PATH
