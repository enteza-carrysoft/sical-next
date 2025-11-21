@echo off
REM Script para instalar Oracle Instant Client

echo ============================================================
echo Instalacion de Oracle Instant Client
echo ============================================================
echo.

REM Verificar si el directorio ya existe
if exist "C:\oracle\instantclient_19_23\" (
    echo [INFO] El directorio C:\oracle\instantclient_19_23 ya existe
    echo.
    dir "C:\oracle\instantclient_19_23\" | find "oci.dll"
    if errorlevel 1 (
        echo [ERROR] El directorio existe pero no contiene los archivos correctos
        echo Por favor, extrae el ZIP de Oracle Instant Client manualmente
    ) else (
        echo [OK] Oracle Instant Client parece estar instalado correctamente
    )
    pause
    exit /b
)

echo [PASO 1] Creando directorio C:\oracle
mkdir C:\oracle 2>nul

echo [PASO 2] Por favor, extrae el archivo ZIP de Oracle Instant Client
echo.
echo Instrucciones:
echo 1. Descarga instantclient-basic-windows.x64-XX.zip
echo 2. Extrae la carpeta instantclient_XX_X a C:\oracle\
echo 3. Renombra la carpeta a: C:\oracle\instantclient_19_23\
echo.
echo Presiona cualquier tecla cuando hayas terminado...
pause >nul

REM Verificar instalacion
echo.
echo [VERIFICANDO] Comprobando instalacion...
if exist "C:\oracle\instantclient_19_23\oci.dll" (
    echo [OK] Oracle Instant Client instalado correctamente!
    echo.
    dir "C:\oracle\instantclient_19_23\"
) else (
    echo [ERROR] No se encontro oci.dll en C:\oracle\instantclient_19_23\
    echo Por favor, verifica que hayas extraido el ZIP correctamente
)

echo.
echo ============================================================
echo Instalacion completada
echo ============================================================
pause
